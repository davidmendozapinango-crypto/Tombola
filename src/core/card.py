"""Card generation helpers (non-OOP)."""

import random
from typing import Any, Container, Dict, List, Optional, Sequence, Set, Tuple


def generate_card(
    dimension: int, pattern: Optional[Set[Tuple[int, int]]] = None
) -> List[List[Optional[int]]]:
    """Generate an NxN card.

    If a figure pattern is provided, only those cells receive numbers from the
    range 1..N*N; the rest are left as None. Without a pattern the whole grid is
    filled, preserving backward compatibility for tests and demos.
    """
    grid: List[List[Optional[int]]] = [
        [None for _ in range(dimension)] for _ in range(dimension)
    ]
    numbers = list(range(1, dimension * dimension + 1))
    random.shuffle(numbers)

    if pattern is None:
        index = 0
        for row in range(dimension):
            for col in range(dimension):
                grid[row][col] = numbers[index]
                index += 1
        return grid

    pattern_cells = list(pattern)
    for index, (row, col) in enumerate(pattern_cells):
        if 0 <= row < dimension and 0 <= col < dimension:
            grid[row][col] = numbers[index]
    return grid


def make_cards(
    dimension: int,
    main_pattern: Optional[Set[Tuple[int, int]]] = None,
    complement_pattern: Optional[Set[Tuple[int, int]]] = None,
) -> Dict[str, Any]:
    """Create a main and complement card pair.

    When patterns are supplied, only the figure cells are numbered. Otherwise the
    full grid is filled for compatibility with demos and legacy callers.
    """
    return {
        "main": generate_card(dimension, main_pattern),
        "complement": generate_card(dimension, complement_pattern),
    }


def card_sum(card: Sequence[Sequence[Optional[int]]]) -> int:
    """Return the sum of all numbered cells in a card."""
    total = 0
    for row in card:
        for value in row:
            if value is not None:
                total += value
    return total


def mark_number(
    card: Sequence[Sequence[Optional[int]]], marked: Set[int], number: int
) -> bool:
    """Mark a number on a card if present. Return True if found."""
    found = False
    for row in card:
        if number in row:
            found = True
            break
    if found:
        marked.add(number)
    return found


def is_fully_marked(card: Sequence[Sequence[Optional[int]]], marked: Set[int]) -> bool:
    """Return True when every numbered cell on the card has been marked."""
    for row in card:
        for value in row:
            if value is not None and value not in marked:
                return False
    return True


def card_points(card: Sequence[Sequence[Optional[int]]], marked: Container[int]) -> int:
    """Return the sum of marked numbered cells on a card."""
    total = 0
    for row in card:
        for value in row:
            if value is not None and value in marked:
                total += value
    return total
