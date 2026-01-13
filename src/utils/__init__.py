"""Utility modules for Azure OpenAI proxy."""
from .platform import get_shell_profile, add_env_to_profile, is_env_configured

__all__ = ["get_shell_profile", "add_env_to_profile", "is_env_configured"]
