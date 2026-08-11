# ADR-0002: Transición de Backend a FastAPI + WebSockets

* **Estatus**: Aprobado
* **Fecha**: 2026-08-10
* **Autores**: Staff Software Architect & Principal Engineer

## Contexto
El servidor backend inicial utilizaba la clase nativa `http.server.SimpleHTTPRequestHandler` de Python. Aunque simple, carecía de validación de datos en tiempo de compilación, no generaba documentación OpenAPI y obligaba al frontend a realizar polling HTTP cada 2 segundos para obtener el estado del renderizado.

## Decisión
Migrar la capa del servidor backend a **FastAPI + Uvicorn**, con validación de modelos via **Pydantic** y soporte de **WebSockets** bidireccionales en `/ws/render`.

## Consecuencias
* **Positivas**:
  * Especificación interactiva OpenAPI 3.0 / Swagger en `/docs`.
  * Telemetría de renderizado en tiempo real por WebSockets sin sobrecarga de red.
  * Desacoplamiento de la lógica de renderizado en `RemotionRendererService`.
* **Negativas**:
  * Adición de las dependencias `fastapi` y `uvicorn` en `requirements.txt`.
