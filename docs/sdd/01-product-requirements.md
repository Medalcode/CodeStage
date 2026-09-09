# 01 PRODUCT REQUIREMENTS

## 1. Functional Requirements (FR)

### FR-001: Script Ingestion
- **Description**: The system must parse video scripts defined in a structured format (JSON or YAML) into the Domain Model.
- **Rationale**: Decouples script generation from video execution.
- **Inputs**: `.json` or `.yaml` file.
- **Outputs**: Validated `Script` object in memory.
- **Acceptance Criteria**: Strict schema validation rejecting invalid schemas.

### FR-002: Scene Sequencing
- **Description**: The system calculates absolute start and end times on a main timeline based on Audio durations.
- **Inputs**: `Script` containing multiple `Scene` blocks.
- **Outputs**: Timeline manifest with precise frame timestamps.

### FR-003: Asset Generation Orchestration
- **Description**: The orchestrator must evaluate required assets (Audio, Avatar, IDE frames) and delegate generation to specific Providers.
- **Rationale**: Parallelizes asset creation and delegates complex tasks.

### FR-004: Audio Generation
- **Description**: Generate speech audio from text.
- **Dependencies**: Any provider implementing `AudioProviderProtocol`.

### FR-005: Avatar Generation
- **Description**: Generate visual representations of the speaker.
- **Dependencies**: Any provider implementing `VideoGenerationProtocol` (e.g., H3MaxProvider).

### FR-006: Deterministic Code Rendering
- **Description**: Render code typing and terminal execution identically on every run.
- **Dependencies**: Any provider implementing `IDERendererProtocol` (e.g., Remotion).

### FR-007: Cache Management
- **Description**: Persist intermediate `Artifact` objects in local storage indexed by a strong deterministic Identity Key.
- **Rationale**: Prevent re-rendering expensive generative video (H3 Max) unless the underlying prompt, text, or configuration changes.

### FR-008: Scene Composition
- **Description**: Assemble visual and audio artifacts into a single output video deterministically.
- **Outputs**: Single high-quality `MP4` file.

## 2. Non-Functional Requirements
- **NFR-001 Reproducibility**: Given the same Script, configuration, and a primed Cache, the compositor MUST produce an output bit-for-bit identical to previous runs.
- **NFR-002 Extensibility**: Adding new AI Models or Renderers MUST only require creating a class that adheres to the respective `typing.Protocol`.
- **NFR-003 Decoupling**: Domain models (Scenes, Tracks, Elements) MUST NOT contain rendering logic or import infrastructure libraries (FFmpeg, requests).
