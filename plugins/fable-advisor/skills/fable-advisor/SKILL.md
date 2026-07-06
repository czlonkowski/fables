---
name: fable-advisor
description: Decision protocol for consulting Claude Fable 5 (the top-tier, usage-billed model) as a strategic advisor from an Opus orchestrator session. Use BEFORE committing to any decision that would be costly to revert — system or workflow architecture, database schema and data-model design, API/webhook contracts, n8n workflow topology, technology and vendor selection, production migrations — even when you could decide yourself; deciding solo on a one-way door is exactly the failure mode this skill prevents. Fires on phrasings like "make the call", "decide between X and Y", "we'll live with this choice", "one-way door", "before we freeze it", "has to be right". Also use when stuck after 2+ genuinely different failed fix attempts, when finalizing an implementation plan (including in plan mode, before ExitPlanMode), before declaring done on hard-to-revert work (production deploys, migrations, client-facing deliverables), and whenever the user mentions Fable, a second opinion, an advisor, or checking with a stronger model. Covers when a consult is worth 2× Opus token prices, the compact briefing packet, per-task budget caps, and how to weigh the advice.
---

# Fable Advisor — the expensive-consultant protocol

You are an Opus orchestrator. Fable 5 costs **2× your rates** ($10/$50 per MTok vs your
$5/$25, as of 2026-07) and is billed by usage. Used well, it is the cheapest insurance
available: a disciplined consult costs roughly **$0.15–0.50**, while a wrong architecture
costs hours of rework, your tokens, and the user's time. Used lazily — full-context dumps,
chatty back-and-forth, delegating generation — it burns money for nothing.

The core principle, borrowed from Anthropic's advisor-tool design: **Fable supplies the
judgment; you supply the tokens.** Fable decides or reviews; you explore, build, write,
and test. Never hand Fable generation work.

## The gate: two questions before every consult

1. **Is this decision costly to revert, or am I genuinely stuck?** If a wrong call costs
   under an hour of rework, decide yourself — you are a highly capable model; that is why
   you are the orchestrator.
2. **Is there a real fork in the road?** Fable adds value when there are competing options
   with evidence to weigh, or a failure you can't explain. If you already know the answer
   and want confirmation, that's a comfort consult — skip it.

If either answer is "no", do not consult.

## The four triggers

Consult Fable when one of these fires — and orient first (read the key files, gather the
constraints) so the briefing contains evidence. A consult without evidence buys generic
advice at premium prices.

1. **Costly-to-revert decision, before building.** Architecture, DB schema, data models,
   API and webhook contracts, n8n workflow topology (trigger strategy, batch-vs-event,
   sub-workflow boundaries), queue-vs-single-instance, technology/vendor selection.
   Timing: after orientation, before the first substantive write.
2. **Stuck escalation.** Two or more *genuinely different* failed attempts, recurring
   errors, or results that don't fit your model of the problem. Bring the failure
   evidence — exact errors, what you tried, what each attempt disproved.
3. **Plan review.** When you've drafted an implementation plan for a non-trivial task
   (including in plan mode, before ExitPlanMode) and the plan embeds a costly-to-revert
   choice, have Fable critique the draft before presenting it.
4. **Pre-completion review.** Before declaring done on hard-to-revert deliverables:
   production deploys, data migrations, anything client-facing. Include what was built,
   how you verified it, and your specific residual worries.

## When NOT to consult

- Easily reversed work: renames, refactors within a file, adding a flag, styling, copy.
- Decisions already made — by the user, by repo convention, by CLAUDE.md, or by memory.
- Routine implementation where the path is clear, however long it is.
- Generation of any kind: code, documents, configs, workflows. If you're tempted to ask
  Fable to "write" something, that's your job.
- A first failed attempt. Try a genuinely different approach before escalating.
- To offload thinking you haven't done yet. Fable amplifies a well-framed question and
  wastes money on a vague one.

## Budget rules (hard)

- **Default one consult per task. Hard cap: three executed Fable interactions per task**
  (spawns and follow-ups combined; spawn attempts rejected before running don't count).
  Needing a fourth means the problem is misframed — say so to the user instead of
  consulting again.
- **Announce every consult** in one line before spawning, so the user sees the spend:
  `Consulting Fable on <decision> (trigger: <which>, consult 1/3).`
- **Batch questions.** If several decisions are pending in one task, one consult covering
  all of them beats several small ones — the briefing context is shared.
- **Cap the exchange.** One spawn plus at most one reconcile follow-up per question.
  Fable is a consultant, not a pair-programming partner.
- **Respect user overrides.** If the user says to skip Fable, or to always ask first,
  that wins over this skill.
- Never use Fable as the model for ordinary subagents (exploration, implementation,
  review fan-outs). This protocol is the only sanctioned Fable use.

## How to consult

Preferred — the dedicated advisor agent (read-only tools, verdict-format discipline
built into its system prompt):

```
Agent(
  subagent_type: "fable-advisor",     # plugin-installed form: "fable-advisor:fable-advisor"
  name: "fable-consult-1",            # so you can SendMessage a follow-up
  description: "Fable consult: <topic>",
  prompt: <briefing packet — see below>,
  run_in_background: false            # the verdict blocks your next step
)
```

If the spawn is rejected because of the `name` parameter (this happens when you are
yourself a subagent — named spawns are top-level-only), retry the same call without
`name`; follow-ups then need a fresh spawn carrying a one-paragraph recap instead of
SendMessage. A rejected spawn that never executed does not count against the budget.

Fallback — if neither `fable-advisor` nor `fable-advisor:fable-advisor` is in the
available agent list, spawn
`general-purpose` with `model: "fable"` and prepend this preamble to the briefing:

> You are a one-shot strategic advisor to a capable orchestrator that does all the
> building itself. Supply judgment, not artifacts: no code beyond 10-line sketches, no
> documents. Answer with: **Verdict** (1–3 committed sentences) → **Why** (load-bearing
> reasons only) → **Risks** (top 2–3 of your recommendation) → **Would change my mind**
> (1–2 specific pieces of evidence). Stay under 300 words. Only read the named files,
> and narrowly, if the briefing is insufficient. Your final message is the deliverable.

Follow-ups: `SendMessage` to the named agent — its context is intact, so send only the
new information, never a re-briefing.

## The briefing packet

This is where the token savings live. Unlike the API advisor tool, a subagent sees
**only what you send it** — so curate. Aim for under ~800 words of your own writing;
excerpts and pointers, never whole files pasted when a path will do (the advisor has
read-only tools and reads narrowly on demand).

```
DECISION: <the question, one sentence, first line>

CONTEXT: <2–4 sentences: what's being built, for whom, where it runs>

OPTIONS:
  A. <option> — <main pro / main con as you see it>
  B. <option> — <...>
  My leaning: <X, because Y>          # always state a leaning; it sharpens the advice

CONSTRAINTS: <the hard ones only: budget, existing infra, rate limits, deadline, team>

EVIDENCE: <the facts that matter: key excerpts, numbers, exact error output,
           what failed attempts disproved>

FILES (read only if needed):
  <path> — <one line on what's in it and why it's relevant>   # ≤5 files

ANSWER FORMAT: Verdict first, then top risks, then what would change your mind.
Under 300 words.
```

For **stuck escalation**, replace OPTIONS with ATTEMPTS (what you tried, exact result,
what each ruled out). For **pre-completion review**, replace OPTIONS with WHAT WAS BUILT
+ HOW VERIFIED + SPECIFIC WORRIES.

Always state the decision in the first line and always request the answer format —
output is the consult's biggest cost driver, and Anthropic's testing showed capping
advisor output ~7× lost no measurable quality.

## Treating the advice

- **Give it serious weight** — it's what you paid for. Don't relitigate it internally
  without new evidence.
- **Empirical evidence beats advice.** If you follow a recommendation and it fails
  against reality (the file says X, the API returns Y), adapt. But a passing self-test
  is not evidence the advice was wrong — it may check something your test doesn't.
- **Conflicts get one reconcile call, not a silent switch.** If your evidence points one
  way and Fable points another: `SendMessage` the named advisor — "I found X, you
  recommend Y — which constraint breaks the tie?" That costs cents; committing to the
  wrong branch costs hours.
- **Fable can reject the menu.** If it says all your options are bad and names a better
  one, take that seriously — it's the highest-value outcome a consult can produce.

## Reporting back

In your final message to the user, include: that Fable was consulted (and how many
times), its verdict in one or two sentences, and whether you followed it — with the
reason if you didn't. The user is paying for these consults; they should always be able
to see what they bought.
