import pytest
from .solve import *

@pytest.fixture
def test_data():
    with open('test.txt', 'r') as f:
        text = f.read()
    return text

@pytest.fixture
def test1_data():
    with open('test1.txt', 'r') as f:
        text = f.read()
    return text

@pytest.fixture
def test2_data():
    with open('test2.txt', 'r') as f:
        text = f.read()
    return text

@pytest.fixture
def test3_data():
    with open('test3.txt', 'r') as f:
        text = f.read()
    return text

@pytest.fixture
def test4_data():
    with open('test4.txt', 'r') as f:
        text = f.read()
    return text

def test_parse_input(test_data,
                     test1_data,
                     test2_data,
                     test3_data,
                     test4_data,):
    packets = parse_data(test_data)
    assert type(packets) == str
    assert len(packets) == 4 * 6
    
    packets = parse_data(test1_data)
    assert len(packets) == 4 * 18
    
    packets = parse_data(test2_data)
    assert len(packets) == 4 * 26
    
    packets = parse_data(test3_data)
    assert len(packets) == 4 * 28
    
    packets = parse_data(test4_data)
    assert len(packets) == 4 * 30
  
def test_all_part1(test_data,
             test1_data,
             test2_data,
             test3_data,
             test4_data,):
    packet_data = parse_data(test_data)
    packet, _ = decode_packet(packet_data)
    assert packet.version == 6
    assert packet.type == 4
    assert packet.value == 2021
    
    packet_data = parse_data(test1_data)
    packet, _ = decode_packet(packet_data)
    assert packet.version == 4
    assert packet.type != 4
    assert len(packet.op_subpackets) == 1
    p = packet.op_subpackets[0]
    assert p.version == 1
    assert p.type != 4
    assert len(p.op_subpackets) == 1
    p = p.op_subpackets[0]
    assert p.version == 5
    assert p.type != 4
    assert len(p.op_subpackets) == 1
    p = p.op_subpackets[0]
    assert p.version == 6
    assert p.type == 4
    assert p.value != -1
    
    packet_data = parse_data(test2_data)
    packet, _ = decode_packet(packet_data)
    assert packet.op_len == 2
    assert len(packet.op_subpackets) == 2
    p1 = packet.op_subpackets[0]
    assert p1.op_type == 0
    assert p1.op_len == 22
    assert len(p1.op_subpackets) == 2
    p2 = packet.op_subpackets[1]
    assert len(p2.op_subpackets) == 2
    assert get_packet_version_sum(packet) == 12
    
    packet_data = parse_data(test3_data)
    packet, _ = decode_packet(packet_data)
    assert get_packet_version_sum(packet) == 23
        
    packet_data = parse_data(test4_data)
    packet, _ = decode_packet(packet_data)
    assert get_packet_version_sum(packet) == 31
    
def test_all_part2():
    packet_data = parse_data('C200B40A82')
    packet, _ = decode_packet(packet_data)
    assert packet.value == 3
    
    packet_data = parse_data('04005AC33890')
    packet, _ = decode_packet(packet_data)
    assert packet.value == 54
    
    packet_data = parse_data('880086C3E88112')
    packet, _ = decode_packet(packet_data)
    assert packet.value == 7
    
    packet_data = parse_data('CE00C43D881120')
    packet, _ = decode_packet(packet_data)
    assert packet.value == 9
    
    packet_data = parse_data('D8005AC2A8F0')
    packet, _ = decode_packet(packet_data)
    assert packet.value == 1
    
    packet_data = parse_data('F600BC2D8F')
    packet, _ = decode_packet(packet_data)
    assert packet.value == 0
    
    packet_data = parse_data('9C005AC2F8F0')
    packet, _ = decode_packet(packet_data)
    assert packet.value == 0
    
    packet_data = parse_data('9C0141080250320F1802104A08')
    packet, _ = decode_packet(packet_data)
    assert packet.value == 1