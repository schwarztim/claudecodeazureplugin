#!/usr/bin/env python3
"""Cross-platform session start hook for Azure OpenAI proxy.

This hook runs when a Claude Code session starts and:
1. Checks if the proxy is configured
2. Starts the proxy if auto-start is enabled
3. The proxy then handles Claude API requests via Azure OpenAI
"""
import sys
import os
import subprocess
import time
from pathlib import Path


def get_plugin_dir() -> Path:
    """Get the plugin directory (parent of hooks/)."""
    return Path(__file__).parent.parent


def get_config_path() -> Path | None:
    """Get the config file path, checking global location first.

    Priority:
    1. Global config: ~/.claude/azure-openai/.env
    2. Plugin directory: .env (fallback for development)
    """
    global_config = Path.home() / ".claude" / "azure-openai" / ".env"
    plugin_config = get_plugin_dir() / ".env"

    if global_config.exists():
        return global_config
    elif plugin_config.exists():
        return plugin_config
    return None


def load_env_file(path: Path) -> dict:
    """Load environment variables from a .env file."""
    env = {}
    if not path.exists():
        return env

    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, _, value = line.partition("=")
                # Remove quotes if present
                value = value.strip().strip('"').strip("'")
                env[key.strip()] = value
    return env


def is_proxy_running(pid_file: Path) -> bool:
    """Check if the proxy process is running."""
    if not pid_file.exists():
        return False

    try:
        pid = int(pid_file.read_text().strip())
        if sys.platform == "win32":
            # Windows: use tasklist
            result = subprocess.run(
                ["tasklist", "/FI", f"PID eq {pid}", "/NH"],
                capture_output=True,
                text=True,
            )
            return str(pid) in result.stdout
        else:
            # Unix: send signal 0 to check if process exists
            os.kill(pid, 0)
            return True
    except (ProcessLookupError, ValueError, PermissionError, OSError):
        # Process not found or invalid PID
        if pid_file.exists():
            pid_file.unlink()  # Clean up stale PID file
        return False


def get_venv_python(plugin_dir: Path) -> Path:
    """Get the path to the venv Python executable."""
    if sys.platform == "win32":
        return plugin_dir / "venv" / "Scripts" / "python.exe"
    return plugin_dir / "venv" / "bin" / "python"


def get_venv_pip(plugin_dir: Path) -> Path:
    """Get the path to the venv pip executable."""
    if sys.platform == "win32":
        return plugin_dir / "venv" / "Scripts" / "pip.exe"
    return plugin_dir / "venv" / "bin" / "pip"


def setup_venv(plugin_dir: Path) -> bool:
    """Create virtual environment and install dependencies."""
    venv_python = get_venv_python(plugin_dir)

    if not venv_python.exists():
        # Create virtual environment
        result = subprocess.run(
            [sys.executable, "-m", "venv", str(plugin_dir / "venv")],
            capture_output=True,
        )
        if result.returncode != 0:
            return False

        # Install dependencies
        pip = get_venv_pip(plugin_dir)
        requirements = plugin_dir / "requirements.txt"
        if requirements.exists():
            result = subprocess.run(
                [str(pip), "install", "-q", "-r", str(requirements)],
                capture_output=True,
            )
            if result.returncode != 0:
                return False

    return True


def start_proxy(plugin_dir: Path, config: dict) -> int | None:
    """Start the proxy server as a background process.

    Returns the process ID if successful, None otherwise.
    """
    venv_python = get_venv_python(plugin_dir)

    if not venv_python.exists():
        if not setup_venv(plugin_dir):
            return None

    # Set environment variables for the proxy
    env = os.environ.copy()
    for key, value in config.items():
        env[key] = value

    # Start proxy as daemon/background process
    log_file = plugin_dir / "proxy.log"

    try:
        if sys.platform == "win32":
            # Windows: use CREATE_NEW_PROCESS_GROUP and DETACHED_PROCESS
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE

            proc = subprocess.Popen(
                [str(venv_python), str(plugin_dir / "start_proxy.py")],
                cwd=str(plugin_dir),
                env=env,
                stdout=open(log_file, "w"),
                stderr=subprocess.STDOUT,
                startupinfo=startupinfo,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS,
            )
        else:
            # Unix: use start_new_session for daemon behavior
            proc = subprocess.Popen(
                [str(venv_python), str(plugin_dir / "start_proxy.py")],
                cwd=str(plugin_dir),
                env=env,
                stdout=open(log_file, "w"),
                stderr=subprocess.STDOUT,
                start_new_session=True,
            )

        # Save PID
        pid_file = plugin_dir / ".proxy.pid"
        pid_file.write_text(str(proc.pid))

        # Wait briefly and verify it started
        time.sleep(1)
        if is_proxy_running(pid_file):
            return proc.pid
        return None

    except Exception:
        return None


def main():
    """Main entry point for the session start hook."""
    # Find config
    config_path = get_config_path()
    if not config_path:
        # Not configured, skip silently
        sys.exit(0)

    # Load config
    config = load_env_file(config_path)

    # Check if auto-start is enabled (default: true)
    auto_start = config.get("AZURE_OPENAI_AUTO_START", "true").lower()
    if auto_start != "true":
        sys.exit(0)

    # Check if configured
    if not config.get("OPENAI_API_KEY"):
        # Not configured, skip silently
        sys.exit(0)

    plugin_dir = get_plugin_dir()
    pid_file = plugin_dir / ".proxy.pid"

    # Start proxy if not running
    if not is_proxy_running(pid_file):
        pid = start_proxy(plugin_dir, config)
        if pid:
            print(f"Azure OpenAI proxy started (PID: {pid})")
        else:
            print("Failed to start Azure OpenAI proxy", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
