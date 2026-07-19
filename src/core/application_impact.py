"""Ayudantes para registro y manejo de impactos observables de la aplicación.

Descripción:
    Se usa para construir registros que describen el antes y después de una
    interacción relevante (por ejemplo, ejecución de un cálculo). Estos
    registros facilitan auditoría y trazabilidad.
"""

from typing import Any, Dict, List


def make_impact_record(
    impact_id: str,
    interaction_point: str,
    before_behavior: str,
    after_behavior: str,
    validation_reference: str,
) -> Dict[str, Any]:
    """Crear un diccionario que representa un registro de impacto.

    Args:
        impact_id: Identificador único del impacto.
        interaction_point: Punto de interacción (p. ej. pantalla UI).
        before_behavior: Descripción del estado antes de la acción.
        after_behavior: Descripción del estado después de la acción.
        validation_reference: Referencia para validar (p. ej. comando id).

    Returns:
        Dict[str, Any]: Registro listo para almacenarse.
    """
    return {
        "impact_id": impact_id,
        "interaction_point": interaction_point,
        "before_behavior": before_behavior,
        "after_behavior": after_behavior,
        "validation_reference": validation_reference,
    }


def make_impact_store() -> List[Dict[str, Any]]:
    """Crear un almacén simple (lista) para registros de impacto."""
    return []


def add_impact_record(store: List[Dict[str, Any]], record: Dict[str, Any]) -> None:
    """Añadir un registro al almacén de impactos."""
    store.append(record)


def list_impact_records(store: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Devolver todos los registros de impacto existentes."""
    return list(store)


def impact_records_to_dicts(store: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Devolver registros como diccionarios (identidad en este diseño)."""
    return list(store)
