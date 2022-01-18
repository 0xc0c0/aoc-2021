from numpy.lib.function_base import gradient
import pytest
from .solve import *

@pytest.fixture
def test_data():
    with open('test.txt', 'r') as f:
        text = f.read()
    return text

def test_parse_input(test_data):
    dots, folds = parse_data(test_data)
    assert dots[0] == [6,10]
    assert len(dots) == 18
    assert folds[0] == ['y', 7]
    assert len(folds) == 2
  
def test_all(test_data):
    dots, folds = parse_data(test_data)
    map = create_dotmap(dots, folds)
    fold_map(map, folds[0])
    assert count_dots(map) == 17
    
    map = create_dotmap(dots, folds)
    map = fold_map_all(map, folds)
    assert count_dots(map) == 16