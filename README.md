# Azure OpenAI Plugin for Claude Code

**Use Azure OpenAI with Claude Code - No manual proxy setup required!**

A Claude Code plugin that enables seamless integration with Azure OpenAI and other OpenAI-compatible providers. Simply install the plugin, run the setup wizard, and start using Claude Code with your Azure OpenAI deployment.

[![Claude Code](https://img.shields.io/badge/Claude_Code-Plugin-blue)](https://claude.ai/code)
[![Azure OpenAI](https://img.shields.io/badge/Azure-OpenAI-0078D4)](https://azure.microsoft.com/en-us/products/ai-services/openai-service)

## Why Use This Plugin?

- **Enterprise Azure OpenAI** - Use your Azure OpenAI deployments with Claude Code
- **Zero Manual Setup** - No need to manually start proxy servers or configure environment variables
- **Cost Optimization** - Leverage Azure OpenAI credits and enterprise agreements
- **Data Privacy** - Keep your data within your Azure tenant
- **One-Time Configuration** - Setup once, use forever
- **Auto-Start** - Proxy automatically starts when you use Claude Code

## Quick Start

### 1. Install the Plugin

```bash
# Install from GitHub
claude plugin install schwarztim/claudecodeazureplugin

# Or install locally
git clone https://github.com/schwarztim/claudecodeazureplugin.git
claude plugin install ./claudecodeazureplugin
```

### 2. Run the Setup Wizard

```bash
claude
> /azure-openai setup
```

You'll be prompted for:
- **Azure OpenAI API Key**
- **Azure OpenAI Endpoint** (e.g., `https://your-resource.openai.azure.com/`)
- **API Version** (default: `2024-08-01-preview`)
- **Model Deployments**:
  - Big Model (for Claude Opus) - e.g., `gpt-4`
  - Middle Model (for Claude Sonnet) - e.g., `gpt-4`
  - Small Model (for Claude Haiku) - e.g., `gpt-4o-mini`

### 3. Start Using Claude Code

That's it! The plugin handles everything automatically. Use Claude Code normally:

```bash
claude
> What is the capital of France?
```

All requests will be routed through your Azure OpenAI deployment.

## How It Works

The plugin bundles a proxy server that automatically starts when you use Claude Code:

```
┌─────────────────────────────────────────┐
│ You use Claude Code normally            │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│ Plugin Auto-Starts Proxy                │
│ (Converts Claude API ↔ Azure OpenAI)    │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│ Your Azure OpenAI Deployment            │
└─────────────────────────────────────────┘
```

**Behind the scenes:**
1. When Claude Code starts, the plugin's session hook activates
2. The proxy server starts automatically (if enabled)
3. Claude Code is configured to use `http://localhost:8082`
4. All API calls go through the local proxy
5. The proxy converts Claude API format → Azure OpenAI format
6. Responses are converted back and returned to Claude Code

## Plugin Commands

The plugin provides a `/azure-openai` skill with management commands:

### `/azure-openai` or `/azure-openai help`
Show current status and available commands

### `/azure-openai setup`
Interactive setup wizard for Azure OpenAI configuration

### `/azure-openai start`
Manually start the proxy server

### `/azure-openai stop`
Stop the proxy server

### `/azure-openai restart`
Restart the proxy server

### `/azure-openai status`
Check proxy status, configuration, and recent logs

### `/azure-openai test`
Test the connection to Azure OpenAI

### `/azure-openai config`
Display current configuration (with sensitive values masked)

## Configuration

### Plugin Settings

Configure via Claude Code settings (`.claude/settings.json`):

```json
{
  "plugins": {
    "azure-openai": {
      "enabled": true,
      "autoStart": true,
      "apiKey": "your-azure-api-key",
      "baseUrl": "https://your-resource.openai.azure.com/",
      "apiVersion": "2024-08-01-preview",
      "bigModel": "gpt-4",
      "middleModel": "gpt-4",
      "smallModel": "gpt-4o-mini",
      "proxyPort": 8082
    }
  }
}
```

### Environment Variables

Or configure via `.env` file in the plugin directory:

```bash
# Azure OpenAI Configuration
OPENAI_API_KEY=your-azure-api-key
OPENAI_BASE_URL=https://your-resource.openai.azure.com/
AZURE_API_VERSION=2024-08-01-preview

# Model Mapping
BIG_MODEL=gpt-4          # Used for Claude Opus requests
MIDDLE_MODEL=gpt-4       # Used for Claude Sonnet requests
SMALL_MODEL=gpt-4o-mini  # Used for Claude Haiku requests

# Optional Settings
PORT=8082
AZURE_OPENAI_AUTO_START=true
```

### Disable Auto-Start

If you prefer to start the proxy manually:

```json
{
  "plugins": {
    "azure-openai": {
      "autoStart": false
    }
  }
}
```

Then use `/azure-openai start` when needed.

## Supported Features

The plugin supports all major Claude Code features:

- ✅ **Streaming responses** - Real-time output
- ✅ **Function calling / Tool use** - Full tool support
- ✅ **Multimodal inputs** - Images and text
- ✅ **All models** - Maps Claude model names to your deployments
- ✅ **Context windows** - Configurable token limits
- ✅ **Stop sequences** - Full parameter support

## Other OpenAI-Compatible Providers

While designed for Azure OpenAI, this plugin works with any OpenAI-compatible API:

### Official OpenAI

```bash
OPENAI_API_KEY=sk-...
OPENAI_BASE_URL=https://api.openai.com/v1
BIG_MODEL=gpt-4o
SMALL_MODEL=gpt-4o-mini
```

### Local Models (Ollama)

```bash
OPENAI_API_KEY=dummy-key
OPENAI_BASE_URL=http://localhost:11434/v1
BIG_MODEL=llama3.1:70b
SMALL_MODEL=llama3.1:8b
```

### LiteLLM Gateway

```bash
OPENAI_API_KEY=sk-litellm-...
OPENAI_BASE_URL=https://your-litellm-server:4000
BIG_MODEL=azure/gpt-4
SMALL_MODEL=azure/gpt-35-turbo
```

## Troubleshooting

### Check Plugin Status

```bash
claude
> /azure-openai status
```

### View Logs

```bash
# Find plugin directory
claude plugin list

# View logs
tail -f ~/.claude/plugins/claudecodeazureplugin/proxy.log
```

### Test Connection

```bash
claude
> /azure-openai test
```

### Common Issues

#### "Proxy not starting"

1. Verify Python 3.8+ is installed: `python3 --version`
2. Check virtual environment:
   ```bash
   cd ~/.claude/plugins/claudecodeazureplugin
   ls -la venv/
   ```
3. Reinstall dependencies:
   ```bash
   cd ~/.claude/plugins/claudecodeazureplugin
   rm -rf venv
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

#### "Connection refused"

1. Check if proxy is running: `/azure-openai status`
2. Verify port is available: `lsof -i :8082`
3. Restart proxy: `/azure-openai restart`

#### "Unsupported parameter"

Your Azure API version may be outdated. Update in `.env`:
```bash
AZURE_API_VERSION=2024-08-01-preview
```

## Documentation

- **[INSTALL.md](INSTALL.md)** - Detailed installation instructions
- **[PLUGIN.md](PLUGIN.md)** - Complete plugin documentation
- **Manual Setup** - See the [proxy repository](https://github.com/schwarztim/claude-code-azure-proxy) for manual proxy setup

## Requirements

- **Claude Code CLI** - Version 1.0.0 or higher
- **Python 3.8+** - For running the embedded proxy server
- **Azure OpenAI** - Or any OpenAI-compatible API provider

## Uninstallation

```bash
# Stop the proxy
claude
> /azure-openai stop

# Uninstall the plugin
claude plugin uninstall claudecodeazureplugin

# Clean up (optional)
rm -rf ~/.claude/plugins/claudecodeazureplugin
```

## Development

### Plugin Structure

```
claudecodeazureplugin/
├── plugin.json              # Plugin manifest and settings
├── skills/
│   └── azure-openai.md      # /azure-openai skill definition
├── hooks/
│   └── session-start.sh     # Auto-start session hook
├── src/                     # Proxy source code
│   ├── api/                 # API endpoints
│   ├── conversion/          # Format converters
│   ├── core/                # Core functionality
│   └── models/              # Data models
├── start_proxy.py           # Proxy entry point
├── requirements.txt         # Python dependencies
└── .env.example             # Example configuration
```

### Testing Changes

```bash
# Reload plugin
claude plugin reload claudecodeazureplugin

# Test commands
claude
> /azure-openai status
```

### Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Test with Claude Code
4. Submit a pull request

## Security

- **API keys are masked** in command output
- **Proxy binds to localhost only** - Not exposed to network
- **Never commit `.env` files** - Contains sensitive credentials
- **Logs may contain data** - Review before sharing

## Comparison: Plugin vs Manual Setup

### Before (Manual Proxy)

```bash
# Terminal 1: Start proxy
cd claude-code-azure-proxy
source venv/bin/activate
python start_proxy.py

# Terminal 2: Configure and run Claude Code
export ANTHROPIC_BASE_URL=http://localhost:8082
export ANTHROPIC_API_KEY=any-value
claude
```

### After (Plugin)

```bash
# One-time setup
claude plugin install schwarztim/claudecodeazureplugin
claude
> /azure-openai setup

# Then just use Claude Code - that's it!
claude
> Hello!
```

## License

MIT License - See LICENSE file for details

## Related Projects

- **[claude-code-azure-proxy](https://github.com/schwarztim/claude-code-azure-proxy)** - Original proxy implementation with manual setup
- **[claude-code-proxy](https://github.com/fuergaosi233/claude-code-proxy)** - Original proxy inspiration

## Support

For issues, questions, or contributions:

- **Issues**: [GitHub Issues](https://github.com/schwarztim/claudecodeazureplugin/issues)
- **Discussions**: [GitHub Discussions](https://github.com/schwarztim/claudecodeazureplugin/discussions)

## Links

- **Claude Code**: https://claude.ai/code
- **Azure OpenAI Service**: https://azure.microsoft.com/products/ai-services/openai-service
- **Plugin Repository**: https://github.com/schwarztim/claudecodeazureplugin
- **Proxy Repository**: https://github.com/schwarztim/claude-code-azure-proxy
