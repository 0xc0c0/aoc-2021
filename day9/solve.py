import logging
import numpy as np
import os
import math

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

def parse_data(text_data):
    text_lines = text_data.strip().split('\n')
    heightmap = [[int(n) for n in list(line)]for line in text_lines]
    return heightmap

def is_low_point_incorrect(heightmap, r, c):
    if r == 0:
        rows = range(0, 2)
    elif r == len(heightmap) - 1:
        rows = range(r - 1, r + 1)
    else:
        rows = range(r - 1, r + 2)
    
    if c == 0:
        cols = range(0, 2)
    elif c == len(heightmap[0]) - 1:
        cols = range(c - 1, c + 1)
    else:
        cols = range(c - 1, c + 2)
    
    for ri in rows:
        for ci in cols:
            if ri == r and ci == c:
                continue
            #logging.debug(f"ri: {ri} ci: {ci} r: {r} c: {c}")
            if heightmap[ri][ci] <= heightmap[r][c]:
                return False
    return True

def is_low_point(heightmap, r, c):
    tp = heightmap[r][c]
    #logging.debug(f"r: {r} c: {c}")
    if ((r > 0 and heightmap[r - 1][c] <= tp) or 
            (r < len(heightmap) - 1 and heightmap[r + 1][c] <= tp) or
            (c > 0 and heightmap[r][c - 1] <= tp) or
            (c < len(heightmap[0]) - 1 and heightmap[r][c + 1] <= tp)):
        return False
    return True
    
def find_low_points(heightmap):
    points = []
    for r in range(len(heightmap)):
        for c in range(len(heightmap[0])):
            if is_low_point(heightmap, r, c):
                points.append((r,c))
    #logging.info(f"points: {points}")
    return points

def get_risk_level(heightmap, points):
    return sum([heightmap[r][c] + 1 for (r,c) in points])
    
def main():
    logger.setLevel(level=logging.INFO)
    with open("input.txt") as f:
        data = f.read()
       
    hm = parse_data(data)
    pts = find_low_points(heightmap=hm)
    answer = get_risk_level(heightmap=hm, points=pts)
    logger.info(f"Puzzle1: Lowest: {answer}")
    answer = 0
    logger.info(f"Puzzle2: Complex: {answer}")
    
if __name__ == '__main__':
    main()