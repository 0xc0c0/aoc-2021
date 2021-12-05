import logging
import numpy as np
import os

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

def parse_line(text):
    return tuple([tuple([int(x) for x in x.split(',')]) for x in text.split(' -> ')])

def parse_data(text_data):
    text_data = text_data.strip().split('\n')
    lines = [parse_line(x) for x in text_data]
    logger.debug(lines[3])
    return lines

def find_matrix_dims(lines):
    points = [point for line in lines for point in line]
    all_x, all_y = list(zip(*points))
    #logging.debug(points)
    logger.info(f"x: min: {min(all_x)}, max: {max(all_x)}")
    logger.info(f"y: min: {min(all_y)}, max: {max(all_y)}")
    return max(all_x) + 1, max(all_y) + 1

def create_matrix(x,y):
    return np.array([0]*x*y).reshape((x,y))

def update_matrix(matrix, lines, diag=False):
    for line in lines:
        p1 = line[0]
        p2 = line[1]
        
        x1, y1 = p1
        x2, y2 = p2
        
        xd = x2 - x1
        yd = y2 - y1
        
        if xd > 0:
            rx = range(x1, x2 + 1, 1)
        elif xd < 0:
            rx = range(x1, x2 - 1, -1)
        
        if yd > 0:
            ry = range(y1, y2 + 1, 1)
        elif yd < 0:
            ry = range(y1, y2 - 1, -1)
        
        #vertical line
        if xd == 0:
            for y in ry:
                matrix[x1, y] += 1

        #horizonal line
        elif yd == 0:
            for x in rx:
                matrix[x, y1] += 1
                
        elif diag:
            for x, y in zip(rx, ry):
                matrix[x, y] += 1
    
    logger.debug(matrix)
    return matrix

def find_overlaps(matrix, threshold=2):
    overlaps = (matrix >= threshold)
    return list(zip(*np.where(overlaps)))

def main():
    logger.setLevel(level=logging.INFO)
    with open("input.txt") as f:
        data = f.read()
    lines = parse_data(data)
    
    #Part 1
    vents = create_matrix(*(find_matrix_dims(lines)))
    vents = update_matrix(vents, lines)
    more_than_2 = len(find_overlaps(vents))
    logger.info(f"Puzzle1: 2+ Overlaps: {more_than_2}")
            
    #Part 1
    vents = create_matrix(*(find_matrix_dims(lines)))
    vents = update_matrix(vents, lines, diag=True)
    more_than_2 = len(find_overlaps(vents))
    logger.info(f"Puzzle2: 2+ Overlaps: {more_than_2}")
    

if __name__ == '__main__':
    main()