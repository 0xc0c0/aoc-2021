import logging
import os
import numpy as np
import ast

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

def get_file_data(fn='input.txt'):
    with open(fn) as f:
        data = f.read()
    return data

def parse_data(text_data):
    
    blobs = [blob for blob in text_data.strip('\n').strip().split('\n\n')]
    scanner_data = list()
    for blob in blobs:
        scans = [ast.literal_eval(f"[{line}]") for line in blob.split('\n')[1:]]
        scanner_data.append(scans)
    return scanner_data

def get_scanned_beacon_distances(scans):
    lookup_distances_sq = dict()
    for beacon1 in scans:
        for beacon2 in scans:
            key = set(beacon1, beacon2)
            if beacon1 == beacon2 or key in lookup_distances_sq:
                continue
            #add distance calc
            x1, y1, z1 = beacon1
            x2, y2, z2 = beacon2
            lookup_distances_sq[key] = (x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2
    return lookup_distances_sq

def get_overlapping_beacon_count(lu1, lu2):
    for k1, v1 in enumerate(lu1):
        for k2, v2 in enumerate(lu2):
            if v1 == v2:
                logger.info(f"{k1} looks like it could match {k2}")
            

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