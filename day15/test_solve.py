import pytest
from .solve import *
import numpy as np

@pytest.fixture
def test_data():
    with open('test.txt', 'r') as f:
        text = f.read()
    return text

@pytest.fixture
def full_map():
    with open('full_map.txt', 'r') as f:
        text = f.read()
    return text

def test_parse_input(test_data):
    grid = parse_data(test_data)
    assert type(grid) == np.ndarray
    assert grid[1,3] == 1
    assert grid.ndim == 2
    assert grid.shape == (10,10)
  
def test_all(test_data, full_map):
    chitons = parse_data(test_data)
    check = find_lowest_risk(chitons)
    assert check == 40
    
    full = make_full_map(chitons)
    full_check = parse_data(full_map)
    assert type(full) == np.ndarray
    assert type(full_check) == np.ndarray
    assert compare_maps(full, full_check)
    check = find_lowest_risk(full)
    assert check == 315