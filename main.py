from collections import namedtuple

from ALU import alu
from BinaryNumber import Bin
from ControlUnits import control_unit, alu_control_unit
from Gates import mux
from ReadInput import get_instructions
from Register import Register

########################################################################################################################

register_count = 32
mem_size = 128
infinite_loop_counter = {}

########################################################################################################################

instruction_mem_bin = []
registers = [Register(i) for i in range(register_count)]
data_mem = [Bin() for _ in range(mem_size)]
pc = Bin()
ra = registers[31]
if_id = (None, None, None)
id_ex = (None, None, None, None, None, None)
ex_mem = (None, None, None, None, None)
mem_wb = (None, None, None, None, None)
flush = False

########################################################################################################################


def instruction_fetch():
    global pc
    temp = namedtuple('Instruction_Fetch', ['pc_4', 'instruction', 'instruction_eng'])
    if pc is not None:
        try:
            instruction, instruction_eng, pc = instruction_mem_bin[int(pc)], instruction_mem_eng[int(pc)], pc + Bin(1)
            return temp(pc, instruction, instruction_eng)
        except IndexError:
            return temp(None, None, None)


def instruction_decode(pc_4: Bin, instruction: Bin, instruction_eng):
    temp = namedtuple('Instruction_Decode', [
        'read_data1', 'read_data2', 'sign_extend', 'write_reg', 'control_signal', 'instruction_eng'
    ])
    global flush
    if pc_4 is None or instruction is None or flush:
        flush = False
        return temp(None, None, None, None, None, None)

    control_signal = control_unit(instruction[26:32])
    read_data1 = registers[int(instruction[21:26])]
    read_data2 = registers[int(instruction[16:21])]
    sign_extended = instruction[0:16].sign_extend(32)
    write_reg = mux([read_data2, registers[int(instruction[11:16])]], control_signal.pop('reg_dst'))

    jump_branch_handling(pc_4, sign_extended, instruction, read_data1, read_data2, control_signal)

    return temp(read_data1, read_data2, sign_extended, write_reg, control_signal, instruction_eng)


def jump_branch_handling(pc_4, sign_extended, instruction, read_data1, read_data2, control_signal):
    global flush, pc, infinite_loop_counter
    branch_address = pc_4 + sign_extended
    jump_address = mux([pc_4[26:32].concatenate(instruction[0:26]),
                        ra.read_data()], control_signal.pop('return_address'))
    zero = read_data1.read_data() == read_data2.read_data()
    branch = control_signal.pop('branch') & zero
    jump = control_signal.pop('jump')

    if control_signal.pop('link'):
        ra.write_data(pc_4)

    next_address = mux([pc_4, branch_address], branch)
    pc = mux([next_address, jump_address], jump)
    if branch | jump:
        flush = True

    if not infinite_loop_counter.get(str(pc)):
        infinite_loop_counter[str(pc)] = 0
    infinite_loop_counter[str(pc)] += 1


def execution(read_data1: Register, read_data2: Register,
              sign_extend: Bin, write_reg: Register, control_signal: dict, instruction_eng):
    temp = namedtuple('Execution', ['alu_result', 'write_data', 'write_reg', 'control_signal', 'instruction_eng'])
    if read_data1 is None or\
            read_data2 is None or\
            sign_extend is None or\
            write_reg is None or\
            control_signal is None:
        return temp(None, None, None, None, None)

    alu_control = alu_control_unit(control_signal.pop('alu_op'), sign_extend[0:6])
    read_data_2_alu = mux([read_data2.read_data(), sign_extend], control_signal.pop('alu_src'))
    alu_out = alu(read_data1.read_data(), read_data_2_alu, alu_control)

    return temp(alu_out.result, read_data2, write_reg, control_signal, instruction_eng)


def memory(alu_result: Bin, write_data: Register, write_reg: Register, control_signal: dict, instruction_eng):
    temp = namedtuple('Memory', [
        'read_data', 'alu_result', 'write_reg', 'control_signal', 'instruction_eng'
    ])
    if alu_result is None or\
            write_data is None or\
            write_reg is None or\
            control_signal is None:
        return temp(None, None, None, None, None)

    if control_signal.pop('mem_write'):
        data_mem[int(alu_result)] = write_data.read_data()
    if control_signal.pop('mem_read'):
        read_data = data_mem[int(alu_result)]
    else:
        read_data = None

    return temp(read_data, alu_result, write_reg, control_signal, instruction_eng)


def write_back(read_data: Bin, alu_result: Bin, write_reg: Register, control_signal: dict, instruction_eng):
    temp = namedtuple('Write_back', ['instruction_eng'])
    if (read_data is None and alu_result is None) or write_reg is None or control_signal is None:
        return temp(False)

    if control_signal.pop('reg_write'):
        write_data = mux([alu_result, read_data], control_signal.pop('mem_to_reg'))
        write_reg.write_data(write_data)
    return temp(instruction_eng)


if __name__ == '__main__':
    instruction_mem_bin, instruction_mem_eng = get_instructions('Instructions.txt')
    for i in zip(instruction_mem_bin, instruction_mem_eng):
        print(i)
    # exit()
    print()
    print('#######################################################################################################')
    while True:
        if_id, id_ex, ex_mem, mem_wb, wb = instruction_fetch(), \
                                           instruction_decode(*if_id), \
                                           execution(*id_ex), \
                                           memory(*ex_mem), \
                                           write_back(*mem_wb)

        if all([False for v in (if_id + id_ex + ex_mem + mem_wb + wb) if v]):
            break

        if any([True for a in infinite_loop_counter.values() if a == 10]):
            print('Infinite loop breaking now')
            break

        print(if_id)
        print(id_ex)
        print(ex_mem)
        print(mem_wb)
        print(wb)
        print()
        print('Memory content', [(i, v) for i, v in enumerate(data_mem) if v])
        print('Register content', [(i, v.read_data()) for i, v in enumerate(registers) if v.read_data()])
        print('#######################################################################################################')

    print('Exited')
    print(if_id)
    print(id_ex)
    print(ex_mem)
    print(mem_wb)
    print(wb)
    print()
    print('Memory content', [(i, v) for i, v in enumerate(data_mem) if v])
    print('Register content', [(i, v.read_data()) for i, v in enumerate(registers) if v.read_data()])
    print('#######################################################################################################')
