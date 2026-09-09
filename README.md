# CodeStage

**Automated Technical Video Production Engine**

CodeStage is a programmatic video rendering engine designed to turn structured scripts (YAML/JSON) into high-quality technical tutorial videos. It composes AI-generated avatars, text-to-speech, and a deterministic virtual IDE to create engaging programming content.

## Architecture

CodeStage abstracts the video generation process into discrete, interchangeable providers:

- **Scene Engine**: Parses structured JSON/YAML scripts into a timeline.
- **Audio Engine**: Synthesizes speech using providers like EdgeTTS.
- **Avatar Engine**: Renders a speaking avatar via providers (Local procedural, SadTalker, H3 Max).
- **IDE Engine**: Deterministically renders code typing and terminal execution using Remotion.
- **Compositor**: Stitches the layers together frame by frame.

## Documentation

The full Software Design Document (SDD) can be found in `docs/sdd/`:
- [Product Requirements](docs/sdd/01-product-requirements.md)
- [System Architecture](docs/sdd/02-system-architecture.md)
- [Scene Engine](docs/sdd/03-scene-engine.md)

## Current Status

*Project is currently undergoing architectural migration from its legacy procedural pipeline into the CodeStage Engine architecture (Phase 1).*
