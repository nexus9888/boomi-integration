# boomi-integration Skill

> **Note:** `OPENCODE.md` is the primary instruction file for this fork with OpenCode-specific guidance. This file (`AGENTS.md`) is the universal fallback loaded by all agent platforms.

## What This Is

The boomi-integration skill — a framework for AI coding agents to build Boomi integration processes programmatically. See `README.md` for full details.

## Development Notes

- The `SKILL.md` is the agent-facing entry point. The `README.md` is for humans.
- `references/` contains curated Boomi platform documentation — treat it as authoritative.
- `scripts/` contains CLI scripts the agent uses to interact with the Boomi platform API.
- Boomi platform API calls from scripts must go through the `boomi_api` helper in `scripts/boomi-common.sh` (non-platform HTTP — e.g. WSS endpoint testing — is exempt). It wraps `boomi_curl`, which injects `-A "$BOOMI_USER_AGENT"` (`boomi-companion/<version>`, from `../VERSION`), applies the SSL-verify flag, sets the timeout, and handles basic auth. `boomi_api` also captures the response into the globals `RESPONSE_CODE` and `RESPONSE_BODY` so callers don't need to roll their own output parsing. If `boomi_api` is missing something you need for a platform call, extend the helper rather than bypassing it.
- Keep changes minimal and focused. This skill is consumed by multiple platforms.

## Credential handling

Credentials must not reach the command line, a child-process environment, or a
shell trace. Preserve these upstream guardrails:

- Authentication reaches `curl` through a config file on stdin (`-K -`), so
  stdin is reserved in `boomi_curl` and `boomi_api`; never use `@-`, `-T -`, or
  pipe request data into them.
- `load_env` must not export `.env` values and must source `./.env`, not a bare
  `.env` that could resolve through `$PATH`.
- Expand variables by name only through `var_is_set`, which owns the xtrace
  fence.
- Keep whole-file xtrace protection in scripts that handle credentials outside
  the common helper: `event-streams-setup.sh`, `boomi-wss-test.sh`,
  `boomi-extensions.sh`, and `boomi-shared-server-info.sh`.
- Fence `RESPONSE_BODY` both when captured and whenever a caller expands it;
  error and diff responses may contain credential values.
- Every script must retain its own `set +x` guard because child shells can read
  `BASH_ENV` even when xtrace was disabled by a parent.

## Skill VERSION files

Boomi's release pipelines own `VERSION`. Agents must not modify it manually.
