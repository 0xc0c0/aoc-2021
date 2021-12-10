import logging
import numpy as np
import os
import math

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

def parse_data(text_data):
    data = text_data.strip('\n').strip().split(',')
    data = [int(x) for x in data]
    data.sort()
    return data

def main():
    logger.setLevel(level=logging.INFO)
    with open("input.txt") as f:
        data = f.read()
       
    #Part 1  Full Simulation Algorithm
    data = parse_data(data)
    answer = 0
    logger.info(f"Puzzle1: Lowest: {answer}")
    answer = 0
    logger.info(f"Puzzle2: Complex: {answer}")
    
if __name__ == '__main__':
    main()