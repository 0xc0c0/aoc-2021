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
    #parse into list of links
    paths = [[x for x in line.split('-')] for line in text_data.strip('\n').strip().split('\n')]
    directed_paths = paths + [path[::-1] for path in paths]
    #update node dictionary for each end
    caves = dict()
    for a,b in directed_paths:
        if a not in caves:
            caves[a] = list()
        caves[a].append(b)
    return directed_paths, caves

def is_big_cave(cave):
    return cave.isupper()

def get_traversal(paths, caves, found_traversals=None):
    if not found_traversals:
        found_traversals = list()
    cur_cave = 'start'
    #look

def main():
    logger.setLevel(level=logging.INFO)
    data = get_file_data()
    graph = parse_data(data)
    
    answer = 0
    logger.info(f"Puzzle1: <SUMMARY>: {answer}")
    answer = 0
    logger.info(f"Puzzle2: <SUMMARY>: {answer}")
    
if __name__ == '__main__':
    main()