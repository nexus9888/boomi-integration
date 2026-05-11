# boomi-integration Skill (OpenCode Fork)

> **This is an unofficial community fork** of [OfficialBoomi/boomi-integration](https://github.com/OfficialBoomi/boomi-integration), optimized for use with **OpenCode** and other provider-agnostic coding agents. It is not affiliated with or endorsed by Boomi, LP.
>
> ### What's different from upstream
>
> - **`OPENCODE.md`** added as the primary instruction file — OpenCode loads this automatically alongside `AGENTS.md`
> - **`AGENTS.md`** added — the emerging cross-platform standard, natively loaded by OpenCode, OpenAI Codex, Claude Code, and Gemini CLI
> - **`CLAUDE.md`** kept for backward compatibility with Claude Code users
> - **`GEMINI.md`** — deprecated in favor of `OPENCODE.md`; kept for legacy compatibility
> - **Claude-specific references removed** from `SKILL.md` — path examples, slash command references, and folder names are now agent-agnostic
> - **Standalone canvas arranger** (`scripts/boomi-canvas-arrange.py`) — replaces the Claude Code agent with a portable Python script that works with any agent. Validates step-path integrity (orphans, broken connections, unset dragpoints) and arranges shape layout for clean visual presentation in the Boomi GUI
> - **Canvas arranger wired into SKILL.md** — agents are instructed to run it automatically after building or modifying processes
>
> ### Recommended Agent Runtime: OpenCode
>
> OpenCode is provider-agnostic — it supports Anthropic, Google Gemini, OpenAI, OpenRouter, and custom providers. This means you get Claude Code-quality Boomi development with any model you prefer, without needing separate Gemini CLI scripts.
>
> ```bash
> # Install
> npm i -g opencode-ai@latest
> opencode auth login
>
> # Use
> opencode run 'Build a REST listener to Database process' \
>   --model openrouter/anthropic/claude-sonnet-4-20250514
> ```
>
> ### Staying up to date with upstream
>
> ```bash
> git fetch upstream
> git merge upstream/main
> ```
>
> Upstream changes may occasionally re-introduce Claude-specific wording — check for conflicts in `SKILL.md` and `references/` after merging.

---

The official Boomi Companion skill for building Boomi integration processes programmatically with AI coding agents. The intended audience of this README.md document is humans seeking to understand the skill.

> **Important:** Boomi Companion is a publicly available developer offering, not an officially supported Boomi product. It is provided as-is and is not covered by Boomi support agreements or SLAs. Boomi curates and maintains this tool on a best-effort basis — treat it as a self-service resource. Boomi reserves the right to modify or discontinue it at any time without notice.

This project is licensed under the [BSD-2-Clause License](LICENSE). If you fork or modify this code, you should not use the name "Boomi" for your version.

## Feedback & Issues

Found a bug or have a feature idea? Email solutions@boomi.com with a clear description, steps to reproduce, and any relevant error messages.

## What is this?

This is a distributable skill that provides AI coding agents with knowledge and tooling for working with Boomi Enterprise platform. It enables:

- Programmatic creation and modification of Boomi components (processes, profiles, connections, operations, topics, subscriptions)
- Bi-directional component push/pull with the Boomi platform API
- Reference documentation for Boomi componentry and development patterns
- CLI tools for deployment, testing, and component management

## Prerequisites

- `curl` (universally available)
- `jq` (install via `brew install jq` on macOS or `apt install jq` on Linux)
- Python 3 (only for `boomi-profile-inspect.py` — stdlib only, no pip deps)

## Installation

### OpenCode (Recommended)

1. Install OpenCode: `npm i -g opencode-ai@latest`
2. Authenticate: `opencode auth login`
3. Clone this fork into your skill directory
4. OpenCode will auto-load `OPENCODE.md` and `AGENTS.md` when working in a Boomi project

### Claude Code (via the bc-integration plugin)

Install through the Claude Code plugin system — the skill is included automatically:

1. Add the Boomi marketplace: `/plugin marketplace add OfficialBoomi/boomi-companion`
2. Install the plugin: `/plugin install bc-integration@boomi-companion`

Alternatively, navigate the `/plugin` menu interactively within Claude Code to add the marketplace and install.

### Manual configuration

Clone or copy this skill directory into the location your platform uses for agent skills. Consult your platform's documentation for the correct skill directory path.

### Quick Start with Template

The `template/` directory provides everything you need for a new Boomi project:

```bash
# 1. Copy the template
cp -r boomi-integration/template/ ~/workspace/my-boomi-project/
cd ~/workspace/my-boomi-project/

# 2. Set up credentials
cp .env.example .env
# Edit .env with your Boomi API credentials

# 3. Verify
bash <path-to-skill>/scripts/boomi-env-check.sh
bash <path-to-skill>/scripts/boomi-folder-create.sh --test-connection

# 4. Start building
opencode run 'Build a REST listener to Database process...'
```

The template includes:
- `opencode.json` — model config (default: Claude Sonnet 4 via OpenRouter)
- `OPENCODE.md` — project-level agent instructions
- `AGENTS.md` — universal fallback instructions
- `.env.example` — credentials template
- `.gitignore` — pre-configured for Boomi projects
- `active-development/` — directory structure for components
- `.opencode/` — OpenCode agents/commands (extensible)

## Project Setup

Once the skill is installed it works in an individual project folder as follows:

### 1. Directory Structure

```
your-project/
├── .env                    # Your credentials (created during setup)
└── active-development/     # All working files (auto-created as needed)
    ├── processes/          # Process XML files
    ├── profiles/           # Profile XML files
    ├── connections/        # Connection XML files
    ├── operations/         # Operation XML files
    ├── maps/               # Map XML files
    ├── document-caches/    # Document cache XML files
    ├── scripts/            # Script XML files
    ├── .sync-state/        # Component sync state tracking
    └── feedback/           # Test execution results
```

If using the skill via the bc-integration plugin, there is a series of quality of life setup steps that help template and spin up project workspaces rapidly. See the README.md file for the plugin for more details, or ask your AI agent for help. 

### 2. Environment Variables

A Boomi development project (i.e. the folder in which you are working, not this skill directory itself) will require a `.env` file in your project root with:

```
# Platform API Credentials (required)
BOOMI_API_URL=https://your-platform.boomi.com
BOOMI_USERNAME=your_username
BOOMI_API_TOKEN=your_api_token
BOOMI_ACCOUNT_ID=your_account_id
BOOMI_VERIFY_SSL=true

# Default Folder (if no folder is specified, the agent will put projects here - optional).
BOOMI_TARGET_FOLDER=your_default_folder_guid

# Environment and Runtime Details (lets the agent deploy processes - optional)
BOOMI_ENVIRONMENT_ID=your_environment_id
BOOMI_TEST_ATOM_ID=your_test_atom_id

# Shared Web Server Runtime Credentials (lets the agent test listeners - optional)
SERVER_BASE_URL=https://your-atom.integrate.boomi.com
SERVER_USERNAME=your_runtime_username
SERVER_TOKEN=your_runtime_token
SERVER_VERIFY_SSL=false
```

**Where to find these:**
- API credentials: Boomi platform → Account settings → API Management
- Folder GUIDs: Create folders via GUI or use `boomi-folder-create.sh`
- Environment/Atom IDs: Boomi platform → Environment management

Your AI agent has more info about the necessary pieces of data and can talk you through them one by one - just ask!

## Usage

Once the skill is installed, you can work with your AI coding agent to build Boomi processes:

1. **Start a conversation**: Describe what you want to build
2. **The agent loads the skill**: References comprehensive Boomi documentation
3. **Programmatic development**: The agent creates/modifies XML components
4. **Platform sync**: The agent uses custom CLI tools to push/pull components to/from Boomi
5. **Deploy and test**: The agent can also use its tools to deploy to a runtime and test your processes

### Example Workflow

```
You: "Create a REST API endpoint that fetches weather data and returns JSON"

Agent: [Loads BOOMI_THINKING.md and relevant references]
       [Creates project folder]
       [Creates JSON profiles for request/response]
       [Pushes profile components to platform]
       [Creates REST connection and operation]
       [Pushes connection and operation components to platform]
       [Creates WSS operation for endpoint]
       [Creates process with all steps]
       [Pushes all components to platform]

You: "Deploy and test it"

Agent: [Deploys process to runtime]
       [Runs a curl command to test, or provides you the details to test yourself]
```

## Tools Overview

The skill makes the following CLI tools available to the agent:

- `boomi-env-check.sh` - Checks which .env variables are set without revealing values
- `boomi-folder-create.sh` - Creates project folders
- `boomi-component-create.sh` - Creates new components
- `boomi-component-push.sh` - Updates existing components
- `boomi-component-pull.sh` - Downloads components from platform
- `boomi-deploy.sh` - Packages and deploys processes to runtime
- `boomi-undeploy.sh` - Undeploys processes from runtime
- `boomi-test-execute.sh` - Executes and tests processes via platform API
- `boomi-wss-test.sh` - Tests WSS listener endpoints via the shared web server
- `boomi-profile-inspect.py` - Extracts field metadata from large profiles (Python stdlib)
- `event-streams-setup.sh` - Configures Event Streams

## Documentation Structure

The skill includes the following Boomi-centric reference documentation:

### Core Guides
- `BOOMI_THINKING.md` - Essential mental models (always read first)
- `references/guides/boomi_error_reference.md` - Error patterns, silent failures, and troubleshooting
- `references/guides/boomi_platform_reference.md` - Platform services and boundaries

### Component References
- `components/` - Detailed specs for all component types
  - Profiles (JSON, XML, Flat File)
  - Connections (REST, Salesforce, Event Streams)
  - Operations (Connectors, WSS)
  - Maps, Processes, Scripts

### Step References
- `steps/` - Process step documentation with examples
  - REST Connector, Map, Message, Set Properties
  - Branch, Decision, Try-Catch
  - Process Call, Return Documents
  - Event Streams, Salesforce

## Roadmap / Future Ideas

Ideas for extending this fork. Contributions and private forks welcome.

### Integration-Specific Patterns
- Pre-built reference docs for common integration domains (identity management, ERP, CRM, finance)
- Domain-specific connector templates — field mappings, error handling, retry logic tailored to specific systems
- Gotcha guides — the things that catch you out on specific connectors that aren't in the official docs

### Testing Skill
- Automated test suite for core integrations — validate field mappings, check edge cases, verify error handling
- Execution result analysis — parse process logs and flag anomalies
- Regression testing patterns — snapshot known-good outputs, diff against new runs

### Reusable Component Library
- Pre-built connection configs for common systems (with credential patterns)
- Profile templates for standard data formats used across projects
- Process skeletons — boilerplate for common patterns (poll → transform → push, API gateway, error handler)
- Map templates for frequent transformations

### Environment Knowledge
- Per-team configuration: runtime IDs, folder structures, naming conventions, deployment targets
- Company-specific patterns: security requirements, approval workflows, change management
- Private fork support: `.env.example` tuned for your org, internal documentation references

### Advanced Agent Features
- Boomi code review agent — validate process XML quality, flag anti-patterns, check naming conventions
- Lightweight integration planning — checklist-based pre-build analysis for complex multi-system integrations
- Deployment pipeline integration — CI/CD hooks for automated push, deploy, test cycles

---

## Support and Issues

This skill is designed to be agent-agnostic, with OpenCode as the recommended runtime. Agent Skills are an open standard accessible to multiple models and platforms.

### OpenCode Troubleshooting

| Problem | Fix |
|---------|-----|
| OpenCode can't find skill scripts | Ensure fork is cloned at `~/workspace/boomi-integration/`. Check `opencode --version`. |
| Auth errors on Boomi API | Run `bash <skill-path>/scripts/boomi-env-check.sh` to verify credentials are set. |
| Model not found | Check `opencode auth list` — ensure provider is configured. Use `openrouter/` prefix for OpenRouter models. |
| SSL handshake failures (exit 35) | Check Zscaler or corporate VPN. |
| Canvas arranger drops XML comments | Expected — `xml.etree.ElementTree` strips comments. Boomi doesn't depend on them. |

### Upstream Boomi Skill Resources

- Agent Skills overview: https://agentskills.io/home
- Claude Code skill docs: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- Claude Code intro course: https://anthropic.skilljar.com/claude-code-in-action
- Official feedback: solutions@boomi.com

### OpenCode Resources

- Docs: https://opencode.ai/docs
- GitHub: https://github.com/anomalyco/opencode
- Config reference: https://opencode.ai/config.json
