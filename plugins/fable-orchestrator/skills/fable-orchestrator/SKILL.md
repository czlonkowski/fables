---
name: fable-orchestrator
description: Delegation protocol for sessions running on Claude Fable 5 (or any premium model) — plan big, execute small. Use BEFORE pulling any bulk material into your own context — sweeping a codebase, triaging logs, reviewing a document set, researching across many web pages, verifying N facts against sources, auditing every workflow/config/endpoint, or any task where the reading is mandatory and voluminous. Critical because subagents inherit the session model — on a Fable session an un-pinned Explore or general-purpose spawn bills at Fable rates, so delegation alone saves nothing; this skill makes the rate split real with parallel workers pinned to Sonnet/Haiku that read in their own contexts and report distilled findings (~2.5× cheaper, ~3× faster, 84–98% of input at worker rates in Anthropic's cookbook measurements). Fires on phrasings like "sweep", "audit all", "go through every", "check each", "triage these logs", "research across", "verify against the docs", "keep the cost down", "fan out", "delegate the reading", "plan big execute small". Covers the delegate-or-read gate, the worker brief format, model-tier choice, brief granularity, premise verification, and when NOT to split (narrow reads, judgment that needs frontier eyes on the raw material).
---

# Fable Orchestrator — plan big, execute small

You are an expensive model orchestrating a session: Fable 5 bills **$10/$50 per MTok —
5× Sonnet 5 ($2/$10 introductory) and 10× Haiku 4.5 ($1/$5), as of 2026-07**. Most
substantial tasks hide two very different jobs: a small amount of planning and judgment,
and a large amount of mechanical reading. Your judgment is why the user runs you. The
mechanical reading is a waste of your rate.

The core principle, from Anthropic's coordinator-pattern cookbook: **you supply the
judgment; workers supply the tokens.** You decompose, weigh, and synthesize. Cheap
workers read the codebase, the logs, the documents, the web — each in its own context —
and only distilled findings ever enter yours. On the cookbook's measured runs this split
came out roughly **2.5× cheaper and 3× faster** than one frontier agent doing its own
reading at the same rigor, with **84–98% of input tokens billed at worker rates**.

## The trap this skill exists for

**Subagents inherit the session model.** On a Fable session, `Explore`,
`general-purpose`, and every other spawn runs on Fable unless `model` says otherwise.
Delegation without pinning saves nothing — the same reading bills at the same premium
rate, plus spawn overhead. The rate split only exists when workers run on a cheap model.
That is the one mechanical habit this protocol enforces: **never spawn a reading worker
without a cheap model pinned.**

## The gate: two questions before any bulk read

1. **Is the reading mandatory and voluminous?** Mandatory: the answer can't come from
   your context or knowledge — someone has to read the material. Voluminous: more than
   a handful of files or pages. Each worker spawn has a floor cost; delegating a
   two-file read pays overhead to save pennies. Small mandatory reads you just do.
2. **Can a cheap model extract what you need?** Fact-finding, inventory, pattern
   matching, coverage checks: yes. But when the judgment lives *in* the raw material —
   subtle document analysis, code where the problem is in what's absent, nuance a
   summary would flatten — read it yourself. A cheap reader summarizes away exactly
   what mattered.

Mandatory + voluminous + extractable → delegate. Anything else → handle it yourself.

## The workload shapes

Fan out when the task looks like one of these — each brief covering one independent axis:

1. **Codebase sweep.** "Every place we call X", "all endpoints and their auth",
   "which workflows use this credential". One worker per subsystem or directory tree.
2. **Log triage.** Multi-file or multi-day log analysis. One worker per day, service,
   or host; each reports anomalies with timestamps and line pointers.
3. **Document review.** A corpus of contracts, tickets, transcripts, or docs. One
   worker per document family; extraction criteria stated in the brief.
4. **Web research.** Facts verified against authoritative sources. One worker per
   source family or sub-question; require URLs in the report.
5. **Coverage verification.** N claims × M sources ("check every item against the
   official page"). The shape the cookbook measured — reading is unavoidable, so the
   only question is what rate it bills at and whether it runs in parallel.

## How to delegate

Preferred — the bundled worker (read-only tools, distilled-report contract in its
system prompt, Sonnet by default):

```
Agent(
  subagent_type: "fable-orchestrator:worker",   # use the exact name shown in your available-agents list
  description: "Sweep auth in services/",
  prompt: <the brief — see below>
  # model omitted → worker's own default (sonnet); pass model: "haiku" for mechanical sweeps
)
```

Send **independent briefs in one message** — parallel spawns, parallel contexts. Workers
run in the background; synthesize when the reports are in, not one report at a time.

Fallback — if `fable-orchestrator:worker` isn't in the agent list, spawn `Explore`
(reading inside the repo) or `general-purpose` (web research) with `model: "haiku"` or
`model: "sonnet"` **explicitly set**, and prepend to the brief:

> You are a read-and-report worker for an expensive coordinator. Read only within the
> brief's scope. Report distilled findings with an evidence pointer (path:line, URL,
> or ≤2-line quote) per claim — never raw dumps. State what remains uncertain. Your
> final message is the deliverable.

## The worker brief

```
SUB-QUESTION: <one focused question, first line>

SCOPE: <exactly what to read: paths, globs, directories, URLs, log files>

REPORT: <what to return and its shape — e.g. "table: endpoint → auth mechanism →
        file:line", plus a length cap>

DON'T: <out of scope; known rabbit holes; "skip services/legacy — another worker has it">
```

Always cap the report length and state its shape — worker output is what enters your
premium context, and an unshaped report arrives as a costly essay.

**Model tier per brief:**
- `haiku` — mechanical: grep-shaped sweeps, inventories, "list every X with file:line",
  format and link checks.
- `sonnet` (worker default) — reading judgment: summarizing intent, spotting log
  anomalies, cross-checking claims, weighing source quality.
- Never Fable for workers. And never delegate the *decision* down: workers report
  facts; the weighing, the plan, and the synthesis are yours.

**Granularity: fewer, bigger briefs.** Each worker pays a fixed spawn cost; the
cookbook found that splitting the same work into more, narrower briefs *raised* the
bill. One worker per independent axis — per subsystem, per log day, per source family —
never per file. If two briefs would read the same material, merge them.

## Premise verification

The verification standard only covers what you put in it. If the decomposition rests on
an assumed list — "the ten largest X", "all services that touch Y" — spend one extra
worker verifying the list itself before fanning out on it. In the cookbook's own run,
both arms verified all twenty facts flawlessly against official sources, while the
park list they fanned out over came from model memory and had the wrong #10. If the
premise matters, it gets a worker too.

## When a worker fails

An infrastructure error or a mushy, unusable report → re-assign the **same brief** to a
fresh worker, once. The reflex to "just read it yourself" silently converts the task
back to premium rates — resist it. If the second worker also fails, the brief is the
problem: rewrite it (narrower scope, sharper report spec) rather than escalating the
reading to yourself.

## Trusting the reports

- **Don't re-read what a worker read.** That pays for the same tokens twice — at your
  rate. The report is the deliverable; use it.
- **Spot-check narrowly, not broadly.** When a finding is both load-bearing and
  surprising, verify that one claim via its evidence pointer — one file, one URL —
  not by re-doing the sweep.
- **Conflicts between workers** get one targeted follow-up or one narrow read of the
  disputed evidence, then a decision. You are the tiebreaker; that's the job.

## When NOT to split

- **Narrow reads.** A handful of files or one page: read them. The gate exists so you
  don't pay spawn overhead to avoid pocket change.
- **You already know the answer.** A delegation that reads nothing is a frontier
  round-trip wasted. Watch for fan-outs with no reading in them.
- **Judgment on the raw material.** Subtle analysis, style, what's-missing reviews:
  frontier eyes on the source, no intermediary.
- **Generation and decisions.** Workers are readers. Code, documents, plans, and the
  final synthesis never go down the hierarchy — that's the "plan big" half.
- **User override.** If the user says to read it yourself or to skip delegation,
  that wins over this skill.

## Reporting the split

In your final message, give the user the shape of the run in one line — they are paying
for it and should see the arbitrage:

```
Fan-out: 6 workers (4 haiku, 2 sonnet) read ~90 files; only their reports entered
Fable context. Premise check included (service list verified against docker-compose).
```

## Sibling protocol

This skill points **down**: you are the expensive model, pushing token-heavy legs to
cheap workers. Its sibling `fable-advisor` points **up**: a cheaper orchestrator buying
one-shot Fable judgment at costly-to-revert inflection points. If you are *not* the
premium model in the session and are considering consulting one, that skill — not this
one — has the protocol.
