"""Persistence adapter for application impact records (non-OOP)."""

import json
from typing import Any, Dict, List

from src.persistence.io_safety import append_bytes, make_safe_writer, read_bytes


def make_impact_persistence(
    filename: str = "impact_records.json", data_dir: str = "data"
) -> Dict[str, Any]:
    """Create an impact persistence dictionary."""
    writer = make_safe_writer(data_dir)
    return {
        "writer": writer,
        "filename": filename,
        "file_path": writer["data_dir"] / filename,
    }


def save_impact_records(
    persistence: Dict[str, Any], records: List[Dict[str, Any]]
) -> None:
    """Persist impact records to a local JSON file using append-safe I/O."""
    data = [dict(record) for record in records]
    serialized = json.dumps(data, default=str, indent=2)
    append_bytes(
        persistence["writer"], persistence["filename"], serialized.encode("utf-8")
    )


def load_impact_records(persistence: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Load impact records from the persistence file."""
    raw = read_bytes(persistence["writer"], persistence["filename"])
    if not raw:
        return []
    data = json.loads(raw.decode("utf-8"))
    return [dict(item) for item in data]
