from collections import namedtuple

from BinaryNumber import Bin
from Gates import mux


def alu(bin1: Bin, bin2: Bin, alu_control: Bin):
    alu_results = [
        bin1 & bin2,
        bin1 | bin2,
        bin1 + bin2,
        bin1 << bin2,
        None,
        None,
        bin1 - bin2,
        bin1 < bin2,
        None,
        None,
        None,
        None,
        Bin(bin1 | bin2).not_(),
        None,
        None,
        None
    ]

    temp = namedtuple('alu', ['result'])
    return temp(mux(alu_results, alu_control))
