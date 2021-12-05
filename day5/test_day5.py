import pytest
from day5.day5 import *

@pytest.fixture
def test1_data():
    with open('test1.txt', 'r') as f:
        text = f.read()
    return text

def test_parse_input(test1_data):
    drawing, boards = parse_data(test1_data)
    assert drawing[0] == 7
    assert boards[0]['nums'][0,0] == 22
    assert boards[1]['nums'][2,1] == 8
    assert boards[2]['nums'][2,4] == 20
    assert boards[1]['marks'][3,3] == False
    assert boards[1]['marks'][3,4] == 0

def test_all(test1_data):
    drawing, boards = parse_data(test1_data)
    winners = run_rounds(boards, drawing)
    assert winners[0][2] == 4512
    assert winners[-1][2] == 1924