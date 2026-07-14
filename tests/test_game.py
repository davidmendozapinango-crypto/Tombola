"""Tests for game logic and SDG figure winner detection."""

from src.core.card import generate_card
from src.core.game import (
    check_winner,
    draw_next,
    game_summary,
    make_number_pool,
)


def test_make_number_pool_has_all_numbers():
    dimension = 5
    pool = make_number_pool(dimension)
    assert len(pool) == dimension * dimension
    assert set(pool) == set(range(1, dimension * dimension + 1))


def test_draw_next_returns_unique_numbers():
    pool = make_number_pool(5)
    drawn = {draw_next(pool) for _ in range(10)}
    assert len(drawn) == 10
    assert all(number is not None for number in drawn)


def test_draw_next_returns_none_when_empty():
    pool = []
    assert draw_next(pool) is None


def test_check_winner_detects_main_figure_completion():
    # ODS 1 -> type A main figure is a diamond over 5x5
    main_card = generate_card(5)
    complement_card = generate_card(5)
    marked_main = {
        main_card[row][col]
        for row, col in [
            (0, 0),
            (0, 1),
            (0, 2),
            (0, 3),
            (0, 4),
            (1, 1),
            (1, 2),
            (1, 3),
            (2, 2),
            (3, 1),
            (3, 2),
            (3, 3),
            (4, 0),
            (4, 1),
            (4, 2),
            (4, 3),
            (4, 4),
        ]
    }
    winner = check_winner(main_card, marked_main, complement_card, set(), "A")
    assert winner == "main"


def test_check_winner_detects_complement_figure_completion():
    main_card = generate_card(5)
    complement_card = generate_card(5)
    marked_complement = {
        complement_card[row][col]
        for row, col in [
            (0, 0),
            (0, 4),
            (1, 1),
            (1, 3),
            (2, 2),
            (3, 1),
            (3, 3),
            (4, 0),
            (4, 4),
        ]
    }
    winner = check_winner(main_card, set(), complement_card, marked_complement, "A")
    assert winner == "complement"


def test_check_winner_no_winner():
    main_card = generate_card(5)
    complement_card = generate_card(5)
    winner = check_winner(main_card, set(), complement_card, set(), "A")
    assert winner is None


def test_game_summary_contains_points():
    main_card = generate_card(5)
    complement_card = generate_card(5)
    summary = game_summary(main_card, set(), complement_card, set(), "A")
    assert "main_points" in summary
    assert "complement_points" in summary
    assert summary["winner"] is None


def test_figure_scaling_for_larger_dimensions():
    dimension = 7
    main_card = generate_card(dimension)
    complement_card = generate_card(dimension)
    # Completing the full main card should definitely complete the scaled figure
    marked_main = {
        main_card[row][col] for row in range(dimension) for col in range(dimension)
    }
    winner = check_winner(main_card, marked_main, complement_card, set(), "A")
    assert winner == "main"
