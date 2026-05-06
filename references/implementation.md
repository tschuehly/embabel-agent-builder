# Embabel Agent Implementation Route

Use this route when the input is an approved high-level Embabel agent spec or the user asks to implement after planning.

## Preconditions

Implementation should start from a high-level Embabel agent spec. If no spec exists, route to `planning.md` first unless the user explicitly says to bypass planning.

If the user bypasses planning, state the risk: Embabel's typed GOAP flow depends on coherent domain objects, blackboard facts, action inputs/outputs, and goal boundaries.

## Workflow

1. Locate or create the spec.
   - Use the project's existing spec/planning location when available.
   - Otherwise create or update `docs/agents/<agent-name>-spec.md` if implementation is requested.
   - Keep progress statuses current.

2. Inspect the project.
   - Identify language, build tool, package layout, Spring Boot setup, existing agents, tests, fixtures, and conventions.
   - Do not invent a new structure when the project already has one.

3. Fetch version-matched Embabel docs as needed.
   - Use `references/docs-map.md` and `scripts/fetch-docs-section.py`.
   - For implementation in a Maven project, run the fetcher from the target project or pass `--project-dir` so it uses `<embabel-agent.version>` and fetches docs from the matching `embabel-agent` tag.
   - Fetch only the narrow docs needed for the construct being implemented.
   - Do not inspect Maven JARs, source JARs, decompiled classes, or local dependency caches as a substitute for docs research. Use local artifacts only after version-matched docs are insufficient and a concrete compile/runtime mismatch remains.

4. Implement from the spec.
   - Add or modify domain objects first when they are the core blackboard facts.
   - Add actions with typed parameters and return types matching the GOAP flow.
   - Mark the goal-achieving action deliberately.
   - Use normal services for deterministic work; use LLM calls only where the spec requires reasoning, generation, extraction, or classification.
   - Implement structured-output contracts for typed LLM calls: nullable fields must have explicit absent semantics, strict Kotlin constructor fields must be prompt-compatible or defaulted, and `SomeOf` outputs must bind only intended non-null facts.
   - Use `creating(...).withExample(...)` or equivalent typed examples for outputs with optional nested objects, union-style `SomeOf` results, or strict non-null fields.
   - Keep tool exposure action-scoped or prompt-runner-scoped unless current docs justify broader exposure.
   - Use states, chatbot processes, RAG, or subagents only when the spec's advanced pattern decisions call for them.

5. Test.
   - Unit-test action methods with fake or mocked LLM interactions.
   - Integration-test the full flow when planning, binding, agent discovery, or invocation matters.
   - Verify prompts, model options, tool groups, and output types where relevant.
   - Test structured-output binding for optional nested objects, required constructor fields, `SomeOf` binding, validation/default behavior, and malformed-but-plausible LLM shapes such as `{}` for absent nested context.
   - Test formatter truthfulness: final text must only mention facts supplied to the formatter action.

6. Update the spec.
   - Mark work items and verification checks as done or blocked.
   - Record open follow-ups as current intended work, not history.

7. Run verification.
   - Execute the project's relevant tests/build commands.
   - Run a structured-output acceptance pass: inspect retries, validation repairs, blackboard omissions, and final formatter claims in a fixture-based or live supported invocation.
   - If verification cannot run, state why and what remains unverified.

## Implementation Guardrails

Prefer annotation-based agents unless the current docs and spec point to DSL builders, subprocesses, or tool-style handoff.

Do not collapse multiple meaningful domain facts into one generic object just to simplify code.

Do not expose mutating domain behavior as an LLM tool without an explicit safety decision in the spec.

Do not rely on prompt text alone to satisfy sharp Kotlin schema constraints. Prefer explicit nullable semantics, constructor defaults, bean validation, deterministic normalization, or typed examples when the model must produce nested structured output.

Do not mark LLM-heavy implementation complete if the only tests inject already-valid objects. At least one verification path must exercise conversion, binding, and final formatter claims, or the spec must record the blocker.

Do not let project documentation describe prior failed approaches, migration history, or old-vs-new framing. Keep docs focused on the supported current workflow and intended state.
