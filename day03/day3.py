import logging
import binascii

def parse_line(text_line):
    text = text_line.strip()
    return int(text, base=2)

def parse_data(text_data):
    text_data = text_data.strip().split('\n')
    logging.debug(text_data)
    code_length = len(text_data[0].strip())
    codes = []
    for line in text_data:
        codes.append(parse_line(line))
    return codes, code_length

def get_code_masks(code_length):
    masks = []
    for i in range(code_length):
        masks.append(2 ** i)
    masks.sort(reverse=True)
    return masks

def get_most_common_bit(codes, mask):
    count_0 = 0
    count_1 = 0
    for code in codes:
        if (code & mask) == mask:
            count_1 += 1
        else:
            count_0 += 1
    if count_1 >= count_0:
        return 1
    else:
        return 0

def get_gamma_rate(codes, code_length):
    gr = 0
    for mask in get_code_masks(code_length=code_length):
        bit = get_most_common_bit(codes, mask)
        if bit == 1:
            gr += mask
    return gr

def get_epsilon_rate(gr, code_length):
    return ~gr & (2 ** code_length - 1)

def get_ox_gen_rating(codes, code_length):
    masks = get_code_masks(code_length=code_length)
    local_codes = codes.copy()
    for mask in masks:
        bit = get_most_common_bit(local_codes, mask)
        local_codes = [code for code in local_codes if (code & mask) == (bit * mask)]
        logging.debug(local_codes)
        if len(local_codes) == 1:
            return local_codes[0]

def get_co2_scrubber_rating(codes, code_length):
    masks = get_code_masks(code_length=code_length)
    local_codes = codes.copy()
    for mask in masks:
        bit = get_most_common_bit(local_codes, mask)
        local_codes = [code for code in local_codes if (code & mask) == ((bit ^ 1) * mask)]
        logging.debug(local_codes)
        if len(local_codes) == 1:
            return local_codes[0]

def main():
    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.INFO)
    with open("input.txt") as f:
        data = f.read()
    codes, code_len = parse_data(data)
    
    #Part 1
    gr = get_gamma_rate(codes, code_length=code_len)
    er = get_epsilon_rate(gr, code_length=code_len)
    logger.info(f"Puzzle1: Gamma Rate: {gr}, Epsilon Rate: {er}")
    logger.info(f"Puzzle1: Answer: Power Consumption {gr * er}") 
    
    #Part 2
    ogr = get_ox_gen_rating(codes, code_length=code_len)
    co2r = get_co2_scrubber_rating(codes, code_length=code_len)
    logger.info(f"Puzzle1: Oxygen Generator Rating: {ogr}, CO2 Scrubber Rating: {co2r}")
    logger.info(f"Puzzle1: Answer: Life Support Rating {ogr * co2r}") 

if __name__ == '__main__':
    main()