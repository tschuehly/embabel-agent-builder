# Embabel Docs Map

Use this map to fetch current Embabel documentation on demand. Fetch only the files needed for the current design or implementation task.

Source tree:
https://github.com/embabel/embabel-agent/tree/main/embabel-agent-docs/src/main/asciidoc

Raw file pattern:

```text
https://raw.githubusercontent.com/embabel/embabel-agent/main/embabel-agent-docs/src/main/asciidoc/<path>
```

If a local Embabel checkout is available, prefer the user's supplied checkout path for faster reads.

## Core Domain and GOAP Design

Read when designing the typed flow, blackboard facts, actions, and goals:

- `overview/concepts.adoc`
- `agent-design/page.adoc`
- `reference/domain/page.adoc`
- `reference/flow/page.adoc`
- `reference/annotations/page.adoc`

## Project Setup and Configuration

Read when adding Embabel to a project, choosing starters, configuring providers, or running the shell:

- `getting-started/quickstart/page.adoc`
- `getting-started/installing/page.adoc`
- `getting-started/running/page.adoc`
- `reference/configuration/page.adoc`
- `shell/how-to.adoc`
- `shell/commands.adoc`

## LLM Calls and Prompting

Read when implementing `OperationContext`, `Ai`, `PromptRunner`, model roles, prompt templates, or structured object creation:

- `reference/types/page.adoc`
- `reference/llms/page.adoc`
- `reference/templates/page.adoc`
- `reference/prompt-contributors/page.adoc`
- `reference/thinking/page.adoc`
- `reference/streaming/page.adoc`

## Tools, MCP, and Tool Exposure

Read when exposing domain behavior or external capabilities to the LLM:

- `reference/tools/page.adoc`
- `reference/domain/page.adoc`
- `reference/integrations/page.adoc`
- `reference/guardrails/page.adoc`
- `reference/interceptors/page.adoc`

## Stateful Loops and Human-in-the-Loop

Read when the flow revisits stages, waits for feedback, uses state classes, or loops:

- `reference/states/page.adoc`
- `reference/termination/page.adoc`
- `reference/annotations/page.adoc`

## Chatbot Processes

Read when building long-lived conversational agents or message-triggered processes:

- `reference/chatbots/page.adoc`
- `reference/states/page.adoc`
- `reference/planners/page.adoc`
- `reference/agent-process/page.adoc`

## RAG

Read when grounding responses in indexed or searchable knowledge:

- `reference/rag/page.adoc`
- `reference/types/page.adoc`
- `reference/tools/page.adoc`

## Subagents, DSL, and Composition

Read when an action delegates to another agentic workflow, uses a subprocess, or should be built with DSL builders:

- `reference/dsl/page.adoc`
- `reference/annotations/page.adoc`
- `reference/invoking/page.adoc`
- `reference/tools/page.adoc`

## Invocation and Runtime

Read when invoking agents from code, web applications, shell, or an agent platform:

- `reference/invoking/page.adoc`
- `reference/agent-platform/page.adoc`
- `reference/agent-process/page.adoc`
- `reference/flow/page.adoc`

## Testing and Evaluation

Read before adding or changing tests:

- `reference/testing/page.adoc`
- `eval/eval-guide.adoc`

## Provider-Specific or Advanced Integration

Read only when the current task needs these providers or extension points:

- `reference/bedrock/page.adoc`
- `reference/minimax/page.adoc`
- `reference/customizing/page.adoc`
- `reference/asynch-mode/page.adoc`
- `reference/api-spi/page.adoc`

## Usually Avoid for Skill Work

Do not load these unless the user explicitly asks. They are less useful for building the current supported workflow:

- `reference/migrating/page.adoc`
- `reference/api-evolution/page.adoc`
- `roadmap/roadmap.adoc`
- `appendix/page.adoc`
