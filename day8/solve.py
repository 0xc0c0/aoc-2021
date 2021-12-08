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
       
    data = parse_data(data)
    answer1 = 0  #change this
    logger.info(f"Puzzle1: {answer1}")
    answer2 = 0  #change this
    logger.info(f"Puzzle2: {answer2}")

if __name__ == '__main__':
    main()