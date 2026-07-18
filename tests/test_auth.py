"""Tests for authentication and registration validation."""
import pytest

from src.auth.validator import (check_password_criteria, validate_password,
                                validate_registration_data)


def test_valid_password_passes():
    (valid, errors) = validate_password('Hola1=')
    assert valid
    assert not errors

@pytest.mark.parametrize('password,expected_error', [('abc', 'La clave debe tener entre 6 y 10 caracteres.'), ('abcdef', 'La clave debe incluir al menos una mayuscula.'), ('ABCDEF', 'La clave debe incluir al menos una minuscula.'), ('Abcdef', 'La clave debe incluir al menos un numero.'), ('Abcdef1', 'La clave debe incluir al menos un caracter especial'), ('Aaaaa1=', 'La clave no puede tener mas de 3 caracteres iguales seguidos.')])
def test_password_rules(password, expected_error):
    (valid, errors) = validate_password(password)
    assert not valid
    assert any((expected_error in error for error in errors))

def test_check_password_criteria_returns_all_fields():
    criteria = check_password_criteria('Hola1=')
    assert all(criteria.values())

def test_check_password_criteria_detects_missing_uppercase():
    criteria = check_password_criteria('hola1=')
    assert not criteria['has_uppercase']
    assert criteria['has_lowercase']

def test_registration_valid_data():
    data = {'player_id': '12345678', 'full_name': 'Juan Perez', 'gender': 'm', 'birthdate': '2000-01-01', 'state_code': 'CCS', 'access_key': 'Hola1='}
    (valid, errors) = validate_registration_data(data)
    assert valid
    assert not errors

def test_registration_invalid_state_code():
    data = {'player_id': '12345678', 'full_name': 'Juan Perez', 'gender': 'm', 'birthdate': '2000-01-01', 'state_code': 'XYZ', 'access_key': 'Hola1='}
    (valid, errors) = validate_registration_data(data)
    assert not valid
    assert any(('codigo de estado' in error for error in errors))

def test_registration_invalid_gender():
    data = {'player_id': '12345678', 'full_name': 'Juan Perez', 'gender': 'x', 'birthdate': '2000-01-01', 'state_code': 'CCS', 'access_key': 'Hola1='}
    (valid, errors) = validate_registration_data(data)
    assert not valid
    assert any(('sexo' in error for error in errors))

def test_registration_missing_required_fields():
    data = {'player_id': '', 'full_name': '', 'gender': '', 'birthdate': '', 'state_code': '', 'access_key': ''}
    (valid, errors) = validate_registration_data(data)
    assert not valid
    assert len(errors) >= 4