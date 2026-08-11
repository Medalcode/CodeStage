import os
import json
import urllib.request
from typing import Dict, Any
from logger import get_logger

logger = get_logger("generator.script")

def generate_multidomain_script(idea: str, target_length: str = "standard") -> Dict[str, Any]:
    """
    Genera un guion rico adaptado a la tecnología solicitada sin plantillas estáticas repetitivas.
    """
    idea_lower = idea.lower()

    # Detección de dominio
    if any(k in idea_lower for k in ["python", "pandas", "numpy", "data"]):
        domain = "python_data"
    elif any(k in idea_lower for k in ["docker", "contenedor", "devops", "kubernete"]):
        domain = "docker"
    elif any(k in idea_lower for k in ["react", "next", "frontend", "component"]):
        domain = "react"
    elif any(k in idea_lower for k in ["sql", "postgres", "database", "base de dato"]):
        domain = "sql"
    elif any(k in idea_lower for k in ["git", "github", "commit", "branch"]):
        domain = "git"
    elif any(k in idea_lower for k in ["fastapi", "uvicorn"]):
        domain = "fastapi"
    else:
        domain = "general"

    title_clean = idea.strip() or "Guía Práctica de Desarrollo"

    # Construcción de escenas según dominio
    if domain == "python_data":
        scenes = [
            {
                "id": "scene-1-intro",
                "type": "intro",
                "title": title_clean,
                "subtitle": "Análisis y Procesamiento de Datos con Python",
                "requirements": ["Python 3.10+", "Biblioteca Pandas", "Jupyter / VS Code"],
                "speechText": f"Bienvenidos a esta guía sobre {title_clean}. En el desarrollo moderno, el procesamiento de datos estructurados es fundamental para extraer información de alto valor para las organizaciones."
            },
            {
                "id": "scene-2-diagram",
                "type": "diagram",
                "title": "Pipeline de Procesamiento de Datos",
                "nodes": ["Archivos CSV / JSON", "DataFrames Pandas", "Limpieza & Transformación", "Exportación / BI"],
                "speechText": "Revisemos el flujo de datos. Primero leemos la fuente de información, la cargamos en memoria utilizando DataFrames de Pandas, filtramos las anomalías y generamos los reportes finales."
            },
            {
                "id": "scene-3-setup",
                "type": "terminal",
                "title": "Entorno Virtual e Instalación",
                "terminalPrompt": "user@laptop:~/data-project$",
                "commands": [
                    { "text": "python -m venv venv && source venv/bin/activate" },
                    { "text": "pip install pandas numpy openpyxl matplotlib", "output": ["Successfully installed pandas-2.2.0 numpy-1.26.0"] }
                ],
                "speechText": "Abrimos nuestra terminal para configurar un entorno virtual aislado de Python e instalar Pandas junto con las dependencias necesarias."
            },
            {
                "id": "scene-4-editor",
                "type": "editor",
                "filename": "analysis.py",
                "codeLines": [
                    "import pandas as pd",
                    "",
                    "# Cargar datos de ventas",
                    "df = pd.read_csv('ventas_2026.csv')",
                    "",
                    "# Filtrar ventas mayores a 1000 USD",
                    "df_filtered = df[df['total'] > 1000]",
                    "",
                    "# Agrupar por región y calcular el promedio",
                    "resumen = df_filtered.groupby('region')['total'].mean()",
                    "print(resumen)"
                ],
                "speechText": "En nuestro script creamos el DataFrame, aplicamos filtros sobre los montos de ventas y agrupamos por región geográfica calculando métricas clave de forma inmediata."
            },
            {
                "id": "scene-5-features",
                "type": "features",
                "title": "Beneficios de Automatizar con Python",
                "features": ["Procesamiento en milisegundos", "Integración con Bases de Datos", "Cero errores manuales en Excel"],
                "speechText": "Al automatizar este flujo con Python reducimos el tiempo de procesamiento de horas a milisegundos y eliminamos por completo los errores de edición manual."
            },
            {
                "id": "scene-6-outro",
                "type": "outro",
                "title": "¡Procesamiento Completado!",
                "subtitle": "Suscríbete y activa la campanita para más tutoriales de Data Science",
                "githubRepo": "github.com/Medalcode/python-data-automation",
                "speechText": "Y con esto hemos completado nuestro pipeline automatizado en Python. Si te ha gustado esta guía, apóyame suscribiéndote al canal."
            }
        ]
    elif domain == "docker":
        scenes = [
            {
                "id": "scene-1-intro",
                "type": "intro",
                "title": title_clean,
                "subtitle": "Contenedores y Despliegue Profesional",
                "requirements": ["Docker Desktop", "Terminal / PowerShell", "Código de tu aplicación"],
                "speechText": f"Bienvenidos a esta guía práctica sobre {title_clean}. Los contenedores permiten empaquetar aplicaciones junto con todas sus dependencias garantizando que funcionen idénticamente en cualquier entorno."
            },
            {
                "id": "scene-2-diagram",
                "type": "diagram",
                "title": "Arquitectura de Contenedores",
                "nodes": ["Código Fuente", "Dockerfile Script", "Docker Image", "Contenedor en Ejecución"],
                "speechText": "Comprendamos la arquitectura. A partir del código escribimos la receta Dockerfile, construimos la imagen inmutable y la desplegamos como un contenedor aislado."
            },
            {
                "id": "scene-3-setup",
                "type": "terminal",
                "title": "Verificación e Inspección de Docker",
                "terminalPrompt": "user@laptop:~/app$",
                "commands": [
                    { "text": "docker --version", "output": ["Docker version 25.0.3, build 4debf41"] },
                    { "text": "docker build -t mi-app:v1 .", "output": ["Step 1/5 : FROM node:20-alpine", "Successfully tagged mi-app:v1"] },
                    { "text": "docker run -d -p 8080:8080 mi-app:v1", "output": ["a1b2c3d4e5f67890"] }
                ],
                "speechText": "En la consola verificamos que el demonio de Docker esté activo, construimos la imagen asignando una etiqueta de versión y lanzamos el contenedor exponiendo el puerto del servidor."
            },
            {
                "id": "scene-4-editor",
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
                "speechText": "En el Dockerfile definimos una imagen base ligera Alpine, establecemos el directorio de trabajo, instalamos dependencias y configuramos el comando de arranque."
            },
            {
                "id": "scene-5-outro",
                "type": "outro",
                "title": "¡Contenedor Desplegado!",
                "subtitle": "Suscríbete para aprender Kubernetes y CI/CD DevOps",
                "githubRepo": "github.com/Medalcode/docker-devops-guide",
                "speechText": "Ahora tu aplicación está completamente contenida y lista para ser enviada a la nube. Suscríbete para aprender más sobre arquitectura DevOps."
            }
        ]
    else:
        scenes = [
            {
                "id": "scene-1-intro",
                "type": "intro",
                "title": title_clean,
                "subtitle": "Guía Paso a Paso para Desarrolladores",
                "requirements": ["Entorno de Desarrollo", "Terminal de Comandos", "Visual Studio Code"],
                "speechText": f"Bienvenidos a este tutorial completo sobre {title_clean}. Hoy aprenderemos las mejores prácticas para estructurar e implementar esta solución desde cero."
            },
            {
                "id": "scene-2-diagram",
                "type": "diagram",
                "title": "Flujo de Ejecución del Sistema",
                "nodes": ["Entrada de Datos", "Módulo Central de Lógica", "Capa de Validación", "Resultado de Salida"],
                "speechText": "Analicemos primero el diseño conceptual de la solución para comprender cómo fluye la información entre cada componente."
            },
            {
                "id": "scene-3-setup",
                "type": "terminal",
                "title": "Configuración del Proyecto",
                "terminalPrompt": "user@laptop:~/proyecto$",
                "commands": [
                    { "text": "mkdir proyecto-demo && cd proyecto-demo" },
                    { "text": "git init", "output": ["Initialized empty Git repository in /proyecto-demo/.git/"] }
                ],
                "speechText": "Comenzamos abriendo nuestra terminal para inicializar el repositorio y preparar la estructura del proyecto."
            },
            {
                "id": "scene-4-editor",
                "type": "editor",
                "filename": "main.js",
                "codeLines": [
                    "// Implementación principal de " + title_clean,
                    "function initApplication() {",
                    "    console.log('Inicializando sistema...');",
                    "    return { status: 'success', timestamp: Date.now() };",
                    "}",
                    "",
                    "module.exports = { initApplication };"
                ],
                "speechText": "En el editor desarrollamos el código limpio aplicando modularidad, buenas prácticas de naming y manejo de estado."
            },
            {
                "id": "scene-5-outro",
                "type": "outro",
                "title": "¡Proyecto Completado!",
                "subtitle": "Suscríbete para ver la siguiente lección en video",
                "githubRepo": "github.com/Medalcode/canal-tutorial-automation",
                "speechText": "Y así concluimos esta lección. Si te ha resultado útil, no olvides darle un me gusta y suscribirte al canal."
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
            prompt_text = f"""Genera un guion detallado y rico para un video tutorial basado en la siguiente idea: "{idea}".
Debes devolver UNICAMENTE un objeto JSON válido con la siguiente estructura (sin formato de markdown, sin ```json):
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
      "speechText": "Explicación detallada en español de al menos 3 oraciones completas sobre lo que se aprenderá..."
    }},
    {{
      "id": "scene-2",
      "type": "diagram",
      "title": "Arquitectura del Sistema",
      "nodes": ["Componente A", "Componente B", "Componente C"],
      "speechText": "Explicación detallada en español del diagrama de arquitectura..."
    }},
    {{
      "id": "scene-3",
      "type": "terminal",
      "title": "Instalación de Dependencias",
      "terminalPrompt": "user@laptop:~/proyecto$",
      "commands": [
        {{"text": "comando 1"}},
        {{"text": "comando 2", "output": ["resultado"]}}
      ],
      "speechText": "Explicación detallada en español de los comandos..."
    }},
    {{
      "id": "scene-4",
      "type": "editor",
      "filename": "main.py",
      "codeLines": [
        "# Codigo principal especifico para " + idea,
        "def main():",
        "    pass"
      ],
      "speechText": "Explicación detallada en español del código escrito..."
    }},
    {{
      "id": "scene-5",
      "type": "features",
      "title": "Ventajas Clave",
      "features": ["Ventaja 1", "Ventaja 2", "Ventaja 3"],
      "speechText": "Explicación detallada en español de los beneficios..."
    }},
    {{
      "id": "scene-6",
      "type": "outro",
      "title": "¡Proyecto Completado!",
      "subtitle": "Suscríbete para ver la siguiente lección",
      "githubRepo": "github.com/usuario/repo",
      "speechText": "Palabras finales de despedida e invitación a suscribirse..."
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

    # Fallback inteligente multidominio
    return generate_multidomain_script(idea, target_length)
