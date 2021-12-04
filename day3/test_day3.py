import pytest
from day3.day3 import *

@pytest.fixture
def test1_data():
    with open('test1.txt', 'r') as f:
        text = f.read()
    return text

def test_parse_input(test1_data):
    codes, code_len = parse_data(test1_data)
    assert type(codes) == list
    assert codes[0] == 4
    assert codes[11] == 10
    assert len(codes) == 12
    assert code_len == 5

def test_all(test1_data):
    diagnostics, code_len = parse_data(test1_data)
    gr = get_gamma_rate(diagnostics, code_len)
    assert gr == 22
    er = get_epsilon_rate(gr, code_len)
    assert er == 9
    ogr = get_ox_gen_rating(diagnostics, code_length=code_len)
    assert ogr == 23
    co2r = get_co2_scrubber_rating(diagnostics, code_length=code_len)
    assert co2r == 10