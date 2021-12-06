import pytest
from .solve import *

@pytest.fixture
def test_data():
    with open('test.txt', 'r') as f:
        text = f.read()
    return text

def test_parse_input(test_data):
    fish = parse_data(test_data)
    assert fish == [3,4,3,1,2]
  
def test_all(test_data):
    fish = parse_data(test_data)
    f = fish.copy()
    age_fish(f)
    assert f == [2,3,2,0,1]
    f = fish.copy()
    age_rounds(f, rounds=18)
    assert len(f) == 26
    f = fish.copy()
    age_rounds(f, rounds=80)
    assert len(f) == 5934
    
    #Computationally too expensive
    #f = fish.copy()
    #age_rounds(f, rounds=256)
    #assert len(f) == 26984457539
    
def test_all_better(test_data):
    tallies = parse_data_better(test_data)
    t = tallies.copy()
    age_fish_better(t)
    assert t == [1,1,2,1,0,0,0,0,0]
    t = tallies.copy()
    age_rounds_better(t, rounds=18)
    assert sum(t) == 26
    t = tallies.copy()
    age_rounds_better(t, rounds=80)
    assert sum(t) == 5934
    t = tallies.copy()
    age_rounds_better(t, rounds=256)
    assert sum(t) == 26984457539