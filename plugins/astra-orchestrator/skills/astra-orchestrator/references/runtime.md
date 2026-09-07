# Running GPT reading workers

Use Codex native sub-agents. Model IDs were checked on 2026-09-07 against the local
Codex model catalog and available native spawn schema. Preserve user model
choices and check current access; a catalog entry is not proof of a successful run.

## Codex native delegation

Use the native agent tool with explicit model and effort selection and a fresh
context. For a host exposing `collaboration.spawn_agent`, an example is:

```json
{
  "task_name": "auth_inventory",
  "model": "gpt-5.6-terra",
  "reasoning_effort": "medium",
  "fork_turns": "none",
  "message": "<worker.md contents followed by the completed brief>"
}
```

Select Luna/low or Sol/high instead when the skill's work table calls for it.
`fork_turns: "none"` avoids transcript inheritance and allows model overrides in
this interface. Include the project path and relevant instructions in the brief.
Runtime system context still applies. Inspect other hosts' actual schemas; do not
invent these fields for a tool that does not support them. Use available read-only
tool restrictions. Collect completed final reports using the host's wait/result
mechanism and keep any follow-up attached to the original worker where supported.

## Unsupported host or unavailable model

If native delegation is absent or disallowed, report the limitation and handle the
parent task locally where feasible. Do not start nested Codex CLI worker processes.
In Claude Code, use `astra-advisor` only when a compact Astra consultation is wanted;
this orchestration skill does not turn a Claude session into an Astra parent.

Stop on authentication, quota, or unavailable-model errors. Do not silently choose
a different model or fall back to inherited Astra workers. Distinguish a failed
spawn from a completed report; report missing coverage honestly.

Sources: [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents),
[OpenAI model catalog](https://developers.openai.com/api/docs/models).
The Luna/Terra/Sol assignments in the skill are operating defaults to evaluate on
the actual task, not benchmark-derived cost or quality promises.
