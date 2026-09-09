# 03 SCENE ENGINE

## 1. Concept
The Scene Engine defines the canonical data structure for CodeStage. A script is a collection of scenes.

## 2. Data Models (Pydantic representation)

### 2.1. Script
- `title` (str)
- `global_settings` (dict): e.g., default voice, resolution.
- `scenes` (List[Scene])

### 2.2. Scene
A scene represents a discrete segment of the video with a single continuous narration and layout.
- `id` (str)
- `narration` (Narration)
- `layout` (Enum): `split_screen`, `full_ide`, `full_avatar`.
- `avatar` (Optional[AvatarAction])
- `ide` (Optional[IDEAction])

### 2.3. Narration
- `text` (str)
- `voice_override` (Optional[str])

### 2.4. AvatarAction
- `provider` (str): e.g., `h3max`, `sadtalker`
- `pose` (Enum): `idle`, `typing`, `explaining`
- `look` (Enum): `camera`, `screen`

### 2.5. IDEAction
Can be one of several subtypes:

#### EditorAction
- `file_path` (str)
- `content` (str)
- `action` (Enum): `type_all`, `highlight_line`, `replace`

#### TerminalAction
- `command` (str)
- `output` (str)

#### BrowserAction
- `url` (str)
- `action` (Enum): `load`, `scroll`

## 3. YAML Example

```yaml
title: "Hello World Python"
scenes:
  - id: "scene-1-intro"
    layout: split_screen
    narration:
      text: "Hola, vamos a escribir nuestro primer script en Python."
    avatar:
      provider: h3max
      pose: explaining
      look: camera
    ide:
      type: editor
      file_path: "main.py"
      content: ""
      
  - id: "scene-2-code"
    layout: split_screen
    narration:
      text: "Simplemente usamos la función print."
    avatar:
      provider: h3max
      pose: typing
      look: screen
    ide:
      type: editor
      file_path: "main.py"
      action: type_all
      content: |
        def main():
            print("Hello World")
```
