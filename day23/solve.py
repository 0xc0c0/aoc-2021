import logging
import os
import numpy as np
import re

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

def get_file_data(fn='input.txt'):
    with open(fn) as f:
        data = f.read()
    return data

###################################
##0  1  2  3  4  5  6  7  8  9 10##
########11####13####15####17#######
########12####14####16####18#######

AVAILABLE_MOVES={
    0: [1],
    1: [0,2],
    2: [1,3,11],
    3: [2,4],
    4: [3,5,13],
    5: [4,6],
    6: [5,7,15],
    7: [6,8],
    8: [7,9,17],
    9: [8,10],
    10:[9],
    11:[2,12],
    12:[11],
    13:[4,14],
    14:[13],
    15:[6,16],
    16:[15],
    17:[8,18],
    18:[17]
}

#higher number filled first
TARGETS={
    'A': [11,12],
    'B': [13,14],
    'C': [15,16],
    'D': [17,18]
}

FIRST_FILL_I = 1
SECOND_FILL_I = 0

COST={
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000
}

def parse_data(text_data):
    lines = text_data.strip('\n').strip().split('\n')
    index_order = [11,13,15,17,12,14,16,18]
    locations=[None]*19
    results = re.findall(r'#([A-D])',text_data)
    assert len(results) == 8
    o = 0
    for i in index_order:
        locations[i] =  results[o]
        o += 1
    return tuple(locations)

def swap(locations, index1, index2):
    new_locations = list(locations)
    saved = new_locations[index1]
    new_locations[index1] = new_locations[index2]
    new_locations[index2] = saved
    return tuple(new_locations)

def check_complete(locations, targets=TARGETS):
    for k, target_indices in enumerate(targets):
        for i in target_indices:
            if targets[i] != k:
                return False
    return True

def find_good_available_moves(locations, available_moves=AVAILABLE_MOVES, targets=TARGETS):
    moves = {
        'A': [],
        'B': [],
        'C': [],
        'D': []
    }
    for location, letter in enumerate(locations):
        #if location has a letter, look at next options where it could move
        if letter:
            #if bottom position and already correctly filled/finished, skip changing it
            if targets[letter][FIRST_FILL_I] == location:
                continue
            #if top position and both slots are correctly filled, skip it
            elif (targets[letter][SECOND_FILL_I] == location and 
                  locations[targets[letter][FIRST_FILL_I]] == letter):
                continue
            for new_i in available_moves[location]:
                # make sure the spot isn't full
                if not locations[new_i]:
                    moves[letter].append((location, new_i))
    return moves

def find_lowest_cost_solve(locations, accrued_starting_cost=0, max_cost=12521, started_solves=dict(), completed_solves=dict()):
    logger.debug(f"CHANGE TO ITERATE STYLE CODE")
    logger.debug(f"finding for locations: {locations}")
    #if this state has already been solved, just return the value
    if locations in completed_solves:
        return completed_solves[locations]
    
    #if this is complete, costs nothing to solve it, so update with 0 and return
    if check_complete(locations):
        completed_solves[locations] = 0
        return 0
    
    #if already reached this state with lower cost to get to this state from the start, skip this tree
    if locations in started_solves and started_solves[locations] <= accrued_starting_cost:
        return None
    #otherwise keep going and insert/update the entry in the started_solves tracker
    else:
        started_solves[locations] = accrued_starting_cost
        
    #if max_cost is set and has been reached, give up
    if max_cost > 0 and accrued_starting_cost >= max_cost:
        return None
    
    else:
        min = None
        # take the multiverse approach and simply brute force with dynamic programming to save rework
        moves = find_good_available_moves(locations)
        for letter in moves:
            for move in moves[letter]:
                next_step = swap(locations, move[0], move[1])
                result = find_lowest_cost_solve(next_step, 
                                                COST[letter] + accrued_starting_cost, 
                                                max_cost, 
                                                started_solves)
                if result != None:
                    result_cost = COST[letter] + result
                    if min == None or result_cost < min:
                        min = result_cost
        completed_solves[locations] = min
        return min
        
def main():
    logger.setLevel(level=logging.INFO)
    with open("input.txt") as f:
        data = f.read()
       
    data = parse_data(data)
    answer = 0
    logger.info(f"Puzzle1: <SUMMARY>: {answer}")
    answer = 0
    logger.info(f"Puzzle2: <SUMMARY>: {answer}")
    
if __name__ == '__main__':
    main()