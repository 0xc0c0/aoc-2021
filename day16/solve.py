from binascii import hexlify, unhexlify
import errno
import logging
import numpy as np
import os
import math
from dataclasses import dataclass
from typing import List

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

def get_file_data(fn='input.txt'):
    with open(fn) as f:
        data = f.read()
    return data

def parse_data(text_data):
    hex_data = list(text_data.strip('\n').strip())
    binary_stream = "".join([f"{int(b, 16):0>4b}" for b in hex_data])
    return binary_stream

@dataclass
class Packet:
    version: int = -1
    type: int = -1
    value: int = -1
    
@dataclass
class OpPacket(Packet):
    op_type: int = -1
    op_len: int = -1
    op_subpackets: list = None

def decode_int(stream=None, bitlen=4, offset=0):
    if not stream or not (len(stream) >= bitlen):
        raise ValueError(errno)
    
    value = int(stream[offset:offset+bitlen], 2)
    if offset == 0:
        remaining_stream = stream[bitlen:]
    else:
        remaining_stream = None

    return value, remaining_stream

def decode_packet_header(stream=None, packet=None):
    if packet == None:
        packet = Packet()
    # logger.debug(f"Packet Stream: {stream}")
    packet.version, stream = decode_int(stream, 3)
    packet.type, stream = decode_int(stream, 3)
    # logger.debug(packet)
    return packet, stream

def decode_literal_packet(stream=None, packet=None):
    packet, stream = decode_packet_header(stream)

    more_bits, stream = decode_int(stream, 1)
    val, stream = decode_int(stream, 4)
    vals = [val]
    while more_bits and len(stream) >= 5:
        more_bits, stream = decode_int(stream, 1)
        val, stream = decode_int(stream, 4)
        vals.append(val)
    val_bits = "".join([f"{i:0>4b}" for i in vals])
    packet.value = int(val_bits, 2)
    logger.debug(f"Decoded Literal Value Packet: {packet}")
    return packet, stream

def decode_operator_packet(stream, packet=None):
    packet, stream = decode_packet_header(stream, packet=OpPacket())

    packet.op_type, stream = decode_int(stream, 1)
    packet.op_subpackets = list()
    if packet.op_type == 0:
        packet.op_len, stream = decode_int(stream, 15)
        substream = stream[:packet.op_len]
        stream = stream[packet.op_len:]
        logger.debug(f"OpPacket substream: {substream}")
        remaining_op_bits = packet.op_len
        while remaining_op_bits > 0:
            saved_len = len(substream)
            p, substream = decode_packet(substream)
            remaining_op_bits = saved_len - len(substream)
            if p:
                packet.op_subpackets.append(p)
            else:
                break 
        
    elif packet.op_type == 1:
        packet.op_len, stream = decode_int(stream, 11)
        remaining_op_packets = packet.op_len
        while remaining_op_packets > 0:
            p, stream = decode_packet(stream)
            remaining_op_packets -= 1
            if p:
                packet.op_subpackets.append(p)
            else:
                break
            
    t = packet.type

    if t == 0:
        packet.value = sum([p.value for p in packet.op_subpackets])
    elif t == 1:
        packet.value = math.prod([p.value for p in packet.op_subpackets])
    elif t == 2:
        packet.value = min([p.value for p in packet.op_subpackets])
    elif t == 3:
        packet.value = max([p.value for p in packet.op_subpackets])
    elif t == 5:
        packet.value = (packet.op_subpackets[0].value > packet.op_subpackets[1].value)
    elif t == 6:
        packet.value = (packet.op_subpackets[0].value < packet.op_subpackets[1].value)
    elif t == 7:
        packet.value = (packet.op_subpackets[0].value == packet.op_subpackets[1].value)

    logger.debug(f"Decoded Operator Packet: {packet}")
    return packet, stream        
        
def decode_packet(stream):
    if len(stream) < 11:
        return None, stream
    
    # look ahead for packet type
    packet_type, _ = decode_int(stream, bitlen=3, offset=3)
    
    # literal value packet
    if packet_type == 4:
        return decode_literal_packet(stream)
    # operator packet
    else:
        return decode_operator_packet(stream)

def get_packet_version_sum(packet):
    if isinstance(packet, OpPacket):
        sum = packet.version
        for p in packet.op_subpackets:
            sum += get_packet_version_sum(p)
        return sum
        
    elif isinstance(packet, Packet):
        return packet.version
    

def main():
    logger.setLevel(level=logging.INFO)
    with open("input.txt") as f:
        data = f.read()
       
    packet_data = parse_data(data)
    packet, _ = decode_packet(packet_data)
    answer = get_packet_version_sum(packet)
    logger.info(f"Puzzle1: Version Sum: {answer}")
    answer = packet.value
    logger.info(f"Puzzle2: Evaluated Packet Value: {answer}")
    
if __name__ == '__main__':
    main()