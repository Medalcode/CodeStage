# ADR 0001: Multi-Engine Branch Isolation Architecture

**Estado**: Aceptado  
**Fecha**: 2026-08-23  
**Autor**: CTO & Staff Software Architect  

---

##  Contexto

El sistema requiere soportar múltiples tecnologías de generación de video (React Remotion, MoviePy 2D Sprite, Manim Vectorial, VS Code Purist Simulator y LTX AI Avatar). Cada motor presenta dependencias exclusivas y requisitos de rendimiento distintos.

##  Decisión de Arquitectura

Decidimos aislar cada motor de renderizado en **5 ramas de Git independientes** y asignarle a cada una un **puerto de ejecución dedicado**:

1. `main` -> Puerto `5000` (Remotion React Engine)
2. `feature/python-sprite-compositor` -> Puerto `5001` (Python 40/60 Sprite Compositor)
3. `feature/manim-vector-engine` -> Puerto `5002` (Manim Vector Engine)
4. `feature/vscode-ide-purist-engine` -> Puerto `5003` (VS Code Purist IDE Simulator)
5. `feature/ltx-ai-avatar-engine` -> Puerto `5004` (LTX AI Avatar Diffusion Engine)

## 🎯 Consecuencias y Beneficios

- **Cero Choques de Dependencias**: Los requerimientos pesados (como Manim o Chromium) no contaminan los entornos ligeros de Python nativo.
- **Pruebas Automatizadas Verificables**: Cada rama mantiene 100% de pasabilidad en `pytest`.
- **Navegación Unificada**: El cliente puede conmutar entre los motores en vivo utilizando el **Unified Engine Switcher Dropdown** en el encabezado del Dashboard.
