"""Cross-platform utilities for Azure OpenAI plugin."""
import sys
import os
import subprocess
from pathlib import Path
from typing import Optional, Tuple


def get_shell_profile() -> Optional[Path]:
    """Get the user's shell profile path.

    Returns the first existing profile in order of preference,
    or ~/.bashrc as default if none exist.
    Returns None on Windows (uses setx instead).
    """
    if sys.platform == "win32":
        return None  # Windows uses setx instead

    home = Path.home()
    # Check in order of preference
    profiles = [
        home / ".zshrc",
        home / ".bashrc",
        home / ".bash_profile",
        home / ".profile",
    ]
    for profile in profiles:
        if profile.exists():
            return profile
    return profiles[1]  # Default to .bashrc


def add_env_to_profile(var_name: str, value: str) -> Tuple[bool, str]:
    """Add environment variable to shell profile or Windows environment.

    Args:
        var_name: The environment variable name (e.g., ANTHROPIC_BASE_URL)
        value: The value to set (e.g., http://localhost:8082)

    Returns:
        Tuple of (success: bool, message: str)
    """
    if sys.platform == "win32":
        # Windows: use setx to set user environment variable
        result = subprocess.run(
            ["setx", var_name, value],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return True, "Added to Windows user environment. Restart terminal to apply."
        return False, f"Failed to set environment variable: {result.stderr}"

    # Linux/Mac: add to shell profile
    profile = get_shell_profile()
    if not profile:
        return False, "Could not find shell profile"

    export_line = f'export {var_name}="{value}"'

    # Check if already configured
    content = profile.read_text() if profile.exists() else ""
    if var_name in content:
        # Check if it's set to the correct value
        if f'{var_name}="{value}"' in content or f"{var_name}={value}" in content:
            return True, f"Already configured in {profile}"
        else:
            return False, f"{var_name} is already set in {profile} with a different value. Please update manually."

    # Append to profile
    with open(profile, "a") as f:
        f.write(f"\n# Azure OpenAI Proxy for Claude Code\n{export_line}\n")

    return True, f"Added to {profile}. Run 'source {profile}' or restart terminal to apply."


def remove_env_from_profile(var_name: str) -> Tuple[bool, str]:
    """Remove environment variable from shell profile.

    Note: On Windows, this doesn't remove the variable (setx doesn't support removal).
    Users need to remove it manually via System Properties.

    Args:
        var_name: The environment variable name to remove

    Returns:
        Tuple of (success: bool, message: str)
    """
    if sys.platform == "win32":
        return False, "To remove on Windows, use System Properties > Environment Variables"

    profile = get_shell_profile()
    if not profile or not profile.exists():
        return True, "No shell profile found"

    content = profile.read_text()
    if var_name not in content:
        return True, f"{var_name} not found in {profile}"

    # Remove the export line and comment
    lines = content.split("\n")
    new_lines = []
    skip_next = False
    for line in lines:
        if "# Azure OpenAI Proxy" in line:
            skip_next = True
            continue
        if skip_next and var_name in line:
            skip_next = False
            continue
        skip_next = False
        new_lines.append(line)

    profile.write_text("\n".join(new_lines))
    return True, f"Removed from {profile}"


def is_env_configured(var_name: str) -> bool:
    """Check if environment variable is set in current session."""
    return var_name in os.environ


def get_env_value(var_name: str) -> Optional[str]:
    """Get the value of an environment variable."""
    return os.environ.get(var_name)
