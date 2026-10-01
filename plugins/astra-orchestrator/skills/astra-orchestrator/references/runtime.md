# Running GPT reading workers

Use Codex native sub-agents with Sol 6.1 and Luna 6 as the normal workers,
and Astra for justified difficult branches. Check the current native tool's
supported model IDs and effort values before spawning. Use `gpt-6-luna` for
Luna 6 and `gpt-6.1-sol` for Sol 6.1. A catalog entry is not proof of a
successful run.

## Codex native delegation

Use the native agent tool with explicit model and effort selection and a fresh
context. For a host exposing `collaboration.spawn_agent`, an example is:

```json
{
  "task_name": "auth_inventory",
  "model": "gpt-6.1-sol",
  "reasoning_effort": "high",
  "fork_turns": "none",
  "message": "<worker.md contents followed by the completed brief>"
}
```

Use the skill's routing table for other model/effort choices. Omit fixed-model
agent roles that pin older models, such as `azure_luna` or `azure_terra`, when
selecting Luna 6 or Sol 6.1. Before any spawn, an unavailable unpinned Luna 6 may
be routed to available Sol 6.1 with a stated reason, as described in the skill;
this is not a retry after a failed call. For a justified
Astra branch, explicitly set `model: "gpt-6-astra"` and the selected effort
(`high` is the starting point); do not rely on parent inheritance. State why
Astra is useful for that branch. A reasoning-gap escalation consumes the brief's
single retry; access/authentication/quota failures do not trigger model fallback.
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
All routing choices are operating defaults to evaluate on the actual task, not
guaranteed cost or quality improvements. Record the actual model and effort from
session metadata when available; a requested model alone does not prove execution.
