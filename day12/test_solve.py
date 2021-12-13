from numpy.lib.function_base import gradient
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

@pytest.fixture
def test3_data():
    with open('test3.txt', 'r') as f:
        text = f.read()
    return text

def test_parse_input(test_data, test2_data, test3_data):
    dp, caves = parse_data(test_data)
    assert len(dp) == 7 * 2
    assert dp[0] == ['start','A']
    assert dp[6] == ['b','end']
    assert dp[2][1] == 'c'
    assert dp[7] == ['A', 'start']
    assert 'd' in caves['b']
    assert len(caves) == 6
    assert len(caves['A']) == 4
    assert len(caves['b']) == 4
    assert not is_big_cave('b')
    assert is_big_cave('A')
    
    dp, caves = parse_data(test2_data)
    assert len(dp) == 10 * 2
    dp, caves = parse_data(test3_data)
    assert len(dp) == 18 * 2
  
def test_all(test_data, test2_data, test3_data):
    paths, caves = parse_data(test_data)
    
    paths, caves = parse_data(test2_data)
    
    paths, caves = parse_data(test3_data)