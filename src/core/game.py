"""Tombola gameplay helpers (non-OOP)."""
import random
from typing import Any, Container, Dict, List, Optional, Sequence, Set
from src.core.card import card_points
from src.core.card_figures import get_figure_pattern, is_figure_complete

def make_number_pool(dimension: int, numbers: Optional[Set[int]]=None) -> List[int]:
    """Create a shuffled pool of numbers.

    If a set of numbers is supplied, only those values are included; otherwise
    the full range 1..N*N is used.
    """
    if numbers is None:
        pool = list(range(1, dimension * dimension + 1))
    else:
        pool = list(numbers)
    random.shuffle(pool)
    return pool

def draw_next(pool: List[int]) -> Optional[int]:
    """Draw and return the next number from the pool, or None if empty."""
    if not pool:
        return None
    return pool.pop()

def check_winner(main_card: Sequence[Sequence[Optional[int]]], marked_main: Container[int], complement_card: Sequence[Sequence[Optional[int]]], marked_complement: Container[int], card_type: str) -> Optional[str]:
    """Return 'main' or 'complement' if the SDG figure is complete."""
    dimension = len(main_card)
    main_pattern = get_figure_pattern(card_type, is_main=True, dimension=dimension)
    complement_pattern = get_figure_pattern(card_type, is_main=False, dimension=dimension)
    if is_figure_complete(main_card, marked_main, main_pattern):
        return 'main'
    if is_figure_complete(complement_card, marked_complement, complement_pattern):
        return 'complement'
    return None

def game_summary(main_card: Sequence[Sequence[Optional[int]]], marked_main: Container[int], complement_card: Sequence[Sequence[Optional[int]]], marked_complement: Container[int], card_type: str) -> Dict[str, Any]:
    """Return a summary of current game state."""
    winner = check_winner(main_card, marked_main, complement_card, marked_complement, card_type)
    main_points = card_points(main_card, marked_main)
    complement_points = card_points(complement_card, marked_complement)
    return {'winner': winner, 'main_points': main_points, 'complement_points': complement_points}