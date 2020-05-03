from sys import argv
from BF import interpret
from Tests.test_HBF import transform_data, problematic_bits
from constants.CONSTANTS import M, N
from converters.ASM2HBF import ASM2HBF, split_ASM
from converters.main_converter import HBF2BF


def ASM2BF(ASM):
	print('got ASM code (untrimmed):')
	print('\n'.join(['{}: '.format(i) + f'{com:0{32}b}' for i, com in enumerate(split_ASM(ASM))]), end='\n\n')
	HBF = ASM2HBF(ASM)
	print('got HBF code (trimmed, real length: {}):'.format(len(HBF)))
	print(HBF[:1000], end='\n\n')
	BF = HBF2BF(HBF, N, M)
	print('got BF code (trimmed, real length: {}):'.format(len(BF)))
	print(BF[:1000], end='\n\n')
	return BF


def runASMasBF(ASM):
	BF = ASM2BF(ASM)
	interpret(BF, do_tqdm=False)


def main():
	file_path = 'samples/TEST.asm'
	if len(argv) == 2:
		file_path = argv[1]
	with open(file_path, 'rb') as f:
		ASM_CODE = f.read()

	BF = ASM2BF(ASM_CODE)
	print('problematic HBF parts:')
	print(problematic_bits(BF), end='\n\n')
	print('commands run:')
	data = interpret(BF, do_tqdm=False, show_data=False)
	print('finished running', end='\n\n')
	print('data:')
	data = transform_data(data, M, N)
	print(data)


if __name__ == '__main__':
	main()
