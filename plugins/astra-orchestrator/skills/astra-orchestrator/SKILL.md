---
name: astra-orchestrator
description: Coordinate substantial fact-finding from a GPT-6 Astra session in Codex using native GPT-5.6 Luna, Terra, or Sol workers. Use for codebase sweeps, multi-file log triage, document corpora, research, and coverage checks where independent readers can return concise evidence. Keeps judgment and synthesis on Astra while bounding worker context and retries. Skip small reads, pure generation, and second-opinion requests that belong to astra-advisor.
---

# Astra Orchestrator

Keep planning, decisions, and synthesis with the parent. Move substantial,
extractable reading into smaller worker contexts. This protocol is designed for a
`gpt-6-astra` parent in Codex, using native sub-agents only; invoking a skill does
not change the parent model. In Claude Code, this orchestration mode is unavailable;
the `astra-advisor` sibling provides the Codex CLI consultation route. If running
on another model, disclose that when relevant and delegate only when the same
tradeoff makes sense. Do not label a run Astra-led unless it is.

## Gate the split

Delegate when the reading is necessary, larger than a handful of files or pages,
and a worker can extract the needed facts without losing decisive nuance. Handle
small reads locally. Keep raw material with the parent when the judgment depends
on subtle wording, missing behavior, or context a summary would erase.

This skill explicitly instructs bounded worker delegation when that gate is met
and Codex permits native delegation. Honor the user's instruction to work solo or use a
particular model. Do not spawn agents merely to demonstrate this skill.

## Select the worker deliberately

| Work | Default model | Reasoning |
|---|---|---|
| Mechanical inventory, exact pattern extraction, link or format checks | `gpt-5.6-luna` | `low` |
| Code tracing, log triage, source cross-checks, document extraction | `gpt-5.6-terra` | `medium` |
| Difficult bounded reading that needs more reasoning | `gpt-5.6-sol` | `high` |

These are starting choices, not measured task-quality guarantees. Preserve user
overrides and verify availability in the active host. Do not silently substitute
another model on failure. Set the model and effort on every spawn: unconfigured
subagents can inherit Astra and its reasoning effort, defeating the intended split.
Do not use Astra for a routine reading worker. If the work requires Astra judgment,
the parent handles it or uses a separately justified independent review.

## Decompose once

Perform a small orientation read to establish scope. Divide by independent
subsystem, source family, or question, not by individual file. Merge overlapping
briefs. If the task assumes a list such as "all services using X", verify the list
from an authoritative inventory before distributing it; this may be a first worker
task. Do not fan out over an unverified model-memory list.

Default to two or three independent workers in a wave, limited by host capacity
and actual useful work. One worker is enough for one substantial extraction. State
the planned number and models. Keep useful parent work moving while they run.

```text
SUB-QUESTION: <one focused question>
SCOPE: <absolute project path, directories/globs/URLs and exclusions>
REPORT: <specific table or findings; default at most 500 words>
EVIDENCE: <path:line or direct source URL for every decisive claim>
DON'T: <out-of-scope areas; no writes, external mutations, or child agents>
```

Include applicable project constraints and enough context to work independently.
Read [the worker prompt](references/worker.md) and prepend it to each brief. Follow
[the runtime instructions](references/runtime.md) to launch fresh, explicitly
model-selected contexts. Do not fork the whole parent conversation into workers.

## Bound retries and trust evidence

- Default to at most six executed worker interactions per task, including premise
  checks, retries, and follow-ups. Plan within that cap and any stricter user limits;
  a larger workload needs a stated revised budget, not an open-ended fan-out.
- For an incomplete report, send one focused follow-up or retry that brief once.
  Stop after a repeated failure, report the gap, and resolve a narrow decisive part
  locally if useful. Access or quota errors are blockers to that route, not grounds
  for repeated calls or silent model escalation.
- Use the compact reports; do not repeat the entire sweep. Verify surprising,
  decisive claims at their evidence pointers. A report without usable pointers is
  insufficient for a consequential conclusion.
- Resolve conflicting reports with one targeted evidence check or follow-up, within
  the budget. Distinguish verified facts, inferences, and unexamined areas.
- Reading workers do not generate deliverables, edit code, make final decisions,
  publish, or spawn more workers. Permissions come from the user and host, not this
  protocol. Read-only shell settings alone do not constrain all external tools.

## Finish the parent task

Weigh the findings, implement or write the authorized deliverable, and verify it.
Report how many workers completed, their actual models, the scope covered, and any
gaps. Example: `Three workers (one Luna, two Terra) covered the API, jobs, and auth
modules; I verified the disputed auth finding and made the final recommendation.`

Do not claim a savings percentage, token count, or bill without measured usage.
Separate API per-token prices from subscription allowances; retries and reasoning
can offset nominal savings. No Fable benchmark result transfers to this protocol.

For a lower-tier parent seeking a compact Astra verdict, use the sibling
`astra-advisor` protocol instead.
