---
name: fable-advisor
description: Consult Claude Fable for a compact strategic second opinion from Codex or Claude Code. Use before costly-to-revert architecture, schema, API, migration, or unattended-automation decisions; after two distinct failed fix attempts; for consequential plan or completion review; or when the user explicitly asks for Fable advice. Codex invokes claude -p with an explicit Fable model; Claude Code uses its native advisor agent. Covers compact evidence packets, three-interaction budgets, and weighing the verdict. Skip routine reversible edits and questions merely about Fable.
---

# Fable Advisor — the expensive-consultant protocol

You are a Codex or Claude Code orchestrator consulting Claude Fable. Keep the
consult small: Fable supplies a verdict; the parent gathers evidence, builds, and
verifies. Do not assume the parent is Opus or that a fixed price ratio applies to
its model or subscription. The Codex CLI route pins `claude-fable-5-1`; the native
Claude agent uses the host's `fable` alias. Use `xhigh` effort for consultations
on both routes; preserve an explicit user model or effort choice.

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

If either answer is "no", skip an automatic consult. Honor an explicit request for
a Fable second opinion even if the parent already runs on a premium model.

## The five triggers

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
5. **Unattended-automation design.** Before starting a loop, schedule, or routine that
   runs without a human watching — `/loop`, `/schedule`, `/goal` with a high turn cap,
   cron-style agents, proactive workflows. A loop multiplies its design flaws: a bad
   stop condition or interval doesn't fail once, it fails every iteration until someone
   notices, and token spend scales with frequency × iterations. One review before it
   starts is the cheapest point of intervention. Have Fable check: stop conditions
   (deterministic and reachable?), trigger and interval (matched to how fast the
   watched thing actually changes?), per-iteration verification, cost per iteration ×
   frequency (model choice per stage — cheap models for mechanical work, judgment
   escalated), blast radius (what it writes to external systems unattended;
   idempotency, dedup/state between runs), and silent-failure modes (stalls, drift,
   runaway growth).

## When NOT to consult

- Easily reversed work: renames, refactors within a file, adding a flag, styling, copy.
- Decisions already made — by the user, by repo convention, by AGENTS.md / CLAUDE.md, or by memory.
- Routine implementation where the path is clear, however long it is.
- Generation of any kind: code, documents, configs, workflows. If you're tempted to ask
  Fable to "write" something, that's your job.
- A first failed attempt. Try a genuinely different approach before escalating.
- A low-stakes, easily-cancelled loop: read-only polling ("check deploy status every
  5 min") needs no review — cancelling a loop is free. Consult only when the routine
  acts on external systems unattended, or cost per iteration × frequency is material.
- To offload thinking you haven't done yet. Fable amplifies a well-framed question and
  wastes money on a vague one.

## Budget rules (hard)

- **Default one consult per task. Hard cap: three executed Fable interactions per task**
  (native spawns, CLI invocations, and follow-ups combined; attempts rejected before
  model execution do not count).
  Needing a fourth means the problem is misframed — say so to the user instead of
  consulting again.
- **Announce every consult** in one line before invoking, so the user sees the spend:
  `Consulting Fable on <decision> (trigger: <which>, consult 1/3).`
- **Batch questions.** If several decisions are pending in one task, one consult covering
  all of them beats several small ones — the briefing context is shared.
- **Cap the exchange.** One spawn plus at most one reconcile follow-up per question.
  Fable is a consultant, not a pair-programming partner.
- **Respect user overrides.** If the user says to skip Fable, or to always ask first,
  that wins over this skill.
- Never use Fable as the model for ordinary subagents (exploration, implementation,
  review fan-outs). This advisory protocol does not restrict separately authorized Fable work.

## How to consult

Route by the parent host:

- **Codex:** use `claude -p`, not a Codex native sub-agent with a Claude model name.
  Read [the Codex CLI route](references/codex-cli.md) for the exact command, tool
  isolation, result checks, and fresh-invocation follow-ups. No Claude plugin install
  is required: the skill folder contains everything needed to construct the brief.
- **Claude Code:** use the native agent below. The `fable` alias is host-configurable;
  record the actual model when available and honor explicit version requests.

### Claude Code native agent

Preferred — the dedicated advisor agent (read-only tools, verdict-format discipline
built into its system prompt, `effort: xhigh` in its definition):

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
`general-purpose` with `model: "fable"` and an explicit host-supported `xhigh`
effort setting. If the spawn schema cannot set effort, use a custom read-only
agent definition with `effort: xhigh`; do not assume the parent effort or a prompt
request changes the runtime setting. Prepend this preamble to the briefing:

> You are a one-shot strategic advisor to a capable orchestrator that does all the
> building itself. Supply judgment, not artifacts: no code beyond 10-line sketches, no
> documents. Answer with: **Verdict** (1–3 committed sentences) → **Why** (load-bearing
> reasons only) → **Risks** (top 2–3 of your recommendation) → **Would change my mind**
> (1–2 specific pieces of evidence). Stay under 300 words. Only read the named files,
> and narrowly, if the briefing is insufficient. Your final message is the deliverable.

Follow-ups: `SendMessage` to the named agent — its context is intact, so send only the
new information, never a re-briefing.

## The briefing packet

Curate the briefing rather than forwarding the parent transcript. Aim for 800 words,
with a 1,200-word ceiling including excerpts. Native advisors can read named files
narrowly. The default Codex CLI route has no tools: include decisive excerpts and
label paths as evidence citations, not requests to open files. Runtime system
context may still be added; a fresh process is not a zero-overhead prompt.

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

FILES (native: read narrowly if needed; tools-disabled CLI: citations only):
  <path> — <one line on what's in it and why it's relevant>   # ≤5 files

ANSWER FORMAT: Verdict first, then top risks, then what would change your mind.
Under 300 words.
```

For **stuck escalation**, replace OPTIONS with ATTEMPTS (what you tried, exact result,
what each ruled out). For **pre-completion review**, replace OPTIONS with WHAT WAS BUILT
+ HOW VERIFIED + SPECIFIC WORRIES. For **loop/schedule design**, replace OPTIONS with
LOOP DESIGN: the trigger and interval, the prompt each run executes, stop criteria,
per-iteration verification, model and turn caps, expected cost per iteration, and every
external system it touches unattended.

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
  way and Fable points another, send the named native advisor one focused follow-up,
  or make one fresh CLI invocation with the prior verdict and new evidence. Ask which
  constraint breaks the tie. Count either route within the same interaction cap.
- **Fable can reject the menu.** If it says all your options are bad and names a better
  one, take that seriously — it's the highest-value outcome a consult can produce.

## Reporting back

In your final message to the user, include: that Fable was consulted (and how many
times), its verdict in one or two sentences, and whether you followed it — with the
reason if you didn't. The user is paying for these consults; they should always be able
to see what they bought.
