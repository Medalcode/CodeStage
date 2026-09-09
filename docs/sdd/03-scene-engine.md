# 03 SCENE ENGINE

## 1. Concept
The Scene Engine defines the declarative structure of a video. 
Instead of rigid structures where a Scene explicitly has an `Avatar` and an `IDE`, we use a flexible `Layer/Element` model.

## 2. Data Models (Pydantic)

### 2.1. Script
- `title` (str)
- `scenes` (List[Scene])

### 2.2. Scene
A discrete timeline block.
- `id` (str)
- `audio_track` (List[AudioElement]) -> Primarily Narration.
- `visual_layers` (List[VisualElement]) -> Ordered by Z-Index.

### 2.3. Audio Elements
#### NarrationElement
- `text` (str)
- `voice_id` (str)

### 2.4. Visual Elements

All Visual Elements share base properties:
- `layout_position` (e.g., "left_half", "full_screen", "picture_in_picture")

#### AvatarElement
- `pose` (str)
- `look_target` (str)
- `sync_with_audio` (bool) -> If true, syncs with the `audio_track` narration.

#### IDEElement
- `file_path` (str)
- `code_content` (str)
- `action` (str) -> e.g., "type", "highlight"

#### TerminalElement
- `command` (str)
- `output` (str)

## 3. YAML Example

```yaml
title: "Docker Tutorial"
scenes:
  - id: "scene-1"
    audio_track:
      - type: narration
        text: "Vamos a crear nuestro Dockerfile."
    visual_layers:
      - type: avatar
        pose: explaining
        look_target: camera
        layout_position: right_half
        sync_with_audio: true
      - type: ide
        file_path: "Dockerfile"
        code_content: "FROM ubuntu:latest"
        action: type
        layout_position: left_half
```
