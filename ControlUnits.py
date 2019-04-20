from BinaryNumber import Bin


def control_unit(op_code: Bin):
    titles = [
        'reg_dst',
        'jump',
        'branch',
        'mem_read',
        'mem_to_reg',
        'alu_op',
        'mem_write',
        'alu_src',
        'reg_write',
        'link',
        'return_address'
    ]

    op0, op1, op2, op3, op4, op5 = op_code

    signals = [
        (op5.not_() & op4.not_() & op3.not_() & op2.not_() & op1.not_() & op0.not_())[0],
        (op5.not_() & op4.not_() & op3.not_() & op1)[0],
        (op5.not_() & op4.not_() & op3.not_() & op2 & op1.not_() & op0.not_())[0],
        (op5 & op4.not_() & op3.not_() & op2.not_() & op1 & op0)[0],
        (op5 & op4.not_() & op3.not_() & op2.not_() & op1 & op0)[0],
        (op5.not_() & op4.not_() & op3.not_() & op2.not_() & op1.not_() & op0.not_())[0].concatenate(
            (op5.not_() & op4.not_() & op3.not_() & op2 & op1.not_() & op0.not_())[0]),
        (op5 & op4.not_() & op3 & op2.not_() & op1 & op0)[0],
        (op5 & op4.not_() & op2.not_() & op1 & op0 | (
            op5.not_() & op4.not_() & op3 & op2.not_() & op1.not_() & op0.not_()))[0],
        (((op4.not_() & op3.not_() & op2.not_()) & ((op5 & op1 & op0) | (op5.not_() & op1.not_() & op0.not_()))) | (
            op5.not_() & op4.not_() & op3 & op2.not_() & op1.not_() & op0.not_()))[0],
        (op5.not_() & op4.not_() & op3.not_() & op2.not_() & op1 & op0)[0],
        (op5.not_() & op4.not_() & op3.not_() & op2 & op1 & op0)[0]
    ]
    return dict(zip(titles, signals))


def alu_control_unit(alu_op: Bin, funct: Bin):
    if not alu_op:
        return Bin('0010', 'add')
    if alu_op[0]:
        return Bin('0110', 'sub')
    if funct == Bin('100000'):
        return Bin('0010', 'add')
    if funct == Bin('100010'):
        return Bin('0110', 'sub')
    if funct == Bin('100100'):
        return Bin('0000', 'and')
    if funct == Bin('100101'):
        return Bin('0001', 'or')
    if funct == Bin('101010'):
        return Bin('0111', 'slt')
    if funct == Bin('100111'):
        return Bin('1100', 'nor')
    if funct == Bin('000000'):
        return Bin('0011', 'sll')
