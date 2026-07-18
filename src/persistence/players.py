"""Ayudantes para persistencia de jugadores (I/O binario con append seguro).

Este módulo permite leer/escribir registros de player serializados con
`pickle`. Incluye utilidades para crear jugadores por defecto y mantener
compatibilidad con almacenamiento secuencial en disco.
"""

import pickle
from datetime import datetime
from typing import Any, Dict, List, Optional
from src.config import PLAYERS_FILE


def _default_players() -> List[Dict[str, Any]]:
    """
    Devuelve una lista de jugadores por defecto para facilitar la experiencia
    al arrancar la aplicación por primera vez.
    """
    return [
        {
            "player_id": "12345678",
            "full_name": "Jugador Demo",
            "gender": "m",
            "birthdate": "2000-01-01",
            "state_code": "CCS",
            "access_key": "Hola1=",
            "registered_at": datetime.now(),
        }
    ]


def _append_player_record(file_path: str, player: Dict[str, Any]) -> None:
    """Añade un registro de jugador al fichero binario sin sobrescribir."""
    with open(file_path, "ab") as file:
        pickle.dump(player, file)


def load_players(file_path: str = str(PLAYERS_FILE)) -> List[Dict[str, Any]]:
    """
    Carga todos los registros de jugadores desde el fichero binario.

    Si el fichero no existe o está corrupto, la función devuelve una lista
    vacía para mantener tolerancia a fallos.
    """
    players: List[Dict[str, Any]] = []
    try:
        with open(file_path, "rb") as file:
            eof = False
            while not eof:
                try:
                    record = pickle.load(file)
                except EOFError:
                    eof = True
                else:
                    if isinstance(record, dict):
                        players.append(record)
    except (FileNotFoundError, EOFError, pickle.PickleError):
        return []
    return players


def save_player(file_path: str, player: Dict[str, Any]) -> None:
    """Persiste un jugador usando I/O binario en modo append."""
    _append_player_record(file_path, player)


def save_players(
    players: List[Dict[str, Any]], file_path: str = str(PLAYERS_FILE)
) -> None:
    """Sobrescribe el fichero guardando la lista completa de jugadores."""
    with open(file_path, "wb") as file:
        for player in players:
            pickle.dump(player, file)


def find_player(
    players: List[Dict[str, Any]], player_id: str
) -> Optional[Dict[str, Any]]:
    """Busca un jugador por `player_id` y lo devuelve si existe."""
    normalized_id = player_id.strip()
    for player in players:
        if player.get("player_id", "").strip() == normalized_id:
            return player
    return None


def player_exists(players: List[Dict[str, Any]], player_id: str) -> bool:
    """Devuelve `True` si existe un jugador con el identificador dado."""
    return find_player(players, player_id) is not None


def add_player(
    players: List[Dict[str, Any]],
    player: Dict[str, Any],
    file_path: str = str(PLAYERS_FILE),
) -> List[Dict[str, Any]]:
    """Añade un nuevo jugador a la lista en memoria y lo persiste en disco."""
    players.append(player)
    save_player(file_path, player)
    return players


def ensure_default_players(file_path: str = str(PLAYERS_FILE)) -> List[Dict[str, Any]]:
    """Garantiza que existan jugadores por defecto si el fichero está vacío."""
    players = load_players(file_path)
    if not players:
        players = _default_players()
        save_players(players, file_path)
    return players
