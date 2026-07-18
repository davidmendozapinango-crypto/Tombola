"""Authentication and validation helpers (non-OOP)."""
from typing import Any, Dict, List, Tuple
from src.config import STATE_CODES

def _is_uppercase(char: str) -> bool:
    return 'A' <= char <= 'Z'

def _is_lowercase(char: str) -> bool:
    return 'a' <= char <= 'z'

def _is_digit(char: str) -> bool:
    return '0' <= char <= '9'

def _is_special(char: str) -> bool:
    return char in '*=%_'

def _has_type(key: str, index: int, predicate) -> bool:
    """Recursively check if key contains at least one char satisfying predicate."""
    if index >= len(key):
        return False
    if predicate(key[index]):
        return True
    return _has_type(key, index + 1, predicate)

def _no_long_run(key: str, index: int, current_char: str, count: int) -> bool:
    """Recursively ensure no more than 3 consecutive identical characters."""
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
    """Return a dictionary with the status of each password rule."""
    return {'length_ok': 6 <= len(key) <= 10, 'has_uppercase': _has_type(key, 0, _is_uppercase), 'has_lowercase': _has_type(key, 0, _is_lowercase), 'has_digit': _has_type(key, 0, _is_digit), 'has_special': _has_type(key, 0, _is_special), 'no_long_run': len(key) > 0 and _no_long_run(key, 1, key[0], 1)}

def validate_password(key: str) -> Tuple[bool, List[str]]:
    """Validate an access key and return (valid, error_messages)."""
    criteria = check_password_criteria(key)
    errors = []
    if not criteria['length_ok']:
        errors.append('La clave debe tener entre 6 y 10 caracteres.')
    if not criteria['has_uppercase']:
        errors.append('La clave debe incluir al menos una mayuscula.')
    if not criteria['has_lowercase']:
        errors.append('La clave debe incluir al menos una minuscula.')
    if not criteria['has_digit']:
        errors.append('La clave debe incluir al menos un numero.')
    if not criteria['has_special']:
        errors.append('La clave debe incluir al menos un caracter especial (* = % _).')
    if not criteria['no_long_run']:
        errors.append('La clave no puede tener mas de 3 caracteres iguales seguidos.')
    return (len(errors) == 0, errors)

def validate_registration_data(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate registration form data."""
    errors = []
    player_id = str(data.get('player_id', '')).strip()
    full_name = str(data.get('full_name', '')).strip()
    gender = str(data.get('gender', '')).strip().lower()
    birthdate = str(data.get('birthdate', '')).strip()
    state_code = str(data.get('state_code', '')).strip().upper()
    access_key = str(data.get('access_key', '')).strip()
    if not player_id:
        errors.append('La cedula es obligatoria.')
    if not full_name:
        errors.append('El nombre completo es obligatorio.')
    if gender not in ('m', 'f'):
        errors.append("El sexo debe ser 'm' o 'f'.")
    if not birthdate:
        errors.append('La fecha de nacimiento es obligatoria.')
    if state_code not in STATE_CODES:
        errors.append('El codigo de estado no es valido.')
    (valid_key, key_errors) = validate_password(access_key)
    if not valid_key:
        errors.extend(key_errors)
    return (len(errors) == 0, errors)