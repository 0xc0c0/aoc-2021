from asyncio.proactor_events import _ProactorDuplexPipeTransport
import logging
from unittest.mock import NonCallableMagicMock
import numpy as np
import os
import math
from collections import Counter

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

def get_file_data(fn='input.txt'):
    with open(fn) as f:
        data = f.read()
    return data

def parse_data(text_data):
    polymer_text, pair_rules_text = text_data.strip('\n').split('\n\n')
    polymer = list(polymer_text.strip())
    
    pair_rules = [line.split(' -> ') for line in pair_rules_text.split('\n')]
    rules = dict()
    for pair, result in pair_rules:
        if pair[0] not in rules:
            rules[pair[0]] = dict()
        rules[pair[0]][pair[1]] = result
    
    logging.debug(f"polymer: {polymer}")
    logging.debug(f"rules: {rules}")
    return polymer, rules

def parse_data_better(text_data):
    polymer_text, pair_rules_text = text_data.strip('\n').split('\n\n')
    polymer = list(polymer_text.strip())
    
    pair_rules = [line.split(' -> ') for line in pair_rules_text.split('\n')]
    rules = dict()
    for pair, result in pair_rules:
        rules[pair] = result
    
    logging.debug(f"polymer: {polymer}")
    logging.debug(f"rules: {rules}")
    return polymer, rules

def run_round(polymer_chain=None, rules=None):
    new_polymers = [None] * (len(polymer_chain) - 1)
    output = [None] * ((2 * len(polymer_chain)) - 1)
    for index, polymer in enumerate(polymer_chain):
        if index == len(polymer_chain) - 1:
            continue
        else:
            next = polymer_chain[index + 1]
            new_polymers[index] = rules[polymer][next]
    output[::2] = polymer_chain
    output[1::2] = new_polymers
    return output

def get_counts(polymer_chain):
    counts = {p:polymer_chain.count(p) for p in set(polymer_chain)}
    return counts

def get_high_low_computation(polymer_chain=None, counts=None):
    if not counts:
        counts = get_counts(polymer_chain)
    max_key = max(counts, key=counts.get)
    min_key = min(counts, key=counts.get)
    retval = counts[max_key] - counts[min_key]
    logging.debug(retval)
    return retval

def run_rounds(polymer_chain=None, rules=None, count=1):
    for i in range(count):
        polymer_chain = run_round(polymer_chain, rules)
    return polymer_chain
        
def init_counter(polymer_template):
    c = Counter()
    for index, p in enumerate(polymer_template):
        if index == len(polymer_template) - 1:
            continue
        c[p + polymer_template[index + 1]] += 1
    return c

def run_rounds_better(rules=None, rounds=1, template=None):
    pairs = init_counter(polymer_template=template)
    for i in range(rounds):
        next_pairs = Counter()
        for pair in pairs:
            next_pairs[pair[0] + rules[pair]] += pairs[pair]
            next_pairs[rules[pair] + pair[1]] += pairs[pair]
        pairs = next_pairs
        polymers = Counter()
        for pair in pairs:
            polymers[pair[0]] += pairs[pair]
        polymers[template[-1]] += 1
        logger.debug(f"polymers: {polymers} ")
    return polymers
    

def main():
    logger.setLevel(level=logging.INFO)
    with open("input.txt") as f:
        data = f.read()
       
    chain, rules = parse_data(data)
    chain = run_rounds(chain, rules, 10)
    answer = get_high_low_computation(chain)
    logger.info(f"Puzzle1: 10 Rounds of Polymerization: {answer}")
    chain, rules = parse_data_better(data)
    polymers = run_rounds_better(rules=rules, rounds=40, template=chain)
    answer = get_high_low_computation(counts=polymers)
    logger.info(f"Puzzle2: 40 Rounds of Polymerization: {answer}")
    
if __name__ == '__main__':
    main()