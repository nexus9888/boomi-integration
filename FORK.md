# Boomi Integration — Team Fork

Forked from [OfficialBoomi/boomi-integration](https://github.com/OfficialBoomi/boomi-integration) for team use with OpenCode and custom tooling.

## What's Custom

- ✅ Canvas arranger script (`scripts/boomi-canvas-arrange.py`)
- ✅ OpenCode-optimized instruction files (`OPENCODE.md`, `AGENTS.md`)
- ✅ Project template with scaffolding (`template/`)
- ✅ Provider-agnostic — works with any model via OpenCode
- (Add more as you customize)

## Staying Up To Date

Pull upstream changes:
```bash
git fetch upstream
git merge upstream/main
```

Or use GitHub's sync:
```bash
gh repo sync nexus9888/boomi-integration -b main
```

## Installation (Team Members)

```bash
git clone https://github.com/nexus9888/boomi-integration.git

# Copy the template to start a new project
cp -r boomi-integration/template/ ~/workspace/my-boomi-project/
cd ~/workspace/my-boomi-project/
cp .env.example .env  # Fill in your credentials

# OpenCode will auto-load OPENCODE.md + AGENTS.md from the project root
opencode run 'Verify Boomi connection — run boomi-env-check.sh and boomi-folder-create.sh --test-connection'
```
