"""Persistence adapter for application impact records (non-OOP)."""
import json
from pathlib import Path
from typing import Any, Dict, List
from src.persistence.io_safety import append_bytes, make_safe_writer, read_bytes

def make_impact_persistence(filename: str='impact_records.jsonl', data_dir: str='data') -> Dict[str, Any]:
    """Create an impact persistence dictionary."""
    writer = make_safe_writer(data_dir)
    return {'writer': writer, 'filename': filename, 'file_path': writer['data_dir'] / filename}

def _serialize_record(record: Dict[str, Any]) -> bytes:
    """Serialize a single impact record to a JSON line."""
    return json.dumps(dict(record), default=str, ensure_ascii=False).encode('utf-8') + b'\n'

def save_impact_records(persistence: Dict[str, Any], records: List[Dict[str, Any]]) -> None:
    """Persist impact records as append-safe line-delimited JSON (JSONL)."""
    if not records:
        return
    data = b''.join((_serialize_record(record) for record in records))
    append_bytes(persistence['writer'], persistence['filename'], data)

def _parse_record_line(line: bytes) -> Dict[str, Any]:
    """Parse a single JSONL line into a record dict."""
    text = line.decode('utf-8').strip()
    if not text:
        return {}
    parsed = json.loads(text)
    if not isinstance(parsed, dict):
        return {}
    return dict(parsed)

def _validate_record(record: Dict[str, Any]) -> bool:
    """Return True if the record has all required ApplicationImpactRecord fields."""
    required = {'impact_id', 'interaction_point', 'before_behavior', 'after_behavior', 'validation_reference'}
    return required.issubset(record.keys())

def load_impact_records(persistence: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Load and validate impact records from the persistence file."""
    raw = read_bytes(persistence['writer'], persistence['filename'])
    if not raw:
        return []
    records: List[Dict[str, Any]] = []
    for line in raw.splitlines():
        try:
            record = _parse_record_line(line)
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue
        if _validate_record(record):
            records.append(record)
    return records

def impact_records_file_path(persistence: Dict[str, Any]) -> Path:
    """Return the absolute path of the impact records file."""
    return persistence['file_path']