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
    data = [[int(x) for x in list(line)] for line in text_data.strip('\n').strip().split('\n')]
    return np.array(data)

def main():
    logger.setLevel(level=logging.INFO)
    with open("input.txt") as f:
        data = f.read()
       
    grid = parse_data(data)
    answer = 0
    logger.info(f"Puzzle1: <SUMMARY>: {answer}")
    answer = 0
    logger.info(f"Puzzle2: <SUMMARY>: {answer}")
    
if __name__ == '__main__':
    main()