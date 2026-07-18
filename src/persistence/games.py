"""Game persistence helpers (non-OOP) using binary append-safe records."""
import pickle
from datetime import datetime
from typing import Any, Dict, List, Set
from src.config import GAMES_FILE
from src.core.card import card_points
from src.core.card_figures import get_card_type, get_figure_pattern, is_figure_complete

def _append_game_record(file_path: str, game: Dict[str, Any]) -> None:
    """Append a single game record to the binary file without overwriting."""
    with open(file_path, 'ab') as file:
        pickle.dump(game, file)

def load_games(file_path: str=str(GAMES_FILE)) -> List[Dict[str, Any]]:
    """Load all game records from the binary file using sequential reads."""
    games: List[Dict[str, Any]] = []
    try:
        with open(file_path, 'rb') as file:
            while True:
                try:
                    record = pickle.load(file)
                except EOFError:
                    break
                if isinstance(record, dict):
                    games.append(record)
    except (FileNotFoundError, EOFError, pickle.PickleError):
        return []
    return games

def save_game(file_path: str, game: Dict[str, Any]) -> None:
    """Persist a single game record using append-safe binary I/O."""
    _append_game_record(file_path, game)

def save_games(games: List[Dict[str, Any]], file_path: str=str(GAMES_FILE)) -> None:
    """Persist the game history to the binary file (legacy bulk overwrite)."""
    with open(file_path, 'wb') as file:
        for game in games:
            pickle.dump(game, file)

def add_game(games: List[Dict[str, Any]], game: Dict[str, Any], file_path: str=str(GAMES_FILE)) -> List[Dict[str, Any]]:
    """Append a new game record and return the updated in-memory list."""
    games.append(game)
    save_game(file_path, game)
    return games

def make_game_record(player_id: str, sdg_id: int, dimension: int, main_card: List[List[int]], complement_card: List[List[int]], drawn_numbers: List[int]) -> Dict[str, Any]:
    """Create a game record dictionary with only raw data (no calculated fields)."""
    return {'player_id': player_id, 'played_at': datetime.now(), 'sdg_id': sdg_id, 'dimension': dimension, 'main_card': main_card, 'complement_card': complement_card, 'drawn_numbers': drawn_numbers}

def _marks_from_drawn(card: List[List[int]], drawn_numbers: List[int]) -> Set[int]:
    """Return the set of marked numbers on a card given the drawn numbers."""
    drawn = set(drawn_numbers)
    return {value for row in card for value in row if value in drawn}

def calculate_game_summary(game: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate points and winner from a raw game record."""
    main_card = game['main_card']
    complement_card = game['complement_card']
    drawn_numbers = game.get('drawn_numbers', [])
    dimension = game.get('dimension', len(main_card))
    card_type = get_card_type(game.get('sdg_id', 1))
    marked_main = _marks_from_drawn(main_card, drawn_numbers)
    marked_complement = _marks_from_drawn(complement_card, drawn_numbers)
    main_points = card_points(main_card, marked_main)
    complement_points = card_points(complement_card, marked_complement)
    main_pattern = get_figure_pattern(card_type, is_main=True, dimension=dimension)
    complement_pattern = get_figure_pattern(card_type, is_main=False, dimension=dimension)
    if is_figure_complete(main_card, marked_main, main_pattern):
        winning_card = 'main'
    elif is_figure_complete(complement_card, marked_complement, complement_pattern):
        winning_card = 'complement'
    else:
        winning_card = ''
    return {'main_points': main_points, 'complement_points': complement_points, 'total_points': main_points + complement_points, 'winning_card': winning_card}