# 01 PRODUCT REQUIREMENTS

## 1. Functional Requirements (FR)

### FR-001: Script Ingestion
- **Description**: The system must parse video scripts defined in a structured format (JSON or YAML).
- **Rationale**: Decouples script generation (AI/Manual) from video execution.
- **Inputs**: `.json` or `.yaml` file containing the scene definitions.
- **Outputs**: Validated `Script` object in memory.
- **Dependencies**: Scene Engine (Pydantic models).
- **Acceptance Criteria**: System rejects invalid schemas with precise error messages.

### FR-002: Scene Sequencing
- **Description**: The system must process scenes in sequential order, calculating absolute start and end times on the main timeline.
- **Rationale**: Required for the final compositor to stitch clips without gaps or overlaps.
- **Inputs**: List of `Scene` objects.
- **Outputs**: Timeline manifest with exact timestamps.

### FR-003: TTS Generation
- **Description**: Generate speech audio from text using external providers.
- **Rationale**: Automated narration.
- **Inputs**: Text string, voice ID, provider ID.
- **Outputs**: Audio file (`.wav` or `.mp3`) and duration.
- **Dependencies**: Audio Engine, Audio Providers (EdgeTTS, ElevenLabs).

### FR-004: Lip Synchronization
- **Description**: Extract visemes or phonemes from the generated audio to sync with avatar animations.
- **Rationale**: Make characters look like they are actually speaking.
- **Inputs**: Audio file, text transcript.
- **Outputs**: Array of timestamps mapped to mouth shapes.
- **Dependencies**: LipSync Provider (e.g., Rhubarb).

### FR-005: Avatar Rendering
- **Description**: Generate the visual representation of the speaker.
- **Rationale**: Core feature of CodeStage videos.
- **Inputs**: Audio file, viseme data, Avatar instructions (pose, look direction).
- **Outputs**: Video clip (MP4) with transparent or solid background.
- **Dependencies**: Avatar Engine, Avatar Providers (SadTalker, H3 Max).

### FR-006: Progressive Code Rendering
- **Description**: Animate typing of code character by character or line by line.
- **Rationale**: Simulate a real developer writing code.
- **Inputs**: Code snippet, typing speed, syntax highlighting rules.
- **Outputs**: Video sequence of code being written.
- **Dependencies**: IDE Engine (Remotion).

### FR-007: Terminal Simulation
- **Description**: Animate a command line interface executing commands and displaying output.
- **Rationale**: Demonstrate DevOps/CLI steps.
- **Inputs**: Command string, simulated output, delays.
- **Outputs**: Video sequence of the terminal execution.
- **Dependencies**: IDE Engine.

### FR-008: Scene Composition
- **Description**: Overlay all visual and audio elements (Avatar, IDE, Background) into a single frame sequence.
- **Rationale**: Final look of the video.
- **Inputs**: Avatar clip, IDE clip, Audio clip, Composition rules (split-screen, full-screen).
- **Outputs**: Final composite video segment.
- **Dependencies**: Compositor Engine.

### FR-009: Output Generation
- **Description**: Concatenate all composed scenes into the final deliverable.
- **Rationale**: End-user deliverable.
- **Inputs**: Ordered list of composite segments.
- **Outputs**: Single high-quality `MP4` file.
- **Dependencies**: FFmpeg.

### FR-010: Cache Management
- **Description**: Persist intermediate artifacts (audio, avatar clips, IDE renders) and reuse them if the inputs haven't changed.
- **Rationale**: Drastically reduce render times and API costs (e.g., H3 Max).
- **Inputs**: Hashes of scene parameters.
- **Outputs**: Cache hit/miss status and file paths.

## 2. Non-Functional Requirements
- **NFR-001 Reproducibility**: Given the same Script JSON, the system MUST produce visually identical output across different runs.
- **NFR-002 Extensibility**: Adding a new AI Provider (e.g., a new TTS or Avatar model) MUST NOT require changing the core Scene Engine or Compositor.
