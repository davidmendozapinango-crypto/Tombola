"""
Adaptador de persistencia para registros de impacto de la aplicacion.

Descripción:
  Proporciona una interfaz simple para guardar y cargar registros de impacto
  (ApplicationImpactRecord) usando archivos JSONL (line-delimited JSON).
  Los registros se almacenan en el directorio gestionado por `make_safe_writer`.
"""

import json
from pathlib import Path
from typing import Any, Dict, List
from src.persistence.io_safety import append_bytes, make_safe_writer, read_bytes


def make_impact_persistence(
    filename: str = "impact_records.jsonl", data_dir: str = "data"
) -> Dict[str, Any]:
    """Crear la estructura de persistencia para registros de impacto.

    Returns:
        Dict[str, Any]: Objeto con keys: 'writer', 'filename', 'file_path'.
    """
    writer = make_safe_writer(data_dir)
    return {
        "writer": writer,
        "filename": filename,
        "file_path": writer["data_dir"] / filename,
    }


def _serialize_record(record: Dict[str, Any]) -> bytes:
    """Serializar un registro de impacto a JSON (una sola linea UTF-8)."""
    return (
        json.dumps(dict(record), default=str, ensure_ascii=False).encode("utf-8")
        + b"\n"
    )


def save_impact_records(
    persistence: Dict[str, Any], records: List[Dict[str, Any]]
) -> None:
    """Persistir registros de impacto en formato JSONL usando append seguro."""
    if not records:
        return
    data = b"".join((_serialize_record(record) for record in records))
    append_bytes(persistence["writer"], persistence["filename"], data)


def _parse_record_line(line: bytes) -> Dict[str, Any]:
    """Parsear una linea JSONL y devolver el diccionario resultante."""
    text = line.decode("utf-8").strip()
    if not text:
        return {}
    parsed = json.loads(text)
    if not isinstance(parsed, dict):
        return {}
    return dict(parsed)


def _validate_record(record: Dict[str, Any]) -> bool:
    """Validar que el registro contiene los campos requeridos de impacto."""
    required = {
        "impact_id",
        "interaction_point",
        "before_behavior",
        "after_behavior",
        "validation_reference",
    }
    return required.issubset(record.keys())


def load_impact_records(persistence: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Cargar y validar registros de impacto desde el archivo JSONL.

    Ignora lineas inválidas o entradas que no cumplan el esquema mínimo.
    """
    raw = read_bytes(persistence["writer"], persistence["filename"])
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
    """Devuelve la ruta absoluta del archivo de registros de impacto.

    Args:
        persistence: Estructura creada por `make_impact_persistence` que
            contiene la clave 'file_path'.

    Returns:
        Path: Ruta absoluta al archivo JSONL de registros de impacto.
    """
    return persistence["file_path"]
