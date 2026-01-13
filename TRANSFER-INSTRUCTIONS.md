# Transfer Instructions

This directory contains the complete Claude Code plugin for Azure OpenAI that should be transferred to the `claudecodeazureplugin` repository.

## How to Transfer These Files

### Method 1: Clone and Copy (Recommended)

```bash
# 1. Clone both repositories
git clone https://github.com/schwarztim/claude-code-azure-proxy.git
git clone https://github.com/schwarztim/claudecodeazureplugin.git

# 2. Checkout the export branch
cd claude-code-azure-proxy
git checkout plugin-export-for-claudecodeazureplugin

# 3. Copy files to the plugin repo
cp -r export-to-claudecodeazureplugin/* ../claudecodeazureplugin/
cp export-to-claudecodeazureplugin/.env.example ../claudecodeazureplugin/
cp export-to-claudecodeazureplugin/.gitignore ../claudecodeazureplugin/

# 4. Commit and push
cd ../claudecodeazureplugin
git add -A
git commit -m "Initial Claude Code plugin for Azure OpenAI integration

This plugin enables seamless Azure OpenAI integration with Claude Code,
eliminating the need for manual proxy setup and configuration.

Features:
- Auto-starting proxy server via session hook
- Interactive setup wizard via /azure-openai command
- Comprehensive management commands (start, stop, status, test)
- Support for Azure OpenAI and OpenAI-compatible providers

Components:
- Plugin manifest and settings schema
- Skill definitions and session hooks
- Complete proxy server implementation
- Comprehensive documentation

Makes Azure OpenAI + Claude Code as simple as:
1. claude plugin install
2. /azure-openai setup
3. Use Claude Code normally"

git push origin main
```

### Method 2: Download from GitHub UI

1. Go to https://github.com/schwarztim/claude-code-azure-proxy
2. Switch to branch `plugin-export-for-claudecodeazureplugin`
3. Download the `export-to-claudecodeazureplugin` directory
4. Clone `claudecodeazureplugin` repository
5. Copy all files from the download into the repository
6. Commit and push

### Method 3: Use GitHub's Web UI

1. Go to the `plugin-export-for-claudecodeazureplugin` branch
2. For each file in `export-to-claudecodeazureplugin/`:
   - Copy the file content
   - Go to `claudecodeazureplugin` repository
   - Create/edit the file via GitHub UI
   - Paste the content
   - Commit

## Files to Transfer

All files in this directory should be copied to the root of the `claudecodeazureplugin` repository:

```
.env.example
.gitignore
INSTALL.md
PLUGIN.md
README.md
plugin.json
requirements.txt
start_proxy.py
hooks/
  └── session-start.sh
skills/
  └── azure-openai.md
src/
  ├── __init__.py
  ├── main.py
  ├── api/
  │   └── endpoints.py
  ├── conversion/
  │   ├── request_converter.py
  │   └── response_converter.py
  ├── core/
  │   ├── client.py
  │   ├── config.py
  │   ├── constants.py
  │   ├── logging.py
  │   └── model_manager.py
  └── models/
      ├── claude.py
      └── openai.py
```

## Verification

After transferring, verify the plugin structure:

```bash
cd claudecodeazureplugin

# Should see all files
ls -la

# Validate plugin.json
python3 -m json.tool plugin.json > /dev/null && echo "✓ Valid plugin.json"

# Check required directories
ls -d skills hooks src && echo "✓ Required directories present"
```

## Next Steps After Transfer

1. **Test locally**:
   ```bash
   claude plugin install ./claudecodeazureplugin
   claude
   > /azure-openai status
   ```

2. **Tag a release**:
   ```bash
   git tag -a v1.0.0 -m "Initial release"
   git push origin v1.0.0
   ```

3. **Update GitHub repository**:
   - Add description: "Claude Code plugin for Azure OpenAI integration"
   - Add topics: `claude-code`, `azure-openai`, `openai`, `plugin`, `proxy`
   - Enable Discussions for user support

4. **Share with users**:
   ```bash
   claude plugin install schwarztim/claudecodeazureplugin
   ```

## Support

If you encounter issues during transfer:
- Check that all hidden files (.env.example, .gitignore) are copied
- Verify file permissions (hooks/session-start.sh should be executable)
- Ensure directory structure matches exactly

## What This Plugin Does

This plugin makes Azure OpenAI integration with Claude Code seamless:

**Before:**
- Manually start proxy server
- Configure environment variables
- Repeat every session

**After:**
- One-time setup: `/azure-openai setup`
- Proxy auto-starts with Claude Code
- Zero ongoing maintenance

Users can now use Azure OpenAI with Claude Code as easily as:
```bash
claude plugin install schwarztim/claudecodeazureplugin
claude
> /azure-openai setup
> [Enter credentials]
> [Use Claude Code normally]
```
