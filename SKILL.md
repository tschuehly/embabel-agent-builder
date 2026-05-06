---
name: embabel-agent-builder
description: "Use only when the user explicitly invokes the embabel-agent-builder skill by name or path. When invoked, route the request to the right Embabel agent-building phase: planning from a prompt/product/feature spec, current-docs research for implementation questions, implementation from an approved high-level spec, or an end-to-end spec-first build."
---

# Embabel Agent Builder

Use this skill only when the user explicitly invokes `embabel-agent-builder` by name or path. Do not use it automatically for general Embabel work.

This skill routes a prompt, product spec, feature spec, docs question, existing high-level agent spec, or implementation request to the right Embabel workflow. The default route is spec-first: produce or update a high-level Embabel agent spec, then use that spec to ground implementation and progress.

## Route Selection

Choose one route from the user's input:

| Input | Route | Load |
|---|---|---|
| Prompt, product spec, feature spec, ticket, rough idea, or existing domain model | Planning | `references/planning.md` |
| Specific Embabel API, annotation, tool, state, RAG, chatbot, planner, invocation, or testing question | Docs research | `references/docs-research.md` |
| Approved high-level Embabel agent spec, or request to implement an existing spec | Implementation | `references/implementation.md` |
| Request to build the whole agent from idea/spec through code | End-to-end | Planning, then Docs research as needed, then Implementation |
| Ambiguous request | Clarify route | Ask whether the user wants planning only, docs research only, implementation from a spec, or end-to-end build |

Do not start implementation without a high-level Embabel agent spec unless the user explicitly says to bypass planning. If the user bypasses planning, state that this is risky because Embabel's typed GOAP flow depends on domain and blackboard design.

## Shared Rules

Inspect the codebase before asking questions that local files can answer. Look for existing domain types, services, agents, tests, docs, `CONTEXT.md`, `CONTEXT-MAP.md`, and ADRs.

Challenge vague or overloaded terms. Propose canonical domain language when needed.

Ask one unresolved blocking question at a time, give a recommended answer, and continue only after the user accepts, rejects, or refines it.

When implementation touches Embabel-specific APIs, fetch version-matched docs using `references/docs-map.md` and `scripts/fetch-docs-section.py`. Run the fetcher from the target project or pass `--project-dir` so it resolves the repository's Embabel version. Fetch only the narrowest docs needed.

Do not inspect Maven JARs, source JARs, decompiled classes, or local dependency caches as a substitute for Embabel docs research. Use them only after the version-matched docs are insufficient and there is a concrete compile/runtime mismatch to investigate.

Do not copy migration, roadmap, or old-vs-new framing into project documentation. Describe only the supported current workflow and intended state.

## High-Level Spec Contract

Planning and implementation routes revolve around a high-level Embabel agent spec. Keep it as the grounding artifact and progress tracker.

The spec must cover:

- source input and user outcome
- domain model and important terms
- blackboard facts
- GOAP flow
- advanced pattern decisions for stateful loops, chatbots, tool exposure, RAG, and subagents
- implementation plan and progress
- tests and verification
- open questions and assumptions

If the project has a spec location, use it. Otherwise, keep the spec in the conversation during planning; when implementing, create or update a repo-local spec file such as `docs/agents/<agent-name>-spec.md` unless the project has a better established location.

## Phase References

Load exactly the reference needed for the selected route:

- Planning: `references/planning.md`
- Docs research: `references/docs-research.md`
- Implementation: `references/implementation.md`
- Version-matched Embabel docs map: `references/docs-map.md`
