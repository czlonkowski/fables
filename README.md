# fables

**Advisor and orchestrator protocols for Claude Fable and GPT-6 Astra.**

Each plugin is a small fable about using a premium model well, sharing a moral —
*judgment belongs on the strongest model, tokens belong on the cheapest one that can do
the leg.* Same economics, opposite directions:

| Plugin | Direction | For sessions running on | One line |
|---|---|---|---|
| [**fable-advisor**](#fable-advisor-consult-up) | consult **up** | Opus (or any model below Fable) | Buy Fable judgment rarely, at costly-to-revert inflection points, with a compact brief |
| [**fable-orchestrator**](#fable-orchestrator-delegate-down) | delegate **down** | Fable 5 (or any premium model) | Plan big, execute small: push bulk reading to cheap parallel workers, keep only distilled findings at Fable rates |
| [**astra-advisor**](#astra-advisor-and-astra-orchestrator) | consult **up** | Codex, or Claude Code with Codex CLI | Buy a compact GPT-6 Astra verdict through the host-appropriate route |
| [**astra-orchestrator**](#astra-advisor-and-astra-orchestrator) | delegate **down** | GPT-6 Astra in Codex | Use native Luna/Terra/Sol readers; keep decisions and synthesis on Astra |

Install the Fable plugins in Claude Code:

```
/plugin marketplace add czlonkowski/fables
/plugin install fable-advisor@fables
/plugin install fable-orchestrator@fables
```

---

## astra-advisor and astra-orchestrator

The Astra pair follows the same consult-up / delegate-down pattern, with explicit
GPT model selection and separate runtime routes:

| Skill | In Codex | In Claude Code |
|---|---|---|
| `astra-advisor` | Native `gpt-6-astra` sub-agent, fresh context, `high` reasoning by default | Authenticated `codex exec --model gpt-6-astra`, read-only shell sandbox, ephemeral session |
| `astra-orchestrator` | Astra parent with native `gpt-5.6-luna`, `gpt-5.6-terra`, or `gpt-5.6-sol` workers | Not supported; CLI consultation belongs to the advisor |

The model IDs were checked against the local Codex catalog and [official OpenAI
model documentation](https://developers.openai.com/api/docs/models/gpt-6-astra) on
2026-09-07. CLI examples were checked against `codex-cli 0.153.4 --help`; account
access must still be available when invoked. A skill does not switch the parent
model, and a Claude Code agent's model field cannot select a GPT model.

### Use in Codex

This checkout includes `.agents/skills/astra-advisor` and
`.agents/skills/astra-orchestrator` as relative symlinks to the packaged skills.
Open Codex in this repository (`fable-advisor/`) and invoke:

```text
Use $astra-advisor to review this architecture decision before we implement it.
Use $astra-orchestrator to inventory all API clients and their retry behavior.
```

Codex supports [repository skills and symlinked skill
folders](https://learn.chatgpt.com/docs/build-skills). For another project, copy the
complete desired skill folder from `plugins/<name>/skills/<name>/` into that
project's `.agents/skills/`. Both packages also contain `.codex-plugin/plugin.json`
for Codex plugin distribution. No user-level installation or settings change is
performed by this repository change.

Native delegation explicitly pins model and reasoning and starts with a compact
brief instead of the parent transcript. If native sub-agents are unavailable,
report that limitation; do not start nested CLI workers from Codex. See the
runtime references linked from each skill for the available-tool contract.

### Use the advisor in Claude Code

The Claude Code marketplace includes `astra-advisor` alongside the Fable plugins.
To load the plugin directly from this checkout:

```bash
claude --plugin-dir ./plugins/astra-advisor
```

Or install it from the marketplace:

```text
/plugin marketplace add czlonkowski/fables
/plugin install astra-advisor@fables
```

Invoke `/astra-advisor:astra-advisor` or explicitly ask to use the Astra advisor.
The skill uses your installed, authenticated Codex CLI, passes the compact brief
through stdin, and reads the final verdict file after successful completion. It
does not define a Claude sub-agent with an unsupported GPT model field.

### Protocols and limits

- **Advisor:** default one consult, maximum three executed interactions per task;
  brief under 1,200 words, up to five file pointers, answer under 300 words. The
  parent implements and verifies. Explicit second-opinion requests are honored;
  routine edits and comfort checks do not trigger extra calls.
- **Orchestrator:** Luna/low for mechanical extraction, Terra/medium for tracing
  and cross-checks, Sol/high for harder bounded reading. Default two or three
  independent workers per wave and at most six interactions including retries.
  Reports carry evidence pointers; the parent checks decisive claims and decides.
- **Host boundaries:** read-only shell sandboxing does not automatically restrict
  every connector. Advisors and workers must not mutate external systems, edit
  project files, or recursively delegate. Respect host permissions and user scope.

These are initial operating defaults. API prices, subscription usage, reasoning,
and retries affect actual cost; no Fable savings or trigger benchmark is claimed
for Astra. The new scenarios in `evals/astra-advisor.json` and
`evals/astra-orchestrator.json` cover consult restraint, exact model selection,
host routing, worker reports, failures, and user overrides. They are evaluation
specifications, not measured GPT behavioral results.

---

## fable-advisor (consult up)

**Spend Fable 5 tokens only where they change the outcome.**

Teaches an Opus orchestrator to consult **Claude Fable 5** the way you'd use a
top-dollar consultant: rarely, at the right moment, with a well-prepared brief, for a
terse verdict. Day-to-day work runs on Opus. Fable gets called at **inflection
points**: the decisions that are costly to revert once you start building.

### Why

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

### What's inside

| Component | What it does |
|---|---|
| **Skill** `fable-advisor` | The decision protocol: when to consult (and when not to), hard budget caps, the briefing-packet format, how to weigh the advice |
| **Agent** `fable-advisor` | A read-only subagent pinned to `model: fable` with a system prompt that enforces terse, committed verdicts (Verdict → Why → Risks → Would change my mind, ≤300 words) |

**Recommended:** add this line to your project or global `CLAUDE.md` — it makes the
skill fire deterministically instead of relying on Claude's own skill-triggering
judgment (see [Making it fire reliably](#making-it-fire-reliably) for why):

```
Before committing to any costly-to-revert decision (architecture, DB schema, API/webhook
contracts, technology selection, production migration plans), before starting any
unattended loop/schedule/routine, or when stuck after 2+ failed fix attempts, consult
the fable-advisor skill first.
```

Requirements: Claude Code with Fable 5 available as a subagent model. Designed for
sessions where the base model is Opus (works from any orchestrator model below Fable).

### Making it fire reliably

We benchmarked the skill's triggering on 20 realistic queries (10 should-fire, 10 tricky
near-miss negatives) across four description variants, ~200 runs on Opus. Result: **zero
false-fires** in every variant — the skill never triggered on trivial changes, decided
architectures, or questions *about* Fable — but recall on bare decision prompts plateaued
around 50–60% regardless of description wording. The cause is structural: Claude Code
consults skills only for tasks it can't handle alone, and Opus believes (correctly, in a
narrow sense) that it can answer a design question itself. That belief is the exact
failure mode this skill exists to counter.

If you want deterministic triggering, use the one-line `CLAUDE.md` setup above. Naming
it also works: prompts that mention Fable, a "second opinion", or "check with a stronger
model" trigger far more reliably (see Prompts to try below).

### How it works

**The gate — two questions before every consult:**
1. Is this decision costly to revert, or am I genuinely stuck?
2. Is there a real fork in the road, with evidence to weigh?

If either is "no", the orchestrator decides on its own.

**The five triggers:**
1. **Costly-to-revert decision, before building** — architecture, DB schema, API/webhook
   contracts, n8n workflow topology, technology selection
2. **Stuck escalation** — 2+ genuinely different failed attempts, evidence in hand
3. **Plan review** — a draft implementation plan embedding a costly-to-revert choice
4. **Pre-completion review** — before declaring done on production deploys, migrations,
   client-facing deliverables
5. **Unattended-automation design** — before starting a loop, schedule, or routine
   (`/loop`, `/schedule`, `/goal`, cron-style agents) that runs without a human
   watching. A loop multiplies its design flaws — a bad stop condition or interval
   fails on *every* iteration — so Fable reviews stop conditions, interval-to-change-rate
   match, per-iteration verification, blast radius, and cost per iteration, once,
   before it runs. (Read-only, easily-cancelled polling doesn't need this.)

**The budget (hard rules):**
- Default **one** consult per task, hard cap **three** Fable interactions
- Every consult announced to the user in one line before it happens
- One spawn + at most one reconcile follow-up per question
- Generation work (code, docs, configs, workflows) never goes to Fable

**The briefing packet:** decision in the first line, options with a stated leaning, hard
constraints, curated evidence, ≤5 file pointers the advisor may read narrowly — and an
explicit answer-format request, because advisor output is the biggest cost driver
(Anthropic measured ~7× output reduction from capping, with no quality loss).

### What a consult looks like

```
Consulting Fable on sync architecture (trigger: costly-to-revert, consult 1/3).

→ Fable verdict: nightly batch delta sync; per-document webhooks add SharePoint
  subscription-renewal failure modes your one-person team can't absorb. Revisit if
  freshness requirements drop below 4 hours.
```

### Prompts to try

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

```
I'm about to turn this on for the weekend: /schedule every 15 min, triage new support tickets and reply automatically. get a Fable review of the loop design first — stop conditions, interval, what could go wrong unattended
```

The skill can also trigger without Fable being named when a task hits a costly-to-revert
decision, a stuck debugging loop, or a pre-production review — but unnamed triggering is
~50–60% reliable in our benchmark. For deterministic behavior, use the one-line
`CLAUDE.md` setup from What's inside.

### Evals

The repo ships the eval scenarios used to develop the skill (`evals/`): an
architecture-decision task (should consult once), a trivial-change task (should not
consult at all), and a production-migration plan review (should consult before
finalizing). Runs compare with-skill vs. no-skill orchestrators on consult discipline,
briefing compactness, and outcome quality.

**Measured results (v0.1, 3 scenarios × with/without skill, Opus orchestrators):**

- Consult discipline was perfect: exactly **1** consult on each costly-to-revert task,
  **0** on the trivial task. Briefings came in at ~511 words — well under budget — and
  every consult was announced to the user with the verdict relayed afterward.
- On the trivial task the skill added **zero overhead** (same duration as baseline,
  ~half the output tokens).
- The consults earned their keep: in the architecture task Fable corrected the polling
  cadence and contributed the failure-mode list; in the migration review it confirmed
  the orchestrator's 8 fixes and **added 3 gaps the orchestrator had missed** (window
  pre-staging, owner-account ordering before credential import, webhook re-registration
  verification).
- Trigger benchmark: ~200 runs across 4 description variants — **zero false-fires**,
  which is why the budget rules can afford to be generous about consulting.

---

## fable-orchestrator (delegate down)

**Plan big, execute small.**

Teaches a session running **on Fable 5** to work like the coordinator in
[Anthropic's plan-big-execute-small cookbook](https://github.com/anthropics/claude-cookbooks/blob/main/managed_agents/CMA_plan_big_execute_small.ipynb):
Fable plans, decomposes, and synthesizes — but never pulls bulk material into its own
context. Cheap parallel workers (Sonnet/Haiku) do the token-heavy reading in their own
context windows and report back distilled findings.

### Why

Most substantial tasks are two jobs in one: a little judgment and a lot of mechanical
reading. On a Fable session both bill at **$10/$50 per MTok** — 5× Sonnet 5, 10× Haiku
4.5 — unless the reading is moved.

And there's a trap that makes naive delegation useless: **subagents inherit the session
model.** On a Fable session, an un-pinned `Explore` or `general-purpose` spawn runs on
Fable too — same reading, same premium rate, plus spawn overhead. The rate split only
exists when workers are explicitly pinned to a cheap model, which is the one mechanical
habit this skill enforces.

The cookbook measured the split honestly against a rigor-matched solo frontier agent:
roughly **2.5× cheaper and 3× faster**, with **84–98% of input tokens billed at worker
rates**. (Their numbers, on web research; we haven't re-measured in Claude Code yet.)

### What's inside

| Component | What it does |
|---|---|
| **Skill** `fable-orchestrator` | The delegation protocol: the delegate-or-read gate, five workload shapes, the worker brief format, model-tier choice, brief granularity, premise verification, and when NOT to split |
| **Agent** `worker` | A read-only reader (`Read, Grep, Glob, WebFetch, WebSearch`) pinned to `model: sonnet` (override to `haiku` per-spawn) whose system prompt enforces the distilled-report contract: findings with evidence pointers, never raw dumps |

**Recommended:** for deterministic firing, add this line to your project or global
`CLAUDE.md` (same reasoning as the advisor's — Claude under-consults skills for work it
believes it can do itself, and "just read everything myself" is exactly such work):

```
When this session runs on Fable 5 or another premium model and a task requires bulk
reading — sweeping code, triaging logs, reviewing documents, researching the web —
consult the fable-orchestrator skill before reading the material yourself.
```

Requirements: Claude Code with Sonnet/Haiku available as subagent models. Designed for
sessions where the base model is Fable 5; the protocol applies from any premium
orchestrator.

### How it works

**The gate — two questions before any bulk read:**
1. Is the reading mandatory and voluminous (more than a handful of files or pages)?
2. Can a cheap model extract what's needed, or does the judgment live in the raw
   material itself?

Mandatory + voluminous + extractable → fan out. Anything else → Fable reads it itself.

**The five workload shapes:** codebase sweep · log triage · document review · web
research · coverage verification (N facts × M sources — the shape the cookbook
measured).

**The worker brief:** `SUB-QUESTION` (one line) / `SCOPE` (exact paths, globs, URLs) /
`REPORT` (shape + length cap — worker output is what enters premium context) / `DON'T`
(out of scope, rabbit holes). Independent briefs go out in one message, in parallel.
Fewer, bigger briefs: each spawn has a floor cost, and the cookbook found
over-splitting *raised* the bill.

**The discipline:**
- `haiku` for mechanical sweeps, `sonnet` for reading judgment, never Fable for workers
- Decisions, plans, and synthesis never delegated down — workers report facts
- One premise-verification worker when the fan-out rests on an assumed list (the
  cookbook's own run verified 20 facts perfectly against a park list that was wrong)
- Failed worker → re-assign the brief once; don't quietly read it yourself at 5× the rate
- Reports are trusted: no re-reading what a worker read, spot-checks only narrow and
  only for load-bearing surprises
- The final message tells the user the shape of the run: how many workers, which
  models, what stayed at Fable rates

### What a fan-out looks like

```
Fan-out: 6 workers (4 haiku, 2 sonnet) read ~90 files; only their reports entered
Fable context. Premise check included (service list verified against docker-compose).
```

### Prompts to try

```
audit all ~80 workflows on the n8n instance for hardcoded credentials and http:// endpoints — keep the token bill sane
```

```
go through last week of logs in /var/log/hermes and figure out why memory climbs every night around 02:00
```

```
research current pricing and rate limits for the top 5 managed vector DB providers, verified against official docs (not blog posts), and recommend one for our scale
```

```
sweep the monorepo and inventory every call to the OpenAI API with file:line, model used, and whether it goes through our retry wrapper
```

### Triggering — read this before relying on it

We ran the same 20-query trigger benchmark that shaped `fable-advisor` (10 realistic
bulk-reading tasks that *should* fire, 10 tricky near-misses that shouldn't), 3 probes
each across 5 description variants. Fable wasn't available as the CLI model at test
time, so this ran on **Opus 4.8 as a proxy** — read the numbers as indicative, not as
true Fable behavior.

- **Zero false-fires (precision 100%) on every variant.** The skill stayed quiet on all
  ten near-misses — single-file reads, "explain the pattern" questions, a
  second-opinion prompt that belongs to `fable-advisor`, and pure generation tasks.
- **Recall was near-zero regardless of wording.** Opus rarely *consulted* the skill on
  genuine bulk-reading tasks, and none of four rewrites moved the needle — the original
  description was kept as best. This is the same structural effect measured for
  `fable-advisor`, and it's stronger here: Claude Code consults a skill only for work
  it can't easily do alone, and "read a pile of files myself" is exactly the work a
  capable model is confident it *can* do. That confidence is the failure mode this
  skill counters — and a stronger model (the real Fable target) tends to under-consult
  *more*, not less.

**So don't rely on unnamed triggering — use the `CLAUDE.md` line above.** It's the
deterministic mechanism; the description's job is mainly to not false-fire, which it
does well. Naming the skill, or flagging cost / "fan out" / "at Fable prices" in the
prompt, also helps.

Full eval scenarios (a coverage-shaped task graded on worker fan-out and rate split, a
narrow task graded on zero overhead) are still planned. The ~2.5×/3×/84–98% figures
above remain the cookbook's, on its web-research workload — not yet re-measured in
Claude Code.

---

## Author

Built by [Romuald Członkowski @aiadvisors](https://aiadvisors.pl/en).

## License

MIT — © 2026 [Romuald Członkowski @aiadvisors](https://aiadvisors.pl/en)
