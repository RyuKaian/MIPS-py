from BinaryNumber import Bin


labels = {}


def get_instructions(path):
    with open(path) as f:
        file = f.read().split('\n')
        raw_instructions = extract_labels([ins.strip() for ins in file if ins and ins[0] != '#'])
        return [format_instruction(i, ins) for i, ins in enumerate(raw_instructions) if ins],\
               [ins for ins in raw_instructions if ins]


def extract_labels(raw_instructions):
    global labels
    for i, instruction in enumerate(raw_instructions):
        if instruction.find(':') > -1:
            label_instruction = instruction.split(':')
            raw_instructions[i] = label_instruction[1].strip()
            labels[label_instruction[0]] = Bin(i)
    return raw_instructions


def format_instruction(instruct_pc, instruction):
    if instruction.startswith('`') and instruction.endswith('`') and len(instruction[1:-1]) == 32:
        instruction = instruction[1:-1]
    elif not instruction.isnumeric():
        instruction = [a.strip(',') for a in instruction.split()]

        for i, v in enumerate(instruction):
            if v.startswith('`') and v.endswith('`'):
                instruction[i] = Bin(v[1:-1])

        instruction_builder = [switch_instruction(instruction[0])]

        if instruction_builder[0] == Bin('000000', 'alu op'):
            if instruction[0] != 'nop':
                instruction_builder.append(switch_registers(instruction[2]))
                instruction_builder.append(switch_registers(instruction[3]))
                instruction_builder.append(switch_registers(instruction[1]))
                instruction_builder.append(switch_funct(instruction[0]))
            else:
                instruction_builder.append(Bin()[:26])
        elif instruction_builder[0] == Bin('10x011', 'lw/sw'):
            base_offset = instruction[2][:-1].split('(')
            instruction_builder.append(switch_registers(base_offset[1]))
            instruction_builder.append(switch_registers(instruction[1]))
            instruction_builder.append(Bin(int(base_offset[0]))[0:16])
        elif instruction_builder[0] == Bin('001000', 'addi'):
            instruction_builder.append(switch_registers(instruction[2]))
            instruction_builder.append(switch_registers(instruction[1]))
            instruction_builder.append(Bin(int(instruction[3]))[0:16])
        elif instruction_builder[0] == Bin('00001x', 'j/jal'):
            instruction_builder.append(labels.get(instruction[1])[0:26])
        elif instruction_builder[0] == Bin('000111', 'jra'):
            instruction_builder.append(Bin()[0:26])
        elif instruction_builder[0] == Bin('000100', 'beq'):
            instruction_builder.append(switch_registers(instruction[1]))
            instruction_builder.append(switch_registers(instruction[2]))
            instruction_builder.append((labels.get(instruction[3]) - Bin(instruct_pc + 1))[0:16])
        instruction = Bin.join(instruction_builder)
    return Bin(instruction)


def switch_instruction(instruction):
    instruction_opcodes = {
        'lw': Bin('100011'),
        'sw': Bin('101011'),
        'addi': Bin('001000'),
        'beq': Bin('000100'),
        'j': Bin('000010'),
        'jra': Bin('000111'),
        'jal': Bin('000011'),
    }
    if isinstance(instruction, Bin):
        return instruction
    return instruction_opcodes.get(instruction, Bin('000000', 'alu op'))


def switch_registers(register):
    tmp_register = register[1:]
    offset = 0
    if isinstance(register, Bin):
        return register
    elif not tmp_register.isnumeric():
        register_class, *tmp_register = tmp_register
        tmp_register = ''.join(tmp_register)
        if register_class == 'v':
            offset = 2 if 0 <= int(tmp_register) <= 1 else None
        elif register_class == 'a':
            offset = 4 if 0 <= int(tmp_register) <= 3 else None
        elif register_class == 't':
            offset = 8 if 0 <= int(tmp_register) <= 7 else 24 if 8 <= int(tmp_register) < 10 else None
        elif register_class == 's':
            offset = 16 if 0 <= int(tmp_register) <= 7 else None

    if offset is None:
        print('Invalid register number', register)
        exit()
    return Bin(offset + int(tmp_register))[0:5]


def switch_funct(instruction):
    funct_code = {
        'add': Bin('00000100000'),
        'sub': Bin('00000100010'),
        'and': Bin('00000100100'),
        'or': Bin('00000100101'),
        'slt': Bin('00000101010'),
        'nor': Bin('00000100111'),
    }

    if isinstance(instruction, Bin):
        return instruction
    return funct_code.get(instruction, Bin('00000000000', 'nop'))
