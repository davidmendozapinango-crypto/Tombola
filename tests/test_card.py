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
    values = [value for row in card for value in row if value is not None]
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


def test_generate_card_with_pattern_only_fills_pattern_cells():
    pattern = {(0, 0), (0, 1), (1, 0)}
    card = generate_card(3, pattern)
    assert card[0][0] is not None
    assert card[0][1] is not None
    assert card[1][0] is not None
    assert card[0][2] is None
    assert card[1][1] is None
    assert card[1][2] is None
    assert card[2][0] is None


def test_generate_card_with_pattern_uses_unique_numbers():
    dimension = 5
    pattern = {(0, 0), (0, 1), (1, 1), (2, 2)}
    card = generate_card(dimension, pattern)
    values = [value for row in card for value in row if value is not None]
    assert len(values) == len(pattern)
    assert len(set(values)) == len(values)
    assert all(1 <= value <= dimension * dimension for value in values)


def test_make_cards_with_patterns_returns_figure_cards():
    main_pattern = {(0, 0), (1, 1)}
    complement_pattern = {(0, 1), (1, 0)}
    cards = make_cards(3, main_pattern, complement_pattern)
    main_values = [v for row in cards["main"] for v in row if v is not None]
    complement_values = [v for row in cards["complement"] for v in row if v is not None]
    assert len(main_values) == len(main_pattern)
    assert len(complement_values) == len(complement_pattern)
    assert cards["main"] != cards["complement"]


def test_card_sum_ignores_empty_cells():
    card = [[1, None], [None, 4]]
    assert card_sum(card) == 5


def test_card_points_ignores_empty_cells():
    card = [[1, None], [None, 4]]
    marked = {1, 4}
    assert card_points(card, marked) == 5


def test_is_fully_marked_ignores_empty_cells():
    card = [[1, None], [None, 4]]
    marked = {1, 4}
    assert is_fully_marked(card, marked) is True


def test_mark_number_ignores_empty_cells():
    card = [[1, None], [None, 4]]
    marked = set()
    found = mark_number(card, marked, 99)
    assert found is False
