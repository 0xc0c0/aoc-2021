import pytest
from .solve import *

@pytest.fixture
def test_data():
    with open('test.txt', 'r') as f:
        text = f.read()
    return text

def test_parse_input(test_data):
    bounds = parse_data(test_data)
    assert type(bounds) == dict
    assert type(bounds['x']) == tuple
    assert type(bounds['y']) == tuple
    assert bounds['x'][0] == min(bounds['x'])
    assert bounds['x'][0] == 20
    assert bounds['y'][1] == -5
    assert bounds['y'][1] == max(bounds['y'])
  
def test_all(test_data):
    bounds = parse_data(test_data)
    dx, dy = get_max_y_test_vector_ranges(bounds)
    max_y = run_test(dx, dy, bounds)
    assert max_y == 45
    
    count = count_valid_vectors(bounds)
    assert count == 112