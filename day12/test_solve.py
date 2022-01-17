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
    caves = parse_data(test_data)
    assert 'd' in caves['b']
    assert len(caves) == 6
    assert len(caves['A']) == 4
    assert len(caves['b']) == 4
    assert not is_big_cave('b')
    assert is_big_cave('A')
  
def test_all(test_data, test2_data, test3_data):
    caves = parse_data(test_data)
    paths = get_all_paths(list(), 'start', 'end', caves)
    assert len(paths) == 10
    
    caves = parse_data(test2_data)
    paths = get_all_paths(list(), 'start', 'end', caves)
    assert len(paths) == 19
    
    caves = parse_data(test3_data)
    paths = get_all_paths(list(), 'start', 'end', caves)
    assert len(paths) == 226
    
    caves = parse_data(test_data)
    paths = get_all_paths(list(), 'start', 'end', caves, False)
    assert len(paths) == 36
    
    caves = parse_data(test2_data)
    paths = get_all_paths(list(), 'start', 'end', caves, False)
    assert len(paths) == 103
    
    caves = parse_data(test3_data)
    paths = get_all_paths(list(), 'start', 'end', caves, False)
    assert len(paths) == 3509