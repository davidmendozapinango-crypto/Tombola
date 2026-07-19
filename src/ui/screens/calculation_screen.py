"""Controlador de pantalla para acciones de cálculo en la GUI.

Descripción:
    Provee una interfaz mínima para integrar la lógica de cálculo con la
    navegación por teclado (foco entre controles) y para disparar el flujo
    de cálculo desde la UI.
"""

from typing import Any, Dict
from src.ui.flows.calculation_flow import make_flow, trigger

# Controles que participan en la navegación por teclado para esta pantalla.
CONTROLS = ["calculate_button", "cancel_button"]


def make_screen(
    engine_context: Dict[str, Any], state: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Construir la estructura de la pantalla de cálculo.

    Inicializa el flujo de cálculo y el conjunto de controles enfocables.

    Args:
        engine_context: Contexto del motor de cálculo (reglas, dependencias).
        state: Estado de la aplicación (se pasa al flujo para permitir efectos).

    Devuelve:
        Dict[str, Any]: Estructura de pantalla con `flow`, controles y foco.
    """
    screen = {
        "flow": make_flow(engine_context, state),
        "controls": list(CONTROLS),
        "focus_index": -1,
        "focused_control": None,
    }
    focus_next(screen)
    return screen


def on_calculate_action(
    screen: Dict[str, Any], raw_payload: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Manejar la acción de cálculo disparada por el usuario desde la UI.

    Convierte la carga enviada por la interfaz y la reenvía al flujo de
    cálculo, devolviendo el resultado que contiene estado de éxito/fracaso.
    """
    return trigger(screen["flow"], raw_payload)


def focus_next(screen: Dict[str, Any]) -> None:
    """Mover el foco al siguiente control (navegación con teclado)."""
    screen["focus_index"] = (screen["focus_index"] + 1) % len(screen["controls"])
    screen["focused_control"] = screen["controls"][screen["focus_index"]]


def focus_previous(screen: Dict[str, Any]) -> None:
    """Mover el foco al control anterior (navegación con teclado)."""
    screen["focus_index"] = (screen["focus_index"] - 1) % len(screen["controls"])
    screen["focused_control"] = screen["controls"][screen["focus_index"]]
