import logging
import numpy as np

def parse_drawing(text):
    return [int(x) for x in text.strip().split(',')]

def parse_board(text):
    return np.fromstring(text, dtype=int, sep=' ').reshape((5,5))

def parse_data(text_data):
    text_data = text_data.strip().split('\n\n')
    drawing = parse_drawing(text_data[0])
    boards = []
    for text_blob in text_data[1:]:
        nums = parse_board(text_blob)
        marks = np.array([False]*25).reshape((5,5))
        boards.append({'nums' : nums, 'marks' : marks})
    logging.debug(boards[0])
    return drawing, boards

def update_board(board, num):
    checks = (board['nums'] == num)
    if checks.any():
        i = np.where(checks)
        board['marks'][i] = 1

def check_bingo(board):
    for r in range(5):
        if sum(board['marks'][r,:]) == 5:
            return True
    for c in range(5):
        if sum(board['marks'][:,c]) == 5:
            return True
    return False

def get_winning_number(board, num):
    unmarked = (board['marks'] == False)
    sum_unmarked = np.sum(unmarked * board['nums'])
    return num * sum_unmarked

def run_round(boards, num, remove_winner=True):
    results = list()
    for board in boards:
        update_board(board, num)
    for i, board in enumerate(boards):
        if check_bingo(board):
            if remove_winner:
                del boards[i]
            results.append([board, num, get_winning_number(board, num)])
    return results

def run_rounds(boards, nums):
    ordered_winners = list()
    for num in nums:
        results = run_round(boards, num)
        ordered_winners += results
    return ordered_winners

def main():
    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.INFO)
    with open("input.txt") as f:
        data = f.read()
    drawing, boards = parse_data(data)
    
    #Part 1
    winners = run_rounds(boards, drawing)
    logger.info(f"Puzzle1: Winning Score: {winners[0][2]}")
    logger.info(f"Puzzel2: Worst Board Score: {winners[-1][2]}")

if __name__ == '__main__':
    main()