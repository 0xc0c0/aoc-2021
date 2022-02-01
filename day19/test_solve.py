import pytest
from .solve import *

@pytest.fixture
def test_data():
    with open('test.txt', 'r') as f:
        text = f.read()
    return text

def test_parse_input(test_data):
    scanner_data = parse_data(test_data)
    assert len(scanner_data) == 5
    assert scanner_data[2][0][0] == 649
    assert scanner_data[4][2][2] == -461
  
def test_all(test_data):
    scanner_data = parse_data(test_data)
