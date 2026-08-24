import os
import sys
import json
import asyncio
import time
import re
from pathlib import Path
from typing import Dict, Any, List, Optional
import uuid

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, BackgroundTasks, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

import database
from utils import prepare_script_audio
from logger import get_logger
from generator.script_generator import generate_ai_script
from services.renderer import RemotionRendererService

logger = get_logger("server")

PORT = 5000
BASE_DIR = Path(__file__).parent.resolve()
REMOTION_DIR = BASE_DIR / "remotion-app"
SCRIPT_JSON_PATH = REMOTION_DIR / "src" / "data" / "current_script.json"
OUTPUT_VIDEOS_DIR = BASE_DIR / "output_videos"
GUI_DIR = BASE_DIR / "studio-gui"

renderer_service = RemotionRendererService(
    remotion_dir=REMOTION_DIR,
    output_dir=OUTPUT_VIDEOS_DIR
)

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    database.init_db()
    OUTPUT_VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
    logger.info("Base de datos SQLite studio.db y directorio output_videos/ inicializados con Lifespan API.")
    yield

app = FastAPI(
    title="AI Video Studio API",
    description="API REST y WebSockets para automatización de videos con IA",
    version="2.0.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket Manager for real-time progress
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"Nuevo cliente WebSocket conectado: {websocket.client}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info("Cliente WebSocket desconectado.")

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                pass

manager = ConnectionManager()

# Pydantic Schemas
class GenerateScriptRequest(BaseModel):
    idea: str
    target_length: Optional[str] = "standard"
    voice: Optional[str] = "es-MX-DaliaNeural"

class SaveScriptRequest(BaseModel):
    script: Dict[str, Any]

class RenderVideoRequest(BaseModel):
    compositionId: Optional[str] = "ExpressApiVideo"

def slugify(text: str) -> str:
    """Convierte un texto en un slug seguro para nombres de archivo."""
    text = re.sub(r'[^\w\s-]', '', text.lower())
    return re.sub(r'[-\s]+', '_', text).strip('_')[:30]

async def start_render_background_task(composition_id: str):
    try:
        renderer_service.status["status"] = "rendering"
        renderer_service.status["progress"] = 5
        renderer_service.status["message"] = "Sintetizando locución de voz para las escenas..."
        await manager.broadcast(renderer_service.status)

        # 1. Read current script JSON
        if SCRIPT_JSON_PATH.exists():
            script = json.loads(SCRIPT_JSON_PATH.read_text(encoding="utf-8"))
        else:
            script = generate_ai_script("Tutorial")

        # 2. Synthesize audio TTS for all scenes with progress telemetry
        scenes = script.get("scenes", [])
        for i, scene in enumerate(scenes):
            speech = scene.get("speechText", "")
            if speech:
                pct = min(20, 5 + int(((i + 1) / max(1, len(scenes))) * 15))
                renderer_service.status["progress"] = pct
                renderer_service.status["message"] = f"Sintetizando voz en español (Escena {i+1}/{len(scenes)})..."
                await manager.broadcast(renderer_service.status)

        script_with_audio = prepare_script_audio(script)
        SCRIPT_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
        SCRIPT_JSON_PATH.write_text(json.dumps(script_with_audio, indent=2, ensure_ascii=False), encoding="utf-8")

        # 3. Generate unique filename
        title_slug = slugify(script.get("title", "video"))
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        out_filename = f"video_{timestamp}_{title_slug}.mp4"

        # 4. Invoke Remotion with dynamic props
        await renderer_service.render(
            composition_id=composition_id,
            props_file_path=SCRIPT_JSON_PATH,
            output_filename=out_filename,
            on_progress=manager.broadcast
        )
    except Exception as e:
        logger.error(f"Error en tarea de renderizado: {e}")
        renderer_service.status["status"] = "error"
        renderer_service.status["message"] = f"Error en renderizado: {str(e)}"
        await manager.broadcast(renderer_service.status)

# API Endpoints
@app.get("/api/status")
def get_status():
    return renderer_service.status

@app.get("/api/current-script")
def get_current_script():
    if SCRIPT_JSON_PATH.exists():
        return json.loads(SCRIPT_JSON_PATH.read_text(encoding="utf-8"))
    return {}

@app.post("/api/generate-script")
def api_generate_script(req: GenerateScriptRequest):
    logger.info(f"Generando guion para la idea: {req.idea}")
    script = generate_ai_script(req.idea, target_length=req.target_length or "standard")

    # Synthesize TTS Audio
    script = prepare_script_audio(script, voice=req.voice or "es-MX-DaliaNeural")

    SCRIPT_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    SCRIPT_JSON_PATH.write_text(json.dumps(script, indent=2, ensure_ascii=False), encoding="utf-8")

    project_id = str(uuid.uuid4())[:8]
    database.save_project(
        project_id=project_id,
        title=script.get("title", req.idea),
        subtitle=script.get("subtitle", ""),
        category=script.get("category", "TUTORIAL"),
        script=script
    )
    logger.info(f"Proyecto {project_id} guardado con audios en SQLite studio.db")

    return {"success": True, "project_id": project_id, "script": script}

@app.post("/api/save-script")
def api_save_script(req: SaveScriptRequest):
    script = prepare_script_audio(req.script)
    SCRIPT_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    SCRIPT_JSON_PATH.write_text(json.dumps(script, indent=2, ensure_ascii=False), encoding="utf-8")
    logger.info("Guion y audios guardados en disco.")
    return {"success": True, "message": "Guion y audios actualizados."}

@app.get("/api/projects")
def api_list_projects():
    return database.list_projects()

@app.get("/api/projects/{project_id}")
def api_get_project(project_id: str):
    proj = database.get_project(project_id)
    if not proj:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado.")
    return proj

@app.post("/api/render-video")
async def api_render_video(req: RenderVideoRequest, background_tasks: BackgroundTasks):
    if renderer_service.status["status"] != "rendering":
        renderer_service.status["status"] = "rendering"
        renderer_service.status["progress"] = 2
        renderer_service.status["message"] = "Iniciando tarea de procesamiento..."
        await manager.broadcast(renderer_service.status)

        logger.info(f"Recibida peticion de renderizado para formato: {req.compositionId}")
        background_tasks.add_task(start_render_background_task, req.compositionId)

    return {"success": True, "message": f"Renderizado iniciado en formato '{req.compositionId}'."}

# WebSocket Endpoint for real-time rendering telemetry
@app.websocket("/ws/render")
async def websocket_render_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        await websocket.send_json(renderer_service.status)
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Mount Static Files GUI at root
app.mount("/", StaticFiles(directory=str(GUI_DIR), html=True), name="static")

if __name__ == "__main__":
    logger.info(f"Iniciando AI Video Studio (FastAPI Enterprise Engine v2.0) en http://localhost:{PORT}")
    logger.info(f"Documentación OpenAPI / Swagger disponible en http://localhost:{PORT}/docs")
    try:
        uvicorn.run(app, host="localhost", port=PORT)
    except OSError as e:
        fallback_port = PORT + 100
        logger.warning(f"Puerto {PORT} ocupado. Iniciando automáticamente en puerto alternativo {fallback_port}...")
        uvicorn.run(app, host="localhost", port=fallback_port)
