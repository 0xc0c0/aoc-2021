from dataclasses import dataclass
import logging
import os
from typing import List
import re
from sortedcontainers import SortedDict, SortedList

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

#convert this to lookups with multipliers for '# hops' based on rules
AVAILABLE_DIRECT_MOVES={
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

###################################
##0  1  2  3  4  5  6  7  8  9 10##
########11####13####15####17#######
########12####14####16####18#######
########19####21####23####25#######
########20####22####24####26#######

AVAILABLE_DIRECT_MOVES_DEEP={
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
    12:[11,19],
    13:[4,14],
    14:[13,21],
    15:[6,16],
    16:[15,23],
    17:[8,18],
    18:[17,25],
    19:[12,20],
    20:[19],
    21:[14,22],
    22:[21],
    23:[16,24],
    24:[23],
    25:[18,26],
    26:[25]
}

HALLWAY=[0,1,2,3,4,5,6,7,8,9,10]
OFF_LIMITS=[2,4,6,8]

FIRST_FILL_I = 1
SECOND_FILL_I = 0

COST={
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000
}

def find_path(src, dest, saved_path=[]):
    #ensure src is the beginning of saved_path
    top_level = False
    if not saved_path:
        saved_path = [src]
        top_level = True
        
    if src == dest:
        return saved_path
    
    for option in AVAILABLE_DIRECT_MOVES[src]:
        if option in saved_path:
            continue
        new_path = saved_path + [option]
        result = find_path(option, dest, new_path)
        
        #there's only one valid path
        if result:
            if top_level:
                # trim off src
                result = result[1:]
                logger.debug(f"found path from {src} to {dest}: {result}")
            return result

    #no valid paths found without stomping on saved_path
    return None

@dataclass(eq=True, frozen=True)
class GameState:
    A: tuple
    B: tuple
    C: tuple
    D: tuple
    
    @classmethod
    def from_dict(cls, game):
        for k in game:
            assert type(game[k]) == tuple
        return cls(A=game['A'],
                   B=game['B'],
                   C=game['C'],
                   D=game['D'])
    
    def get_dict(self):
        #could have problems if you don't make copies here
        return {
            'A' : self.A,
            'B' : self.B,
            'C' : self.C,
            'D' : self.D
        }
    
    def get_list(self):
        game_dict = self.get_dict()
        return [ (letter,location) for letter in game_dict for location in game_dict[letter] ]
    
    def copy(self):
        new = self.get_dict()
        return GameState.from_dict(new)
    
    def get_all_taken_spots(self):
        return tuple([location for locations in self.get_dict().values() for location in locations])

    def move_letter(self, letter: str, old_location: int, new_location: int):
        new = self.get_dict()
        tmp = SortedList(new[letter])
        tmp.remove(old_location)
        tmp.add(new_location)
        new[letter] = tuple(tmp)
        # logger.debug(f"new is: {new}")
        return GameState.from_dict(new)

TARGET_GAME = GameState(A=(11,12), B=(13,14), C=(15,16), D=(17,18))
TARGETS = TARGET_GAME.get_dict()

def in_same_room(src, dest):
    if (src in HALLWAY and dest in HALLWAY):
        return True
    if (src not in HALLWAY) and (dest not in HALLWAY):
        for letter in TARGETS:
            if src in TARGETS[letter] and dest in TARGETS[letter]:
                return True
    return False

def init_available_hops():
    hops = [dict() for i in range(len(AVAILABLE_DIRECT_MOVES))]
    for src in range(len(AVAILABLE_DIRECT_MOVES)):
        for dest in range(len(AVAILABLE_DIRECT_MOVES)):
            if in_same_room(src,dest):
                continue
            if dest in hops[src]:
                continue
            if src in OFF_LIMITS or dest in OFF_LIMITS:
                continue

            hops[src][dest] = find_path(src, dest)
    logger.debug(f"hops[7]: {hops[7]}")
    logger.debug(f"hops[3]: {hops[3]}")
    logger.debug(f"hops[13]: {hops[13]}")
    logger.debug(f"hops[14]: {hops[14]}")
    return hops

def parse_data(text_data):
    lines = text_data.strip('\n').strip().split('\n')
    index_order = [11,13,15,17,12,14,16,18]
    results = re.findall(r'#([A-D])',text_data)
    assert len(results) == 8
    o = 0
    data = {
        'A': tuple(SortedList([index_order[i] for i, v in enumerate(results) if v == 'A'])),
        'B': tuple(SortedList([index_order[i] for i, v in enumerate(results) if v == 'B'])),
        'C': tuple(SortedList([index_order[i] for i, v in enumerate(results) if v == 'C'])),
        'D': tuple(SortedList([index_order[i] for i, v in enumerate(results) if v == 'D']))
    }
    return GameState.from_dict(data)

def is_path_blocked(all_taken_spots, path):
    for spot in path:
        if spot in all_taken_spots:
            return True
    return False

def find_reasonable_moves(game: GameState, hops: dict):
    # logger.debug(f"checking moves for: {game}")
    next_moves = list()
    locations = game.get_list()
    game_lookup = game.get_dict()
    all_taken_locations = game.get_all_taken_spots()
    
    for letter, location in locations:
        #if bottom position and already correctly filled/finished, skip changing it
        if TARGETS[letter][FIRST_FILL_I] == location:
            continue
        #if top position and both slots are correctly filled, skip it
        elif (TARGETS[letter][SECOND_FILL_I] == location and 
                [letter, FIRST_FILL_I] in locations):
            continue
               
        #now iterate through options and make sure it's worth the time
        for available_location in hops[location]:
            path = hops[location][available_location]
            
            # make sure the path isn't blocked
            if is_path_blocked(all_taken_locations, path):
                continue
            
            #don't move to a non-HALLWAY location that's not designated for that letter
            if available_location not in HALLWAY:
                if available_location not in TARGETS[letter]:
                    continue
                
                secondary, primary = TARGETS[letter]
                # logger.debug(f"letter: {letter}, primary: {primary}, secondary: {secondary}")
                if (available_location == secondary) and (primary not in game_lookup[letter]):
                    continue
            
            #build new game for next move
            added_cost = COST[letter] * len(path)
            new_game = game.move_letter(letter, location, available_location)
            
            #add game to list
            next_moves.append((new_game, added_cost))
    return next_moves

def find_lowest_cost_solve(starter_game: GameState):
    #lookup for previously hit game states and accrued costs
    started_games = dict()
    
    #finished games with costs
    completed_cost_count = None
    last_current_cost = None
    
    #current set of games to run down
    remaining_games = dict()
    remaining_games[starter_game] = 0
    
    available_hops = init_available_hops()
    
    # as long as we haven't found the finish line
    while not completed_cost_count or last_current_cost < completed_cost_count:
        current_cost = min(remaining_games.values())
        logger.debug(f"running cost: {current_cost}, started: {len(started_games)}, remaining: {len(remaining_games)}")
        # lowest_accrued_cost = min(started_solves.items(), key=lambda x: x[1])
        
        current_games = {x for x in remaining_games if remaining_games[x] == current_cost}
        
        for current_game in current_games:
            #mark this off as being 'handled'
            del remaining_games[current_game]
            
            #update started games
            if current_game not in started_games or current_cost < started_games[current_game]:
                started_games[current_game] = current_cost
            else:
                current_cost = started_games[current_game]
                       
            #if solved, mark/update completed_solves tracker
            if TARGET_GAME == current_game:
                if completed_cost_count == None or current_cost < completed_cost_count:
                    completed_cost_count = current_cost  
                continue
            
            next_moves = find_reasonable_moves(current_game, available_hops)
            for next_game, added_cost in next_moves:
                new_cost = current_cost + added_cost
                #don't add games already played
                if next_game not in started_games or new_cost < started_games[next_game]:
                    started_games[next_game] = new_cost
                    remaining_games[next_game] = new_cost
        last_current_cost = current_cost
        
    return completed_cost_count
        
def main():
    logger.setLevel(level=logging.INFO)
    with open("input.txt") as f:
        data = f.read()
       
    game = parse_data(data)
    answer = find_lowest_cost_solve(game)
    logger.info(f"Puzzle1: Lowest Cost to Solve: {answer}")
    logger.info(f"Use solve2.py for Puzzle2")
    
if __name__ == '__main__':
    main()