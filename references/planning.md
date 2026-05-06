# Embabel Agent Planning Route

Use this route when the input is a prompt, product spec, feature spec, ticket, rough idea, or existing domain model.

## Output

Produce or update a high-level Embabel agent spec. Do not implement unless the user also asks for end-to-end build or explicitly asks to continue into implementation.

## Workflow

1. Ingest the input.
   - Extract the intended user outcome, actors, domain terms, constraints, integrations, and non-goals.
   - Preserve product intent, but translate it into Embabel concepts.
   - Mark assumptions explicitly.

2. Inspect local context when available.
   - Find existing domain types, services, repositories, events, agents, tests, docs, and planning files.
   - Prefer existing domain language over invented names.
   - Challenge language that conflicts with existing terms.

3. Define the goal.
   - Name the final user-visible outcome.
   - Choose the goal-achieving output type.
   - Decide whether the outcome is one-shot, long-lived, looped, or delegated.

4. Model blackboard facts.
   - List typed facts the planner should reason about.
   - Avoid generic objects such as `Result`, `Context`, `Data`, or `Response` unless they are real domain terms.
   - Prefer rich domain objects with behavior over anemic DTOs.

5. Design the GOAP flow.
   - Each action consumes typed inputs and returns a typed output.
   - Method parameters become preconditions; return types become postconditions.
   - Normal service calls, LLM calls, and tool-enabled LLM calls can coexist in one flow.

6. Pressure-test advanced patterns.
   - Decide whether stateful loops, chatbot processes, tool exposure, RAG, or subagents are needed.
   - Use the simplest pattern that preserves the domain semantics.

7. Ask one blocking question at a time.
   - Ask only when code inspection and the input cannot answer it.
   - Include a recommended answer and its tradeoff.

## Spec Template

```md
# <Agent Name> Embabel Agent Spec

## Source Input

Summarize the prompt, product spec, feature spec, ticket, or code context that motivated the agent.

## User Outcome

Describe the user-visible result the agent must produce.

## Domain Model

| Term | Meaning | Existing Type | New/Changed Type | Notes |
|---|---|---|---|---|
|  |  |  |  |  |

## Blackboard Facts

| Fact Type | Producer | Consumers | Why It Belongs On The Blackboard |
|---|---|---|---|
|  |  |  |  |

## GOAP Flow

| Step | Action | Inputs | Output | Purpose | LLM? | Tools? | Goal? |
|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |

## Advanced Pattern Decisions

| Pattern | Decision | Reason |
|---|---|---|
| Stateful loops | Use / Avoid / Open |  |
| Chatbot process | Use / Avoid / Open |  |
| Tool exposure | Use / Avoid / Open |  |
| RAG | Use / Avoid / Open |  |
| Subagents | Use / Avoid / Open |  |

## Implementation Plan

| Status | Work Item | Notes |
|---|---|---|
| pending |  |  |

## Tests And Verification

| Status | Check | Notes |
|---|---|---|
| pending |  |  |

## Open Questions

- 

## Assumptions

- 
```

## Flow Challenges

After drafting the GOAP table, challenge it:

- Is each output a meaningful domain fact, or only implementation plumbing?
- Does each action do one thing that can be retried or replaced?
- Would a human domain expert recognize the terms?
- Can the planner infer a path from available starting inputs to the goal?
- What happens if an action returns null or produces a subtype route?
- Which actions are read-only, costly, valuable, or unsafe to rerun?
- Which facts must persist across loops or user turns?

## Advanced Pattern Questions

Stateful loops:

- Does the flow return to an earlier stage?
- Is the loop over the same domain object, a revised object, or a new state?
- What data must survive each iteration?
- Should this be plain GOAP, `@State`, `canRerun`, `clearBlackboard`, or `WaitFor`?

Chatbot processes:

- Is this a one-shot task or an ongoing conversation?
- Does the process pause between messages?
- Are actions triggered by new messages or selected toward a terminal goal?
- Should Utility AI choose among response strategies?

Tool exposure:

- Is the tool safe for an LLM to call?
- Is it read-only, externally mutating, or internally mutating?
- Should it be a domain object method, separate tool object, tool group, MCP tool, or normal service call outside the LLM?
- Which single action needs the tool?

RAG:

- Is retrieval actually needed, or can typed domain objects and services provide the facts?
- What is the corpus and who owns it?
- Should the LLM control search as agentic tools?
- What cited or auditable output does the user expect?

Subagents:

- Is the subtask independently goal-oriented?
- Does it deserve its own domain model, goal, and tests?
- What typed object does the parent pass in?
- What typed result does the subagent return?
- Is this simpler as a normal service call, state transition, DSL subprocess, or tool-style handoff?
