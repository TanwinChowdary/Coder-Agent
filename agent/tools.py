import pathlib
import subprocess
from typing import Tuple

from langchain_core.tools import tool

PROJECT_ROOT = pathlib.Path.cwd() / "generated_project"


def safe_path_for_project(path: str) -> pathlib.Path:
    p = (PROJECT_ROOT / path).resolve()
    if (
        PROJECT_ROOT.resolve() not in p.parents
        and PROJECT_ROOT.resolve() != p.parent
        and PROJECT_ROOT.resolve() != p
    ):
        raise ValueError("Attempt to write outside project root")
    return p


@tool
def write_file(path: str, content: str) -> str:
    """Writes content to a file at the specified path within the project root."""
    p = safe_path_for_project(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)
    return f"WROTE:{p}"


@tool
def read_file(path: str) -> str:
    """Reads content from a file at the specified path within the project root."""
    p = safe_path_for_project(path)
    if not p.exists():
        return ""
    with open(p, "r", encoding="utf-8") as f:
        return f.read()


@tool
def get_current_directory() -> str:
    """Returns the current working directory."""
    return str(PROJECT_ROOT)


@tool
def print_tree(path: str = ".", depth: int = 2) -> str:
    """Return a simple tree listing of files under the project root up to `depth` levels."""
    p = safe_path_for_project(path)
    if not p.exists():
        return f"ERROR: {p} does not exist"

    lines = []

    def _walk(dir_path: pathlib.Path, prefix: str, current_depth: int):
        if current_depth > depth:
            return
        try:
            entries = sorted(dir_path.iterdir(), key=lambda x: (not x.is_dir(), x.name))
        except PermissionError:
            lines.append(prefix + "[permission denied]")
            return
        for entry in entries:
            rel = entry.relative_to(PROJECT_ROOT)
            marker = "/" if entry.is_dir() else ""
            lines.append(f"{prefix}{entry.name}{marker}")
            if entry.is_dir():
                _walk(entry, prefix + "  ", current_depth + 1)

    _walk(p, "", 0)
    return "\n".join(lines) if lines else "<empty>"


@tool
def list_files(directory: str = ".") -> str:
    """Lists all files in the specified directory within the project root."""
    p = safe_path_for_project(directory)
    if not p.is_dir():
        return f"ERROR: {p} is not a directory"
    files = [str(f.relative_to(PROJECT_ROOT)) for f in p.glob("**/*") if f.is_file()]
    return "\n".join(files) if files else "No files found."


@tool
def run_cmd(cmd, cwd: str = None, timeout: int = 30) -> Tuple[int, str, str]:
    """
    Runs a shell command in the specified directory.
    Accepts:
    - cmd: string
    - cmd: ["bash", "-lc", "ls -R"]   <-- LLM often sends this form
    """
    # If cmd is a list, join into a shell-friendly string
    if isinstance(cmd, list):
        cmd = " ".join(cmd)

    if not isinstance(cmd, str):
        raise ValueError(f"Invalid cmd type: {type(cmd)}")

    cwd_dir = safe_path_for_project(cwd) if cwd else PROJECT_ROOT

    res = subprocess.run(
        cmd,
        shell=True,
        cwd=str(cwd_dir),
        capture_output=True,
        text=True,
        timeout=timeout
    )

    return res.returncode, res.stdout, res.stderr


def init_project_root():
    PROJECT_ROOT.mkdir(parents=True, exist_ok=True)
    return str(PROJECT_ROOT)



write_file.name = "repo_browser.write_file"
read_file.name = "repo_browser.read_file"
list_files.name = "repo_browser.list_files"
get_current_directory.name = "repo_browser.get_current_directory"
run_cmd.name = "repo_browser.run_cmd"
print_tree.name = "repo_browser.print_tree"