"""Claude Code Proxy

A proxy server that enables Claude Code to work with OpenAI-compatible API providers.
"""

from dotenv import load_dotenv
from pathlib import Path


def get_config_path():
    """Get global config path, with fallback to plugin directory.

    Checks in order:
    1. Global config: ~/.claude/azure-openai/.env
    2. Plugin directory: .env in the plugin root (for development)

    Returns the first path that exists, or the global path if neither exists.
    """
    # Global config location (cross-platform)
    global_config_dir = Path.home() / ".claude" / "azure-openai"
    global_config_file = global_config_dir / ".env"

    # Plugin directory fallback (for development)
    plugin_env = Path(__file__).parent.parent / ".env"

    if global_config_file.exists():
        return global_config_file
    elif plugin_env.exists():
        return plugin_env

    # Return global path even if doesn't exist (will be created by setup)
    return global_config_file


# Load environment variables from config file
load_dotenv(get_config_path())

__version__ = "1.0.0"
__author__ = "Claude Code Proxy"
