import logging
import math
import os
import numpy as np
import ast
from anytree import Node

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

def get_file_data(fn='input.txt'):
    with open(fn) as f:
        data = f.read()
    return data

def parse_data(text_data):
    snailnums = [list(ast.literal_eval(line)) for line in text_data.strip('\n').strip().split('\n')]
    return snailnums

def find_nearest_right_int(snailnum, i1, i2, i3, i4):
    for i in range(i4 + 1,len(snailnum[i1][i2][i3])):
        logger.debug(f"trying snailnum[i1][i2][i3], index {i}, value {snailnum[i1][i2][i3][i]}")
        if type(snailnum[i1][i2][i3][i]) == int:
            return (i1, i2, i3, i)

    for i in range(snailnum[i1][i2]):
        pass
        
def build_tree_from_list(snailnum=None, parent=None):
    if not snailnum:
        return None
    root = Node(name='Pair', parent=parent)
    for entry in snailnum:
        if type(entry) == int:
            n = Node(name=entry, parent=root)
        elif type(entry) == list:
            n = build_tree_from_list(snailnum=entry, parent=root)
    return root

def build_list_from_tree(n):
    if type(n.name) == int:
        return n.name
    else:
        pair = list()
        for c in n.children:
            pair.append(build_list_from_tree(c))
        return pair

def get_index(n):
    if n and n.parent:
        for i, p in enumerate(n.parent.children):
            if p == n:
                return i
    return None

def add(n1, n2):
    if not n1 or not n2 or type(n1.name) == int or type(n2.name) == int:
        raise ValueError(f"addition must be two Pairs")
    newroot = Node('Pair')
    n1.parent = newroot
    n2.parent = newroot
    logger.debug(f"added, not yet reduced: {build_list_from_tree(newroot)}")
    return newroot

def find_nearest_left_child_int(p, n_index=None):
    if n_index == None:
        n_index = len(p.children)
    for i in range(n_index - 1, -1, -1):
        tmp = p.children[i]
        if type(tmp.name) == int:
            return tmp
        else:
            check = find_nearest_left_child_int(tmp)
            if check:
                return check
    return None

def find_nearest_left_int(n):
    found = None
    while not found and not n.is_root:
        n_index = get_index(n)
        p = n.parent
        found = find_nearest_left_child_int(p, n_index)
        if found:
            return found
        n = n.parent
    return None

def find_nearest_right_child(p, n_index=None, sn_type=int, depth=None, thresh=None):
    if n_index == None:
        n_index = -1
    for i in range(n_index + 1, len(p.children)):
        tmp = p.children[i]
        if type(tmp.name) == sn_type:
            if sn_type == int:
                if not thresh or tmp.name >= thresh:
                    return tmp
            if sn_type == str:
                if not depth or tmp.depth == depth:
                    return tmp
        if type(tmp.name) == str:
            check = find_nearest_right_child(tmp, sn_type=sn_type, depth=depth, thresh=thresh)
            if check:
                return check
            
def find_nearest_right_int(n):
    found = None
    while not found and not n.is_root:
        n_index = get_index(n)
        p = n.parent
        found = find_nearest_right_child(p, n_index)
        if found:
            return found
        n = n.parent
    return None

def explode(n):
    if n.name != 'Pair':
        raise ValueError('Attempted to explode snailnum of wrong type')
    if len(n.children) != 2 or type(n.children[0].name) != int or type(n.children[1].name) != int:
        raise ValueError('Attempted to explode Pair of something other than two integers')
    # left side
    left = find_nearest_left_int(n)
    if left:
        left.name += n.children[0].name
    # right side
    right = find_nearest_right_int(n)
    if right:
        right.name += n.children[1].name
        
    #remove subordinate nodes and convert me to an int
    for x in n.children:
        x.parent = None
    n.name = 0  

def split(n):
    tmp = Node(name=math.floor(n.name / 2), parent=n)
    tmp = Node(name=math.ceil(n.name / 2), parent=n)
    n.name = 'Pair'

def reduce(n):
    reduction_needed = True
    while reduction_needed:
        deep_pair = find_nearest_right_child(n, sn_type=str, depth=4)
        if deep_pair:
            explode(deep_pair)
            continue
        first_10 = find_nearest_right_child(n, thresh=10)
        if first_10:
            split(first_10)
            continue
        reduction_needed = False

def add_all(snailnums):
    sum = build_tree_from_list(snailnums[0])
    for snailnum in snailnums[1:]:
        n = build_tree_from_list(snailnum)
        logger.debug(f"adding {build_list_from_tree(n)}...")
        sum = add(sum, n)
        reduce(sum)
    return sum

def magnitude(n):
    if type(n.name) == int:
        return n.name
    else:
        return (3 * magnitude(n.children[0])) + (2 * magnitude(n.children[1]))

def get_largest_magnitude_pair(snailnums):
    count = 0
    high = 0
    for a1 in snailnums:
        for a2 in snailnums:
            count += 1
            if a1 == a2:
                continue
            n1 = build_tree_from_list(a1)
            n2 = build_tree_from_list(a2)
            s = add(n1, n2)
            reduce(s)
            m = magnitude(s)
            if m > high:
                high = m
                logger.debug(f"new high: {high}, count: {count}")
    return high
            

def main():
    logger.setLevel(level=logging.INFO)
    with open("input.txt") as f:
        data = f.read()
       
    snailnums = parse_data(data)
    sum = add_all(snailnums)
    answer = magnitude(sum)
    logger.info(f"Puzzle1: Magnitude of Snailnum Addition: {answer}")
    answer = get_largest_magnitude_pair(snailnums)
    logger.info(f"Puzzle2: Highest Magnitude Addition of 2 Numbers: {answer}")
    
if __name__ == '__main__':
    main()