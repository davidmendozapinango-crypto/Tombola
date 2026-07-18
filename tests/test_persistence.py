"""Tests for binary persistence append behavior and calculated fields."""
from datetime import datetime

from src.persistence.games import (add_game, calculate_game_summary,
                                   load_games, make_game_record, save_game)
from src.persistence.players import add_player, load_players, save_player


def test_player_append_does_not_overwrite_existing(tmp_path):
    file_path = str(tmp_path / 'JUGADORES.bin')
    first = {'player_id': '111', 'full_name': 'Primero', 'gender': 'm', 'birthdate': '2000-01-01', 'state_code': 'CCS', 'access_key': 'Hola1=', 'registered_at': datetime.now()}
    second = {'player_id': '222', 'full_name': 'Segundo', 'gender': 'f', 'birthdate': '2001-02-02', 'state_code': 'BOL', 'access_key': 'Mundo2=', 'registered_at': datetime.now()}
    save_player(file_path, first)
    save_player(file_path, second)
    players = load_players(file_path)
    assert len(players) == 2
    assert players[0]['player_id'] == '111'
    assert players[1]['player_id'] == '222'

def test_add_player_appends_to_file(tmp_path):
    file_path = str(tmp_path / 'JUGADORES.bin')
    players = []
    player = {'player_id': '333', 'full_name': 'Tercero', 'gender': 'm', 'birthdate': '2002-03-03', 'state_code': 'ZUL', 'access_key': 'Test3=', 'registered_at': datetime.now()}
    add_player(players, player, file_path=file_path)
    add_player(players, player.copy(), file_path=file_path)
    loaded = load_players(file_path)
    assert len(loaded) == 2

def test_game_append_does_not_overwrite_existing(tmp_path):
    file_path = str(tmp_path / 'JUEGOS.bin')
    main_card = [[1, 2], [3, 4]]
    complement_card = [[5, 6], [7, 8]]
    first = make_game_record(player_id='p1', sdg_id=1, dimension=2, main_card=main_card, complement_card=complement_card, drawn_numbers=[1, 2, 3, 4])
    second = make_game_record(player_id='p2', sdg_id=2, dimension=2, main_card=main_card, complement_card=complement_card, drawn_numbers=[5, 6, 7, 8])
    save_game(file_path, first)
    save_game(file_path, second)
    games = load_games(file_path)
    assert len(games) == 2
    assert games[0]['player_id'] == 'p1'
    assert games[1]['player_id'] == 'p2'

def test_game_record_does_not_store_calculated_fields():
    record = make_game_record(player_id='p1', sdg_id=1, dimension=2, main_card=[[1, 2], [3, 4]], complement_card=[[5, 6], [7, 8]], drawn_numbers=[1, 2, 3, 4])
    assert 'main_points' not in record
    assert 'complement_points' not in record
    assert 'winning_card' not in record

def test_calculate_game_summary_from_raw_record():
    main_card = [[1, 2], [3, 4]]
    complement_card = [[5, 6], [7, 8]]
    record = make_game_record(player_id='p1', sdg_id=1, dimension=2, main_card=main_card, complement_card=complement_card, drawn_numbers=[1, 2, 3, 4])
    summary = calculate_game_summary(record)
    assert summary['main_points'] == 10
    assert summary['complement_points'] == 0
    assert summary['winning_card'] == 'main'
    assert summary['total_points'] == 10

def test_calculate_game_summary_no_winner():
    main_card = [[1, 2], [3, 4]]
    complement_card = [[5, 6], [7, 8]]
    record = make_game_record(player_id='p1', sdg_id=1, dimension=2, main_card=main_card, complement_card=complement_card, drawn_numbers=[1, 5])
    summary = calculate_game_summary(record)
    assert summary['winning_card'] == ''
    assert summary['main_points'] == 1
    assert summary['complement_points'] == 5