---
name: astra-advisor
description: Consult GPT-6 Astra for a compact second opinion on costly-to-revert decisions, architecture forks, stuck debugging after two distinct failed attempts, production plans, or consequential unattended automation. Use when the user asks for Astra advice or when a lower-tier orchestrator needs an evidence-backed strategic verdict. Covers briefing, explicit model selection, bounded consults, and weighing the answer; skip routine reversible edits and requests merely asking about Astra.
---

# Astra Advisor

Buy a small amount of GPT-6 Astra judgment at a decision point. The parent agent
gathers evidence, implements, and verifies; the advisor returns a verdict. Default
advisor: `gpt-6-astra`, reasoning `high`. Honor an explicit user model or effort
choice; do not silently substitute a different model if Astra is unavailable.

## Decide whether to consult

Consult when both conditions hold:

1. A wrong decision would cause substantial rework or consequences, or two genuinely
   different fix attempts have failed.
2. There is a real choice, unresolved failure, or concrete residual concern that an
   independent review could resolve.

Useful moments: before committing to architecture, schema or API contracts; before
finalizing a production migration; before declaring consequential work complete;
before starting unattended automation that changes external state or accumulates
material cost. For automation, include interval, state/deduplication, verification,
stop conditions, action limits, and expected per-run cost.

Gather enough evidence to frame the question before consulting. Skip mechanical
changes, settled choices, a first failed attempt, and easily cancelled read-only
polling. An explicit request for an Astra second opinion overrides this relevance
gate. If the parent already runs on Astra, decide locally by default; an explicitly
requested independent review can still justify a separate Astra context.

## Bound the exchange

- Default to one consult per task, maximum three executed advisor interactions,
  counting follow-ups. Use at most one reconciliation follow-up per question.
- Announce the topic, model, trigger, and count before each interaction:
  `Consulting GPT-6 Astra on <decision> (trigger: <reason>, interaction 1/3).`
- Aim for an 800-word brief; stay below 1,200 words including excerpts. Provide at
  most five precise file pointers. Request an answer under 300 words.
- Batch related questions. Follow up only for new evidence or a specific conflict;
  do not retry until the advisor agrees. Stop at the cap and explain unresolved gaps.
- These are interaction and prompt limits, not guaranteed billing caps: reasoning,
  tool calls, and runtime-provided context also consume resources. Respect any user
  spend or time limit; do not invent dollar savings from word counts.

## Prepare the brief

```text
DECISION: <one focused question>
CONTEXT: <what is being built and for whom>
OPTIONS: <A/B with real tradeoffs; include your leaning and why>
CONSTRAINTS: <hard requirements, existing infrastructure, team, deadline>
EVIDENCE: <observed facts, exact errors, relevant excerpts>
FILES: <up to five paths, line ranges, and why they matter>
ANSWER: Verdict / Why / Risks / Would change my mind; under 300 words.
```

For debugging, replace OPTIONS with ATTEMPTS and what each result ruled out. For
completion review, use WHAT CHANGED, HOW VERIFIED, and SPECIFIC WORRIES. Do not send
the full conversation, whole files, or secrets when a focused excerpt suffices.

## Dispatch

This skill instructs a bounded advisor delegation when the gate above is met and
the host permits delegation. Read [the advisor prompt](references/advisor.md),
prepend it to the brief, and use [the runtime instructions](references/runtime.md).
Use a fresh context with the model explicitly pinned; a skill name alone does not
select a model. The advisor may read only the named evidence and must not edit,
publish, call mutating connectors, or delegate further. A read-only shell sandbox
does not itself constrain every connector, so use tool restrictions when available.

Respect the user's instruction to skip delegation or require approval. If the host
cannot run the chosen model within the allowed permissions, report the limitation
and continue the parent task where possible without claiming an advisor review.

## Use the answer

Treat the verdict as advice. Check decisive claims against the evidence, resolve a
material contradiction with one narrow follow-up or source read, and make the final
call yourself. Explain any reasoned disagreement. A review does not authorize a
deployment, publication, or other action outside the user's scope.

Tell the user the model consulted, the verdict, and what changed because of it.
Never present an attempted or failed invocation as a completed review.

The sibling `astra-orchestrator` handles the reverse direction: an Astra parent
delegates substantial fact-finding to explicitly selected lower-cost GPT workers.
