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
    assert data[0][0][0] == 'be'
    assert len(data) == 10
  
def test_all(test_data):
    data = parse_data('acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf')
    d = create_decoder(data[0][0])
    assert d['abd'] == 7
    assert d['bcdefg'] == 6
    assert d['bcdef'] == 5
    data = parse_data(test_data)
    assert count_all_easy(data) == 26
    s = get_output_sum(data)
    assert s == 61229