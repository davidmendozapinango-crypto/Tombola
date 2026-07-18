"""Helpers de persistencia de juegos (I/O binario con append seguro).

Las funciones de este módulo leen y escriben registros de juego serializados
con `pickle`. Las docstrings explican el comportamiento, los parámetros y
proporcionan ejemplos de uso cuando procede.
"""

import pickle
from datetime import datetime
from typing import Any, Dict, List, Set

from src.config import GAMES_FILE
from src.core.card import card_points
from src.core.card_figures import (get_card_type, get_figure_pattern,
                                   is_figure_complete)


def _append_game_record(file_path: str, game: Dict[str, Any]) -> None:
    """
    Añade un único registro de juego al fichero binario sin sobrescribir el
    contenido existente.

    Parámetros
    ----------
    file_path : str
        Ruta al fichero donde se guardan los registros (binario).
    game : Dict[str, Any]
        Diccionario con los campos del juego (por ejemplo, `player_id`,
        `main_card`, `drawn_numbers`, ...).
    """
    with open(file_path, "ab") as file:
        pickle.dump(game, file)


def load_games(file_path: str = str(GAMES_FILE)) -> List[Dict[str, Any]]:
    """
    Carga todos los registros de juego desde el fichero binario.

    Descripción
    ----------
    Lee secuencialmente objetos serializados con `pickle` hasta EOF. Si el
    fichero no existe o ocurre un error de deserialización, devuelve una lista
    vacía para mantener comportamiento tolerante a fallos.

    Devuelve
    -------
    List[Dict[str, Any]]
        Lista de registros de juego cargados desde disco.
    """
    games: List[Dict[str, Any]] = []
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
                        games.append(record)
    except (FileNotFoundError, EOFError, pickle.PickleError):
        return []
    return games


def save_game(file_path: str, game: Dict[str, Any]) -> None:
    """
    Persiste un único registro de juego usando I/O binario en modo append.

    Véase `_append_game_record` para la implementación.
    """
    _append_game_record(file_path, game)


def save_games(games: List[Dict[str, Any]], file_path: str = str(GAMES_FILE)) -> None:
    """
    Persiste la lista completa de juegos sobreescribiendo el fichero (modo
    legacy/antiguo).

    Nota: `save_game` usa append y es más seguro para adiciones incrementales;
    `save_games` sobrescribe el archivo y escribe todos los registros.
    """
    with open(file_path, "wb") as file:
        for game in games:
            pickle.dump(game, file)


def add_game(
    games: List[Dict[str, Any]], game: Dict[str, Any], file_path: str = str(GAMES_FILE)
) -> List[Dict[str, Any]]:
    """
    Añade un nuevo registro de juego a la lista en memoria y lo persiste en
    disco.

    Devuelve la lista actualizada para facilitar encadenamiento en el código
    llamador.
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
    Construye un diccionario con los datos 'raw' de un juego (sin campos
    calculados como puntos o ganador).

    Parámetros
    ----------
    player_id : str
        Identificador del jugador.
    sdg_id : int
        Identificador del tipo de tarjeta (tipo de figura).
    dimension : int
        Dimensión N de las tarjetas.
    main_card, complement_card : List[List[int]]
        Matrices con los números de cada tarjeta.
    drawn_numbers : List[int]
        Secuencia de números extraídos durante el juego.

    Devuelve
    -------
    Dict[str, Any]
        Diccionario con la estructura mínima para persistir el juego.
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
    Calcula el conjunto de números marcados en una tarjeta a partir de los
    números extraídos.

    Devuelve un `set` con los valores de la tarjeta que coinciden con los
    números extraídos.
    """
    drawn = set(drawn_numbers)
    return {value for row in card for value in row if value in drawn}


def calculate_game_summary(game: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calcula el resumen de un juego: puntos por tarjeta, puntos totales y
    tarjeta ganadora si existe.

    Descripción
    ----------
    - Calcula los números marcados en cada tarjeta.
    - Suma puntos usando `card_points`.
    - Determina si alguna figura está completa (ganadora) consultando
      `is_figure_complete` usando los patrones correspondientes.

    Devuelve
    -------
    Dict[str, Any]
        Diccionario con claves: `main_points`, `complement_points`,
        `total_points`, `winning_card` ("main", "complement" o "").
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
