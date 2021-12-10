import pytest
import day2

@pytest.fixture
def test1_data():
    with open('test1.txt', 'r') as f:
        text = f.read()
    return text

def test_parse_input(test1_data):
    depth_moves = day2.parse_data(test1_data)
    assert type(depth_moves) == list
    assert depth_moves[0][0] == 'forward'
    assert depth_moves[0][1] == 5
    assert len(depth_moves) == 6

def test_run_moves(test1_data):
    depth_moves = day2.parse_data(test1_data)
    tracker = day2.run_moves(depth_moves)
    assert tracker['position'] == 15
    assert tracker['depth'] == 10
    position, depth = day2.get_tracker_vars(tracker)
    assert position == 15
    assert depth == 10
    
def test_run_moves2(test1_data):
    moves = day2.parse_data(test1_data)
    tracker = day2.run_moves2(moves)
    assert tracker['position'] == 15
    assert tracker['depth'] == 60
    position, depth = day2.get_tracker_vars(tracker)
    assert position == 15
    assert depth == 60

#def test_exec_turns(text_data):
#    depth_moves = day2.parse_input(text_data)
#    tracker = day2.exec_turns(depth_moves)
#    print(tracker)
#    assert tracker['last_num'] == 436