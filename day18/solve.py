import logging
import os
import numpy as np
import ast
from anytree import NodeMixin

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

def get_file_data(fn='input.txt'):
    with open(fn) as f:
        data = f.read()
    return data

def parse_data(text_data):
    snailnums = [list(ast.literal_eval(line)) for line in text_data.strip('\n').strip().split('\n')]
    return snailnums

def find_leftmost_deep_recursive(snailnum):
    for index1, entry1 in enumerate(snailnum):
        if type(entry1) == int:
            continue
        for index2, entry2 in enumerate(entry1):
            if type(entry2) == int:
                continue
            for index3, entry3 in enumerate(entry2):
                if type(entry3) == int:
                    continue
                for index4, entry4 in enumerate(entry3):
                    if type(entry4) == int:
                        continue
                    else:
                        logger.debug(f"found {entry4}")
                        return (index1, index2, index3, index4, entry4)
    return None

def find_nearest_right_int(snailnum, i1, i2, i3, i4):
    for i in range(i4 + 1,len(snailnum[i1][i2][i3])):
        logger.debug(f"trying snailnum[i1][i2][i3], index {i}, value {snailnum[i1][i2][i3][i]}")
        if type(snailnum[i1][i2][i3][i]) == int:
            return (i1, i2, i3, i)

    for i in range(snailnum[i1][i2]):
        
        
def find_nearest_left(snailnum, i1, i2, i3, i4):
    return None

def explode(snailnum, i1, i2, i3, i4):
    left, right = snailnum[i1][i2][i3][i4]
    # walk the dog to the right, first
    result = find_nearest_right(snailnum, i1, i2, i3, i4)
    if result:
        n1, n2, n3, n4 = result
        snailnum[n1][n2][n3][n4] += right
        
    result = find_nearest_left(snailnum, i1, i2, i3, i4)
    if result:
        n1, n2, n3, n4 = result
        snailnum[n1][n2][n3][n4] += left
    # walk the dog to the left, next
    
    # remove the original list
    del snailnum[i1][i2][i3][i4]
    

def reduce_snailnums(snailnums):
    pass

def main():
    logger.setLevel(level=logging.INFO)
    with open("input.txt") as f:
        data = f.read()
       
    data = parse_data(data)
    answer = 0
    logger.info(f"Puzzle1: <SUMMARY>: {answer}")
    answer = 0
    logger.info(f"Puzzle2: <SUMMARY>: {answer}")
    
if __name__ == '__main__':
    main()