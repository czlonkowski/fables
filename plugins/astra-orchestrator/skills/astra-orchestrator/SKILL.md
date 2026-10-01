---
name: astra-orchestrator
description: Coordinate substantial fact-finding from an Astra session in Codex using native Sol 6.1 and Luna 6 workers, with Astra for justified difficult branches. Use for codebase sweeps, log triage, document corpora, research, and coverage checks with independent reading branches. Keep small shared-context work with the parent; bound worker context, verification, and retries. Compact second-opinion verdicts belong to astra-advisor.
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

Delegate necessary reading when it forms a substantial independent branch and a
worker can return the needed evidence without losing decisive nuance. Usually
handle a handful of files locally. Answer related questions over a small shared
corpus in one parent context. Several questions do not by themselves justify
several workers. Keep raw material with
the parent when subtle wording, missing behavior, or shared context would be lost
in a summary. Delegate an independent difficult branch to Astra when the criteria
below apply.

Compare the whole path: worker reading, parent coordination and verification,
retries, and repair. If verification would repeat most of a worker's reading,
prefer direct parent work or a suitably capable worker from the start.

This skill explicitly instructs bounded worker delegation when that gate is met
and Codex permits native delegation. Honor the user's instruction to work solo or use a
particular model. Do not spawn agents merely to demonstrate this skill.

## Select the worker deliberately

| Work | Default model | Reasoning |
|---|---|---|
| Mechanical inventory, exact pattern extraction, link or format checks | `gpt-6-luna` | `low` |
| Routine document extraction, log triage, bounded source cross-checks | `gpt-6-luna` | `high` |
| Code tracing across modules, debugging analysis, or extraction requiring substantial interpretation | `gpt-6.1-sol` | `high` |
| Bounded Sol branch where extra reasoning is justified by complexity | `gpt-6.1-sol` | `xhigh`, selectively |
| Difficult independent branch or separately justified evidence review | `gpt-6-astra` | `high`, starting point |

Sol 6.1 and Luna 6 are the normal worker choices. Terra 5.6 and other 5.6
workers are legacy options only for an explicit user request or concrete
task-specific evidence; do not use them as defaults or automatic fallbacks.
This routing supersedes the earlier preference for Terra over Luna within this
skill. Use `gpt-6-luna` for Luna 6 and `gpt-6.1-sol` for Sol 6.1.

Use an Astra worker when a bounded branch needs subtle multi-step reasoning,
omission detection, or independent verification that a cheap summary is unlikely
to preserve, and the parent has useful separate work. Explain why that branch
benefits from Astra and a fresh context. Keep a narrow decisive check local when
the parent already has its context. Final judgment and synthesis stay with the
parent. A compact second-opinion verdict still belongs to `astra-advisor`.

Choose model and effort together based on the branch; do not automatically
move through a Luna → Sol → Astra ladder. These are operating defaults, not
measured quality or cost rankings. Earlier pilots using 5.6 workers do not
establish how Luna 6 and Sol 6.1 compare.

Preserve user overrides and verify current host model and effort availability
before spawning. If Luna 6 is absent and the user has not pinned Luna, state
that limitation and choose available Sol 6.1 for a justified branch, or handle
it locally. If the user pinned an unavailable model, report the blocker rather
than substitute. Set model and effort on every spawn; inherited Astra settings
are not deliberate routing. Change a failed brief's model only as the announced,
justified recovery below.

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
  For a substantive reasoning or evidence gap, that single retry may instead be
  a fresh, explicitly selected Astra worker when the independent-branch criteria
  apply. State the reason and model before launching; do not first retry the old
  worker and then add an escalation. All attempts count toward the same cap.
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
gaps. Example: `Three workers (two Luna, one Astra) covered the API, jobs, and auth
modules; I verified the disputed auth finding and made the final recommendation.`

Do not claim a savings percentage, token count, or bill without measured usage.
Include parent verification and repair in cost comparisons; report any excluded
coordination overhead. Separate API-equivalent costs from subscription allowances
and actual bills. Reasoning, cache hits, and retries affect the result. No Fable
benchmark result transfers to this protocol.

For a lower-tier parent seeking a compact Astra verdict, use the sibling
`astra-advisor` protocol instead.
