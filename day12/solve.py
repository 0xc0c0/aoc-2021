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
    directed_links = paths + [path[::-1] for path in paths]
    #update node dictionary for each end
    caves = dict()
    for a,b in directed_links:
        if a not in caves:
            caves[a] = list()
        caves[a].append(b)
    return caves

def is_big_cave(cave):
    return cave.isupper()

def get_all_paths(saved_path, cur_cave, tgt_cave, all_caves, twice_used=True):
    if cur_cave == tgt_cave:
        saved_path.append(cur_cave)
        logger.debug(f"Completed path: {saved_path}")
        return [saved_path]
    
    all_paths = list()
    for connected_cave in all_caves[cur_cave]:
        # can't re-use start
        if connected_cave == 'start':
            continue
        
        # skip small caves that have already been traversed
        # one ability to use a little cave twice, but only one
        local_twice_used = twice_used
        if connected_cave in saved_path and not is_big_cave(connected_cave):
            if local_twice_used:
                continue
            else:
                local_twice_used = True
        new_saved_path = saved_path + [cur_cave]
        new_paths = get_all_paths(new_saved_path, connected_cave, tgt_cave, all_caves, local_twice_used)
        #logger.debug(f"Partial paths: {new_paths}")
        for path in new_paths:
            if path:
                all_paths.append(path)
    return all_paths

def main():
    logger.setLevel(level=logging.INFO)
    data = get_file_data()
    caves = parse_data(data)
    all = get_all_paths(list(), 'start', 'end', caves)
    answer = len(all)
    logger.info(f"Puzzle1: <SUMMARY>: {answer}")
    
    all = get_all_paths(list(), 'start', 'end', caves, twice_used=False)
    answer = len(all)
    logger.info(f"Puzzle2: <SUMMARY>: {answer}")
    
if __name__ == '__main__':
    main()