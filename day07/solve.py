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

def complex(num):
    return int(num * (num + 1) / 2)

def get_fuel_cost(data, align_pos, simple=True):
    logger.debug(f"checking fuel cost for alignment to value {align_pos}, simple={simple}")
    if simple:
        return sum([abs(align_pos - x) for x in data])
    else:
        return sum([complex(abs(align_pos - x)) for x in data])

def find_min_fuel_cost(data, median=True):
    if median:
        starting_i = int(len(data)/2)
    else:
        starting_i = int(sum(data)/len(data))
    starting_val = data[starting_i]
    starting = get_fuel_cost(data, starting_val, median)
    low_val = starting_val
    current = low = starting
    while current <= low:
        low = current
        low_val -= 1
        current = get_fuel_cost(data, low_val, median)
    
    high_val = starting_val
    current = high = starting
    while current <= high:
        high = current
        high_val += 1
        current = get_fuel_cost(data, high_val, median)
    
    return min([low,high])
    
def main():
    logger.setLevel(level=logging.INFO)
    with open("input.txt") as f:
        data = f.read()
       
    #Part 1  Full Simulation Algorithm
    data = parse_data(data)
    logger.info(f"Puzzle1: Lowest: {find_min_fuel_cost(data)}")
    logger.info(f"Puzzle2: Complex: {find_min_fuel_cost(data, median=False)}")
    
    #Part 2  Better Algorithm
    #tallies = parse_data_better(data)
    #age_rounds_better(tallies, rounds=256)
    #logger.info(f"Puzzle2: Fish: {sum(tallies)}")

if __name__ == '__main__':
    main()