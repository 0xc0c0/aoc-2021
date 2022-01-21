from numpy.lib.function_base import gradient
import pytest
from .solve import *

@pytest.fixture
def test_data():
    with open('test.txt', 'r') as f:
        text = f.read()
    return text

def test_parse_input(test_data):
    polymer, rules = parse_data(test_data)
    assert len(rules) == 4
    assert rules['N']['N'] == 'C'
  
def test_all(test_data):
    chain, rules = parse_data(test_data)
    chain = run_rounds(chain, rules, 10)
    check = get_high_low_computation(chain)
    assert check == 1588
    
    chain, rules = parse_data_better(test_data)
    polymers = run_rounds_better(rules=rules, rounds=40, template=chain)
    check = get_high_low_computation(counts=polymers)
    assert check == 2188189693529