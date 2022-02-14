from dataclasses import dataclass
import logging
import os
import sys
from typing import final
import numpy as np
import pandas as pd

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

def get_file_data(fn='input.txt'):
    with open(fn) as f:
        data = f.read()
    return data

@dataclass
class Instruction:
    on: np.int8
    ranges: dict

def parse_data(text_data):
    lines = [line for line in text_data.strip('\n').strip().split('\n')]
    instructions = list()
    for line in lines:
        text_dir, text_box = line.strip().split(' ')
        dir = 1 if text_dir == 'on' else 0
        ranges = dict()
        for text_instr in text_box.strip().split(','):
            axis, text_coord_range = text_instr.strip().split('=')
            r = [int(x) for x in text_coord_range.split('..')]
            ranges[axis] = (min(r), max(r))
        instr = Instruction(dir, ranges)
        instructions.append(instr)
    
    return instructions

class Cube:
    offset = 0
    grid = None
    
    def __init__(self, offset=50, size=101):
        self.offset = offset
        self.grid = np.zeros((size, size, size), dtype=np.int8)
    
def apply_instruction(instr, cube):
    logger.debug(f"applying instruction: {instr}")
    x0, x1 = instr.ranges['x']
    y0, y1 = instr.ranges['y']
    z0, z1 = instr.ranges['z']
    
    x0 += cube.offset
    x1 += cube.offset
    y0 += cube.offset
    y1 += cube.offset
    z0 += cube.offset
    z1 += cube.offset
    
    for (x,y,z), value in np.ndenumerate(cube.grid):
        if x >= x0 and x <= x1 and y >= y0 and y <= y1 and z >= z0 and z <= z1:
            cube.grid[x,y,z] = instr.on

def apply_instructions(instructions, cube, inside_cube_only=True):
    for instr in instructions:
        keep_going = True
        if inside_cube_only:
            for axis in instr.ranges:
                r = instr.ranges[axis]
                logger.debug(f"axis: {axis}, r: {r}")
                if r[0] + cube.offset < 0 or r[1] + cube.offset >= cube.grid.shape[0]:
                    keep_going = False
                    break
        if keep_going == False:
            break

        apply_instruction(instr, cube)
    
def count_cubes(cube, on=True):
    if on:
        return np.sum(cube.grid == 1)
    else:
        return np.sum(cube.grid == 0)


def init_sparse_grid(instructions, inside_cube_only=True):
    X = set()
    Y = set()
    Z = set()
    
    X.add(-50)
    X.add(51)
    Y.add(-50)
    Y.add(51)
    Z.add(-50)
    Z.add(51)
    
    S = set()

    #find all points of crossover in instructions to create mini-cuboids to work from    
    for instr in instructions:
        if inside_cube_only and (instr.ranges['x'][0] < -50 or
                                 instr.ranges['x'][1] > 50 or
                                 instr.ranges['y'][0] < -50 or
                                 instr.ranges['y'][1] > 50 or
                                 instr.ranges['z'][0] < -50 or
                                 instr.ranges['z'][1] > 50):
            break

        x0, x1 = instr.ranges['x']
        X.add(x0)
        X.add(x1 + 1)
        y0, y1 = instr.ranges['y']
        Y.add(y0)
        Y.add(y1 + 1)
        z0, z1 = instr.ranges['z']
        Z.add(z0)
        Z.add(z1 + 1)
        
    X = list(X)
    X.sort()
    Y = list(Y)
    Y.sort()
    Z = list(Z)
    Z.sort()
    
    return {'X': X, 'Y': Y, 'Z': Z}

    # logger.debug(f"sparse matrix has roughly {len(X) * len(Y) * len(Z)} bins")

    # sparse_grid = list()
    # for xi, x in enumerate(X):
    #     logger.debug(f"sparse_grid len: {len(sparse_grid)}, size: {sys.getsizeof(sparse_grid)}")
    #     for yi, y in enumerate(Y):
    #         for zi, z in enumerate(Z):
    #             size = 0
    #             # higher outside edges don't represent any 'ons'
    #             if (xi != len(X) - 1 and 
    #                 yi != len(Y) - 1 and 
    #                 zi != len(Z) - 1):
    #                 #get deltas to next grid point on each axis to get representative volume for this sparse grid point
    #                 dx = X[xi + 1] - x
    #                 dy = Y[yi + 1] - y
    #                 dz = Z[zi + 1] - z
    #                 size = dx * dy * dz
    #             sparse_grid.append([x,y,z,0,size])
                
    # logger.debug(f"sparse_grid has {len(sparse_grid)} entries")
    # return sparse_grid

# def init_sparse_dataframe(sparse_grid):
#     df = pd.DataFrame(sparse_grid, columns=['x','y','z','on','size'])
#     df = df.astype({"x": np.int32, 
#                     "y": np.int32, 
#                     "z": np.int32, 
#                     "on": np.int8, 
#                     "size": np.int32})
#     df = df.set_index(['x','y','z'])
#     return df

def apply_sparse_instruction(instruction, sparse_grid, cuboids_on: set):
    x0, x1 = instruction.ranges['x']
    y0, y1 = instruction.ranges['y']
    z0, z1 = instruction.ranges['z']
    initial_len = len(cuboids_on)
    for xi, x in enumerate(sparse_grid['X']):
        if x >= x0 and x < x1:
            for yi, y in enumerate(sparse_grid['Y']):
                if y >= y0 and y < y1:
                    for zi, z in enumerate(sparse_grid['Z']):
                        if z >= z0 and z < z1:
                            if instruction.on:
                                cuboids_on.add((x,y,z))
                            else:
                                cuboids_on.discard((x,y,z))
    final_len = len(cuboids_on)
    return final_len - initial_len

def apply_sparse_instructions(instructions, sparse_grid, inside_cube_only=True):
    cuboids_on = set()    
    for instr in instructions:
        changed = apply_sparse_instruction(instruction=instr, sparse_grid=sparse_grid, cuboids_on=cuboids_on)
        logger.debug(f"instr: {instr}, change: {changed}")
    return cuboids_on

def run(instructions, inside_cube_only=True):
    sg = init_sparse_grid(instructions, inside_cube_only)
    cuboids_on = apply_sparse_instructions(instructions, sg, inside_cube_only)
    return cuboids_on, sg

def count_cuboid_lights(cuboids_on, sparse_grid, on=True):
    count = 0
    for xi, x in enumerate(sparse_grid['X']):
        for yi, y in enumerate(sparse_grid['Y']):
            for zi, z in enumerate(sparse_grid['Z']):
                if (x,y,z) in cuboids_on:
                    dx = sparse_grid['X'][xi + 1] - x
                    dy = sparse_grid['Y'][yi + 1] - y
                    dz = sparse_grid['Z'][zi + 1] - z
                    count += dx * dy * dz
    return count    

def count_dataframe(df):
    # for xi, x in enumerate(X):
    #     for yi, y in enumerate(Y):
    #         for zi, z in enumerate(Z):
    #             size = 0
    #             # higher outside edges don't represent any 'ons'
    #             if (xi != len(X) - 1 and 
    #                 yi != len(Y) - 1 and 
    #                 zi != len(Z) - 1):
    #                 #get deltas to next grid point on each axis to get representative volume for this sparse grid point
    #                 dx = X[xi + 1] - x
    #                 dy = Y[yi + 1] - y
    #                 dz = Z[zi + 1] - z
    #                 size = dx * dy * dz
    #             sparse_grid.append([x,y,z,0,size])
    return df.query('on == 1')['size'].sum()

def main():
    logger.setLevel(level=logging.DEBUG)
    with open("input.txt") as f:
        data = f.read()
    
    instructions = parse_data(data)
    cube = Cube()
    apply_instructions(instructions, cube)
    answer = count_cubes(cube)
    logger.info(f"Puzzle1: Cubes on with interior instructions only: {answer}")
    df = run(instructions, inside_cube_only=False)
    answer = count_dataframe(df)
    logger.info(f"Puzzle2: Cubes on after all instructions: {answer}")
    
if __name__ == '__main__':
    main()