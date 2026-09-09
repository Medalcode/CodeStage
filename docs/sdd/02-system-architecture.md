# 02 SYSTEM ARCHITECTURE

## 1. Core Principles

- **Domain-Driven Separations**: Domain logic (`models/`) is strictly pure Python data structures. Infrastructure (`providers/`, `compositor/`) handles I/O and external calls.
- **Protocol-Based Inversion of Control**: External dependencies are defined by `typing.Protocol` interfaces, enabling structural subtyping, easy testing without ABC inheritance bureaucracy.
- **Deterministic Assembly, Probabilistic Assets**: CodeStage guarantees a deterministic layout and timing pipeline, while allowing assets (Avatar, TTS) to be probabilistic. Reproducibility is achieved by aggressively caching probabilistic `Artifacts`.

## 2. High-Level Components

### 1. Domain Models
- Pure Pydantic schemas. 
- Defines the `Script`, `Scene`, `Tracks`, and `Elements`.

### 2. Orchestrator
- The conductor. It receives a `Script`, walks through the elements, calculates Identity Keys, checks Cache, and delegates work to the Providers.

### 3. Providers (Protocols)
- `AudioProviderProtocol`
- `VideoGenerationProtocol` (e.g., H3 Max, SadTalker)
- `IDERendererProtocol`
- `CompositorProtocol`

### 4. Cache & Artifact System
- Central storage for generated media.
- Maps `IdentityKey(Domain Hash + Config + Version)` -> `Artifact`.

## 3. Architecture Requirements (ARCH)

### ARCH-001: Protocol Interfaces
```python
from typing import Protocol
from codestage.domain.models import Artifact, AvatarElement

class VideoGenerationProtocol(Protocol):
    def generate_avatar(self, element: AvatarElement, audio_artifact: Artifact) -> Artifact:
        ...
```

### ARCH-002: Strict Artifact Identity
Caching is NOT a simple hash of the text. The Identity Key must incorporate:
1. Provider ID & Version.
2. Configuration (e.g., Voice ID, Resolution).
3. The content of the Domain Element.
4. The hashes of dependent source assets (e.g., the hash of the Audio Artifact drives the Avatar identity).

### ARCH-003: Render Manifest
Every final video output must produce a `manifest.json` that details the exact `Artifact` IDs and Providers used for every scene to guarantee provenance and debuggability.
