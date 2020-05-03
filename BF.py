from bfi import interpret as bfi_interpret
from tqdm import tqdm


def find_closing_brackets(string, code_pointer):
	num_brackets = 1
	while num_brackets > 0:
		code_pointer += 1
		if string[code_pointer] == '[':
			num_brackets += 1
		elif string[code_pointer] == ']':
			num_brackets -= 1
	return code_pointer


def find_opening_brackets(string, code_pointer):
	num_brackets = -1
	while num_brackets < 0:
		code_pointer -= 1
		if string[code_pointer] == '[':
			num_brackets += 1
		elif string[code_pointer] == ']':
			num_brackets -= 1
	return code_pointer


def lengthen_list(lst, length):
	while len(lst) < length + 1:
		lst.append(0)


def run_brainfuck_code(string, do_tqdm=False):
	string = string.replace('\n', '').replace(' ', '')
	data = []
	code_pointer = 0
	data_pointer = 0
	lengthen_list(data, 0)
	if do_tqdm:
		t = tqdm(total=len(string))
		i = 0
	while code_pointer < len(string):
		if data_pointer < 0:
			print(code_pointer)
		com = string[code_pointer]
		if com == '<':
			data_pointer -= 1
		elif com == '>':
			data_pointer += 1
			lengthen_list(data, data_pointer)
		elif com == '+':
			data[data_pointer] += 1
			if (data[data_pointer] == 256):
				data[data_pointer] = 0
		elif com == '-':
			data[data_pointer] -= 1
			if (data[data_pointer] == -1):
				data[data_pointer] = 255
		elif com == '[':
			if data[data_pointer] == 0:
				code_pointer = find_closing_brackets(string, code_pointer)
			else:
				pass
		elif com == ']':
			code_pointer = find_opening_brackets(string, code_pointer)
			code_pointer -= 1
		elif com == '.':
			print(chr(data[data_pointer]), end='')
		elif com == ',':
			data[data_pointer] = ord(input()[0])
		else:
			pass
		code_pointer += 1
		# for tqdm:
		if do_tqdm:
			i += 1
			if i % 1000 == 0:
				t.n = code_pointer
				t.refresh()
	return data


def interpret(code, do_tqdm=False, show_data=True):
	if show_data:
		return run_brainfuck_code(code, do_tqdm=do_tqdm)
	else:
		print(bfi_interpret(code))
