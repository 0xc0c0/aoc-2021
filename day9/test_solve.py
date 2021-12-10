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
    assert data[1][2] == 8
    assert len(data) == 5
    assert len(data[2]) == 10
  
def test_all(test_data):
    heightmap = parse_data(test_data)
    points = find_low_points(heightmap)
    assert get_risk_level(heightmap, points) == 15
    assert get_top_basin_sizes(heightmap, points) == 1134