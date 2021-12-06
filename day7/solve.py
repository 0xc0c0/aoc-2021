import logging
import numpy as np
import os
import math

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

def parse_data(text_data):
    text_data = text_data.strip().split(',')
    fish = [int(x) for x in text_data]
    logger.debug(fish)
    return fish

def parse_data_better(text_data):
    text_data = text_data.strip().split(',')
    tallies = [0] * 9
    fish = [int(x) for x in text_data]
    for f in fish:
        tallies[f] += 1
    return tallies

def age_fish(fish):
    stop = len(fish)
    for i, f in enumerate(fish):
        if i == stop:
            break
        if f == 0:
            fish[i] = 6
            fish.append(8)
        else:
            fish[i] -= 1
            
def age_fish_better(tallies):
    saved_0 = 0
    for age, tally in enumerate(tallies):
        if age == 0:
           saved_0 = tally
        if age < 8:
           tallies[age] = tallies[age + 1]
        if age == 6:
            tallies[age] += saved_0
        if age == 8: 
            tallies[age] = saved_0
            
def age_fish_7(fish):
    stop = len(fish)
    for i, f in enumerate(fish):
        if i == stop:
            break
        if f >= 7:
            fish[i] = f - 7
        else:
            fish.append(f + 2)

def age_fish_7_better(tallies):
    saved_tallies = tallies.copy()
    
    #update copies + 2 (modeled after 7 rounds)
    for i in range(7):
        tallies[i + 2] += saved_tallies[i]
       
    #adjust for 7s and 8s
    for i in range(7,9):
        tallies[i] -= saved_tallies[i]
        tallies[i - 7] += saved_tallies[i]

def age_rounds(fish, rounds):
    runs_1 = rounds % 7
    runs_7 = math.floor(rounds / 7)
    for i in range(runs_7):
        age_fish_7(fish)
    for i in range(runs_1):
        age_fish(fish)

def age_rounds_better(tallies, rounds):
    logger.debug(f"tallies: {tallies}, rounds: {rounds}")
    runs_1 = rounds % 7
    runs_7 = math.floor(rounds / 7)
    for i in range(runs_7):
        age_fish_7_better(tallies)
    for i in range(runs_1):
        age_fish_better(tallies)
    logger.debug(f"new tallies: {tallies}")

def main():
    logger.setLevel(level=logging.INFO)
    with open("input.txt") as f:
        data = f.read()
       
    #Part 1  Full Simulation Algorithm
    fish = parse_data(data)
    age_rounds(fish, rounds=80)
    logger.info(f"Puzzle1: Fish: {len(fish)}")
    
    #Part 2  Better Algorithm
    tallies = parse_data_better(data)
    age_rounds_better(tallies, rounds=256)
    logger.info(f"Puzzle2: Fish: {sum(tallies)}")

if __name__ == '__main__':
    main()