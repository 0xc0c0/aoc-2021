import logging
import os
import numpy as np
import ast
import pandas as pd
from itertools import permutations

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

def get_rotations():
    perms = np.array(list(permutations([[1,0,0],[0,1,0],[0,0,1]])))
    multipliers = [[-1 if i=='1' else 1 for i in f"{n:03b}"] for n in range(8)]
    rotations = [p * m for p in perms for m in multipliers]
    return rotations

def find_rotation_from_pair(scans, matches, primary_scanner=None):
    scanners = matches.index.get_level_values('scanner').unique()
    if len(scanners) != 2:
        logger.error(f"Incorrect DataFrame presented to find_offset_from_pair")
        return None
    if primary_scanner != None and primary_scanner in scanners:
        s1 = primary_scanner
        s2 = [s for s in scanners if s != primary_scanner][0]
    else:
        s1, s2 = scanners
    
    
    
    for s1_b1, s1_b2 in matches.loc[s1].index:
        for s2_b1, s2_b2 in matches.loc[s2].index:
            d = matches.loc[s1,s1_b1,s1_b2]['distance_sq'] 
            if d != matches.loc[s2,s2_b1,s2_b2]['distance_sq']:
                continue
            for rot in get_rotations():
                diff1 = np.array(scans.loc[s1,s1_b1]) - np.array(scans.loc[s2,s2_b1]).dot(rot)
                diff2 = np.array(scans.loc[s1,s1_b2]) - np.array(scans.loc[s2,s2_b2]).dot(rot)

                #if they match, the rotation is correct
                if (diff1 == diff2).all():
                    #CHECK MATCHES FOR 12+ HERE
                    base = scans.query(f"scanner == {s1}")
                    check = rotate_translate_beacons(scans, s2, rot, diff1, save=False)
                    overlap = base.merge(check, how='inner', on=['x','y','z'])
                    if len(overlap) >= 12:
                        logger.debug(f"scanner {s2} is offset {diff1}, rotation {rot} relative to scanner {s1}")
                        return diff1, rot
                    break


def get_max_overlapping_beacons(scans, dists_sq, base_index=0, min_count=12, ignored_scanners=[]):
    base_scan = dists_sq.loc[base_index]
    match_count = 0
    ignored = ignored_scanners + [base_index]
    
    for test_index in dists_sq.index.levels[0]:
        if test_index in ignored:
            continue
        
        test_scan = dists_sq.loc[test_index]
        eq_dists = base_scan.merge(test_scan, on=['distance_sq'], how='inner')
        
        base_beacons = set()
        test_beacons = set()
        scanners = [base_index, test_index]
        for d in list(eq_dists['distance_sq']):
            tmp_matches = dists_sq.query(f"scanner in {scanners} and distance_sq == {d}")
            for record1 in tmp_matches.loc[base_index]:
                for record2 in tmp_matches.loc[test_index]:
                    pass
            
            matches = base_scan[base_scan.distance_sq == d].index.tolist()
            for m in matches:
                for b in m:
                    base_beacons.add(b)
            matches = test_scan[test_scan.distance_sq == d].index.tolist()
            for m in matches:
                for b in m:
                    test_beacons.add(b)
        
        base_matches = scans.query(f"scanner == {base_index} and beacon in {list(base_beacons)}")
        test_matches = scans.query(f"scanner == {test_index} and beacon in {list(test_beacons)}")
        
        
        test_count = len(base_matches)
        if test_count > match_count and test_count >= min_count:
            match_index = test_index
            match_count = test_count
            logger.debug(f"found overlap: scanners {base_index} and {test_index}, {match_count} beacons")
            logger.debug(f"found overlap: scanner {base_index} beacons: {base_matches}")
            logger.debug(f"found overlap: scanner {test_index} beacons: {test_matches}")
            match_matches = dists_sq.query(f"scanner in {scanners} and distance_sq in {list(eq_dists['distance_sq'])}")
            logger.debug(f"type of match_index is {type(match_index)}")
            return match_index, match_matches

        logger.debug(f"scanners {base_index} and {test_index} had {test_count} matches")
    return None, None

def rotate_translate_beacons(scans, scanner, rot, offset, save=True):
    rotated_scans = scans.query(f"scanner == {scanner}").dot(rot)
    rotated_scans = rotated_scans.rename(columns={0:'x',1:'y',2:'z'}) + offset
    if save:
        scans.update(rotated_scans)
    return rotated_scans

def align_scans(scans):
    dists_sq = get_scanned_beacon_distances(scans)
    remaining = list(scans.index.get_level_values('scanner').unique())
    scanners_to_review = [0]
    scanner = scanners_to_review.pop()
    completed_rotate_translate = [0]
    offsets = []
    while remaining:
        matched_index, matches = get_max_overlapping_beacons(scans, dists_sq, scanner, ignored_scanners=completed_rotate_translate)
        if matched_index == None:
            #completed this scanner, move on
            remaining.remove(scanner)
            if len(scanners_to_review) > 0:
                scanner = scanners_to_review.pop()
                
        else:
            offset, rot = find_rotation_from_pair(scans, matches, primary_scanner=scanner)
            #rotate and move all beacons to relative to scanner 0
            if matched_index not in completed_rotate_translate:
                logger.debug(f"matched_index {matched_index} not in {completed_rotate_translate}")
                rotate_translate_beacons(scans, matched_index, rot, offset)
                offsets.append(offset)
                completed_rotate_translate.append(matched_index)
            #add scanner to next set to search through for matches/reorientation
            if matched_index not in scanners_to_review:
                scanners_to_review.append(matched_index)
                
    logger.debug(f"completed {completed_rotate_translate} rotations")
    return offsets

def get_unique_beacons(scans):
    return len(scans.drop_duplicates())

def find_farthest_Manhattan_distance(offsets):
    max = 0
    for i, row1, in enumerate(offsets):
        for j, row2 in enumerate(offsets):
            if i == j:
                continue
            x1, y1, z1 = row1
            x2, y2, z2 = row2
            d = abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)
            if d > max:
                max = d
    return max

def main():
    logger.setLevel(level=logging.INFO)
    with open("input.txt") as f:
        data = f.read()
       
    scans = parse_data(data)
    offsets = align_scans(scans)
    answer = get_unique_beacons(scans)
    logger.info(f"Puzzle1: Number of Beacons: {answer}")
    answer = find_farthest_Manhattan_distance(offsets)
    logger.info(f"Puzzle2: Longest Manhattan Distance: {answer}")
    
if __name__ == '__main__':
    main()