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

def count_full_traversals(completed_traversals):
    count = 0
    for t in completed_traversals:
        if t[0] == 'start':
            count += 1
    return count

def get_new_traversal(directed_paths, caves, tmp_path=list(), cur_cave='start', found_traversals=list()):
    new_path = tmp_path + [cur_cave]
    
    #check for invalid condition (hitting a small cave twice)
    if not is_big_cave(cur_cave) and cur_cave in tmp_path:
        return
    
    #check if we've already done this path
    if cur_cave == 'end':
        if (new_path not in found_traversals):
            found_traversals.append(new_path)
    else:
        next_cave_options = caves[cur_cave]
        for opt in next_cave_options:
                get_new_traversal(directed_paths=directed_paths, caves=caves, tmp_path=new_path, cur_cave=opt, found_traversals=found_traversals)
    

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