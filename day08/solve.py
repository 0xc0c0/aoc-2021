import logging
import numpy as np
import os
import math

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

def parse_data(text_data):
    lines = text_data.strip('\n').strip().split('\n')
    entries = [[e[0].split(), e[1].split()] for e in (line.split(' | ') for line in lines)]
    for e in entries:
        e[0].sort(key=len)
        e[0] = [''.join(sorted(x)) for x in e[0]]
        e[1] = [''.join(sorted(x)) for x in e[1]]
    logger.debug(entries[0:4])
    return entries

def create_decoder(signals):
    out = {
        #lowest will be a '1', etc.
        signals[0]: 1,
        signals[1]: 7,
        signals[2]: 4,
        signals[9]: 8
    }
    #next, find the '9'
    six_segments_indices = [6,7,8]
    for n in six_segments_indices:
        matched=True
        for c in signals[2]:
        # all '4' segments are in the '9'
            if c not in signals[n]:
                matched=False
                break
        if matched:
            out[signals[n]] = 9
            six_segments_indices.remove(n)
    
    #next, find the '0', which is the one that's not the 9 that contains the '7'
    for i in six_segments_indices:
        matched=True
        for c in signals[1]:
            if c not in signals[i]:
                matched=False
                break
        if matched:
            out[signals[i]] = 0
            six_segments_indices.remove(i)
    
    #last is the 6
    out[signals[six_segments_indices[0]]] = 6
    
    #on to the 5's
    five_segment_indices = [3,4,5]
    for i in five_segment_indices:
        matched = True
        # '1' is within the '3'
        for c in signals[0]:
            if c not in signals[i]:
                matched=False
                break
        if matched:
            out[signals[i]] = 3
            five_segment_indices.remove(i)
    
    #'2' and '5' are left
    #'5' is in the '6'
    for i in five_segment_indices:
        matched = True
        j = [k for k, v in out.items() if v == 6][0]
        for c in signals[i]:
            if c not in j:
                matched = False
                break
        if matched:
            out[signals[i]] = 5
            five_segment_indices.remove(i)
            
    #last one is a two
    out[signals[five_segment_indices[0]]] = 2
    return out
    

def count_easy(output):
    count = 0
    decoder = { 
        2: 1,
        3: 7,
        4: 4,
        7: 8
    }
    for e in output:
        if len(e) in decoder:
            count += 1
    return count

def count_all_easy(entries):
    count = 0
    for _, output in entries:
        count += count_easy(output)
    return count

def get_output_sum(entries):
    sum = 0
    for signals, output in entries:
        decoder = create_decoder(signals)
        #reframe output as a number before adding to total
        digits = []
        for digit in output:
            digits += [str(decoder[digit])]
        sum += int(''.join(digits))
    return sum
    
def main():
    logger.setLevel(level=logging.INFO)
    with open("input.txt") as f:
        data = f.read()
       
    data = parse_data(data)
    answer1 = count_all_easy(data)
    logger.info(f"Puzzle1: {answer1}")
    answer2 = get_output_sum(data)
    logger.info(f"Puzzle2: {answer2}")

if __name__ == '__main__':
    main()