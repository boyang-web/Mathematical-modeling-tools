"""Launcher used for local startup and future exe packaging."""

from pathlib import Path
import os
import sys
import threading
import time
import webbrowser

from core.runtime import get_distribution_root, get_runtime_root


def get_project_root() -> Path:
    """Return the project root directory."""

    return get_runtime_root()


def get_streamlit_port() -> int:
    """Return the port used by the Streamlit server."""

    port_value = os.environ.get("MMT_STREAMLIT_PORT", "8501")
    try:
        return int(port_value)
    except ValueError:
        return 8501


def get_streamlit_url() -> str:
    """Return the local URL used to open the app."""

    return f"http://127.0.0.1:{get_streamlit_port()}"


def open_browser_later() -> None:
    """Open the default browser after the Streamlit server starts."""

    def _worker() -> None:
        time.sleep(2)
        webbrowser.open(get_streamlit_url())

    thread = threading.Thread(target=_worker, daemon=True)
    thread.start()


def build_streamlit_argv() -> list[str]:
    """Build the command line arguments used to start Streamlit."""

    project_root = get_project_root()
    app_path = project_root / "app" / "main.py"

    return [
        "streamlit",
        "run",
        str(app_path),
        "--server.headless=true",
        f"--server.port={get_streamlit_port()}",
        "--browser.gatherUsageStats=false",
    ]


def main() -> None:
    """Start the Streamlit application."""

    project_root = get_project_root()
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    try:
        from streamlit.web import cli as stcli
    except ModuleNotFoundError as error:
        if error.name == "streamlit":
            python_path = sys.executable
            message = (
                "当前 Python 环境没有安装 streamlit。\n"
                f"正在使用的解释器: {python_path}\n"
                "请先执行: python -m pip install -r requirements.txt"
            )
            raise SystemExit(message) from error
        raise

    os.chdir(project_root)
    print(f"Using Python interpreter: {sys.executable}")
    print(f"App URL: {get_streamlit_url()}")
    print(f"Distribution directory: {get_distribution_root()}")
    open_browser_later()
    sys.argv = build_streamlit_argv()
    raise SystemExit(stcli.main())


if __name__ == "__main__":
    main()
