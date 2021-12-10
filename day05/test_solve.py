import pytest
from .solve import *

@pytest.fixture
def test1_data():
    with open('test.txt', 'r') as f:
        text = f.read()
    return text

def test_parse_input(test1_data):
    text_line = '0,9 -> 5,9'
    entry = parse_line(text_line)
    assert entry == ((0,9),(5,9))
    
    lines = parse_data(test1_data)
    assert type(lines) == list
    assert lines[0] == ((0,9),(5,9))
    assert lines[1] == ((8,0),(0,8))
    assert len(lines) == 10
    
def test_all(test1_data):
    lines = parse_data(test1_data)
    x,y = find_matrix_dims(lines)
    assert x == 10
    assert y == 10
    vents = create_matrix(*(find_matrix_dims(lines)))
    vents = update_matrix(vents, lines)
    more_than_2 = len(find_overlaps(vents))
    assert more_than_2 == 5
    
    vents = create_matrix(*(find_matrix_dims(lines)))
    vents = update_matrix(vents, lines, diag=True)
    more_than_2 = len(find_overlaps(vents))
    assert more_than_2 == 12