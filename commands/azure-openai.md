---
name: azure-openai
description: Manage Azure OpenAI proxy - setup, start, stop, status, test, config
allowed-tools: Bash, Read, Write, Edit
---

# Azure OpenAI Proxy Management

You are helping the user manage the Azure OpenAI proxy for Claude Code.

The user ran: `/azure-openai $ARGUMENTS`

## Parse Arguments

Based on `$ARGUMENTS`, determine the action:
- Empty or "help": Show status and available commands
- "setup": Run configuration wizard
- "start": Start the proxy server
- "stop": Stop the proxy server
- "restart": Restart the proxy
- "status": Show proxy status
- "test": Test Azure OpenAI connection
- "config": Show current configuration

## Configuration Location

**Global config (preferred):** `~/.claude/azure-openai/.env`
- Persists across plugin updates and reinstalls

**Plugin directory (fallback):** `$HOME/.claude/plugins/azure-openai/.env`
- Used for development or if global config doesn't exist

```bash
GLOBAL_CONFIG_DIR="$HOME/.claude/azure-openai"
GLOBAL_ENV="$GLOBAL_CONFIG_DIR/.env"
PLUGIN_DIR="$HOME/.claude/plugins/azure-openai"
```

## Actions

### help (default)
Show:
- Current proxy status (running/stopped)
- Available commands
- Quick start guide if not configured

### setup
1. Create global config directory: `mkdir -p ~/.claude/azure-openai`
2. Check for existing config in `~/.claude/azure-openai/.env`
3. If migrating from plugin-local `.env`, offer to migrate
4. If starting fresh, use template from plugin's `.env.example`
5. Guide user to set:
   - `OPENAI_API_KEY` - Azure OpenAI API key
   - `OPENAI_BASE_URL` - Azure endpoint (e.g., https://your-resource.openai.azure.com/)
   - `OPENAI_API_VERSION` - API version (default: 2024-08-01-preview)
   - `BIG_MODEL` - Model for Claude Opus (e.g., gpt-4)
   - `MIDDLE_MODEL` - Model for Claude Sonnet (e.g., gpt-4)
   - `SMALL_MODEL` - Model for Claude Haiku (e.g., gpt-35-turbo)
6. Write config to `~/.claude/azure-openai/.env`
7. **Auto-configure ANTHROPIC_BASE_URL** (cross-platform):
   - Linux/Mac: Add to shell profile (~/.zshrc or ~/.bashrc)
   - Windows: Use `setx ANTHROPIC_BASE_URL http://localhost:8082`
   - Inform user to restart terminal after setup
8. Offer to start proxy after setup

### start
1. Check if already running (`.proxy.pid` file in plugin dir)
2. Verify config exists (`~/.claude/azure-openai/.env` or plugin dir fallback)
3. If no config, prompt user to run `/azure-openai setup`
4. Create venv if needed: `python3 -m venv venv`
5. Install deps: `./venv/bin/pip install -r requirements.txt`
6. Start proxy: `./venv/bin/python start_proxy.py &`
7. Save PID to `.proxy.pid`
8. Show success with `ANTHROPIC_BASE_URL=http://localhost:8082` export

### stop
1. Read PID from `.proxy.pid`
2. Kill the process
3. Remove `.proxy.pid`
4. Confirm stopped

### restart
1. Run stop
2. Run start

### status
1. Check `.proxy.pid` exists and process is running
2. Show proxy status, port, configuration status
3. Check if `ANTHROPIC_BASE_URL` is set correctly

### test
1. Ensure proxy is running
2. Make test request to `http://localhost:8082/health` or test endpoint
3. Report results

### config
1. Check for config in `~/.claude/azure-openai/.env` first, then plugin dir
2. Read config file and show which location is being used
3. Display settings (mask API keys)
4. Show which are configured vs defaults

## Response Format

Always be concise and actionable. Show clear status indicators (✓/✗) and next steps.
