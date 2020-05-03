"""
This file converts compiled ASM code into high-brainfuck code.
It both creates HBF code to setup the memory, and creates HBF code to read MIPS commands from memory and run them.
"""

from constants import MIPS_instruction_set
from constants.CONSTANTS import *
from converters import MIPS2HBF

"""
PATTERNS - The MIPS binary command patterns we have.
MIPS_TO_HBF_CODE - Each MIPS command with it's corresponding HBF code to run it.
TESTS - Each MIPS command and the HBF to determine whether the matrix we're currently looking at contains it.
"""
PATTERNS = {inst: MIPS_instruction_set.instructions[inst].replace('t', '?').replace('s', '?').replace('d', '?')
	.replace('i', '?').replace('h', '?').replace('-', '?') for inst in MIPS_instruction_set.instructions}
PATTERNS.pop('NOOP')
MIPS_TO_HBF_CODE = MIPS2HBF.instructions
TESTS = {PAT: '>(setb{})<(and)(equate_b{})'.format(PATTERNS[PAT].replace('0', '1').replace('?', '0'),
                                                   PATTERNS[PAT].replace('?', '0'))
         for PAT in PATTERNS}


def check_pattern(command, pattern):
	for i in range(BYTE_SIZE):
		if pattern[i] != '?' and (command >> i) & 1 != int(pattern[i]):
			return False
	return True


def split_ASM(assembly_code):
	commands = []
	i = 0
	for char in assembly_code:
		n = char
		if i == 0:
			commands.append(n)
			i = 1
		else:
			commands[-1] = (commands[-1] << 8) + n
			i = (i + 1) % 4
	if i != 0:
		return commands[:-1]
	return commands


def print_command(command):
	com = str(bin(command)[2:])
	print(com[:len(com) % 4], end=' ')
	for i in range(len(com) // 4):
		print(com[len(com) % 4 + i * 4:len(com) % 4 + (i + 1) * 4], end=' ')
	print()


def setup_memory(assembly_code):
	# setup registers
	HBFcode = '(on_flag6)(on_flag17)'
	HBFcode += '>' * NUM_REGISTERS
	HBFcode += '>'  # LO: special MULT/DIV register
	HBFcode += '>'  # HI: special MULT/DIV register

	# write the commands into memory
	ASM_CODE = split_ASM(assembly_code)
	HBFcode += '(on_flag7)>(on_flag11)'
	for command in ASM_CODE:
		HBFcode += '(set' + str(command) + ')'
		HBFcode += '>'

	# setup ALU segment
	HBFcode += '(on_flag8)'
	HBFcode += '>(on_flag14)'
	HBFcode += '>' * (ALU_SIZE - 1)

	# setup MEM segment
	HBFcode += '(on_flag9)'
	HBFcode += '>'

	# setup stack segment
	HBFcode += '(on_flag10)'
	HBFcode += '(on_flag12)'

	# go back to start
	HBFcode += '(go_back_to_flag11)'

	return HBFcode


def write_main_loop():
	"""
	Each command we run must start and finish on ALU#0
	Commands are copied to ALU#0
	"""

	code = "(while_not_flag8)"  # the flag at the end of the code segment
	code += "(copy_to_flag8)(goto_flag8)"

	# the rest of the commands
	# TODO: remove the next line, designed for testing only
	if False: code += '(printb)'
	for key in PATTERNS:
		code += '(copy_over1)>'
		# do starts at ALU0
		code += '{' + TESTS[key] + '${<' + MIPS_TO_HBF_CODE[key] + '(go_back_to_flag8)(zero)>}$<'
	# we're now in ALU cell #0
	code += '}' * len(PATTERNS)

	code += '(go_back_to_flag11)'
	# back at instruction pointer

	# "increment" instruction pointer
	code += "(off_flag11)>(on_flag11)"  # move ip forward. n need to worry about jmp, it is made in a way in which you end up one before where you are jumping to
	code += "(end_while_not_flag8)"
	return code


def ASM2HBF(ASM):
	"""
	Converts ASM binary code to HBF.
	Does so by first creating HBF initialising the memory, then HBF code that runs ASM commands from memory
	"""
	setup = setup_memory(ASM)
	loop = write_main_loop()
	return setup + loop
