import logging
import os
import numpy as np

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

GAMES = dict()
TRACE = 0

def get_file_data(fn='input.txt'):
    with open(fn) as f:
        data = f.read()
    return data

def parse_data(text_data):
    lines = [line for line in text_data.strip('\n').strip().split('\n')]
    for line in lines:
        if 'Player 1' in line:
            p1_start = int(line.split(':')[1].strip())
        else:
            p2_start = int(line.split(':')[1].strip())
    return p1_start, p2_start

def roll_dice(dice_state=0, times=3):
    distance = 0
    for i in range(times):
        dice_state = (dice_state % 100) + 1
        distance += dice_state
        # logger.debug(f"dice_state: {dice_state}, distance: {distance}")
    return dice_state, distance

def turn(player_position, dice_state):
    dice_state, distance = roll_dice(dice_state)
    player_position = ((player_position + distance - 1) % 10) + 1
    score = player_position
    return score, player_position, dice_state

def run_game(p1, p2, winning_score=1000):
    p1_score, p2_score, dice_state, rolls = 0, 0, 0, 0
    times = 3
    winner, loser = 0, 0
    while p1_score < winning_score and p2_score < winning_score:
        score, p1, dice_state = turn(p1, dice_state)
        p1_score += score
        rolls += 3
        if p1_score >= winning_score:
            winner = p1_score
            loser = p2_score
            break
        score, p2, dice_state = turn(p2, dice_state)
        p2_score += score
        rolls += 3
        if p2_score >= winning_score:
            winner = p2_score
            loser = p1_score
            break
        
    logger.debug(f"winner: {winner}, loser: {loser}, rolls: {rolls}")
    return winner, loser, rolls

def score(player_position, distance):
    player_position = ((player_position + distance - 1) % 10) + 1
    return player_position

def run_quantum_game(p1_pos, p1_score, p2_pos, p2_score, p1_turn=True, winning_score=21):
    global GAMES
    global TRACE
    game_tuple = (p1_pos, p1_score, p2_pos, p2_score, p1_turn)
    
    # if logger.level <= logging.DEBUG:
    logger.debug(game_tuple)
    #     TRACE += 1
    #     if TRACE == 10:
    #         raise ValueError
    
    
    
    if game_tuple in GAMES:
        pass
    
    elif p1_score >= winning_score:
        logger.debug(f"set {game_tuple} to 1, 0")
        GAMES[game_tuple] = np.array([1, 0], dtype=np.int64)
        return GAMES[game_tuple]

    elif p2_score >= winning_score:
        logger.debug(f"set {game_tuple} to 0, 1")
        GAMES[game_tuple] = np.array([0, 1], dtype=np.int64)
        return GAMES[game_tuple]
    
    else:
        tallies = np.array([0, 0], dtype=np.int64)
        if p1_turn:
            p = score(p1_pos, 3)
            logger.debug(f"distance of 3 from {p1_pos} yield a new position of {p}, score from {p1_score} --> {p1_score+p}")
            tallies += 1 * run_quantum_game(p, p1_score+p, p2_pos, p2_score, False)
            p = score(p1_pos, 4)
            tallies += 3 * run_quantum_game(p, p1_score+p, p2_pos, p2_score, False)
            p = score(p1_pos, 5)
            tallies += 6 * run_quantum_game(p, p1_score+p, p2_pos, p2_score, False)
            p = score(p1_pos, 6)
            tallies += 7 * run_quantum_game(p, p1_score+p, p2_pos, p2_score, False)
            p = score(p1_pos, 7)
            tallies += 6 * run_quantum_game(p, p1_score+p, p2_pos, p2_score, False)
            p = score(p1_pos, 8)
            tallies += 3 * run_quantum_game(p, p1_score+p, p2_pos, p2_score, False)
            p = score(p1_pos, 9)
            tallies += 1 * run_quantum_game(p, p1_score+p, p2_pos, p2_score, False)
            GAMES[game_tuple] = tallies
            logger.debug(f"set {game_tuple} to {tallies}")
            
        else:
            # take this turn and explode all the universes
            p = score(p2_pos, 3)
            tallies += 1 * run_quantum_game(p1_pos, p1_score, p, p2_score+p, True)
            p = score(p2_pos, 4)
            tallies += 3 * run_quantum_game(p1_pos, p1_score, p, p2_score+p, True)
            p = score(p2_pos, 5)
            tallies += 6 * run_quantum_game(p1_pos, p1_score, p, p2_score+p, True)
            p = score(p2_pos, 6)
            tallies += 7 * run_quantum_game(p1_pos, p1_score, p, p2_score+p, True)
            p = score(p2_pos, 7)
            tallies += 6 * run_quantum_game(p1_pos, p1_score, p, p2_score+p, True)
            p = score(p2_pos, 8)
            tallies += 3 * run_quantum_game(p1_pos, p1_score, p, p2_score+p, True)
            p = score(p2_pos, 9)
            tallies += 1 * run_quantum_game(p1_pos, p1_score, p, p2_score+p, True)
            logger.debug(f"set {game_tuple} to {tallies}")
            GAMES[game_tuple] = tallies
    
    logger.debug(len(GAMES))
    return GAMES[game_tuple]
              

def main():
    logger.setLevel(level=logging.INFO)
    with open("input.txt") as f:
        data = f.read()
       
    p1, p2 = parse_data(data)
    winner, loser, rolls = run_game(p1, p2)
    answer = loser * rolls
    logger.info(f"Puzzle1: Dirac Dice, game to 1000: {answer}")
    p1, p2 = parse_data(data)
    p1_wins, p2_wins = run_quantum_game(p1, 0, p2, 0)
    answer = p1_wins if p1_wins > p2_wins else p2_wins
    logger.info(f"Puzzle2: Dirac Dice Quantum Winner Count: {answer}")
    
if __name__ == '__main__':
    main()