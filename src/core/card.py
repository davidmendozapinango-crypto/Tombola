"""Card generation helpers (non-OOP)."""

import random
from typing import Any, Dict, List, Set


def generate_card(dimension: int) -> List[List[int]]:
    """Generate an NxN card with unique random numbers from 1 to N*N."""
    numbers = list(range(1, dimension * dimension + 1))
    random.shuffle(numbers)
    card = []
    index = 0
    for _ in range(dimension):
        row = []
        for _ in range(dimension):
            row.append(numbers[index])
            index += 1
        card.append(row)
    return card


def make_cards(dimension: int) -> Dict[str, Any]:
    """Create a main and complement card pair."""
    return {
        "main": generate_card(dimension),
        "complement": generate_card(dimension),
    }


def card_sum(card: List[List[int]]) -> int:
    """Return the sum of all cells in a card."""
    total = 0
    for row in card:
        for value in row:
            total += value
    return total


def mark_number(card: List[List[int]], marked: Set[int], number: int) -> bool:
    """Mark a number on a card if present. Return True if found."""
    found = False
    for row in card:
        if number in row:
            found = True
            break
    if found:
        marked.add(number)
    return found


def is_fully_marked(card: List[List[int]], marked: Set[int]) -> bool:
    """Return True when every number on the card has been marked."""
    for row in card:
        for value in row:
            if value not in marked:
                return False
    return True


def card_points(card: List[List[int]], marked: Set[int]) -> int:
    """Return the sum of marked cells on a card."""
    total = 0
    for row in card:
        for value in row:
            if value in marked:
                total += value
    return total
