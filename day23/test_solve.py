import pytest
from .solve import *

@pytest.fixture
def test_data():
    with open('test.txt', 'r') as f:
        text = f.read()
    return text

def test_parse_input(test_data):
    locations = parse_data(test_data)
    assert type(locations) == tuple
    assert locations[11] == 'B'
    assert locations[18] == 'A'
    assert locations.count('A') == 2
    assert locations.count('B') == 2
    assert locations.count('C') == 2
    assert locations.count('D') == 2
    
def test_all(test_data):
    locations = parse_data(test_data)
    moves = find_good_available_moves(locations)
    assert not moves['A']
    assert len(moves['C']) == 1
    assert len(moves['B']) == 2
    assert moves['B'].count((11,2)) == 1
    assert moves['B'].count((15,6)) == 1
    assert len([moves[k] for k in moves]) == 4
    
    check = find_lowest_cost_solve(locations)
    assert check == 12521