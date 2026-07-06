# fable-advisor

**Spend Fable 5 tokens only where they change the outcome.**

A Claude Code plugin that teaches an Opus orchestrator to consult **Claude Fable 5** —
Anthropic's most capable (and most expensive) model — the way you'd use a top-dollar
consultant: rarely, at the right moment, with a well-prepared brief, for a terse verdict.

Day-to-day work runs on Opus. Fable gets called at **inflection points**: the decisions
that are costly to revert once you start building. Everything else stays at Opus rates.

## Why

Fable 5 is billed at **$10 / $50 per MTok — exactly 2× Opus 4.8** ($5 / $25). Left
undisciplined, an orchestrator either never uses it (leaving quality on the table) or
uses it lazily — full-context dumps, chatty back-and-forth, delegating generation —
which burns money for nothing.

The protocol is adapted from [Anthropic's advisor tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool)
(executor + advisor pattern), rebuilt for local Claude Code orchestration where the
advisor is a subagent and sees **only what you send it** — which is exactly where the
token savings live.

A disciplined consult costs roughly **$0.15–0.50**. A wrong architecture costs hours of
rework, thousands of Opus tokens, and your time.

## What's inside

| Component | What it does |
|---|---|
| **Skill** `fable-advisor` | The decision protocol: when to consult (and when not to), hard budget caps, the briefing-packet format, how to weigh the advice |
| **Agent** `fable-advisor` | A read-only subagent pinned to `model: fable` with a system prompt that enforces terse, committed verdicts (Verdict → Why → Risks → Would change my mind, ≤300 words) |

## Install

```
/plugin marketplace add czlonkowski/fable-advisor
/plugin install fable-advisor@fable-advisor
```

Requirements: Claude Code with Fable 5 available as a subagent model. Designed for
sessions where the base model is Opus (works from any orchestrator model below Fable).

## How it works

**The gate — two questions before every consult:**
1. Is this decision costly to revert, or am I genuinely stuck?
2. Is there a real fork in the road, with evidence to weigh?

If either is "no", the orchestrator decides on its own.

**The four triggers:**
1. **Costly-to-revert decision, before building** — architecture, DB schema, API/webhook
   contracts, n8n workflow topology, technology selection
2. **Stuck escalation** — 2+ genuinely different failed attempts, evidence in hand
3. **Plan review** — a draft implementation plan embedding a costly-to-revert choice
4. **Pre-completion review** — before declaring done on production deploys, migrations,
   client-facing deliverables

**The budget (hard rules):**
- Default **one** consult per task, hard cap **three** Fable interactions
- Every consult announced to the user in one line before it happens
- One spawn + at most one reconcile follow-up per question
- Generation work (code, docs, configs, workflows) never goes to Fable

**The briefing packet:** decision in the first line, options with a stated leaning, hard
constraints, curated evidence, ≤5 file pointers the advisor may read narrowly — and an
explicit answer-format request, because advisor output is the biggest cost driver
(Anthropic measured ~7× output reduction from capping, with no quality loss).

## What a consult looks like

```
Consulting Fable on sync architecture (trigger: costly-to-revert, consult 1/3).

→ Fable verdict: nightly batch delta sync; per-document webhooks add SharePoint
  subscription-renewal failure modes your one-person team can't absorb. Revisit if
  freshness requirements drop below 4 hours.
```

## Prompts to try

In the style of the [Claude Code prompt library](https://code.claude.com/docs/en/prompt-library):

```
plan how to migrate our API from REST to gRPC — this is hard to undo once services depend on it, so get a Fable verdict on the approach before finalizing
```

```
I'm torn between Postgres LISTEN/NOTIFY and a proper queue for job dispatch. decide, and check the decision with Fable before we build around it
```

```
review my deploy plan for Saturday's production migration and fix anything risky before I run it
```

The skill also triggers on its own — without Fable being named — whenever a task hits a
costly-to-revert decision, a stuck debugging loop, or a pre-production review.

## Evals

The repo ships the eval scenarios used to develop the skill (`evals/`): an
architecture-decision task (should consult once), a trivial-change task (should not
consult at all), and a production-migration plan review (should consult before
finalizing). Runs compare with-skill vs. no-skill orchestrators on consult discipline,
briefing compactness, and outcome quality.

## License

MIT
