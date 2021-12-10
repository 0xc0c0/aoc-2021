import logging
import numpy as np
import os
from functools import reduce

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

def parse_data(text_data):
    text_lines = text_data.strip().split('\n')
    return text_lines

def find_first_illegal_char(line):
    stack = []
    open_items = '([{<'
    close_items = ')]}>'
    for i,c in enumerate(line):
        if c in open_items:
            stack.append(c)
        else:
            if len(stack) <= 0:
                return None
            found_i = close_items.index(c)
            if stack.pop() != open_items[found_i]:
                return c
            
    return None

def compute_illegal_chars(lines):
    score = 0
    scores = {
        ')' : 3,
        ']' : 57,
        '}' : 1197,
        '>' : 25137
    }
    incomplete_lines = []
    for line in lines:
        c = find_first_illegal_char(line)
        if c:
            score += scores[c]
        else:
            incomplete_lines.append(line)
    return score, incomplete_lines

def complete_line(line):
    stack = []
    open_items = '([{<'
    close_items = ')]}>'
    for i,c in enumerate(line):
        if c in open_items:
            stack.append(c)
        else:
            if len(stack) <= 0:
                return None
            found_i = close_items.index(c)
            if stack.pop() != open_items[found_i]:
                return c
    add_scores = {
        '(' : 1,
        '[' : 2,
        '{' : 3,
        '<' : 4
    }
    score = 0
    while len(stack) > 0:
        score = (score * 5) + add_scores[stack.pop()]
    return score

def get_completion_score(incomplete_lines):
    scores = []
    for line in incomplete_lines:
        scores.append(complete_line(line))
    scores.sort()
    index = int(len(scores)/2)
    return scores[index]

def main():
    logger.setLevel(level=logging.INFO)
    with open("input.txt") as f:
        data = f.read()
       
    lines = parse_data(data)
    answer, incomplete_lines = compute_illegal_chars(lines)
    logger.info(f"Puzzle1: Lowest: {answer}")
    answer = get_completion_score(incomplete_lines)
    logger.info(f"Puzzle2: Complex: {answer}")
    
if __name__ == '__main__':
    main()