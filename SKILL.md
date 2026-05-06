---
name: embabel-agent-builder
description: Build, design, challenge, implement, and test Embabel agents around domain models, typed GOAP planning, blackboard objects, actions, goals, states, tools, RAG, chatbots, and subagents. Use when creating or modifying Embabel agents, deciding whether a flow should be a simple typed agent, stateful loop, chatbot process, tool-enabled action, RAG workflow, or composed subagent, or when turning an existing domain model into an Embabel agentic flow.
---

# Embabel Agent Builder

Use this skill to design the Embabel agentic flow before coding. Embabel implementation is usually straightforward only after the domain model, blackboard facts, action inputs/outputs, and goal boundaries are coherent.

## Operating Mode

Interview and challenge the design. Ask one unresolved question at a time, give a recommended answer, and continue only after the user accepts, rejects, or refines it.

If a question can be answered by inspecting the codebase, inspect the codebase instead of asking. Look for existing domain types, services, agents, tests, docs, `CONTEXT.md`, `CONTEXT-MAP.md`, and ADRs.

When the user uses vague or overloaded terms, call that out immediately and propose a canonical term. If the project has a glossary or context document, challenge new language against it.

Prefer domain clarity over rapid code generation. Do not implement until the GOAP flow table is coherent enough to explain why each type and action exists.

## Design Workflow

1. Establish the domain context.
   - Identify existing domain objects, services, repositories, events, and user-facing workflows.
   - Separate domain concepts from implementation plumbing.
   - Challenge ambiguous terms and missing ownership boundaries.

2. Define the goal.
   - Name the final user-visible outcome.
   - Decide the goal-achieving output type.
   - Check whether the requested outcome is one-shot, long-lived, looped, or delegated.

3. Model blackboard facts.
   - List the typed objects the planner should reason about.
   - Avoid generic blobs such as `Result`, `Context`, `Data`, or `Response` unless the domain language really uses them.
   - Prefer rich domain objects with behavior over anemic DTOs.

4. Design the GOAP flow.
   - Each action consumes typed inputs and returns a typed output.
   - Method parameters become preconditions; return types become postconditions.
   - Normal service calls, LLM calls, and tool-enabled LLM calls can coexist in the same flow.
   - Use the flow table below as the central design artifact.

5. Pressure-test advanced patterns.
   - Check stateful loops, chatbot processes, tool exposure, RAG, and subagents before coding.
   - Use the simplest pattern that preserves the domain semantics.

6. Fetch current Embabel docs for implementation details.
   - Do not rely on memorized Embabel API details when writing or changing code.
   - Read `references/docs-map.md`, then fetch only the narrowest current docs needed.

7. Implement narrowly.
   - Use the project language, style, package layout, and tests.
   - Prefer annotation-based agents unless the docs and design point to DSL builders or subprocesses.
   - Keep tool exposure action-scoped or prompt-runner-scoped unless current docs justify broader exposure.

8. Verify.
   - Unit-test action methods with fake or mocked LLM interactions.
   - Integration-test the complete agent flow when planning, binding, or agent discovery matters.
   - Run the relevant build/test commands.

## GOAP Flow Table

Produce or update this table before implementation:

```md
| Step | Action | Inputs | Output | Purpose | LLM? | Tools? | Goal? |
|---|---|---|---|---|---|---|---|
| 1 | extractRequest | UserInput | DomainRequest | Parse intent and constraints | yes | no | no |
| 2 | loadFacts | DomainRequest | DomainSnapshot | Gather existing state | no | service | no |
| 3 | decide | DomainRequest, DomainSnapshot | Decision | Choose the domain outcome | yes | optional | no |
| 4 | produceResult | Decision | FinalResult | Return user-visible value | yes/no | optional | yes |
```

After drafting the table, challenge it:

- Is each output a meaningful domain fact, or only an implementation artifact?
- Does each action do one thing that can be retried or replaced?
- Would a human domain expert recognize the terms?
- Can the planner infer a path from available starting inputs to the goal?
- What happens if an action returns null or produces a subtype route?
- Which actions are read-only, costly, valuable, or unsafe to rerun?
- Which facts must persist across loops or user turns?

## Advanced Flow Pressure Tests

### Stateful Loops

Consider states when the workflow revisits a phase, waits for human feedback, performs revision cycles, or has phase-specific available actions.

Ask:

- Does the flow return to an earlier stage?
- Is the loop over the same domain object, a revised object, or a new state?
- What data must survive each iteration?
- Should this be plain GOAP, `@State`, `canRerun`, `clearBlackboard`, or `WaitFor`?

Fetch docs: `reference/states/page.adoc`, `reference/annotations/page.adoc`.

### Chatbot Processes

Consider chatbot process design when the agent is long-lived, receives multiple user messages or events, or keeps a working blackboard across turns.

Ask:

- Is this a one-shot task or an ongoing conversation?
- Does the process pause between messages?
- Are actions triggered by new messages or selected toward a terminal goal?
- Should Utility AI choose among response strategies?
- What session, user, context, or conversation objects belong on the blackboard?

Fetch docs: `reference/chatbots/page.adoc`, `reference/states/page.adoc`, `reference/planners/page.adoc`.

### Tool Exposure

Consider tools when the LLM needs callable capabilities beyond text generation.

Ask:

- Is the tool safe for an LLM to call?
- Is it read-only, externally mutating, or internally mutating?
- Should the tool be a domain object method, separate tool object, tool group, MCP tool, or normal service call outside the LLM?
- Which single action needs the tool?
- What infrastructure context must be hidden from the LLM-facing schema?

Fetch docs: `reference/tools/page.adoc`, `reference/domain/page.adoc`, `reference/integrations/page.adoc`.

### RAG

Consider RAG when answers must be grounded in private, indexed, or discoverable knowledge.

Ask:

- Is retrieval actually needed, or can typed domain objects and services provide the facts?
- What is the corpus and who owns it?
- Should the LLM control search as agentic tools?
- Are vector search, text search, regex search, result expansion, or ingestion needed?
- What cited or auditable output does the user expect?

Fetch docs: `reference/rag/page.adoc`, `reference/types/page.adoc`.

### Subagents

Consider subagents when a step is itself a meaningful goal-oriented workflow.

Ask:

- Is the subtask independently goal-oriented?
- Does it deserve its own domain model, goal, and tests?
- What typed object does the parent pass in?
- What typed result does the subagent return?
- Is this simpler as a normal service call, state transition, DSL subprocess, or tool-style handoff?

Fetch docs: `reference/annotations/page.adoc`, `reference/dsl/page.adoc`, `reference/tools/page.adoc`.

## Implementation Rule

Before implementing an Embabel-specific construct, fetch the relevant current documentation using `references/docs-map.md` or `scripts/fetch-docs-section.py`.

Fetch only the narrowest file needed. Summarize what matters for the implementation, then code against the current project patterns.

Do not copy migration, roadmap, or old-vs-new framing into project documentation. Describe only the supported current workflow and intended state.

## Domain Documentation

When the project uses `CONTEXT.md` or `CONTEXT-MAP.md`, keep domain language aligned with it. If no context file exists, create one lazily only when a domain term has been resolved and the user wants that language captured.

Offer an ADR only when the decision is hard to reverse, surprising without context, and the result of a real trade-off.
