import pytest
from .solve import *

@pytest.fixture
def test_data():
    with open('test.txt', 'r') as f:
        text = f.read()
    return text

def test_parse_input(test_data):
    snailnums = parse_data(test_data)
    assert type(snailnums) == list
    assert snailnums[0][0][0][1][0] == 5
    assert snailnums[2][0] == 6
    assert snailnums[5][1][0][1][1] == 7

def test_builds():
    test1 = [[[[4,3],4],4],[7,[[8,4],9]]]
    n = build_tree_from_list(test1)
    l = build_list_from_tree(n)
    assert l == test1
  
def test_add():
    test1 = [[1,1],[2,2],[3,3],[4,4]]
    n = add_all(test1)
    check = build_list_from_tree(n)
    assert check == [[[[1,1],[2,2]],[3,3]],[4,4]]
    
    test2 = [[1,1],[2,2],[3,3],[4,4],[5,5]]
    n = add_all(test2)
    check = build_list_from_tree(n)
    assert check == [[[[3,0],[5,3]],[4,4]],[5,5]]
    
    test3 = [[1,1],[2,2],[3,3],[4,4],[5,5],[6,6]]
    n = add_all(test3)
    check = build_list_from_tree(n)
    assert check == [[[[5,0],[7,4]],[5,5]],[6,6]]

def test_magnitude():
    test1 = [[1,2],[[3,4],5]]
    n = build_tree_from_list(test1)
    assert magnitude(n) == 143
  
def test_all(test_data):
    snailnums = parse_data(test_data)
    sum = add_all(snailnums)
    assert magnitude(sum) == 4140
    
    high = get_largest_magnitude_pair(snailnums)
    assert high == 3993