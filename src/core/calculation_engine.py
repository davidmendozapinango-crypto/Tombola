"""Orquestador de cálculos con manejo determinista de fallos (no orientado a objetos).

Descripción:
    Punto central que ejecuta comandos internos iniciados por la interfaz
    gráfica (GUI). Valida campos, selecciona reglas de negocio, verifica
    dependencias, evalúa precondiciones, calcula resultados y registra
    impactos observables para auditoría.

Notas/Teoría:
    - El motor está diseñado como una función pura de coordinación: no usa
      estado global compartido; recibe un `context` y opera sobre él.
    - Los impactos (auditoría) se registran siempre en memoria y opcionalmente
      se persisten; esto facilita pruebas y replays sin efectos secundarios
      inesperados cuando no se configura persistencia.
    - El flujo es deliberadamente explícito y secuencial para facilitar el
      rastreo de errores y la explicación en logs o UI.
"""

from typing import Any, Dict, List, Optional
from src.core.application_impact import (
    add_impact_record,
    make_impact_record,
    make_impact_store,
)
from src.core.calculation_rules import compute_result
from src.core.command_contract import validate_required_fields
from src.core.dependencies import check_dependency
from src.core.error_messages import MESSAGES, build_error_response
from src.core.path_rules import select_rule
from src.core.precondition_evaluator import evaluate_preconditions
from src.persistence.impact_records import save_impact_records


def make_engine_context(
    registry: Dict[str, Any],
    preconditions: List[Dict[str, Any]],
    dependency_checker: Dict[str, Any],
    error_catalog: Optional[Dict[str, Dict[str, str]]] = None,
    impact_store: Optional[List[Dict[str, Any]]] = None,
    impact_persistence: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Crear un contexto de motor que agrupa colaboradores y configuraciones.

    Descripción:
        Construye y devuelve un diccionario con las dependencias que el
        motor de cálculo necesitará para operar (registro de reglas, lista de
        precondiciones, verificador de dependencias, catálogo de errores,
        almacén temporal de impactos y persistencia opcional).

    Args:
        registry: Registro de reglas/configuración de rutas.
        preconditions: Lista de precondiciones a evaluar.
        dependency_checker: Estructura usada para verificar dependencias externas.
        error_catalog: Catálogo de mensajes de error (si no se provee se usa MESSAGES).
        impact_store: Lista para almacenar impactos en memoria; si no se provee se crea una nueva.
        impact_persistence: Mecanismo opcional para persistir impactos.

    Devuelve:
        Dict[str, Any]: Contexto empaquetado para pasar al motor.
    """
    return {
        "registry": registry,
        "preconditions": preconditions,
        "dependency_checker": dependency_checker,
        "error_catalog": error_catalog or MESSAGES,
        "impact_store": impact_store
        if impact_store is not None
        else make_impact_store(),
        "impact_persistence": impact_persistence,
    }


def execute_command(command: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """Ejecutar un comando de cálculo interno originado desde la GUI.

    Flujo general:
        1. Verifica que el comando tenga origen UI (`ui_origin`).
        2. Valida campos requeridos en el comando.
        3. Selecciona la regla de negocio correspondiente al `operation_key` y `path_context`.
        4. Comprueba dependencias bloqueantes.
        5. Evalúa precondiciones; si pasan, calcula el resultado.
        6. Registra el impacto observable y devuelve el resultado o un error.

    Args:
        command: Diccionario con la definición del comando proveniente de la UI.
        context: Contexto creado por `make_engine_context` que contiene colaboradores.

    Devuelve:
        Dict[str, Any]: Resultado de la ejecución con `status` y `result_payload`,
        o una respuesta de error construida por `build_error_response`.
    """
    # Referencia al catálogo de mensajes de error local (puede ser inyectado para tests)
    error_catalog = context["error_catalog"]

    # 1) Origen UI obligatorio: si falta, no procesamos el comando
    if not command.get("ui_origin"):
        _record_impact(command, None, False, context)
        return build_error_response(
            "business_precondition_failed", "missing_ui_origin", error_catalog
        )
    # 2) Validar campos esenciales del comando
    missing = validate_required_fields(command)
    if missing:
        # Registrar impacto de rechazo y devolver un error identificable por la UI
        _record_impact(command, None, False, context)
        return build_error_response(
            "business_precondition_failed", f"missing_{missing[0]}", error_catalog
        )
    # 3) Seleccionar la regla de negocio aplicable según la operación y el contexto
    rule = select_rule(
        context["registry"],
        command["operation_key"],
        command["path_context"],
        command["input_payload"],
    )
    if rule is None:
        _record_impact(command, None, False, context)
        return build_error_response(
            "business_precondition_failed", "invalid_path_state", error_catalog
        )
    # 4) Comprobar dependencias bloqueantes declaradas por la regla
    for dep_id in rule["blocking_dependencies"]:
        status = check_dependency(context["dependency_checker"], dep_id)
        if status["status"] == "Unavailable":
            # Registro del intento y falla por dependencia no disponible
            _record_impact(command, rule, False, context)
            return build_error_response(
                "dependency_unavailable", "dependency_unavailable", error_catalog
            )
    payload = {
        "command": command,
        "path_context": command["path_context"],
        "input_payload": command["input_payload"],
    }
    # 5) Evaluar precondiciones de negocio: si alguna falla se reporta la causa
    (passed, failure) = evaluate_preconditions(context["preconditions"], payload)
    if not passed and failure is not None:
        _record_impact(command, rule, False, context, failure=failure)
        return build_error_response(
            "business_precondition_failed", failure["failure_message_id"], error_catalog
        )
    # 6) Ejecutar la lógica de cálculo asociada a la regla y registrar impacto
    result_payload = compute_result(rule, command["input_payload"])
    _record_impact(command, rule, True, context)
    return {
        "status": "success",
        "path_id": rule["path_id"],
        "result_payload": result_payload,
        "impact_marker": rule["output_definition"].get("impact_marker"),
    }


def _record_impact(
    command: Dict[str, Any],
    rule: Optional[Dict[str, Any]],
    success: bool,
    context: Dict[str, Any],
    failure: Optional[Dict[str, Any]] = None,
) -> None:
    """Registrar el impacto observable de la aplicación para auditoría.

    Descripción:
        Construye un `record` que describe el antes y después de la interacción
        y lo añade al `impact_store`. Si `impact_persistence` está configurado,
        también intenta persistir el registro.

    Args:
        command: Comando original que disparó la operación.
        rule: Regla aplicada (si existe).
        success: Indica si la operación terminó con éxito.
        context: Contexto del motor que contiene el `impact_store` y la
            `impact_persistence` (opcional).
        failure: Información de fallo (opcional), usada para describir el motivo.
    """
    # Construir y persistir (opcionalmente) el registro de impacto. Se usa un
    # identificador derivado del comando para facilitar correlación en logs.
    impact_id = f"IMP-{command['command_id']}"
    interaction_point = command.get("ui_origin") or "unknown"
    if success:
        before_behavior = "No calculation result available"
        after_behavior = (
            f"Calculation succeeded via {(rule['path_id'] if rule else 'unknown')}"
        )
    else:
        before_behavior = "No calculation error recorded"
        after_behavior = f"Calculation rejected: {(failure['precondition_id'] if failure else 'precondition_failed')}"
    validation_reference = f"command:{command['command_id']}"
    record = make_impact_record(
        impact_id=impact_id,
        interaction_point=interaction_point,
        before_behavior=before_behavior,
        after_behavior=after_behavior,
        validation_reference=validation_reference,
    )
    # Añadir el registro al almacén en memoria y, si se configuró, persistirlo.
    add_impact_record(context["impact_store"], record)
    persistence = context.get("impact_persistence")
    if persistence is not None:
        save_impact_records(persistence, [record])
