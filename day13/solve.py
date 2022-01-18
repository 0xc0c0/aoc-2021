import logging
import numpy as np
import os
import math
import re
import pandas as pd

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

def get_file_data(fn='input.txt'):
    with open(fn) as f:
        data = f.read()
    return data

def parse_data(text_data):
    dots_text, folds_text = text_data.strip('\n').split('\n\n')
    dots_data = [[int(x.strip()) for x in line.split(',')] for line in dots_text.split('\n')]
    
    text_lines = [line for line in folds_text.split('\n')]
    folds_data = list()
    for line in text_lines:
        fold = re.sub(r'fold along ([xy]=[0-9]*)', '\\1', line).split('=')
        folds_data.append([fold[0], int(fold[1])])
    
    return dots_data, folds_data

def find_max(dots_data, folds_data):
    dots_x, dots_y = list(zip(*dots_data))
    folds_x = [entry[1] * 2 for entry in folds_data if entry[0] == 'x']
    folds_y = [entry[1] * 2 for entry in folds_data if entry[0] == 'y']
    all_x = list(dots_x) + folds_x
    all_y = list(dots_y) + folds_y
    logger.debug(f"max_x = {max(all_x)}, max_y = {max(all_y)}")
    return (max(all_x) + 1, max(all_y) + 1)

def create_dotmap(dots_data, folds_data):
    size = find_max(dots_data, folds_data)
    b = np.zeros(size, int)
    
    for x,y in dots_data:
        b[x][y] = 1
    logger.debug(b)
    return b

def fold_map(dotmap, fold):
    if fold[0] == 'x':
        x_fold = fold[1]
        # all points above 'x' value get mapped to inverse below 'x' value
        # y stays the same
        for (x,y), val in np.ndenumerate(dotmap):
            if val == 1 and x > x_fold:
                new_x = (2 * x_fold) - x
                dotmap[new_x][y] = 1
                dotmap[x][y] = 0
        s = list(dotmap.shape)
        s[0] = x_fold
        dotmap = dotmap[:x_fold,:]
    elif fold[0] == 'y':
        y_fold = fold[1]
        # all points above 'y' value get mapped to inverse below 'y' value
        # x stays the same
        for (x,y), val in np.ndenumerate(dotmap):
            if val == 1 and y > y_fold:
                new_y = (2 * y_fold) - y
                dotmap[x][new_y] = 1
                dotmap[x][y] = 0
        s = list(dotmap.shape)
        s[1] = y_fold
        dotmap = dotmap[:,:y_fold]
    logger.debug(dotmap)
    return dotmap

def count_dots(dotmap):
    return len(np.where(dotmap == 1)[0])

def fold_map_all(dotmap, folds):
    for f in folds:
        dotmap = fold_map(dotmap, f)
    return dotmap

def main():
    logger.setLevel(level=logging.INFO)
    with open("input.txt") as f:
        data = f.read()
    
    dots, folds = parse_data(data)
    map = create_dotmap(dots, folds)
    fold_map(map, folds[0])
    answer = count_dots(map)
    logger.info(f"Puzzle1: <SUMMARY>: {answer}")
    
    map = create_dotmap(dots, folds)
    map = fold_map_all(map, folds)
    answer = np.transpose(map)
    logger.info(f"Puzzle2: saved to answer.txt")
    np.savetxt('answer.txt', answer, delimiter=' ', fmt='%d')
    
if __name__ == '__main__':
    main()