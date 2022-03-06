import pytest
from .solve import *

@pytest.fixture
def test_data():
    with open('test.txt', 'r') as f:
        text = f.read()
    return text

@pytest.fixture
def test2_data():
    with open('test2.txt', 'r') as f:
        text = f.read()
    return text

def test_parse_input(test_data):
    game_state = parse_data(test_data)
    assert type(game_state) == GameState
    assert game_state.B == (11, 15)
    
def test_all(test_data):
    game = parse_data(test_data)
    check = find_path(7,12)
    assert check == [6, 5, 4, 3, 2, 11, 12]
    check = find_path(7,11)
    assert check == [6, 5, 4, 3, 2, 11]
    
    assert in_same_room(3,4) == True
    
    hops = init_available_hops()
    assert 4 not in hops
    assert hops[10][14] == [9,8,7,6,5,4,13,14]
    assert hops[3][14] == [4,13,14]
    cost = find_lowest_cost_solve(game)
    assert cost == 12521
    
from . import solve2

def test_all_2(test2_data):
    game_state = solve2.parse_data(test2_data)
    assert type(game_state) == solve2.GameState
    assert game_state.B == (11, 15, 16, 21)
    
    assert solve2.in_same_room(19,20) == True
    assert solve2.in_same_room(12,20) == True
    
    hops = solve2.init_available_hops()
    cost = solve2.find_lowest_cost_solve(game_state)
    assert cost == 44169