# Orchestrators

Orchestrators are user-facing entry points that decide what AIHub should do.

Examples may include:

- ChatGPT
- Voice
- CLI
- Future web UI

Orchestrators should not contain provider-specific integration logic. They should route requests through capabilities and services.
