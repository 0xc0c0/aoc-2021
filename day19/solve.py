import logging
import os
import numpy as np
import ast
import pandas as pd

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

def get_file_data(fn='input.txt'):
    with open(fn) as f:
        data = f.read()
    return data

def parse_data(text_data):
    
    blobs = [blob for blob in text_data.strip('\n').strip().split('\n\n')]
    #scanner_data = pd.DataFrame(None, columns=)
    scan_data = [[scanner_index] + [line_index] + ast.literal_eval(f"[{line}]") 
             for scanner_index, blob in enumerate(blobs) 
             for line_index, line in enumerate(blob.split('\n')[1:])]
    scans = pd.DataFrame(scan_data, columns=['scanner','beacon', 'x','y','z'])
    scans = scans.set_index(['scanner', 'beacon'])
    return scans

def get_scanned_beacon_distances(scans):
    dists_sq = pd.DataFrame([],columns=['scanner','beacon1','beacon2','distance_sq'])
    dists_sq = dists_sq.set_index(['scanner','beacon1','beacon2'])
    for scanner in scans.index.levels[0]:
        scan = scans.loc[scanner]
        for beacon1, point1 in scan.iterrows():
            tmp = list()
            for beacon2, point2 in scan[beacon1 + 1:].iterrows():
                #add distance_sq calc
                x1, y1, z1 = point1
                x2, y2, z2 = point2
                distance_sq = (x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2
                tmp.append([scanner, beacon1, beacon2, distance_sq])
            tmp_df = pd.DataFrame(data=tmp, columns=['scanner','beacon1','beacon2','distance_sq'])
            tmp_df = tmp_df.set_index(['scanner','beacon1','beacon2'])
            dists_sq = pd.concat([dists_sq, tmp_df])
    logging.debug(dists_sq)
    return dists_sq

def get_max_overlapping_beacons(dists_sq, base_index=0, min_count=12, ignore_scans=[]):
    base_scan = dists_sq.loc[base_index]
    match_count = 0
    match_index = None
    ignore_scans += [base_index]
    for test_index in dists_sq.index.levels[0]:
        if test_index in ignore_scans:
            continue
        
        test_scan = dists_sq.loc[test_index]
        eq_dist = base_scan.merge(test_scan, on=['distance_sq'], how='inner')
        test_count = len(eq_dist)
        if test_count > match_count:
            match_count = test_count
            match_index = test_index
        logger.debug(f"scanners {base_index} and {test_index} had {test_count} matches")

    return match_count, match_index

def find_orientation(dists_sq, index1, index2, min_count=12):
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