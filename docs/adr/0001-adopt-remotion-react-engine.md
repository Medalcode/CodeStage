# ADR-0001: Adopción de Remotion + React como Motor Canónico de Video

* **Estatus**: Aprobado
* **Fecha**: 2026-08-10
* **Autores**: Staff Software Architect & Principal Engineer

## Contexto
Originalmente el proyecto utilizaba bibliotecas de composición de video procedurales (MoviePy / FFmpeg) y parches directos a nivel de script en Python para manipular assets 2D/3D. Esto resultaba en fugas de descriptores de archivos en Windows, sobrecarga excesiva de RAM y dificultad para componer interfaces complejas tipo IDE o consola.

## Decisión
Adoptar **Remotion (React + TypeScript)** como el motor canónico e imperativo de creación de video.

## Consecuencias
* **Positivas**:
  * Programación declarativa de interfaces de video en React.
  * Renderizado determinista a 1080p 30/60 FPS mediante Chromium Headless.
  * Facilidad para crear composiciones horizontales (16:9) y verticales (9:16 Shorts/TikTok).
* **Negativas**:
  * Requiere runtime de Node.js y Chromium instalado en la máquina cliente o contenedor Docker.
