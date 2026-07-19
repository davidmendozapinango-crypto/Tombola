"""
Persistencia de jugadores: utilidades para leer/escribir registros binarios.

Descripción:
    Este módulo ofrece funciones para gestionar el archivo de jugadores usando
    pickling secuencial (append-safe). Permite cargar, buscar, añadir y guardar
    jugadores, así como crear un jugador por defecto si no existen registros.

Notas:
    - No se usan formatos JSON ni bases de datos para mantener compatibilidad
      con el diseño original (registros pickled secuenciales).
"""

import pickle
from datetime import datetime
from typing import Any, Dict, List, Optional
from src.config import PLAYERS_FILE


def _default_players() -> List[Dict[str, Any]]:
    """
    Devuelve una lista de jugadores por defecto para que la aplicación sea
    utilizable inmediatamente cuando no existen registros.

    Returns:
        List[Dict[str, Any]]: Lista con al menos un jugador de ejemplo.
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
    """
    Añade un único registro de jugador al final del archivo binario sin
    sobrescribir el contenido existente (modo append). Utiliza pickle.

    Args:
        file_path: Ruta al archivo de jugadores.
        player: Diccionario que representa al jugador.
    """
    with open(file_path, "ab") as file:
        pickle.dump(player, file)


def load_players(file_path: str = str(PLAYERS_FILE)) -> List[Dict[str, Any]]:
    """
    Carga todos los registros de jugadores desde el archivo binario leyendo
    secuencialmente objetos pickled hasta EOF.

    Args:
        file_path: Ruta al archivo de jugadores (por defecto PLAYERS_FILE).

    Returns:
        List[Dict[str, Any]]: Lista de diccionarios de jugadores.
    """
    players: List[Dict[str, Any]] = []
    try:
        with open(file_path, "rb") as file:
            # Leemos registros pickled secuencialmente hasta EOF. Evitamos
            # usar `while True` con `break` mediante una bandera local `eof`.
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
    """
    Persiste un único registro de jugador usando escritura en modo append.

    Args:
        file_path: Ruta al archivo donde almacenar el registro.
        player: Diccionario con los datos del jugador.
    """
    _append_player_record(file_path, player)


def save_players(
    players: List[Dict[str, Any]], file_path: str = str(PLAYERS_FILE)
) -> None:
    """
    Persiste la lista completa de jugadores sobrescribiendo el archivo.

    Este comportamiento se mantiene para compatibilidad con la estructura
    original (uso de dumps secuenciales).

    Args:
        players: Lista de registros de jugador.
        file_path: Ruta al archivo destino.
    """
    with open(file_path, "wb") as file:
        for player in players:
            pickle.dump(player, file)


def find_player(
    players: List[Dict[str, Any]], player_id: str
) -> Optional[Dict[str, Any]]:
    """
    Busca un jugador por su identificador (player_id).

    Args:
        players: Lista de registros cargados en memoria.
        player_id: Identificador a buscar.

    Returns:
        Optional[Dict[str, Any]]: Registro del jugador si se encuentra, else None.
    """
    normalized_id = player_id.strip()
    for player in players:
        if player.get("player_id", "").strip() == normalized_id:
            return player
    return None


def player_exists(players: List[Dict[str, Any]], player_id: str) -> bool:
    """
    Indica si existe un jugador con la cédula/provided `player_id`.

    Returns:
        bool: True si existe, False en caso contrario.
    """
    return find_player(players, player_id) is not None


def add_player(
    players: List[Dict[str, Any]],
    player: Dict[str, Any],
    file_path: str = str(PLAYERS_FILE),
) -> List[Dict[str, Any]]:
    """
    Añade un nuevo jugador a la lista en memoria y lo persiste en el archivo
    (modo append). Devuelve la lista actualizada.

    Args:
        players: Lista en memoria que será extendida.
        player: Registro del jugador a añadir.
        file_path: Ruta del archivo de persistencia.

    Returns:
        List[Dict[str, Any]]: Lista actualizada de jugadores.
    """
    players.append(player)
    save_player(file_path, player)
    return players


def ensure_default_players(file_path: str = str(PLAYERS_FILE)) -> List[Dict[str, Any]]:
    """
    Garantiza que exista al menos un jugador en el archivo; si no hay
    registros crea y guarda la lista por defecto.

    Args:
        file_path: Ruta del archivo de jugadores.

    Returns:
        List[Dict[str, Any]]: Lista de jugadores cargada/creada.
    """
    players = load_players(file_path)
    if not players:
        players = _default_players()
        save_players(players, file_path)
    return players
