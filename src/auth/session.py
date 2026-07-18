"""Session state helpers (non-OOP)."""
from typing import Any, Dict, Optional


def make_session() -> Dict[str, Any]:
    """Create an empty session dictionary."""
    return {'player': None, 'main_card': None, 'complement_card': None, 'dimension': None, 'sdg_id': None, 'drawn_numbers': [], 'marked_main': set(), 'marked_complement': set(), 'winning_card': None, 'game_over': False}

def login(session: Dict[str, Any], player: Dict[str, Any]) -> Dict[str, Any]:
    """Store the authenticated player in the session."""
    session['player'] = player
    return session

def logout(session: Dict[str, Any]) -> Dict[str, Any]:
    """Clear the session."""
    session.clear()
    return make_session()

def get_player(session: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Return the current player or None."""
    return session.get('player')

def is_authenticated(session: Dict[str, Any]) -> bool:
    """Return True if a player is logged in."""
    return session.get('player') is not None