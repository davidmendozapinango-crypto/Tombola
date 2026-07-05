"""Shared binary I/O safety helpers (non-OOP)."""

from pathlib import Path
from typing import Any, BinaryIO, Callable, Dict


def make_safe_writer(data_dir: str = "data") -> Dict[str, Any]:
    """Create a safe binary writer dictionary."""
    path = Path(data_dir)
    path.mkdir(parents=True, exist_ok=True)
    return {"data_dir": path}


def writer_path(writer: Dict[str, Any], filename: str) -> Path:
    """Return the full path for a file in the writer's data directory."""
    return writer["data_dir"] / filename


def append_bytes(writer: Dict[str, Any], filename: str, data: bytes) -> None:
    """Append bytes safely to a file (no silent overwrite)."""
    file_path = writer_path(writer, filename)
    with open(file_path, "ab") as f:
        f.write(data)


def read_bytes(writer: Dict[str, Any], filename: str) -> bytes:
    """Read all bytes from a file."""
    file_path = writer_path(writer, filename)
    if not file_path.exists():
        return b""
    with open(file_path, "rb") as f:
        return f.read()


def file_exists(writer: Dict[str, Any], filename: str) -> bool:
    """Check whether a file exists in the writer's data directory."""
    return writer_path(writer, filename).exists()


def with_locked_write(file_path: Path, writer: Callable[[BinaryIO], Any]) -> None:
    """Open file for append and execute writer callback safely."""
    with open(file_path, "ab") as f:
        writer(f)
