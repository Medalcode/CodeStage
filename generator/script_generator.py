import os
import json
import urllib.request
from typing import Dict, Any
from logger import get_logger

logger = get_logger("generator.script")

def generate_multidomain_script(idea: str, target_length: str = "standard") -> Dict[str, Any]:
    """
    Genera un guion rico y variado (7-10 escenas) adaptado a la tecnología solicitada
    incorporando IDE, Consola, Navegador Web, Excel, Explorador de Archivos y Analytics.
    """
    idea_lower = idea.lower()

    # Detección de dominio
    if any(k in idea_lower for k in ["python", "pandas", "numpy", "data", "excel"]):
        domain = "python_data"
    elif any(k in idea_lower for k in ["docker", "contenedor", "devops", "kubernete"]):
        domain = "docker"
    elif any(k in idea_lower for k in ["react", "next", "frontend", "web", "html", "css"]):
        domain = "react_web"
    elif any(k in idea_lower for k in ["sql", "postgres", "database", "base de dato"]):
        domain = "sql"
    elif any(k in idea_lower for k in ["power bi", "analytics", "dashboard", "metric"]):
        domain = "analytics"
    else:
        domain = "general"

    title_clean = idea.strip() or "Guía Práctica de Desarrollo"

    # Construcción de 7 a 10 escenas ricas según el dominio
    if domain == "python_data":
        scenes = [
            {
                "id": "scene-1-intro",
                "type": "intro",
                "title": title_clean,
                "subtitle": "Análisis de Datos con Python & Pandas",
                "requirements": ["Python 3.10+", "Pandas & OpenPyXL", "Excel / VS Code"],
                "speechText": f"Bienvenidos a este tutorial sobre {title_clean}. En el desarrollo moderno, la automatización y análisis de datos en archivos Excel con Python es una de las habilidades más demandadas."
            },
            {
                "id": "scene-2-explorer",
                "type": "file_explorer",
                "projectName": "proyecto-analisis-python",
                "files": [
                    { "name": "data/", "type": "folder", "active": False },
                    { "name": "  ventas_2026.xlsx", "type": "file", "active": True },
                    { "name": "script_procesamiento.py", "type": "file", "active": False },
                    { "name": "requirements.txt", "type": "file", "active": False },
                ],
                "activeFileDetails": {
                    "name": "ventas_2026.xlsx",
                    "path": "data/ventas_2026.xlsx",
                    "size": "45.2 KB",
                    "lines": 500
                },
                "speechText": "Revisamos la estructura del proyecto en nuestro explorador de archivos. Tenemos nuestra fuente de datos en Excel y el script principal en Python."
            },
            {
                "id": "scene-3-setup",
                "type": "terminal",
                "title": "Configuración del Entorno de Python",
                "terminalPrompt": "user@laptop:~/data-project$",
                "commands": [
                    { "text": "python -m venv venv && source venv/bin/activate" },
                    { "text": "pip install pandas openpyxl matplotlib", "output": ["Successfully installed pandas-2.2.0 openpyxl-3.1.2"] }
                ],
                "speechText": "Abrimos nuestra consola de comandos para crear un entorno virtual aislado e instalar la librería Pandas junto con OpenPyXL."
            },
            {
                "id": "scene-4-editor",
                "type": "editor",
                "filename": "script_procesamiento.py",
                "codeLines": [
                    "import pandas as pd",
                    "",
                    "# Cargar datos desde la plantilla Excel",
                    "df = pd.read_excel('data/ventas_2026.xlsx')",
                    "",
                    "# Filtrar ingresos mayores a 10,000 USD",
                    "df_top = df[df['Ingresos'] > 10000]",
                    "",
                    "# Exportar reporte procesado",
                    "df_top.to_excel('data/reporte_final.xlsx', index=False)",
                    "print('¡Reporte generado con éxito!')"
                ],
                "speechText": "En nuestro editor de código VS Code leemos la plantilla de Excel, aplicamos filtros de ingresos y exportamos el reporte consolidado."
            },
            {
                "id": "scene-5-excel",
                "type": "excel",
                "title": "Plantilla Excel — Resultados Procesados",
                "sheetName": "Ventas_Consolidadas",
                "formula": "=SUMA(C2:C6)",
                "headers": ["ID", "Región / Cliente", "Ingresos (USD)", "Crecimiento", "Estado"],
                "rows": [
                    ["201", "América del Norte", "$ 45,200", "+ 28%", "Procesado"],
                    ["202", "Latinoamérica", "$ 32,800", "+ 34%", "Procesado"],
                    ["203", "Europa Central", "$ 28,900", "+ 15%", "Procesado"],
                    ["204", "Asia Pacífico", "$ 19,400", "+ 22%", "Procesado"],
                    ["TOTAL", "Ingresos Globales", "$ 126,300", "+ 25%", "COMPLETADO"]
                ],
                "summaryText": "Los datos han sido calculados automáticamente y formateados en la hoja de cálculo.",
                "speechText": "Visualizamos los resultados en la plantilla de Excel. El script ha clasificado los totales de ventas calculando fórmulas consolidadas."
            },
            {
                "id": "scene-6-analytics",
                "type": "analytics_chart",
                "title": "Power BI / Dashboard de Análisis",
                "metrics": [
                    { "label": "Ventas Totales", "value": "$ 126.3 K", "change": "+ 25%" },
                    { "label": "Región Top", "value": "Latam", "change": "+ 34%" },
                    { "label": "Tiempo Proceso", "value": "1.2 sec", "change": "RÁPIDO" },
                    { "label": "Error Rate", "value": "0.0 %", "change": "CERO" }
                ],
                "chartTitle": "Comparativa de Crecimiento por Trimestre",
                "speechText": "Cargamos los datos en nuestro Dashboard de analítica y Power BI para proyectar los gráficos de crecimiento acumulado."
            },
            {
                "id": "scene-7-features",
                "type": "features",
                "title": "Ventajas de Automatizar con Python & Excel",
                "features": ["Reducción de horas a milisegundos", "Cero errores manuales de fórmulas", "Reportes listos para la gerencia"],
                "speechText": "Al integrar Python con plantillas de Excel y analítica, logramos reportes instantáneos listos para la toma de decisiones."
            },
            {
                "id": "scene-8-outro",
                "type": "outro",
                "title": "¡Tutorial Completado!",
                "subtitle": "Suscríbete y activa las notificaciones para más contenido técnico",
                "githubRepo": "github.com/Medalcode/canal-tutorial-automation",
                "speechText": "Y con esto concluimos este tutorial de Python y análisis de datos. Apóyame con un me gusta y suscríbete al canal."
            }
        ]
    elif domain == "docker":
        scenes = [
            {
                "id": "scene-1-intro",
                "type": "intro",
                "title": title_clean,
                "subtitle": "Contenedores y Despliegue DevOps Profesional",
                "requirements": ["Docker Desktop", "Terminal / PowerShell", "Código de Aplicación"],
                "speechText": f"Bienvenidos a este tutorial sobre {title_clean}. Los contenedores permiten empaquetar aplicaciones garantizando que ejecuten idénticamente en cualquier entorno."
            },
            {
                "id": "scene-2-explorer",
                "type": "file_explorer",
                "projectName": "app-dockerizada",
                "files": [
                    { "name": "src/", "type": "folder", "active": False },
                    { "name": "Dockerfile", "type": "file", "active": True },
                    { "name": "docker-compose.yml", "type": "file", "active": False },
                    { "name": ".dockerignore", "type": "file", "active": False },
                ],
                "activeFileDetails": {
                    "name": "Dockerfile",
                    "path": "Dockerfile",
                    "size": "1.2 KB",
                    "lines": 18
                },
                "speechText": "En nuestro explorador de archivos revisamos la receta Dockerfile y los archivos de configuración del contenedor."
            },
            {
                "id": "scene-3-editor",
                "type": "editor",
                "filename": "Dockerfile",
                "codeLines": [
                    "FROM node:20-alpine",
                    "WORKDIR /app",
                    "COPY package*.json ./",
                    "RUN npm install --production",
                    "COPY . .",
                    "EXPOSE 8080",
                    "CMD [\"npm\", \"start\"]"
                ],
                "speechText": "En el editor de código VS Code escribimos el Dockerfile con una imagen ligera Alpine, instalando dependencias y exponiendo el puerto."
            },
            {
                "id": "scene-4-setup",
                "type": "terminal",
                "title": "Construcción y Ejecución del Contenedor",
                "terminalPrompt": "user@laptop:~/app-docker$",
                "commands": [
                    { "text": "docker build -t mi-app:v1 .", "output": ["Step 1/5 : FROM node:20-alpine", "Successfully tagged mi-app:v1"] },
                    { "text": "docker run -d -p 8080:8080 mi-app:v1", "output": ["a1b2c3d4e5f67890"] }
                ],
                "speechText": "Abrimos la consola de comandos para construir la imagen etiquetada e iniciar el contenedor exponiendo el puerto 8080."
            },
            {
                "id": "scene-5-browser",
                "type": "browser",
                "url": "http://localhost:8080",
                "title": "Navegador Web — Contenedor Activo",
                "contentType": "webpage",
                "mainContent": "🐳 Aplicación Contenida en Ejecución",
                "speechText": "Comprobamos en el navegador web que nuestra aplicación dockerizada responde perfectamente en localhost:8080."
            },
            {
                "id": "scene-6-diagram",
                "type": "diagram",
                "title": "Arquitectura de Contenedores",
                "nodes": ["Código Fuente", "Dockerfile Recipe", "Docker Image", "Contenedor Cloud"],
                "speechText": "Revisamos el flujo conceptual de la arquitectura de contenedores desde el código hasta la nube."
            },
            {
                "id": "scene-7-outro",
                "type": "outro",
                "title": "¡Contenedor Desplegado!",
                "subtitle": "Suscríbete para más lecciones de DevOps y Kubernetes",
                "githubRepo": "github.com/Medalcode/canal-tutorial-automation",
                "speechText": "¡Y listo! Tu aplicación está contenida. Suscríbete para más tutoriales de DevOps."
            }
        ]
    elif domain == "react_web":
        scenes = [
            {
                "id": "scene-1-intro",
                "type": "intro",
                "title": title_clean,
                "subtitle": "Desarrollo Web Moderno con React & Node.js",
                "requirements": ["Node.js v20+", "VS Code & Terminal", "Navegador Web"],
                "speechText": f"Bienvenidos a esta guía sobre {title_clean}. Construiremos una aplicación web completa desde la estructura de archivos hasta su ejecución en el navegador."
            },
            {
                "id": "scene-2-explorer",
                "type": "file_explorer",
                "projectName": "app-web-react",
                "files": [
                    { "name": "src/", "type": "folder", "active": True },
                    { "name": "  components/", "type": "folder", "active": False },
                    { "name": "    Header.tsx", "type": "file", "active": False },
                    { "name": "    Dashboard.tsx", "type": "file", "active": False },
                    { "name": "  App.tsx", "type": "file", "active": True },
                    { "name": "  main.tsx", "type": "file", "active": False },
                    { "name": "package.json", "type": "file", "active": False },
                ],
                "activeFileDetails": {
                    "name": "App.tsx",
                    "path": "src/App.tsx",
                    "size": "2.8 KB",
                    "lines": 85
                },
                "speechText": "En el explorador de archivos organizamos nuestros componentes de React e interfaces dentro de la carpeta fuente."
            },
            {
                "id": "scene-3-setup",
                "type": "terminal",
                "title": "Instalación de Dependencias Web",
                "terminalPrompt": "user@laptop:~/app-web$",
                "commands": [
                    { "text": "npx create-react-app app-demo --template typescript" },
                    { "text": "npm start", "output": ["Compiled successfully!", "Local: http://localhost:3000"] }
                ],
                "speechText": "Abrimos la terminal de comandos para inicializar la aplicación con TypeScript e iniciar el servidor de desarrollo en el puerto 3000."
            },
            {
                "id": "scene-4-editor",
                "type": "editor",
                "filename": "App.tsx",
                "codeLines": [
                    "import React, { useState } from 'react';",
                    "",
                    "export const App = () => {",
                    "  const [active, setActive] = useState(true);",
                    "",
                    "  return (",
                    "    <div className='dashboard-container'>",
                    "      <h1>Sistema de Monitoreo Web</h1>",
                    "      <button onClick={() => setActive(!active)}>Toggle Estado</button>",
                    "    </div>",
                    "  );",
                    "};"
                ],
                "speechText": "Escribimos el componente principal en VS Code gestionando el estado con react hooks y estilos responsivos."
            },
            {
                "id": "scene-5-browser",
                "type": "browser",
                "url": "http://localhost:3000",
                "title": "Navegador Web — Aplicación en Vivo",
                "contentType": "webpage",
                "mainContent": "🚀 Aplicación React Desplegada y Funcionando",
                "speechText": "Abrimos el navegador web en localhost:3000. Observamos nuestra aplicación web renderizada e interactiva."
            },
            {
                "id": "scene-6-http",
                "type": "http-client",
                "method": "GET",
                "url": "http://localhost:3000/api/status",
                "statusCode": 200,
                "responseBody": "{\n  \"status\": \"online\",\n  \"latency_ms\": 12,\n  \"users_connected\": 42\n}",
                "speechText": "Probamos la respuesta del backend conectándonos a la API REST e inspeccionando el JSON de salida."
            },
            {
                "id": "scene-7-outro",
                "type": "outro",
                "title": "¡Aplicación Web Lista!",
                "subtitle": "Suscríbete para ver la lección de despliegue en la nube",
                "githubRepo": "github.com/Medalcode/canal-tutorial-automation",
                "speechText": "¡Y listo! Tu interfaz web está funcionando. Suscríbete para más contenido de frontend y backend."
            }
        ]
    else:
        # Dominio general rico (7 escenas)
        scenes = [
            {
                "id": "scene-1-intro",
                "type": "intro",
                "title": title_clean,
                "subtitle": "Tutorial Paso a Paso para Desarrolladores",
                "requirements": ["Entorno de Desarrollo", "Terminal de Comandos", "Visual Studio Code"],
                "speechText": f"Bienvenidos a esta guía sobre {title_clean}. Veremos los componentes principales y herramientas necesarias paso a paso."
            },
            {
                "id": "scene-2-explorer",
                "type": "file_explorer",
                "projectName": "proyecto-demo",
                "files": [
                    { "name": "src/", "type": "folder", "active": False },
                    { "name": "  main.js", "type": "file", "active": True },
                    { "name": "Dockerfile", "type": "file", "active": False },
                    { "name": "package.json", "type": "file", "active": False },
                ],
                "activeFileDetails": {
                    "name": "main.js",
                    "path": "src/main.js",
                    "size": "2.1 KB",
                    "lines": 60
                },
                "speechText": "Revisamos la arquitectura del proyecto en el explorador de archivos con la estructura modular preparada."
            },
            {
                "id": "scene-3-diagram",
                "type": "diagram",
                "title": "Arquitectura y Componentes",
                "nodes": ["Cliente Web", "API Backend", "Base de Datos"],
                "speechText": "En este diagrama observamos la interacción conceptual entre el cliente web, la API y la base de datos."
            },
            {
                "id": "scene-4-setup",
                "type": "terminal",
                "title": "Consola de Comandos",
                "terminalPrompt": "user@laptop:~/proyecto$",
                "commands": [
                    { "text": "mkdir proyecto-demo && cd proyecto-demo" },
                    { "text": "git init", "output": ["Initialized empty Git repository in /proyecto-demo/.git/"] }
                ],
                "speechText": "En la consola ejecutamos los comandos de inicialización del proyecto y control de versiones."
            },
            {
                "id": "scene-5-editor",
                "type": "editor",
                "filename": "main.js",
                "codeLines": [
                    "// Implementación principal para " + title_clean,
                    "function initSystem() {",
                    "    console.log('Sistema iniciado con éxito');",
                    "    return { status: 'ok', timestamp: Date.now() };",
                    "}",
                    "",
                    "module.exports = { initSystem };"
                ],
                "speechText": "En el editor de código desarrollamos la función principal con estándares de código limpio."
            },
            {
                "id": "scene-6-analytics",
                "type": "analytics_chart",
                "title": "Panel de Control y Métricas",
                "metrics": [
                    { "label": "Estado", "value": "ACTIVO", "change": "OK" },
                    { "label": "Rendimiento", "value": "99.8%", "change": "+ 2%" }
                ],
                "chartTitle": "Indicadores Clave del Sistema",
                "speechText": "Verificamos los indicadores y métricas de ejecución en el panel de monitoreo."
            },
            {
                "id": "scene-7-outro",
                "type": "outro",
                "title": "¡Proyecto Completado!",
                "subtitle": "Suscríbete y activa la campanita para más tutoriales",
                "githubRepo": "github.com/Medalcode/canal-tutorial-automation",
                "speechText": "Hemos finalizado el proyecto. Si te ha gustado, suscríbete al canal y dale un me gusta."
            }
        ]

    return {
        "title": title_clean,
        "subtitle": "Guía Práctica Automatizada",
        "category": "TUTORIAL DESARROLLO",
        "scenes": scenes
    }

def generate_ai_script(idea: str, target_length: str = "standard") -> Dict[str, Any]:
    gemini_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")

    if gemini_key:
        try:
            prompt_text = f"""Genera un guion muy rico, variado y completo (entre 7 y 10 escenas) para un video tutorial basado en: "{idea}".
Utiliza variedad de tipos de escenas como: "intro", "file_explorer", "terminal", "editor", "browser", "excel", "analytics_chart", "diagram", "features", "outro".
Debes devolver UNICAMENTE un objeto JSON válido (sin ```json):
{{
  "title": "Título atractivo sobre {idea}",
  "subtitle": "Subtítulo explicativo paso a paso",
  "category": "TUTORIAL DESARROLLO",
  "scenes": [
    {{
      "id": "scene-1",
      "type": "intro",
      "title": "Introducción a {idea}",
      "subtitle": "Aprende los conceptos clave",
      "requirements": ["Requisito 1", "Requisito 2"],
      "speechText": "Explicación detallada de la lección..."
    }},
    {{
      "id": "scene-2",
      "type": "file_explorer",
      "projectName": "proyecto-demo",
      "files": [{{"name": "main.py", "type": "file", "active": true}}],
      "activeFileDetails": {{"name": "main.py", "path": "main.py", "size": "2.4 KB", "lines": 50}},
      "speechText": "Revisamos los archivos del proyecto..."
    }},
    {{
      "id": "scene-3",
      "type": "terminal",
      "title": "Comandos de Consola",
      "commands": [{{"text": "comando 1"}}],
      "speechText": "Ejecutamos en la consola..."
    }},
    {{
      "id": "scene-4",
      "type": "editor",
      "filename": "main.py",
      "codeLines": ["# Codigo"],
      "speechText": "Escribimos el código..."
    }},
    {{
      "id": "scene-5",
      "type": "browser",
      "url": "http://localhost:3000",
      "title": "Navegador Web",
      "mainContent": "Aplicación Funcional",
      "speechText": "Vemos el resultado en el navegador..."
    }},
    {{
      "id": "scene-6",
      "type": "excel",
      "title": "Plantilla Excel",
      "sheetName": "Reporte",
      "formula": "=SUMA(A1:A5)",
      "headers": ["Col 1", "Col 2"],
      "rows": [["Dato 1", "Dato 2"]],
      "speechText": "Analizamos la plantilla de Excel..."
    }},
    {{
      "id": "scene-7",
      "type": "analytics_chart",
      "title": "Dashboard Power BI",
      "metrics": [{{"label": "Ventas", "value": "$100K", "change": "+10%"}}],
      "speechText": "Inspeccionamos los gráficos de analítica..."
    }},
    {{
      "id": "scene-8",
      "type": "outro",
      "title": "¡Fin del Tutorial!",
      "subtitle": "Suscríbete",
      "githubRepo": "github.com/usuario/repo",
      "speechText": "Gracias por ver el video..."
    }}
  ]
}}"""
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}"
            req = urllib.request.Request(
                url,
                data=json.dumps({"contents": [{"parts": [{"text": prompt_text}]}]}).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                text_response = result['candidates'][0]['content']['parts'][0]['text']
                clean_json = text_response.replace("```json", "").replace("```", "").strip()
                return json.loads(clean_json)
        except Exception as e:
            logger.error(f"Error al llamar a Gemini: {e}")

    # Fallback inteligente multidominio con 7-8 escenas ricas
    return generate_multidomain_script(idea, target_length)
