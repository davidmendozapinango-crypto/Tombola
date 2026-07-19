"""
Helpers de autenticación y validación (no-OOP).

Descripción:
  Contiene utilidades para validar criterios de contraseñas y datos de
  registro de jugadores. Implementa comprobaciones recursivas simples para
  aprendizaje didáctico.
"""

from typing import Any, Dict, List, Tuple
from src.config import STATE_CODES


def _is_uppercase(char: str) -> bool:
    return "A" <= char <= "Z"


def _is_lowercase(char: str) -> bool:
    return "a" <= char <= "z"


def _is_digit(char: str) -> bool:
    return "0" <= char <= "9"


def _is_special(char: str) -> bool:
    return char in "*=%_"


def _has_type(key: str, index: int, predicate) -> bool:
    """Comprueba recursivamente si `key` contiene al menos un caracter que
    satisface `predicate`.

    Este enfoque recursivo es intencional para favorecer un estilo educativo
    en el código, aunque una implementación iterativa sería más directa.
    """
    if index >= len(key):
        return False
    if predicate(key[index]):
        return True
    return _has_type(key, index + 1, predicate)


def _no_long_run(key: str, index: int, current_char: str, count: int) -> bool:
    """Asegura recursivamente que no haya más de 3 caracteres idénticos
    consecutivos en la clave.

    Args:
        key: La clave a validar.
        index: Posición actual en la recursión.
        current_char: Caracter que estamos contando consecutivamente.
        count: Conteo actual de repeticiones consecutivas.
    """
    if index >= len(key):
        return True
    if key[index] == current_char:
        new_count = count + 1
        if new_count > 3:
            return False
    else:
        new_count = 1
        current_char = key[index]
    return _no_long_run(key, index + 1, current_char, new_count)


def check_password_criteria(key: str) -> Dict[str, bool]:
    """Devuelve un diccionario con el estado (True/False) de cada criterio de contraseña.

    Criterios incluidos: longitud, mayúscula, minúscula, dígito, carácter
    especial y ausencia de corridas largas de caracteres.
    """
    return {
        "length_ok": 6 <= len(key) <= 10,
        "has_uppercase": _has_type(key, 0, _is_uppercase),
        "has_lowercase": _has_type(key, 0, _is_lowercase),
        "has_digit": _has_type(key, 0, _is_digit),
        "has_special": _has_type(key, 0, _is_special),
        "no_long_run": len(key) > 0 and _no_long_run(key, 1, key[0], 1),
    }


def validate_password(key: str) -> Tuple[bool, List[str]]:
    """Valida una clave de acceso y devuelve (valida, lista_errores).

    Los mensajes de error están en español y son adecuados para mostrar al
    usuario en la UI.
    """
    criteria = check_password_criteria(key)
    errors = []
    if not criteria["length_ok"]:
        errors.append("La clave debe tener entre 6 y 10 caracteres.")
    if not criteria["has_uppercase"]:
        errors.append("La clave debe incluir al menos una mayuscula.")
    if not criteria["has_lowercase"]:
        errors.append("La clave debe incluir al menos una minuscula.")
    if not criteria["has_digit"]:
        errors.append("La clave debe incluir al menos un numero.")
    if not criteria["has_special"]:
        errors.append("La clave debe incluir al menos un caracter especial (* = % _).")
    if not criteria["no_long_run"]:
        errors.append("La clave no puede tener mas de 3 caracteres iguales seguidos.")
    return (len(errors) == 0, errors)


def validate_registration_data(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Valida los datos del formulario de registro y devuelve (valido, errores).

    Comprueba campos obligatorios, formato y criterios de contraseña.
    """
    errors = []
    player_id = str(data.get("player_id", "")).strip()
    full_name = str(data.get("full_name", "")).strip()
    gender = str(data.get("gender", "")).strip().lower()
    birthdate = str(data.get("birthdate", "")).strip()
    state_code = str(data.get("state_code", "")).strip().upper()
    access_key = str(data.get("access_key", "")).strip()
    if not player_id:
        errors.append("La cedula es obligatoria.")
    if not full_name:
        errors.append("El nombre completo es obligatorio.")
    if gender not in ("m", "f"):
        errors.append("El sexo debe ser 'm' o 'f'.")
    if not birthdate:
        errors.append("La fecha de nacimiento es obligatoria.")
    if state_code not in STATE_CODES:
        errors.append("El codigo de estado no es valido.")
    (valid_key, key_errors) = validate_password(access_key)
    if not valid_key:
        errors.extend(key_errors)
    return (len(errors) == 0, errors)
