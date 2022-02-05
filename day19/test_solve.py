import pytest
from .solve import *

@pytest.fixture
def test_data():
    with open('test.txt', 'r') as f:
        text = f.read()
    return text

def test_parse_input(test_data):
    scans = parse_data(test_data)
    assert len(scans) == 127
    assert scans.loc[2,0][0] == 649
    assert scans.loc[4,2][2] == -461
  
def test_all(test_data):
    scans = parse_data(test_data)
    dists_sq = get_scanned_beacon_distances(scans)
    test_01 = (404-528) ** 2 + (643-588) ** 2 + (901+409) ** 2
    assert (dists_sq.loc[0,0,1] == test_01).all()
    
    total, i = get_max_overlapping_beacons(dists_sq)