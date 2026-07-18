"""Helpers para registros de impacto de la aplicación.

Proporciona funciones para crear registros de impacto auditables, almacenarlos
en memoria y exportarlos. Los registros son estructuras sencillas (diccionarios)
pensadas para ser serializadas o mostradas en logs.
"""

from typing import Any, Dict, List


def make_impact_record(
    impact_id: str,
    interaction_point: str,
    before_behavior: str,
    after_behavior: str,
    validation_reference: str,
) -> Dict[str, Any]:
    """
    Construye un registro de impacto con campos estándar.

    Parámetros
    ----------
    impact_id : str
        Identificador del impacto (por ejemplo, "IMP-<command_id>").
    interaction_point : str
        Punto de interacción (p.ej. pantalla o componente UI responsable).
    before_behavior : str
        Descripción del estado antes de la interacción.
    after_behavior : str
        Descripción del estado después de la interacción.
    validation_reference : str
        Referencia usada para validación o auditoría (p. ej. `command:<id>`).

    Devuelve
    -------
    Dict[str, Any]
        Diccionario con el registro de impacto.
    """
    return {
        "impact_id": impact_id,
        "interaction_point": interaction_point,
        "before_behavior": before_behavior,
        "after_behavior": after_behavior,
        "validation_reference": validation_reference,
    }


def make_impact_store() -> List[Dict[str, Any]]:
    """Crea y devuelve un almacén de impactos en memoria (lista vacía)."""
    return []


def add_impact_record(store: List[Dict[str, Any]], record: Dict[str, Any]) -> None:
    """Añade un registro al `store` en memoria."""
    store.append(record)


def list_impact_records(store: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Devuelve una copia de los registros presentes en el almacén."""
    return list(store)


def impact_records_to_dicts(store: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Retorna los registros como diccionarios listos para serializar."""
    return list(store)
