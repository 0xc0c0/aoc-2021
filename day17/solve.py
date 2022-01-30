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
    lines = [line for line in text_data.strip('\n').strip().split('\n') if line]
    text = lines[0]
    HDR = 'target area: '
    bounds_text = None
    logger.debug('text')
    if text.startswith(HDR):
        bounds_text = text[len(HDR):]
    bounds = [bound.strip() for bound in bounds_text.split(',')]
    ranges=dict()
    for bound in bounds:
        v, b = bound.split('=')
        b = [int(r) for r in b.split('..')]
        ranges[v] = (min(b), max(b))
    return ranges

def run_test(dx,dy,bounds):
    # logger.debug(f"Testing: {dx},{dy} for bounds: {bounds}")
    # run until below or to the right of the box
    cur_x, cur_y = 0,0
    cur_dx, cur_dy = dx,dy
    max_y = cur_y
    while cur_y >= bounds['y'][0] or cur_dy > 0:
        cur_x += cur_dx
        cur_y += cur_dy
        cur_dx = cur_dx - 1 if cur_dx > 0 else (cur_dx if cur_dx == 0 else cur_dx + 1)
        cur_dy -= 1
        # logger.debug(f"point: {cur_x}, {cur_y}")
        if cur_y > max_y:
            max_y = cur_y
        if (cur_x >= bounds['x'][0] and cur_x <= bounds['x'][1] and
            cur_y >= bounds['y'][0] and cur_y <= bounds['y'][1]):
            return max_y
    # logger.debug(f"Failed test: {dx},{dy} for bounds: {bounds}")
    return None

def get_max_y_test_vector_ranges(bounds):
    # get minimum dx
    dx = math.floor(math.sqrt(bounds['x'][0] * 2)) + 1
    dy = (0 - bounds['y'][0]) - 1
    logger.info(f"found best vector for height: {dx},{dy}")
    return dx, dy

def count_valid_vectors(bounds):
    dx, max_dy = get_max_y_test_vector_ranges(bounds)
    min_dx = dx - 1
    min_dy = min(bounds['y'])
    max_dx = max(bounds['x'])
    count = 0
    for dx in range(min_dx, max_dx + 1):
        for dy in range(min_dy, max_dy + 1):
            if run_test(dx, dy, bounds) != None:
                count += 1
                logger.debug(f"found {dx},{dy}")
    logger.info(f"counted {count} total valid vectors")
    return count

def main():
    logger.setLevel(level=logging.INFO)
    with open("input.txt") as f:
        data = f.read()
       
    bounds = parse_data(data)
    vector_x, vector_y = get_max_y_test_vector_ranges(bounds)
    answer = run_test(vector_x, vector_y, bounds)
    logger.info(f"Puzzle1: Max Height: {answer}")
    answer = count_valid_vectors(bounds)
    logger.info(f"Puzzle2: Total Valid Vectors: {answer}")
    
if __name__ == '__main__':
    main()