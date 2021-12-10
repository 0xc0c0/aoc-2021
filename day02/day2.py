import logging

def parse_line(text_line):
    text = text_line.strip().split()
    return (text[0],int(text[1]))

def parse_data(text_data):
    text_data = text_data.strip().split('\n')
    logging.debug(text_data)
    moves = []
    for line in text_data:
        moves.append(parse_line(line))
    return moves

def run_move(move, tracker=None):
    if not tracker or 'depth' not in tracker or 'position' not in tracker:
        logging.debug("initializing new tracker object 0,0")
        tracker = {
            'position' : 0,
            'depth' : 0,
        }
    
    direction = move[0]
    distance = move[1]

    if direction == 'forward':
        tracker['position'] += distance
    elif direction == 'down':
        tracker['depth'] += distance
    elif direction == 'up':
        tracker['depth'] -= distance
    else:
        raise ValueError(move) 
    
    return tracker

def run_move2(move, tracker=None):
    if not tracker or 'depth' not in tracker or 'position' not in tracker:
        logging.debug("initializing new tracker object 0,0")
        tracker = {
            'position' : 0,
            'depth' : 0,
            'aim' : 0
        }
    
    direction = move[0]
    units = move[1]

    if direction == 'forward':
        tracker['position'] += units
        tracker['depth'] += (tracker['aim'] * units)
    elif direction == 'down':
        tracker['aim'] += units
    elif direction == 'up':
        tracker['aim'] -= units
    else:
        raise ValueError(move) 
    
    return tracker

def run_moves(moves, tracker=None):
    for move in moves:
        tracker = run_move(move, tracker=tracker)
    return tracker

def run_moves2(moves, tracker=None):
    for move in moves:
        tracker = run_move2(move, tracker=tracker)
    return tracker

def get_tracker_vars(tracker):
    return tracker['position'], tracker['depth']

def main():
    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.INFO)
    with open("input.txt") as f:
        data = f.read()
    moves = parse_data(data)
    
    #Part 1
    position, depth = get_tracker_vars(run_moves(moves))
    logger.info(f"Puzzle1: Final: position: {position}, depth: {depth}")
    logger.info(f"Puzzle1: Answer: {position * depth}") 
    
    #Part 2
    position, depth = get_tracker_vars(run_moves2(moves))
    logger.info(f"Puzzle2: Final: position: {position}, depth: {depth}")
    logger.info(f"Puzzle2: Answer: {position * depth}") 

if __name__ == '__main__':
    main()