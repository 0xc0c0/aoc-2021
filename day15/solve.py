import logging
from multiprocessing import BoundedSemaphore
import numpy as np
import os
import math

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

np.set_printoptions(threshold=np.inf)

def get_file_data(fn='input.txt'):
    with open(fn) as f:
        data = f.read()
    return data

def parse_data(text_data):
    data = [[int(x) for x in list(line)] for line in text_data.strip('\n').strip().split('\n')]
    return np.array(data)

def get_neighbors(grid, point):
    len_r, len_c = grid.shape
    neighbors = list()
    r,c = point
    if (r + 1) < len_r: 
        neighbors.append((r + 1, c))
    if (r - 1) >= 0:
        neighbors.append((r - 1, c))
    if (c + 1) < len_c: 
        neighbors.append((r, c + 1))
    if (c - 1) >= 0:
        neighbors.append((r, c - 1))
    return neighbors
    
def update_next_lowest_risk(chitons, risk, considerations):
    len_r, len_c = risk.shape
    
    # first find lowest new paths to end (lowest (point(s) + lowest attached known path) attached to current completed risk grid)
    lowest_points = list()
    lowest_next_risk = None
    for point in considerations:
        neighbors = get_neighbors(risk, point)
        low_risk = None
        for n in neighbors:
            if risk[n]:
                risk_val = risk[n] + chitons[point]
                if low_risk == None or risk_val < low_risk:
                    low_risk = risk_val
        # if this is lower than anything else, replace saved points
        if lowest_next_risk == None or low_risk < lowest_next_risk:
            lowest_points = [point]
            lowest_next_risk = low_risk
        # if it's the same, just append the point
        elif low_risk == lowest_next_risk:
            lowest_points.append(point)
    
    logging.debug(f"next found risk: {lowest_next_risk}, points: {lowest_points}")
    
    # then remove those points and add all unpopulated new ones
    for point in lowest_points:
        # confirm lowest path to point
        risk[point] = lowest_next_risk
        considerations.remove(point)
        
        # add all new neighbors from those points for the next round
        neighbors = get_neighbors(risk, point)
        for n in neighbors:
            # requires the risk isn't already figured out for those points
            # because multiple is possible, ensure another lowest_point didn't already add that neighbor
            if not risk[n] and n not in considerations:
                considerations.append(n)
            logging.debug(f"point: {point}, next neighbors added: {n}")
            
    return lowest_points

def find_lowest_risk(chitons):
    risk = np.zeros(chitons.shape, dtype=int)
    start = (0,0)
    end = tuple([risk.shape[0] - 1, risk.shape[1] - 1])
    
    # initialize algorithm
    considerations = get_neighbors(risk, end)
    risk[end] = chitons[end]
    
    # run until algorithm completes
    new_points = end
    while start not in new_points:
        new_points = update_next_lowest_risk(chitons, risk, considerations)
    
    logging.debug(f"lowest risk: {risk[start] - chitons[start]}")
    logging.debug(f"risk chart: {risk}")
    
    # adjust for not needing to include (0,0)'s cost itself
    return risk[start] - chitons[start]

def make_full_map(chitons):
    full = np.zeros(np.multiply(chitons.shape,5), dtype=int)
    core_len = chitons.shape[0]
    for r,c in np.ndindex(full.shape):
        core_r = r % core_len
        core_c = c % core_len
        core_val = chitons[core_r, core_c]
        
        # how many cells aware from the core is our point?
        inc_index = (math.floor(c / core_len) + math.floor(r / core_len))
        
        # get the new value
        full[r,c] = (((core_val - 1)  + inc_index) % 9) + 1
    
    logging.debug(full)
    return full

def compare_maps(map1, map2):
    for p in np.ndindex(map1.shape):
        if map1[p] != map2[p]:
            logger.info(f"point {p} does not match, map1: {map1[p]}, map2: {map2[p]}")
            return False
    return True

def main():
    logger.setLevel(level=logging.INFO)
    with open("input.txt") as f:
        data = f.read()
       
    chitons = parse_data(data)
    answer = find_lowest_risk(chitons)
    logger.info(f"Puzzle1: Lowest Risk Path (Initial): {answer}")
    full = make_full_map(chitons)
    answer = find_lowest_risk(full)
    logger.info(f"Puzzle2: Lowest Risk Path (Full): {answer}")
    
if __name__ == '__main__':
    main()