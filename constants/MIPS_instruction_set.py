"""
The compiled MIPS instructions byte code patterns
"""

instructions = {
	'NOOP': '0' * 32,
	'ADD': '000000ssssstttttddddd00000100000',
	'ADDI': '001000ssssstttttiiiiiiiiiiiiiiii',
	'ADDIU': '001001ssssstttttiiiiiiiiiiiiiiii',
	'ADDU': '000000ssssstttttddddd00000100001',
	'AND': '000000ssssstttttddddd00000100100',
	'ANDI': '001100ssssstttttiiiiiiiiiiiiiiii',
	'BEQ': '000100ssssstttttiiiiiiiiiiiiiiii',
	'BGEZ': '000001sssss00001iiiiiiiiiiiiiiii',
	'JMP': '000010iiiiiiiiiiiiiiiiiiiiiiiiii',
	'JAL': '000011iiiiiiiiiiiiiiiiiiiiiiiiii',
	'OR': '000000ssssstttttddddd00000100101',
	'ORI': '001101ssssstttttiiiiiiiiiiiiiiii',
	'XOR': '000000ssssstttttddddd-----100110',
	'JR': '000000sssss000000000000000001000',
	'BGEZAL': '000001sssss10001iiiiiiiiiiiiiiii',
	'BGTZ': '000111sssss00000iiiiiiiiiiiiiiii',
	'BLEZ': '000110sssss00000iiiiiiiiiiiiiiii',
	'BLTZ': '000001sssss00000iiiiiiiiiiiiiiii',
	'BLTZAL': '000001sssss10000iiiiiiiiiiiiiiii',
	'BNE': '000101ssssstttttiiiiiiiiiiiiiiii',
	'XORI': '001110ssssstttttiiiiiiiiiiiiiiii',
	'LB': '100000ssssstttttiiiiiiiiiiiiiiii',
	'LW': '100011ssssstttttiiiiiiiiiiiiiiii',
	'LUI': '001111-----tttttiiiiiiiiiiiiiiii',
	'SLL': '000000ssssstttttdddddhhhhh000000',
	'SRL': '000000-----tttttdddddhhhhh000010',
	'SLLV': '000000ssssstttttddddd-----000100',
	'SB': '101000ssssstttttiiiiiiiiiiiiiiii',
	'SLT': '000000ssssstttttddddd00000101010',
	'SLTI': '001010ssssstttttiiiiiiiiiiiiiiii',
	'SRA': '000000-----tttttdddddhhhhh000011',
	'SRLV': '000000ssssstttttddddd00000000110',
	'SW': '101011ssssstttttiiiiiiiiiiiiiiii',
	'MFLO': '0000000000000000ddddd00000010010',
	'MULT': '000000sssssttttt0000000000011000'
}
