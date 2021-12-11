import logging
import numpy as np
import os
import math

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

def get_file_data(fn='input.txt'):
    with open(fn) as f:
        data = f.read()
    return data

def parse_data(text_data):
    data = [[int(x) for x in list(line)] for line in text_data.strip('\n').strip().split('\n')]
    return np.array(data)

def get_surrounding_points(grid, loc):
    r,c = loc
    #logger.debug(f"loc: {loc}, r: {r}, c: {c}")
    if r == 0:
        rows = range(r, r + 2)
    elif r == len(grid) - 1:
        rows = range(r - 1, r + 1)
    else:
        rows = range(r - 1, r + 2)
    
    if c == 0:
        cols = range(c, c + 2)
    elif c == len(grid) - 1:
        cols = range(c - 1, c + 1)
    else:
        cols = range(c - 1, c + 2) 
    
    #don't change the point itself
    surroundings = [(ri,ci) for ri in rows for ci in cols if (ri,ci) != (r,c)]
    #logger.debug(f"surroundings of {loc}: {surroundings}")
    return surroundings

def oct_flash(grid, flashes, loc):
    changes = get_surrounding_points(grid, loc)
    new_flashes = []
    for r,c in changes:
        # make sure it hasn't alread flashed this step
        if flashes[r,c]:
            continue
        grid[r,c] += 1
        
        if grid[r,c] > 9:
            new_flashes.append((r,c))
    return new_flashes

def init_flashes(grid):
    return np.array([False]*grid.size).reshape(grid.shape)

def oct_step(grid):
    #get fresh flash map for this step
    flashes = init_flashes(grid)
    
    # increase all values
    for loc,val in np.ndenumerate(grid):
        grid[loc] += 1

    ready = list(zip(*np.where(grid > 9)))
    while ready:
        #queue up next batch
        loc = ready.pop()
        #if already flashed, skip
        if flashes[loc] == True:
            continue
        flashes[loc] = True
        grid[loc] = 0
        ready += oct_flash(grid, flashes, loc)
        
    
    for (r,c),val in np.ndenumerate(grid):
            if val > 9:
                flashes[r,c] = True
                grid[r,c] = 0
                oct_flash(grid, flashes, (r,c))
    
    total_flashes = len(np.where(flashes == True)[0])
    return total_flashes

def run_oct_steps(grid, num):
    sum_flashes = 0
    for n in range(num):
        f = oct_step(grid)
        logger.debug(f"step: {n}, flashes: {f}")
        #logger.debug(grid)
        sum_flashes += f
    return sum_flashes

def find_next_all_flash(grid, step_tracker=0):
    flashes = 0
    while flashes < 100:
        step_tracker += 1
        flashes = oct_step(grid)
    return step_tracker

def main():
    logger.setLevel(level=logging.INFO)
    with open("input.txt") as f:
        data = f.read()
       
    grid = parse_data(data)
    answer = run_oct_steps(grid, 100)
    logger.info(f"Puzzle1: Flashes after 100 steps: {answer}")
    grid = parse_data(data)
    answer = find_next_all_flash(grid)
    logger.info(f"Puzzle2: First synchronize flash step: {answer}")
    
if __name__ == '__main__':
    main()