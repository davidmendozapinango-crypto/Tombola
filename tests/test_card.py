"""Tests for card generation and marking helpers."""

from src.core.card import (
    card_points,
    card_sum,
    generate_card,
    is_fully_marked,
    make_cards,
    mark_number,
)


def test_generate_card_has_correct_dimension():
    dimension = 7
    card = generate_card(dimension)
    assert len(card) == dimension
    assert all(len(row) == dimension for row in card)


def test_generate_card_contains_unique_numbers():
    dimension = 5
    card = generate_card(dimension)
    values = [value for row in card for value in row]
    assert len(values) == dimension * dimension
    assert len(set(values)) == len(values)
    assert all(1 <= value <= dimension * dimension for value in values)


def test_make_cards_returns_main_and_complement():
    cards = make_cards(5)
    assert "main" in cards
    assert "complement" in cards
    assert cards["main"] != cards["complement"]


def test_mark_number_detects_present_value():
    card = [[1, 2], [3, 4]]
    marked = set()
    found = mark_number(card, marked, 3)
    assert found is True
    assert 3 in marked


def test_mark_number_ignores_missing_value():
    card = [[1, 2], [3, 4]]
    marked = set()
    found = mark_number(card, marked, 99)
    assert found is False
    assert 99 not in marked


def test_is_fully_marked_true_when_all_cells_marked():
    card = [[1, 2], [3, 4]]
    marked = {1, 2, 3, 4}
    assert is_fully_marked(card, marked) is True


def test_is_fully_marked_false_when_missing_cells():
    card = [[1, 2], [3, 4]]
    marked = {1, 2, 3}
    assert is_fully_marked(card, marked) is False


def test_card_points_sums_marked_cells():
    card = [[1, 2], [3, 4]]
    marked = {1, 4}
    assert card_points(card, marked) == 5


def test_card_sum_sums_all_cells():
    card = [[1, 2], [3, 4]]
    assert card_sum(card) == 10
