import logging
import os
import numpy as np

INSTRUCTION_BLOCK_LENGTH = 18

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

def get_file_data(fn='input.txt'):
    with open(fn) as f:
        data = f.read()
    return data

def parse_instr(text):
    op_pieces = text.split()
    instr = dict()
    instr['op'] = op_pieces[0]
    instr['var1'] = op_pieces[1]
    if len(op_pieces) > 2:
        instr['var2'] = op_pieces[2]
    return instr

def parse_data(text_data):
    instructions = [parse_instr(line) for line in text_data.strip('\n').strip().split('\n')]
    return instructions

def valid_vars():
    return ['w', 'x', 'y', 'z']

def get_var2(instr, alu_vars):
    if instr['var2'] in valid_vars():
        return alu_vars[instr['var2']]
    else:
        return int(instr['var2'])

def run_instruction(i, alu_vars, input):
    if i['op'] == 'inp':
        i['var1']
        alu_vars[i['var1']] = int(input[alu_vars['input_seek']])
        alu_vars['input_seek'] += 1  # update seek pointer for input
    else:
        var2 = get_var2(i, alu_vars)
        if i['op'] == 'add':
            alu_vars[i['var1']] = alu_vars[i['var1']] + var2
        elif i['op'] == 'mul':
            alu_vars[i['var1']] = alu_vars[i['var1']] * var2
        elif i['op'] == 'div':
            if var2 == 0:
                return False
            alu_vars[i['var1']] = int(alu_vars[i['var1']] / var2)
        elif i['op'] == 'mod':
            alu_vars[i['var1']] = alu_vars[i['var1']] % var2
        elif i['op'] == 'eql':
            alu_vars[i['var1']] = 1 if alu_vars[i['var1']] == var2 else 0
    return True

def check_valid(alu_vars):
    return alu_vars['z'] == 0

def init_alu():
    return {
        'input_seek': 0,
        'w': 0,
        'x': 0,
        'y': 0,
        'z': 0
    }

def run_alu_program(instructions=list(), alu_vars=init_alu(), model_num='00000000000000'):
    if len(model_num) != 14:
        return False, 0, alu_vars
    
    total_blocks = int(len(instructions) / INSTRUCTION_BLOCK_LENGTH)
       
    for instr_block in range(total_blocks):
        first_instr = instr_block * INSTRUCTION_BLOCK_LENGTH
        end_instr = (instr_block + 1) * INSTRUCTION_BLOCK_LENGTH
        for i,instr in enumerate(instructions[first_instr:end_instr]):
            logger.debug(f"input_seek: {alu_vars['input_seek']}")
            status = run_instruction(i=instr, alu_vars=alu_vars, input=model_num)
            if status == False:
                return False, instr_block, alu_vars
        if alu_vars['z'] != 0:
            return False, instr_block, alu_vars
        
    return True, total_blocks, alu_vars

def find_largest_valid_model_num(instructions):
    model_num=[9] * 14
    current_index = 0
    current_val = 9
    status = False
    while status != True:
        model_num[current_index] = current_val
        model_string = ''.join([str(x) for x in model_num])
        logger.debug(f"attempting model number {model_string}")
        status, failed_block, alu_vars = run_alu_program(instructions=instructions, model_num=model_string)
        if status == False:
            logger.debug(f"failed block {failed_block}, w:{alu_vars['w']}, x:{alu_vars['x']}, y:{alu_vars['y']}, z:{alu_vars['z']}")
            current_index = failed_block
            current_val = model_num[failed_block]
            # if the current_val is 1, roll back index until there is a non-1 value
            while current_val == 1:
                current_index -= 1
                if current_index < 0:
                    return "Error"
                current_val = model_num[current_index]
                
            # now reduce the last good value by 1
            current_val -= 1
    return model_string
    

def main():
    logger.setLevel(level=logging.DEBUG)
    data = get_file_data()
    instructions = parse_data(data)
    model_num = find_largest_valid_model_num(instructions=instructions)
    answer = model_num
    logger.info(f"Puzzle1: <SUMMARY>: {answer}")
    answer = 0
    logger.info(f"Puzzle2: <SUMMARY>: {answer}")
    
if __name__ == '__main__':
    main()