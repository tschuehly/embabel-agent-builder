# Embabel Docs Research Route

Use this route when the input is a specific Embabel implementation question or when planning/implementation needs version-matched Embabel docs.

## Output

Return a concise finding that answers the specific question and cites the docs file paths or URLs used. Do not summarize broad docs areas unless the user asks.

## Workflow

1. Identify the narrow implementation concern.
   - Examples: `@Action` return types, `@State` loops, tool groups, RAG stores, `AgentInvocation`, testing support.

2. Open `references/docs-map.md`.
   - Select the smallest relevant docs file list.
   - Prefer one file first; add another only if the first does not answer the question.

3. Fetch version-matched docs.
   - Use `scripts/fetch-docs-section.py <path> --project-dir <target-project>` so the script resolves the target project's Embabel version and fetches the matching docs tag.
   - Use `--ref <embabel-agent-ref>` only when the user explicitly supplies a ref such as `v0.3.4`.
   - If a user-supplied local Embabel checkout is available, read local docs only when it is checked out to the target project's Embabel ref.
   - Do not inspect Maven JARs, source JARs, decompiled classes, or local dependency caches as a substitute for docs research.

4. Extract only the answer needed.
   - Mention API names, annotations, properties, and gotchas.
   - Keep examples short and adapted to the user's project style when relevant.

5. Feed the result back into the active spec or implementation.
   - For planning, update advanced pattern decisions or open questions.
   - For implementation, update the spec progress and code accordingly.

## Common Lookups

- agent/domain/GOAP design: `overview/concepts.adoc`, `agent-design/page.adoc`, `reference/flow/page.adoc`
- annotations/actions/goals/parameters: `reference/annotations/page.adoc`
- LLM calls and typed outputs: `reference/types/page.adoc`, `reference/llms/page.adoc`
- tools and MCP: `reference/tools/page.adoc`, `reference/integrations/page.adoc`
- states, loops, human-in-the-loop: `reference/states/page.adoc`
- chatbots: `reference/chatbots/page.adoc`
- RAG: `reference/rag/page.adoc`
- subagents and DSL: `reference/dsl/page.adoc`, `reference/tools/page.adoc`
- invocation/runtime: `reference/invoking/page.adoc`, `reference/agent-process/page.adoc`
- testing: `reference/testing/page.adoc`

## Research Discipline

Do not use docs research to import large sections into the response. The goal is version-matched implementation guidance, not documentation cloning.

Avoid migration, roadmap, and old-vs-new docs unless the user explicitly asks.
