import collections
import heapq
import functools
import bisect
from tqdm import tqdm


def read_input(path: str = 'input.txt'):
    commands = []
    registers = {'A': 0, 'B': 0, 'C': 0}
    passed_registers = False
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()

            if not line:
                passed_registers = True
                continue

            if passed_registers:
                commands = [int(ele) for ele in line.replace('Program: ', "").split(',')]
            else:
                line = line.replace('Register ', "").split(': ')
                registers[line[0]] = int(line[1])
    return registers, commands


def adv(operand: int, registers: dict[str:int], instruction_pointer: int, sysout: list, debug: bool):
    # op code: 0
    if debug:
        print(adv.__name__)
    registers['A'] >>= combo(operand, registers)
    return instruction_pointer + 2


def bxl(operand: int, registers: dict[str:int], instruction_pointer: int, sysout: list, debug: bool):
    # op code 1
    if debug:
        print(bxl.__name__)
    registers['B'] ^= operand
    return instruction_pointer + 2


def bst(operand: int, registers: dict[str:int], instruction_pointer: int, sysout: list, debug: bool):
    # op code 2
    if debug:
        print(bst.__name__)
    registers['B'] = combo(operand, registers)&7
    return instruction_pointer + 2


def jnz(operand: int, registers: dict[str:int], instruction_pointer: int, sysout: list, debug: bool):
    # op code 3
    if debug:
        print(jnz.__name__)
    if registers['A'] == 0:
        return instruction_pointer + 2
    else:
        return operand


def bxc(operand: int, registers: dict[str:int], instruction_pointer: int, sysout: list, debug: bool):
    # op code 4
    if debug:
        print(bxc.__name__)
    registers['B'] ^= registers['C']
    return instruction_pointer + 2


def out(operand: int, registers: dict[str:int], instruction_pointer: int, sysout: list, debug: bool):
    # op code 5
    if debug:
        print(out.__name__)
    sysout.append(combo(operand, registers)&7)
    return instruction_pointer + 2


def bdv(operand: int, registers: dict[str:int], instruction_pointer: int, sysout: list, debug: bool):
    # op code: 6
    if debug:
        print(bdv.__name__)
    registers['B'] = registers['A'] >> combo(operand, registers)
    return instruction_pointer + 2


def cdv(operand: int, registers: dict[str:int], instruction_pointer: int, sysout: list, debug: bool):
    # op code: 7
    if debug:
        print(cdv.__name__)
    registers['C'] = registers['A'] >> combo(operand, registers)
    return instruction_pointer + 2


def combo(operand, registers: dict[str:int]):
    if operand < 4:
        return operand
    elif operand < 7:
        return registers[chr(ord('A')+(operand-4))]
    else:
        raise ValueError('Operand is off.')


def main1():

    # get the input
    registers, commands = read_input()
    instructions = {0: adv, 1: bxl, 2: bst, 3: jnz, 4: bxc, 5: out, 6: bdv, 7: cdv}
    instruction_pointer = 0
    sysout = []
    debug = False
    while instruction_pointer < len(commands):
        instruction_pointer = instructions[commands[instruction_pointer]](commands[instruction_pointer+1], registers, instruction_pointer, sysout, debug)
        if debug:
            print(instruction_pointer, registers, sysout)
            print()
    print(f'The result for solution 1 is: {",".join(map(str, sysout))}')


def step(a_register):
    # This is simply the instructions coded by my program!
    # the program basically takes the last three bits of the a_register, makes some deterministic
    # calculations on them (two XORs)
    #
    # the main trick is that it uses all upper leftover parts of a for a XOR calculation, therefore we
    # need backtracking.

    # get the last three bits into b
    b_register = a_register&7

    # xor b with 2
    b_register = b_register ^ 2

    # get upper a bits into the c register
    c_register = a_register >> b_register

    # xor b with 3
    b_register = b_register ^ 3

    # xor b with c
    b_register = b_register ^ c_register

    # get the last three bits of b
    return b_register&7


def backtracking(a_register, cdx, commands):
    # check whether we are finished

    if cdx > len(commands):
        # we are finished but went one step too far
        return True, a_register >> 3

    # check whether we are wrong
    if step(a_register) != commands[-cdx]:
        return False, a_register

    # test several values for the next three bits of a
    for nx in range(8):
        didit, val = backtracking((a_register << 3) + nx, cdx+1, commands)
        if didit:
            return True, val
    return False, a_register


def main2():

    # get the input
    registers, commands = read_input()

    # go through the numbers in the instructions and create a three bits by three bits
    for idx in range(8):
        didit, val = backtracking(idx, 1, commands)
        if didit:
            print(f'The result for solution 2 is: {val}.')
            return
    raise ValueError('Solution not found.')


if __name__ == '__main__':
    main1()
    main2()
