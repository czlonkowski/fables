# Consult Fable from Codex through Claude CLI

Use this route when the parent runs in Codex. In Claude Code, use the native agent
route in `SKILL.md`. A Codex native sub-agent cannot select a Claude model; invoking
`claude -p` starts a separate Claude process, whose final answer is the consult.

## Prepare and invoke

Check `claude --version` and `claude --help`. The command below was smoke-tested on
2026-09-07 with Claude Code 2.1.263 and the existing subscription login. Fable 5.1
requires 2.1.255 or newer. Use `claude-fable-5-1` for an explicit version; `fable`
is a configurable alias and can change. Honor a user-requested version or provider
model ID. Do not configure a fallback model for a Fable-only consultation.

Create a task-specific temporary directory and put the completed briefing in
`brief.txt`. Prepend the one-shot advisor preamble from `SKILL.md`: verdict, reasons,
risks, what would change the decision, under 300 words, no implementation or further
delegation. Include relevant project instructions and decisive source excerpts.
The default has no tools, so file paths are citations, not readable evidence.

Set `task_tmp` to that directory's absolute path. Run from it using the shell
tool's working-directory parameter, with unique output paths per interaction:

```bash
claude -p --model claude-fable-5-1 --effort xhigh \
  --safe-mode --tools '' \
  --output-format json --no-session-persistence \
  --max-turns 1 --max-budget-usd 1.00 \
  < "$task_tmp/brief.txt" \
  > "$task_tmp/result.json" 2> "$task_tmp/stderr.log"
```

One process is one interaction within the skill's three-interaction task cap.
The example allows one tools-disabled turn and a $1 CLI budget per invocation;
use a lower remaining budget when the user sets a stricter task limit. Set a
bounded wall-clock timeout with the host's process controls, normally five minutes,
and stop the process if it exceeds that limit. Do not silently increase limits or
automatically retry a budget, model-access, or authentication failure.

Pass the brief on stdin; do not interpolate its contents into shell code. Do not
pipe directly to a result extractor: first record the Claude exit status, then
parse the saved response. This preserves the failure status and diagnostics.

## Context, login, and tools

`--safe-mode` disables custom skills, plugins, project instructions, auto memory,
MCP servers, and ordinary hooks while retaining normal authentication. Managed
policy settings can still apply; it is not an OS sandbox. `--tools ''` removes
built-in tools, including shell, edits, reads, and delegation. The parent therefore
supplies all evidence and enforces the read-only advisory scope.

Do not substitute `--bare` when using an existing subscription login: bare mode
does not read OAuth credentials or the keychain. It requires API/provider
credentials. Do not disable permissions or bypass managed policy to make the call
work. If `--safe-mode` is unavailable, update the CLI or report the version gap
rather than silently loading the project's hooks and connectors.

If file access is genuinely needed, prefer gathering the missing excerpt in Codex
and sending it in the one permitted reconciliation follow-up. Keep the default
tools-disabled route; do not expand the child toolset just because a path is listed.

If sandboxed execution reports missing login, check whether access to the existing
Claude authentication is blocked by the sandbox before asking the user to log in.
Use the host's normal escalation flow when authorized. Never read or print token
files to diagnose login.

## Validate the result

A successful process alone is insufficient. Require a valid JSON result with
`type: "result"`, `subtype: "success"`, `is_error: false`, and a nonempty string
`result`. A budget/turn-limit response, permission failure, malformed response, or
partial output is not a completed advisory verdict.

Inspect `modelUsage` and any routing diagnostics. The requested Fable model must
appear. Claude can report ancillary Haiku usage even for a Fable response; do not
mistake that alone for a fallback. If another advisory model or a fallback is
reported, disclose it and do not label that verdict Fable-only. If attribution is
unclear, report the uncertainty instead of inferring the model from the command.
Provider-triggered fallback can occur even without `--fallback-model`; never retry
to evade provider routing or safeguards.

Return the `result` verdict to the parent. Retain `modelUsage`, `num_turns`, and
`total_cost_usd` for the task's accounting when available. The CLI cost is an
estimate, not a verified subscription charge. Do not paste the entire JSON payload
into the parent conversation when the verdict and a short usage summary suffice.

The live advisory smoke test used `--effort xhigh` with a synthetic document-sync
brief. It returned a 172-word verdict, `is_error: false`, one turn, and
`claude-fable-5-1` usage. Its reported total cost was $0.062922 including ancillary
Haiku usage. This verifies CLI invocation and result handling, not a quality benchmark.

## Reconciliation

`--no-session-persistence` means the session cannot be resumed. Do not use
`--continue`, `--resume`, or a Claude `SendMessage` call from Codex. If justified,
make one fresh invocation with the advisor preamble, a short recap, the previous
verdict, and only the new evidence or conflict. It counts within the same cap.

## Documentation checked

- [Programmatic use](https://code.claude.com/docs/en/headless): print mode, stdin,
  output handling, authentication differences, and runtime context.
- [CLI reference](https://code.claude.com/docs/en/cli-reference): command options,
  safe mode, tools, persistence, and invocation limits.
- [Model configuration](https://code.claude.com/docs/en/model-config): Fable
  selection, version requirements, alias resolution, and automatic fallback.
