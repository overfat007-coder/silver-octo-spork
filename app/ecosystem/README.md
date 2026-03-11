# Ecosystem package

Production-oriented extensibility layer for SmartFlow.

## Components
- Contracts and registry for pluggable backends.
- Serializers (`json`, `csv`) for export/import workflows.
- KV storage adapters (`memory`, `sqlite`).
- In-process reliable queue abstraction.
- FastAPI middleware for request context propagation.
- Retry utility for transient fault handling.
- CLI helper for ops scripting.

## Real scenarios
- Export/import task snapshots between environments.
- Cache per-request metadata for debugging and tracing.
- Persist lightweight state without external Redis dependency.
- Build scripts that run maintenance actions from CI/CD.
