from src.core.dependencies import (
    check_dependency,
    make_dependency_checker,
    register_dependency,
)


def test_dependency_available():
    checker = make_dependency_checker()
    register_dependency(checker, "player_session", lambda: True)
    status = check_dependency(checker, "player_session")
    assert status["status"] == "Available"


def test_dependency_unavailable():
    checker = make_dependency_checker()
    register_dependency(checker, "player_session", lambda: False)
    status = check_dependency(checker, "player_session")
    assert status["status"] == "Unavailable"


def test_unregistered_dependency_is_unavailable():
    checker = make_dependency_checker()
    status = check_dependency(checker, "missing_dep")
    assert status["status"] == "Unavailable"
