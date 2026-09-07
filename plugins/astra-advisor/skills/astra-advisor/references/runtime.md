# Running the Astra consult

Route by host: native sub-agents in Codex, Codex CLI in Claude Code. Do not fall
back to nested CLI sessions from Codex. Defaults were checked on 2026-09-07 against
Codex CLI 0.153.4 and its local model catalog: `gpt-6-astra`, reasoning `high`.

## Codex native delegation

Use the native agent tool if it accepts the requested model. Explicitly select
`gpt-6-astra` and `high`, with a fresh context. For a host exposing
`collaboration.spawn_agent`, the arguments are:

```json
{
  "task_name": "astra_consult_1",
  "model": "gpt-6-astra",
  "reasoning_effort": "high",
  "fork_turns": "none",
  "message": "<advisor.md contents followed by the completed brief>"
}
```

`fork_turns: "none"` avoids inheriting the parent transcript and permits an explicit
model override in this interface. Supply the workspace path, relevant project
instructions, and needed facts in the brief. Runtime system context still applies.
Other hosts may expose different fields or configured agent roles; inspect their
schema instead of copying unsupported arguments. Never omit the model and assume
that a named role selects Astra. Await the completed final answer. For a justified
follow-up, use the host's follow-up mechanism on the same agent and send only the
new evidence. Count it as another interaction.

If native delegation is unavailable or disallowed in Codex, report that limitation
and continue the parent task without claiming an Astra consult.

## Claude Code

Use an installed, authenticated Codex CLI. Claude Code's `Agent(model: ...)` does
not select OpenAI models. These plugins intentionally do not define a Claude agent
with a GPT model field.

Inspect `codex exec --help` first; confirm the exact model is available through the
local model picker/catalog. Create `brief.txt` with the advisor prompt followed by
the packet in a task-specific temporary directory. Use the target project as CWD:

```bash
codex exec --model gpt-6-astra \
  -c 'model_reasoning_effort="high"' \
  --sandbox read-only --ephemeral --color never \
  --cd "$task_project" \
  --output-last-message "$task_tmp/verdict.txt" \
  - < "$task_tmp/brief.txt"
```

Set `task_project` and `task_tmp` to absolute paths before invoking. Use a unique
output filename per interaction to avoid stale verdicts. Pass the prompt through
stdin; do not interpolate it into shell command text. Add `--skip-git-repo-check`
only when the target is intentionally outside a Git repository. This command still
loads applicable project instructions and host configuration; it is not a promise
of a prompt-only context. Do not bypass approvals, disable sandboxing, or assume
read-only mode disables mutating MCP tools. If those tools cannot be constrained,
use a host-supported restricted configuration or report the limitation.

Capture exit status and diagnostics separately from the final answer. A successful
consult needs a successful process and a nonempty answer. `--ephemeral` avoids
persisted session files; each CLI follow-up is a new invocation with a short recap,
the previous verdict, and new evidence. Count it within the same three-interaction
budget. On access, quota, or model errors, stop and report the error; no silent model
fallback or automatic paid retry. If a sandbox blocks authentication, distinguish
that from missing login and use the host's normal approval path if authorized.

Sources: [Astra model](https://developers.openai.com/api/docs/models/gpt-6-astra),
[Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents).
Public API reasoning levels and host-specific levels can differ. `high` is the
portable default here; do not assume `ultra` is an API reasoning value.
