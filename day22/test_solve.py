import pytest
from .solve import *

@pytest.fixture
def test_data():
    with open('test.txt', 'r') as f:
        text = f.read()
    return text

@pytest.fixture
def test_data1():
    with open('test1.txt', 'r') as f:
        text = f.read()
    return text

@pytest.fixture
def test_data2():
    with open('test2.txt', 'r') as f:
        text = f.read()
    return text

def test_parse_input(test_data):
    instructions = parse_data(test_data)
    assert type(instructions) == list
  
# def test_all(test_data, test_data1, test_data2):
#     instructions = parse_data(test_data)
#     cube = Cube()
#     assert cube.grid[1,3,5] == 0
#     assert cube.grid.ndim == 3
#     assert cube.grid.shape == (101,101,101)
    
#     instructions = parse_data(test_data1)
#     apply_instruction(instructions[0], cube)
#     assert np.sum(cube.grid == 1) == 27
    
#     apply_instruction(instructions[1], cube)
#     assert np.sum(cube.grid == 1) == 27 + 19

#     apply_instruction(instructions[2], cube)
#     assert np.sum(cube.grid == 1) == 27 + 19 - 8
    
#     instructions = parse_data(test_data)
#     cube = Cube()
#     apply_instructions(instructions, cube)
#     check = count_cubes(cube)
#     assert check == 590784
    
#     instructions = parse_data(test_data2)
#     cube = Cube()
#     apply_instructions(instructions, cube, inside_cube_only=True)
#     check = count_cubes(cube)
#     assert check == 474140
    
#     instructions = parse_data(test_data)
#     df = run(instructions)
#     check = count_dataframe(df)
#     assert check == 590784
    
def test_all_improved(test_data, test_data2):
    instructions = parse_data(test_data)
    cuboids_on, sparse_grid = run(instructions)
    check = count_cuboid_lights(cuboids_on, sparse_grid)
    assert check == 590784
    
    instructions = parse_data(test_data2)
    cuboids_on, sparse_grid = run(instructions)
    check = count_cuboid_lights(cuboids_on, sparse_grid)
    assert check == 474140
    
    cuboids_on, sparse_grid = run(instructions, inside_cube_only=False)
    check = count_cuboid_lights(cuboids_on, sparse_grid)
    assert check == 2758514936282235