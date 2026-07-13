# Embabel Agent Builder

`embabel-agent-builder` is an agent skill for designing and implementing Embabel agents through a spec-first workflow. It routes explicit skill invocations to the right phase: planning, version-matched documentation research, implementation from an approved spec, or an end-to-end build.

The skill uses the portable `SKILL.md` Agent Skills format and works with any tool that supports it, including **Claude Code** and **OpenAI Codex**. All routing, guardrails, and phase references live in tool-agnostic Markdown, so no behavior is specific to one assistant.

Use this skill only when the user explicitly invokes `embabel-agent-builder` by name or path.

## Compatibility

| Tool | How it loads | Install |
|---|---|---|
| Claude Code | Reads `SKILL.md` frontmatter (`name`, `description`) | Place the skill directory under `~/.claude/skills/` or a project `.claude/skills/` directory |
| OpenAI Codex | Reads `SKILL.md`; `agents/openai.yaml` supplies optional interface metadata (display name, prompt) | Place the skill directory where your Codex setup discovers skills |
| Other SKILL.md-compatible tools | Read `SKILL.md` frontmatter | Follow that tool's skill-install path |

`SKILL.md` is the single source of behavior for every tool. `agents/openai.yaml` only adds Codex-facing presentation metadata and is ignored by tools that do not use it.

## Installation

1. Clone or download this repository.
2. Install the skill directory in the location used by your agent tool:
   - **Claude Code:** `~/.claude/skills/` for a user-wide installation, or `.claude/skills/` for a project installation.
   - **OpenAI Codex:** place it where your Codex setup discovers skills.
   - **Other SKILL.md-compatible tools:** follow the tool's skill-install instructions.
3. Invoke the skill explicitly by name or path: `embabel-agent-builder`.

## Supported Workflow

The default workflow is spec-first:

1. Produce or update a high-level Embabel agent spec.
2. Use the spec to guide docs research and implementation.
3. Keep implementation progress, verification, assumptions, and open questions in the spec.

Implementation should start from a high-level spec unless the user explicitly asks to bypass planning. Bypassing planning is risky because Embabel's typed GOAP flow depends on coherent domain objects, blackboard facts, action inputs and outputs, structured-output contracts, and goal boundaries.

## Routes

| User input | Route | Reference |
|---|---|---|
| Prompt, product spec, feature spec, ticket, rough idea, or existing domain model | Planning | [references/planning.md](references/planning.md) |
| Specific Embabel API, annotation, tool, state, RAG, chatbot, planner, invocation, or testing question | Docs research | [references/docs-research.md](references/docs-research.md) |
| Approved high-level Embabel agent spec, or request to implement an existing spec | Implementation | [references/implementation.md](references/implementation.md) |
| Request to build the whole agent from idea/spec through code | End-to-end | Planning, docs research as needed, then implementation |
| Ambiguous request | Clarify route | Ask which supported route the user wants |

## High-Level Spec

The high-level spec is the grounding artifact for planning and implementation. It should cover:

- source input and user outcome
- domain model and important terms
- blackboard facts
- GOAP flow
- structured-output contracts for typed LLM outputs
- advanced pattern decisions for stateful loops, chatbots, tool exposure, RAG, and subagents
- implementation plan and progress
- tests and verification
- open questions and assumptions

When a project has an established spec location, use it. Otherwise, create or update a repo-local file such as `docs/agents/<agent-name>-spec.md` when implementation is requested.

## Documentation Research

Use version-matched Embabel docs for implementation details. Select the narrowest relevant docs file from [references/docs-map.md](references/docs-map.md), then fetch it with:

```bash
python3 scripts/fetch-docs-section.py reference/annotations/page.adoc --project-dir .
```

For Maven projects, the fetcher resolves `<embabel-agent.version>` from `pom.xml` and fetches docs from the matching `embabel-agent` tag. Pass `--version` or `--ref` only when the project version cannot be detected or the user explicitly supplies a ref.

Do not inspect Maven JARs, source JARs, decompiled classes, or local dependency caches as a substitute for Embabel docs research. Use local artifacts only after version-matched docs are insufficient and there is a concrete compile or runtime mismatch to investigate.

## Structured Output Requirements

Every LLM action that creates a typed object needs a structured-output contract. Cover:

- target output type
- nullable fields and absent-value representation
- required Kotlin constructor parameters
- `SomeOf` fields
- validation, defaults, retries, or repair strategy
- typed examples for strict, optional nested, or union-style output
- formatter inputs needed to keep final text truthful

Do not mark an implementation complete while structured-output binding or live or fixture acceptance remains unverified unless the spec records a concrete blocker.

## File Layout

```text
.
|-- SKILL.md                     # portable skill definition + routing (all tools)
|-- README.md
|-- agents/
|   `-- openai.yaml              # optional Codex interface metadata
|-- references/
|   |-- docs-map.md
|   |-- docs-research.md
|   |-- implementation.md
|   `-- planning.md
`-- scripts/
    `-- fetch-docs-section.py
```

## Guardrails

- Inspect the target codebase before asking questions that local files can answer.
- Challenge vague or overloaded domain terms.
- Ask one unresolved blocking question at a time and include a recommended answer.
- Prefer existing project structure, names, services, and tests over invented conventions.
- Keep documentation focused on the supported current workflow and intended state.
- Use advanced Embabel patterns only when the spec calls for them.
