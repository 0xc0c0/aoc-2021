from numpy.lib.function_base import gradient
import pytest
from .solve import *

@pytest.fixture
def test_data():
    with open('test.txt', 'r') as f:
        text = f.read()
    return text

def test_parse_input(test_data):
    grid = parse_data(test_data)
    assert type(grid) == np.ndarray
    assert grid[1,3] == 5
    assert grid.ndim == 2
    assert grid.shape == (10,10)
  
def test_all(test_data):
    grid = parse_data(test_data)
    assert run_oct_steps(grid, 1) == 0
    grid = parse_data(test_data)
    assert run_oct_steps(grid, 2) == 35
    grid = parse_data(test_data)
    assert run_oct_steps(grid, 10) == 204
    grid = parse_data(test_data)
    assert run_oct_steps(grid, 100) == 1656
    
    grid = parse_data(test_data)
    assert find_next_all_flash(grid) == 195