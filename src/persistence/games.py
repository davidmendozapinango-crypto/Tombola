"""Persistencia de partidas: lectura/escritura de registros binarios.

Descripción:
    Utiliza pickling secuencial para almacenar registros de juego en un
    archivo binario. Proporciona utilidades para crear registros, calcular
    resúmenes y convertir tiradas en marcas sobre las tarjetas.
"""

import pickle
from datetime import datetime
from typing import Any, Dict, List, Set
from src.config import GAMES_FILE
from src.core.card import card_points
from src.core.card_figures import get_card_type, get_figure_pattern, is_figure_complete


def _append_game_record(file_path: str, game: Dict[str, Any]) -> None:
    """
    Añade un registro de juego al final del archivo binario sin sobrescribir
    el contenido existente (modo append).

    Args:
        file_path: Ruta del archivo de partidas.
        game: Diccionario con los datos crudos de la partida.
    """
    with open(file_path, "ab") as file:
        pickle.dump(game, file)


def load_games(file_path: str = str(GAMES_FILE)) -> List[Dict[str, Any]]:
    """
    Carga todos los registros de juego desde el archivo binario leyendo
    secuencialmente objetos pickled hasta EOF.

    Args:
        file_path: Ruta al archivo de partidas.

    Returns:
        List[Dict[str, Any]]: Lista de registros de juego.
    """
    games: List[Dict[str, Any]] = []
    try:
        with open(file_path, "rb") as file:
            # Leer registros pickled secuencialmente hasta EOF.
            eof = False
            while not eof:
                try:
                    record = pickle.load(file)
                except EOFError:
                    eof = True
                else:
                    if isinstance(record, dict):
                        games.append(record)
    except (FileNotFoundError, EOFError, pickle.PickleError):
        return []
    return games


def save_game(file_path: str, game: Dict[str, Any]) -> None:
    """
    Persiste un único registro de juego usando escritura en modo append.

    Args:
        file_path: Ruta al archivo donde guardar.
        game: Registro de juego a persistir.
    """
    _append_game_record(file_path, game)


def save_games(games: List[Dict[str, Any]], file_path: str = str(GAMES_FILE)) -> None:
    """
    Persiste la lista completa de partidas sobrescribiendo el archivo.

    Args:
        games: Lista de registros de juego.
        file_path: Ruta al archivo destino.
    """
    with open(file_path, "wb") as file:
        for game in games:
            pickle.dump(game, file)


def add_game(
    games: List[Dict[str, Any]], game: Dict[str, Any], file_path: str = str(GAMES_FILE)
) -> List[Dict[str, Any]]:
    """
    Añade un nuevo registro de juego a la lista en memoria y lo persiste.

    Args:
        games: Lista en memoria de partidas.
        game: Registro a añadir.
        file_path: Ruta del archivo de persistencia.

    Returns:
        List[Dict[str, Any]]: Lista actualizada de partidas.
    """
    games.append(game)
    save_game(file_path, game)
    return games


def make_game_record(
    player_id: str,
    sdg_id: int,
    dimension: int,
    main_card: List[List[int]],
    complement_card: List[List[int]],
    drawn_numbers: List[int],
) -> Dict[str, Any]:
    """
    Crear un diccionario representando una partida con datos crudos.

    No incluye campos derivados como puntaje o ganador; esos se calculan con
    `calculate_game_summary` cuando se necesiten.

    Args:
        player_id: Identificador del jugador (por ejemplo, cédula).
        sdg_id: Identificador del esquema de juego (tipo de cartón).
        dimension: Dimensión (n) de los cartones (n x n).
        main_card: Matriz que representa el cartón principal.
        complement_card: Matriz que representa el cartón complementario.
        drawn_numbers: Lista de números sorteados en la partida.

    Returns:
        Dict[str, Any]: Registro de partida listo para persistir.
    """
    return {
        "player_id": player_id,
        "played_at": datetime.now(),
        "sdg_id": sdg_id,
        "dimension": dimension,
        "main_card": main_card,
        "complement_card": complement_card,
        "drawn_numbers": drawn_numbers,
    }


def _marks_from_drawn(card: List[List[int]], drawn_numbers: List[int]) -> Set[int]:
    """
    Calcula el conjunto de números de un cartón que han sido sorteados.

    Args:
        card: Matriz del cartón.
        drawn_numbers: Lista de números sorteados.

    Returns:
        Set[int]: Conjunto de valores marcados.
    """
    drawn = set(drawn_numbers)
    return {value for row in card for value in row if value in drawn}


def calculate_game_summary(game: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calcula el resumen de una partida: puntos para cada cartón, puntos totales
    y determina si existe un cartón ganador según el patrón de figura.

    Args:
        game: Registro de partida (ver `make_game_record`).

    Returns:
        Dict[str, Any]: Diccionario con keys: 'main_points', 'complement_points',
        'total_points', 'winning_card'.

    Notas:
        - Se evalúa primero el cartón principal; si completa el patrón, se
          declara ganador. En caso contrario se evalúa el cartón complementario.
        - La función utiliza `get_figure_pattern` para obtener el patrón
          correspondiente al tipo de cartón y `is_figure_complete` para la
          comprobación de completitud.
    """
    main_card = game["main_card"]
    complement_card = game["complement_card"]
    drawn_numbers = game.get("drawn_numbers", [])
    dimension = game.get("dimension", len(main_card))
    card_type = get_card_type(game.get("sdg_id", 1))
    marked_main = _marks_from_drawn(main_card, drawn_numbers)
    marked_complement = _marks_from_drawn(complement_card, drawn_numbers)
    main_points = card_points(main_card, marked_main)
    complement_points = card_points(complement_card, marked_complement)
    main_pattern = get_figure_pattern(card_type, is_main=True, dimension=dimension)
    complement_pattern = get_figure_pattern(
        card_type, is_main=False, dimension=dimension
    )
    if is_figure_complete(main_card, marked_main, main_pattern):
        winning_card = "main"
    elif is_figure_complete(complement_card, marked_complement, complement_pattern):
        winning_card = "complement"
    else:
        winning_card = ""
    return {
        "main_points": main_points,
        "complement_points": complement_points,
        "total_points": main_points + complement_points,
        "winning_card": winning_card,
    }
