from numpy.lib.function_base import gradient
import pytest
from .solve import *

@pytest.fixture
def test_data():
    with open('test.txt', 'r') as f:
        text = f.read()
    return text

def test_parse_input(test_data):
    snailnums = parse_data(test_data)
    assert type(snailnums) == list
    assert snailnums[0][0][0][1][0] == 5
    assert snailnums[2][0] == 6
    assert snailnums[5][1][0][1][1] == 7
  
def test_all(test_data):
    snailnums = parse_data(test_data)
    i1, i2, i3, i4, found = find_leftmost_deep_recursive(snailnums)
    assert found == [5,8]
    assert snailnums[i1][i2][i3][i4] == found