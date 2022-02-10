import logging
import os
import numpy as np

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

def get_file_data(fn='input.txt'):
    with open(fn) as f:
        data = f.read()
    return data

FIRST_RUN_DEBUG = False

def init_image(text_image):
    arr = [[1 if symbol == '#' else 0 for symbol in list(line.strip())] for line in text_image.strip('\n').strip().split('\n')]
    # returns 2 dimensional grid of 1s and 0s reflecting lights
    return np.array(arr, dtype=np.int8)
    
def init_enhancement(text_enhancement):
    arr = [1 if symbol == '#' else 0 for symbol in list(text_enhancement.strip('\n').strip())]
    return np.array(arr, dtype=np.int8)

def parse_data(text_data):
    text_enhancement, text_image = [blob for blob in text_data.strip('\n').strip().split('\n\n')]
    return init_enhancement(text_enhancement), init_image(text_image)

def get_binary(lights, row, col, outside=0):
    num = [0] * 9
    i = 0
    R, C = lights.shape
    # first get all the nearby pixels into a correctly arranged array
    for r in range(row - 1, row + 2):
        for c in range(col - 1, col + 2):
            if r < 0 or c < 0 or r >= R or c >= C:
                #basically, whether enhancement[0] is 1 or 0 translates to what infinity looks like
                num[i] = outside
            else:
                num[i] = lights[r,c]
            i += 1

    # convert the array to binary
    return int("".join(str(x) for x in num), 2)

def run_enhancement(enhancement, lights, infinity_state=0):
    global FIRST_RUN_DEBUG
    R, C = lights.shape
    if infinity_state == 1:
        new_lights = np.ones(shape=(R + 2, C + 2), dtype=np.int8)
    else:
        new_lights = np.zeros(shape=(R + 2, C + 2), dtype=np.int8)
    new_lights[1:-1:, 1:-1] = lights
    enhanced = np.copy(new_lights)
    
    #what does current infinity look like?
    #what will next infinity look like?
    current_infinity = infinity_state
    next_infinity = 1 if (enhancement[0] and infinity_state == 0) else 0

    for index, val in np.ndenumerate(new_lights):
        r, c = index
        enhancement_index = get_binary(new_lights, r, c, current_infinity)
        if FIRST_RUN_DEBUG:
            logger.debug(f"offset {r}, {c} uses enhancement index {enhancement_index}")
        enhanced[r, c] = enhancement[enhancement_index]
    FIRST_RUN_DEBUG = False
    logger.debug(enhanced)
    return enhanced, next_infinity

def count_lights(lights):
    return np.sum(lights)

def run(enhancement, lights, count=2):
    infinity_state = 0
    for c in range(count):
        lights, infinity_state = run_enhancement(enhancement, lights, infinity_state)
        logger.debug(f" iteration: {c}, inf st: {infinity_state}")
    return lights

def main():
    logger.setLevel(level=logging.INFO)
    with open("input.txt") as f:
        data = f.read()
       
    enhancement, lights = parse_data(data)
    lights = run(enhancement, lights)
    answer = count_lights(lights)
    logger.info(f"Puzzle1: Lights After 2 Enhancements: {answer}")
    lights = run(enhancement, lights, count=48)
    answer = count_lights(lights)
    logger.info(f"Puzzle2: Lights After 50 Enhancements: {answer}")
    
if __name__ == '__main__':
    main()