import pytest
from .solve import *

@pytest.fixture
def test_data():
    with open('test.txt', 'r') as f:
        text = f.read()
    return text

def test_parse_input(test_data):
    data = parse_data(test_data)
    assert type(data) == list
    assert data[1][2] == '('
    assert len(data) == 10
  
def test_all(test_data):
    lines = parse_data(test_data)
    score, incomplete_lines = compute_illegal_chars(lines) 
    assert score == 26397
    assert get_completion_score(incomplete_lines) == 288957