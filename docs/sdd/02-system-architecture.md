# 02 SYSTEM ARCHITECTURE

## 1. Core Principles

- **Separation of Concerns**: The domain logic (parsing scripts, calculating timelines) is strictly separated from the rendering logic (calling Remotion, FFmpeg, API endpoints).
- **Provider Pattern**: Any external dependency (AI models, CLI tools) must be abstracted behind a standard Python interface.
- **Determinism First**: The system favors reproducible, deterministic outputs. Generative AI is used for asset generation (e.g., Avatar), but not for the layout, code typing, or composition.

## 2. High-Level Components

### 1. Scene Engine
- The source of truth.
- Parses input (YAML/JSON) into strictly typed Pydantic models.
- Validates properties (e.g., "typing speed must be > 0").

### 2. Orchestrator
- Reads the validated Scenes and coordinates the Engines.
- Determines what needs to be rendered and what can be fetched from Cache.

### 3. Engines & Providers
- **Audio Engine**: Interfaces with `TTSProvider` (e.g., `EdgeTTSProvider`).
- **Avatar Engine**: Interfaces with `AvatarProvider` (e.g., `LocalProceduralProvider`, `SadTalkerProvider`, `H3MaxProvider`).
- **IDE Engine**: Interfaces with `IDERendererProvider` (e.g., `RemotionIDEProvider`).
- **Compositor Engine**: Interfaces with `CompositorProvider` (e.g., `FFmpegCompositorProvider`).

## 3. Architecture Requirements (ARCH)

### ARCH-001: Strict Interfaces
All providers must inherit from an Abstract Base Class (ABC).
Example:
```python
class AvatarProvider(ABC):
    @abstractmethod
    def generate(self, scene: Scene, audio_path: str) -> str:
        pass
```

### ARCH-002: Deterministic Hashing
Every Engine must be able to compute a deterministic hash of its inputs.
If `hash(inputs)` exists in the cache directory, the Engine skips generation and returns the cached artifact path.

### ARCH-003: Remotion Isolation
The Remotion App acts as a pure rendering function. It takes a JSON props file and outputs an MP4 or image sequence. It must not make external network requests or side-effects during render.
