import struct
from typing import TypedDict, NewType


UInt8  = NewType('UInt8',  int)  # uint8_t:  0-255
UInt32 = NewType('UInt32', int)  # uint32_t: 0-4294967295

# Packet type
PACKET_STATE = 0x01

# Flags bitmask — indicates which fields were updated in this packet
FLAG_LX       = 0x01
FLAG_LY       = 0x02
FLAG_RX       = 0x04
FLAG_RY       = 0x08
FLAG_SWITCHES = 0x10

# Packet format: type(B) flags(B) seq(I) lx(B) ly(B) rx(B) ry(B) switches(B)
# '>' = big-endian, I = uint32
PACKET_FORMAT = '>BBIBBBBB'
PACKET_SIZE   = struct.calcsize(PACKET_FORMAT)  # 11 bytes


class StatePacket(TypedDict):
    type:     UInt8
    flags:    UInt8   # bitmask of FLAG_* constants
    seq:      UInt32
    lx:       UInt8   # 0-100
    ly:       UInt8   # 0-100
    rx:       UInt8   # 0-100
    ry:       UInt8   # 0-100
    switches: UInt8   # 8-bit bitmask, bit N = switch N+1


def pack(packet: StatePacket) -> bytes:
    return struct.pack(PACKET_FORMAT,
        packet['type'],
        packet['flags'],
        packet['seq'],
        packet['lx'],
        packet['ly'],
        packet['rx'],
        packet['ry'],
        packet['switches'],
    )

def unpack(data: bytes) -> StatePacket:
    type_, flags, seq, lx, ly, rx, ry, switches = struct.unpack(PACKET_FORMAT, data)
    return StatePacket(type=type_, flags=flags, seq=seq,
                       lx=lx, ly=ly, rx=rx, ry=ry, switches=switches)


# --- Switches mask helpers ---

def switches_to_mask(switches: dict[int, bool]) -> UInt8:
    """switches: {1: True, 2: False, ...} — 1-indexed, max 8"""
    mask = 0
    for index, state in switches.items():
        if state:
            mask |= (1 << (index - 1))
    return UInt8(mask)

def mask_to_switches(mask: UInt8) -> dict[int, bool]:
    return {i + 1: bool(mask & (1 << i)) for i in range(8)}


# Test
def test():
    packet: StatePacket = {
        'type':     PACKET_STATE,
        'flags':    FLAG_LX | FLAG_RX | FLAG_SWITCHES,
        'seq':      42,
        'lx':       50,
        'ly':       0,
        'rx':       75,
        'ry':       100,
        'switches': switches_to_mask({1: True, 3: True}),
    }

    packed = pack(packet)
    print(f'Packed ({len(packed)}B): {packed.hex()}')

    unpacked = unpack(packed)
    print(f'Unpacked: {unpacked}')
    print(f'Switches: {mask_to_switches(unpacked["switches"])}')


if __name__ == '__main__':
    test()
