import pytest
from .solve import *

@pytest.fixture
def test_data():
    with open('test.txt', 'r') as f:
        text = f.read()
    return text

@pytest.fixture
def test1_data():
    with open('test1.txt', 'r') as f:
        text = f.read()
    return text

def test_parse_input(test_data, test1_data):
    enhancement, lights = parse_data(test_data)
    assert type(lights) == np.ndarray
    assert lights[1,3] == 0
    assert lights[2,1] == 1
    assert lights[4,4] == 1
    assert lights.ndim == 2
    assert lights.shape == (5,5)
    assert count_lights(lights) == 10
    
    lights = init_image(test1_data)
    assert count_lights(lights) == 35
  
def test_all(test_data):
    enhancement, lights = parse_data(test_data)
    assert get_binary(lights, 2, 2) == 34

    lights, _ = run_enhancement(enhancement, lights)
    assert lights[4,4] == 1
    check = count_lights(lights)
    assert check == 24
    
    enhancement, lights = parse_data(test_data)
    lights = run(enhancement, lights)
    check = count_lights(lights)
    assert check == 35
    
    enhancement, lights = parse_data(test_data)
    lights = run(enhancement, lights, count=50)
    check = count_lights(lights)
    assert check == 3351