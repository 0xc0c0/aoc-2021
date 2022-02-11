import logging
import os
import numpy as np

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

QUANTUM_WINS_P1 = 0
QUANTUM_WINS_P2 = 0

def get_file_data(fn='input.txt'):
    with open(fn) as f:
        data = f.read()
    return data

def parse_data(text_data):
    lines = [line for line in text_data.strip('\n').strip().split('\n')]
    for line in lines:
        if 'Player 1' in line:
            p1_start = int(line.split(':')[1].strip()) - 1
        else:
            p2_start = int(line.split(':')[1].strip()) - 1
    return p1_start, p2_start

def roll_dice(dice_state=-1, times=3):
    distance = 0
    for i in range(times):
        dice_state = (dice_state + 1) % 100
        distance += dice_state + 1
        logger.debug(f"dice_state: {dice_state}, distance: {distance}")
    return dice_state, distance

def turn(player_position, dice_state):
    dice_state, distance = roll_dice(dice_state)
    player_position = (player_position + distance) % 10
    score = player_position + 1
    return score, player_position, dice_state

def run_game(p1, p2, winning_score=1000):
    p1_score, p2_score, dice_state, rolls = 0, 0, -1, 0
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
    player_position = (player_position + distance) % 10
    return player_position + 1, player_position

def run_quantum_game(p1_pos, p1_score, p2_pos, p2_score, p1_turns=0, p2_turns=0, occurrences=1, winning_score=21):
    global QUANTUM_WINS_P1
    global QUANTUM_WINS_P2
    logger.debug(f"{p1_pos}, {p1_score}, {p2_pos}, {p2_score}, {p1_turns}, {p2_turns}, {occurrences}")
    if p1_score >= winning_score:
        QUANTUM_WINS_P1 += occurrences
        logger.debug(f"P1 won {occurrences} more times!")
        return QUANTUM_WINS_P1, QUANTUM_WINS_P2
    if p2_score >= winning_score:
        QUANTUM_WINS_P2 += occurrences
        logger.debug(f"P2 won {occurrences} more times!")
        return QUANTUM_WINS_P1, QUANTUM_WINS_P2
    
    if p1_turns <= p2_turns:
        s, p = score(p1_pos, 3)
        run_quantum_game(p, p1_score+s, p2_pos, p2_score, p1_turns+1, p2_turns, occurrences)
        s, p = score(p1_pos, 4)
        run_quantum_game(p, p1_score+s, p2_pos, p2_score, p1_turns+1, p2_turns, occurrences * 3)
        s, p = score(p1_pos, 5)
        run_quantum_game(p, p1_score+s, p2_pos, p2_score, p1_turns+1, p2_turns, occurrences * 6)
        s, p = score(p1_pos, 6)
        run_quantum_game(p, p1_score+s, p2_pos, p2_score, p1_turns+1, p2_turns, occurrences * 7)
        s, p = score(p1_pos, 7)
        run_quantum_game(p, p1_score+s, p2_pos, p2_score, p1_turns+1, p2_turns, occurrences * 6)
        s, p = score(p1_pos, 8)
        run_quantum_game(p, p1_score+s, p2_pos, p2_score, p1_turns+1, p2_turns, occurrences * 3)
        s, p = score(p1_pos, 9)
        run_quantum_game(p, p1_score+s, p2_pos, p2_score, p1_turns+1, p2_turns, occurrences) 
        
    else:
        s, p = score(p2_pos, 3)
        run_quantum_game(p1_pos, p1_score, p, p2_score+s, p1_turns, p2_turns+1, occurrences)
        s, p = score(p2_pos, 4)
        run_quantum_game(p1_pos, p1_score, p, p2_score+s, p1_turns, p2_turns+1, occurrences * 3)
        s, p = score(p2_pos, 5)
        run_quantum_game(p1_pos, p1_score, p, p2_score+s, p1_turns, p2_turns+1, occurrences * 6)
        s, p = score(p2_pos, 6)
        run_quantum_game(p1_pos, p1_score, p, p2_score+s, p1_turns, p2_turns+1, occurrences * 7)
        s, p = score(p2_pos, 7)
        run_quantum_game(p1_pos, p1_score, p, p2_score+s, p1_turns, p2_turns+1, occurrences * 6)
        s, p = score(p2_pos, 8)
        run_quantum_game(p1_pos, p1_score, p, p2_score+s, p1_turns, p2_turns+1, occurrences * 3)
        s, p = score(p2_pos, 9)
        run_quantum_game(p1_pos, p1_score, p, p2_score+s, p1_turns, p2_turns+1, occurrences)
          

def main():
    logger.setLevel(level=logging.INFO)
    with open("input.txt") as f:
        data = f.read()
       
    p1, p2 = parse_data(data)
    winner, loser, rolls = run_game(p1, p2)
    answer = loser * rolls
    logger.info(f"Puzzle1: Dirac Dice, game to 1000: {answer}")
    answer = 0
    logger.info(f"Puzzle2: <SUMMARY>: {answer}")
    
if __name__ == '__main__':
    main()