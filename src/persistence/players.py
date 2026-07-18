"""Player persistence helpers (non-OOP) using binary append-safe records."""
import pickle
from datetime import datetime
from typing import Any, Dict, List, Optional
from src.config import PLAYERS_FILE

def _default_players() -> List[Dict[str, Any]]:
    """Return a default player list so the app is usable immediately."""
    return [{'player_id': '12345678', 'full_name': 'Jugador Demo', 'gender': 'm', 'birthdate': '2000-01-01', 'state_code': 'CCS', 'access_key': 'Hola1=', 'registered_at': datetime.now()}]

def _append_player_record(file_path: str, player: Dict[str, Any]) -> None:
    """Append a single player record to the binary file without overwriting."""
    with open(file_path, 'ab') as file:
        pickle.dump(player, file)

def load_players(file_path: str=str(PLAYERS_FILE)) -> List[Dict[str, Any]]:
    """Load all player records from the binary file using sequential reads."""
    players: List[Dict[str, Any]] = []
    try:
        with open(file_path, 'rb') as file:
            while True:
                try:
                    record = pickle.load(file)
                except EOFError:
                    break
                if isinstance(record, dict):
                    players.append(record)
    except (FileNotFoundError, EOFError, pickle.PickleError):
        return []
    return players

def save_player(file_path: str, player: Dict[str, Any]) -> None:
    """Persist a single player record using append-safe binary I/O."""
    _append_player_record(file_path, player)

def save_players(players: List[Dict[str, Any]], file_path: str=str(PLAYERS_FILE)) -> None:
    """Persist the player list to the binary file (legacy bulk overwrite)."""
    with open(file_path, 'wb') as file:
        for player in players:
            pickle.dump(player, file)

def find_player(players: List[Dict[str, Any]], player_id: str) -> Optional[Dict[str, Any]]:
    """Find a player by ID."""
    normalized_id = player_id.strip()
    for player in players:
        if player.get('player_id', '').strip() == normalized_id:
            return player
    return None

def player_exists(players: List[Dict[str, Any]], player_id: str) -> bool:
    """Return True if a player with the given ID exists."""
    return find_player(players, player_id) is not None

def add_player(players: List[Dict[str, Any]], player: Dict[str, Any], file_path: str=str(PLAYERS_FILE)) -> List[Dict[str, Any]]:
    """Append a new player record and return the updated in-memory list."""
    players.append(player)
    save_player(file_path, player)
    return players

def ensure_default_players(file_path: str=str(PLAYERS_FILE)) -> List[Dict[str, Any]]:
    """Create default players if the file is missing or empty."""
    players = load_players(file_path)
    if not players:
        players = _default_players()
        save_players(players, file_path)
    return players