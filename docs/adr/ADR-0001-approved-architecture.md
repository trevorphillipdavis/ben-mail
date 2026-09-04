# ADR-0001: Approved AIHub Architecture

## Status

Approved

## Date

2026-09-04

## Context

AIHub is intended to become a personal AI operating system rather than a collection of one-off automations. The system needs to support multiple orchestrators, interchangeable providers, deterministic local execution, and durable documentation.

The architecture must minimize long-term maintenance, avoid vendor lock-in, and keep executable code reproducible from a clean machine.

## Decision

AIHub will use a capability-based, service-oriented architecture:

```text
User
  -> Orchestrator
  -> Capability
  -> Service
  -> Provider
  -> External Service
```

The approved principles are:

- GitHub is the source of truth for executable code.
- Obsidian is the source of truth for documentation, ADRs, architecture, and operational knowledge.
- Prefer official APIs and supported integrations.
- Prefer deterministic local execution whenever practical.
- Use AI only when reasoning adds meaningful value.
- Build capabilities rather than one-off scripts.
- Keep providers interchangeable behind stable capability interfaces.
- Separate orchestration from execution.
- Treat every executable component as a service.
- Propose architectural changes before implementing them.

## Consequences

- New executable components should live under `services/`.
- Capability interfaces should live under `capabilities/`.
- Provider-specific integrations should live under `providers/`.
- Orchestrators should call services or capabilities instead of directly calling vendors.
- Secrets must not be stored in source control or documentation.
- Significant architectural changes require a new ADR.

## Initial Scope

The first scaffolded capability is Email.

The first placeholder provider is Nylas.

No functionality is implemented by this ADR.
