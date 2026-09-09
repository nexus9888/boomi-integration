# Boomi Integration — Team Fork

Forked from [OfficialBoomi/boomi-integration](https://github.com/OfficialBoomi/boomi-integration) for team use with OpenCode and custom tooling.

## What's Custom

- ✅ Canvas arranger script (`scripts/boomi-canvas-arrange.py`)
- ✅ OpenCode-optimized instruction files (`OPENCODE.md`, `AGENTS.md`)
- ✅ Project template with scaffolding (`template/`)
- ✅ Provider-agnostic — works with any model via OpenCode
- (Add more as you customize)

## Staying Up To Date

The fork intentionally diverges from upstream, so do not use GitHub's discard
workflow or merge upstream directly into `main`. Review each release on a branch:

```bash
git fetch origin upstream
git switch -c sync/upstream-<version> origin/main
git merge --no-ff --no-commit upstream/main
```

Resolve shared-file conflicts in favor of upstream, then reapply only the
fork-owned adaptations documented above. Validate the full tree, push the sync
branch, and merge it through a pull request.

## Roadmap / Future Ideas

### Integration-specific patterns
- Domain references for identity, ERP, CRM, and finance integrations
- Connector-specific field mappings, retries, error handling, and gotchas

### Testing and review
- Automated mapping and edge-case tests
- Execution-result analysis and regression snapshots
- Process XML review for anti-patterns and naming standards

### Reusable components and environments
- Connection, profile, process-skeleton, and map templates
- Team runtime IDs, folder structures, naming standards, and deployment targets
- Private environment documentation and change-management workflows

### Agent capabilities
- Lightweight multi-system integration planning
- CI/CD hooks for push, deploy, test, and review cycles

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
