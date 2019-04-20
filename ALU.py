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
    alu_out = mux(alu_results, alu_control)

    if alu_out is not None:
        temp = namedtuple('alu', ['result', 'zero'])
        return temp(alu_out, Bin(alu_out) == Bin(0))
