"""Application impact record helpers (non-OOP)."""

from typing import Any, Dict, List


def make_impact_record(
    impact_id: str,
    interaction_point: str,
    before_behavior: str,
    after_behavior: str,
    validation_reference: str,
) -> Dict[str, Any]:
    """Create an application impact record dictionary."""
    return {
        "impact_id": impact_id,
        "interaction_point": interaction_point,
        "before_behavior": before_behavior,
        "after_behavior": after_behavior,
        "validation_reference": validation_reference,
    }


def make_impact_store() -> List[Dict[str, Any]]:
    """Create an empty impact store (list)."""
    return []


def add_impact_record(store: List[Dict[str, Any]], record: Dict[str, Any]) -> None:
    """Add a record to the impact store."""
    store.append(record)


def list_impact_records(store: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Return all impact records."""
    return list(store)


def impact_records_to_dicts(store: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Return records as plain dictionaries (already dicts)."""
    return list(store)
