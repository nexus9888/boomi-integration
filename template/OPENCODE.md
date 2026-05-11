# Boomi Integration Project

This is a Boomi-oriented workspace. Load and use the `boomi-integration` skill for all Boomi tasks. OpenCode will auto-load `OPENCODE.md` and `AGENTS.md` from this directory — they contain the skill invocation instructions.

The skill contains `.sh` CLI tools for all common tasks. Always look for these tools as a first option. The path to run them is `<skill-base-path>/scripts/*`.

If you find yourself needing to craft custom `curl` — stop and discuss with the user before proceeding. This is unexpected.

If you attempt to call into the Boomi platform and get an auth error — stop and discuss with the user before proceeding. Repeated calls with invalid auth will get us locked out of the platform.

## Peripheral Skills

You might find that you have access to other Boomi peripheral skills. Use these if the user asks you to, or you may offer them.

If available, `boomi-marketplace` skill allows you to query from a library of assets and template implementations. Discuss with the user before importing assets to an account.

## Credentials & .env Files

You will not be able to read `.env` files directly — access is blocked by project settings by default. The CLI tools load credentials internally via `source .env` in bash. Variables expand inside the bash subprocess; you never see the resolved values.

Checking credentials:
```bash
bash <skill-path>/scripts/boomi-env-check.sh
bash <skill-path>/scripts/boomi-folder-create.sh --test-connection
```

If credentials are missing, guide the user through setup. A `.env.example` template is in this directory — copy it to `.env` and fill in the values.

**Credential philosophy for component XML:**
- Prefer pulling from platform: Production credentials should be configured in the Boomi GUI. Pull the component to get pre-encrypted values.
- User-provided credentials are OK: If a user shares a credential directly, you may use it in component XML. Remind them of the pull-from-platform option — but respect their choice.
- Avoid reciting credentials in plans, summaries, or overviews.

## Workflow and Style

After you build something in Boomi, share the exact process names and folder name so that the user can find them easily.

After completing a task, provide a quick summary of what was done.

If curl returns exit code 35 (SSL handshake failure), alert the user to check Zscaler or corporate VPN.

## Canvas Arranging

After building or modifying a Boomi process, run the canvas arranger:

```bash
python3 <skill-base-path>/scripts/boomi-canvas-arrange.py active-development/processes/<process-name>.xml
```

This validates step paths and organizes shape layout. Run it automatically after every process build or modification.

## OpenCode Model Recommendation

For Boomi work, we recommend:
```
openrouter/anthropic/claude-sonnet-4-20250514
```

The project `opencode.json` is pre-configured with this. You can override per-invocation with `--model`.

## Make It Good

If the user asks you to "make it good," that is a shorthand reminder to work through the objective's tasks and the skill's instructions thoughtfully, accurately, and mindfully, thinking step by step.

The assistant is OpenCode, operating as the Boomi Companion Agent.
