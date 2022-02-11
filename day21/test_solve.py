import pytest
from .solve import *

@pytest.fixture
def test_data():
    with open('test.txt', 'r') as f:
        text = f.read()
    return text

def test_parse_input(test_data):
    p1, p2 = parse_data(test_data)
    assert p1 == 3
    assert p2 == 7
  
def test_all(test_data):
    p1, p2 = parse_data(test_data)
    score, p1, dice = turn(p1, dice_state=-1)
    assert score == 10
    assert p1 == 9
    assert dice == 2
    
    
    
    p1, p2 = parse_data(test_data)
    winner, loser, rolls = run_game(p1, p2)
    assert winner >= 1000
    assert loser == 745
    assert rolls == 993

    # p1_wins, p2_wins = run_quantum_game(p1, 20, p2, 0)
    # assert p1_wins == 444356092776315
    # assert p2_wins == 341960390180808

    p1_wins, p2_wins = run_quantum_game(p1, 0, p2, 0)
    assert p1_wins == 444356092776315
    assert p2_wins == 341960390180808