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
    assert data[1] == 1
    assert len(data) == 10
  
def test_all(test_data):
    data = parse_data(test_data)
    