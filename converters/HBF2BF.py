"""
Every function in this file corresponds to one HBF function.
The python function convert the HBF string to a a mix of HBF and BF.
If you take HBF code and run it through every one of these function sequentially and in reverse order, you will get
your BF code.

The conversions happen as follows:
f1: HBF intersection with f1 command            -> BF
f2: HBF intersection with f1,f2 commands        -> BF
f3: HBF intersection with f1,f2,f3 commands     -> BF
.
.
.
fn: HBF intersection with f1...fn-1 commands    -> BF
"""


def three_d_brainfuck(code, n, m):
	code = code.replace(">", ">" * n * m)
	code = code.replace("(up)", ">" * m)
	code = code.replace("(left)", ">")
	code = code.replace("<", "<" * n * m)
	code = code.replace("(down)", "<" * m)
	code = code.replace("(right)", "<")
	return code


def if_not_0_brainfuck(code, n, m):
	code = code.replace("}", "(left)](right)")
	code = code.replace("{", (("[-(left)+(left)+(right)(right)]"
	                           "(left)(left)[-(right)(right)+(left)(left)](right)(right)(up)") * n)[:-4] +
	                    "(left)" + ("[[-](left)+(right)]"
	                                "(left)"
	                                "[-(right)(down)[-]+(up)(left)]"
	                                "(right)(down)") * (n - 1) +
	                    "[[-](right)")
	return code


def save_load_brainfuck(code, n, m):
	save_code = "(left)(left)(left)(left)[-](right)(right)(right)(right)" + \
	            "[-(left)(left)+(left)(left)+(right)(right)(right)(right)]" \
	            + "(left)(left)[-(right)(right)+(left)(left)](right)(right)"
	load_code = "[-](left)(left)(left)(left)" + \
	            "[-(right)(right)+(right)(right)+(left)(left)(left)(left)]" + \
	            "(right)(right)[-(left)(left)+(right)(right)](right)(right)"
	code = code.replace("(save_all)", "(up)".join([save_code] * n) + "(down)" * (n - 1))
	code = code.replace("(load_all)", "(up)".join([load_code] * n) + "(down)" * (n - 1))
	parts = code.split("(save")
	new_code = parts[0]
	for part in parts[1:]:
		sub_parts = part.split(")")
		rest = ")".join(sub_parts[1:])
		num = int(sub_parts[0])
		new_code += "(up)" * num + save_code + "(down)" * num
		new_code += rest
	code = new_code
	parts = code.split("(load")
	new_code = parts[0]
	for part in parts[1:]:
		sub_parts = part.split(")")
		rest = ")".join(sub_parts[1:])
		num = int(sub_parts[0])
		new_code += "(up)" * num + load_code + "(down)" * num
		new_code += rest
	return new_code


def add_next_brainfuck(code, n, m):
	add_code = "(left)" + "(up)" * (n - 1) + "++(right)" + "(down)" * (n - 1) + \
	           ">(save_all)" + \
	           "(up)".join(["[-]"] * (n)) + \
	           "(down)" * (n - 1)
	for i in range(0, n):
		add_code += "(load" + str(i) + ")" + \
		            "(up)" * i + \
		            "[-<[-(up)]+" + \
		            "(left)--[++(up)--]++" + \
		            "(right)[[-]" + "(down)" * (n - 17) + "(left)(left)(left)[-]+(right)(right)(right)" + "(up)" * (
				            n - 17) + "]>" + \
		            "(down)" * (n - 1 - i) + \
		            "]" + "(down)" * i
	add_code += "(load_all)<(left)" + "(up)" * (n - 1) + "--(right)" + "(down)" * (n - 1)
	return code.replace("(add)", add_code)


def go_to_flag_brainfuck(code, n, m):
	parts = code.split("(goto_flag")
	new_code = parts[0]
	for part in parts[1:]:
		num = int(part.split(")")[0])
		new_code += "(up)" * num + "(left)(left)(left)-[+>-]+(right)(right)(right)" + "(down)" * num
		new_code += part[len(str(num) + ")"):]
	return new_code


def go_back_to_flag(code, n, m):
	parts = code.split("(go_back_to_flag")
	new_code = parts[0]
	for part in parts[1:]:
		num = int(part.split(")")[0])
		new_code += "(up)" * num + "(left)(left)(left)-[+<-]+(right)(right)(right)" + "(down)" * num
		new_code += part[len(str(num) + ")"):]
	return new_code


def set_flag_brainfuck(code, n, m):
	parts = code.split("(on_flag")
	new_code = parts[0]
	for part in parts[1:]:
		num = int(part.split(")")[0])
		new_code += "(up)" * num + "(left)(left)(left)[-]+(right)(right)(right)" + "(down)" * num
		new_code += part[len(str(num) + ")"):]
	parts = new_code.split("(off_flag")
	newer_code = parts[0]
	for part in parts[1:]:
		num = int(part.split(")")[0])
		newer_code += "(up)" * num + "(left)(left)(left)[-](right)(right)(right)" + "(down)" * num
		newer_code += part[len(str(num) + ")"):]
	return newer_code


# current matrix holds x, advances the next appearance of the flag by x matrices
# works with up to 16 bits
def advance_flag_brainfuck(code, n, m):
	parts = code.split("(advance_flag")
	new_code = parts[0]
	for i, part in enumerate(parts[1:]):
		num = int(part.split(")")[0])
		new_code += "(save_all)(on_flag0)"
		weight = 1
		for i in range(0, min(n, 16)):
			new_code += "(up)" * i + "[-" + "(down)" * i + \
			            "(goto_flag" + str(num) + ")(off_flag" + str(num) + ")" + \
			            ">" * weight + "(on_flag" + str(num) + ")(go_back_to_flag0)" + \
			            "(up)" * i + "]" + "(down)" * i
			weight *= 2
		new_code += "(load_all)(off_flag0)" + part[len(str(num) + ")"):]
	return new_code


def not_brainfuck(code, n, m):
	not_code = "(left)+(right)[-(left)-(right)](left)[-(right)+(left)](right)(up)" * (n - 1) + "(down)" * (n - 1)
	code = code.replace("(not)", not_code)
	return code


def zero_brainfuck(code, n, m):
	return code.replace("(zero)", "[-](up)" * (n - 1) + "(down)" * (n - 1))


def and_brainfuck(code, n, m):
	and_code = "(save_all)(zero)>(save_all)(zero)"
	for i in range(0, n):
		and_code += "(load" + str(i) + "){<(load" + str(i) + ")>(zero)}"
	and_code += "(load_all)<"
	return code.replace("(and)", and_code)


def or_brainfuck(code, n, m):
	return code.replace("(or)", "(not)>(not)<(and)(not)>(not)<")


def setb_brainfuck(code, n, m):
	parts = code.split("(setb")
	new_code = parts[0]
	for part in parts[1:]:
		new_code += "(zero)"
		sub_parts = part.split(")")
		rest = ")".join(sub_parts[1:])
		for digit in sub_parts[0][::-1]:
			if (digit == "1"):
				new_code += "+"
			new_code += "(up)"
		new_code += "(down)" * len(sub_parts[0]) + rest
	return new_code


def set_brainfuck(code, n, m):
	parts = code.split("(set")
	new_code = parts[0]
	for part in parts[1:]:
		if part[0] != 'b':
			sub_parts = part.split(")")
			rest = ")".join(sub_parts[1:])
			new_code += "(setb" + bin(int(sub_parts[0]))[2:] + ")" + rest
		else:
			new_code += '(set' + part
	return new_code


# current matrix holds x, sets the next appearance of the flag to be x
def copy_to_flag_brainfuck(code, n, m):
	parts = code.split("(copy_to_flag")
	new_code = parts[0]
	for part in parts[1:]:
		sub_parts = part.split(")")
		rest = ")".join(sub_parts[1:])
		num = sub_parts[0]
		new_code += "(save_all)(on_flag0)(goto_flag" + num + ")(zero)(go_back_to_flag0)"
		for i in range(0, n):
			new_code += "(up)" * i + \
			            "[-" + "(down)" * i + "(goto_flag" + num + ")" + "(up)" * i + "+" + "(down)" * i + "(go_back_to_flag0)" + "(up)" * i + "]" + \
			            "(down)" * i
		new_code += "(load_all)(off_flag0)" + rest
	return new_code


# same, but backwards
def copy_behind_to_flag_brainfuck(code, n, m):
	parts = code.split("(copy_behind_to_flag")
	new_code = parts[0]
	for part in parts[1:]:
		sub_parts = part.split(")")
		rest = ")".join(sub_parts[1:])
		num = sub_parts[0]
		new_code += "(save_all)(on_flag0)(go_back_to_flag" + num + ")(zero)(goto_flag0)"
		for i in range(0, n):
			new_code += "(up)" * i + \
			            "[-" + "(down)" * i + "(go_back_to_flag" + num + ")" + "(up)" * i + "+" + "(down)" * i + "(goto_flag0)" + "(up)" * i + "]" + \
			            "(down)" * i
		new_code += "(load_all)(off_flag0)" + rest
	return new_code


# loads the data saved in load to next appearance of flag
def load_to_flag_brainfuck(code, n, m):
	parts = code.split("(load_to_flag")
	new_code = parts[0]
	for part in parts[1:]:
		sub_parts = part.split(")")
		rest = ")".join(sub_parts[1:])
		num = sub_parts[0]
		new_code += "(on_flag0)(goto_flag" + num + ")(zero)(go_back_to_flag0)"
		for i in range(0, n):
			new_code += "(up)" * i + "(left)(left)[-](left)(left)" \
			                         "[-(right)(right)+(right)(right)" + "(down)" * i + "(goto_flag" + num + ")" + "(up)" * i + "+" + "(down)" * i + "(go_back_to_flag0)" + "(up)" * i + "(left)(left)(left)(left)]" + \
			            "(right)(right)[-(left)(left)+(right)(right)]" + \
			            "(down)" * i + "(right)(right)"
		new_code += "(off_flag0)" + rest
	return new_code


# current matrix holds x, advances the previous appearance of the flag by x matrices
def advance_behind_flag_brainfuck(code, n, m):
	parts = code.split("(advance_behind_flag")
	new_code = parts[0]
	for part in parts[1:]:
		sub_parts = part.split(")")
		rest = ")".join(sub_parts[1:])
		num = sub_parts[0]
		'''new_code += "(save_all)(on_flag1)(go_back_to_flag" + num + ")(save_all)(goto_flag1)" + \
					"(copy_behind_to_flag" + num + ")(go_back_to_flag" + num + ")(load_to_flag1)" + \
					"(advance_flag" + num + ")(on_flag2)(goto_flag1)(copy_behind_to_flag2)(go_back_to_flag2)(off_flag2)" + \
					"(goto_flag1)(off_flag1)(load_all)" + '''
		new_code += "(save_all)(on_flag1)(go_back_to_flag" + num + ")(save_all)(goto_flag1)" + \
		            "(copy_behind_to_flag" + num + ")(go_back_to_flag" + num + ")(load_to_flag1)" + \
		            "(advance_flag" + num + ")(on_flag2)(save_all)(goto_flag1)(copy_behind_to_flag2)(go_back_to_flag2)(off_flag2)" + \
		            "(load_to_flag1)(goto_flag1)(off_flag1)" + \
		            rest
	return new_code


def inc_brainfuck(code, n, m):
	return advance_behind_flag_brainfuck(code.replace("(inc)", "(up)" * (n - 1) + "(left)++(right)" + "(down)" * (
			n - 1) + "[-(up)]+(left)--[++(up)--](right)[-]" + "(down)" * (n - 1)), n, m)


# sets the next appearance of flag 3 to be the number of matrices between current cell
# and previous appearance of the parameter flag
def dist_from_flag_brainfuck(code, n, m):
	parts = code.split("(dist_to_flag")
	new_code = parts[0]
	for part in parts[1:]:
		sub_parts = part.split(")")
		rest = ")".join(sub_parts[1:])
		num = int(sub_parts[0])
		new_code += "(on_flag0)(on_flag1)(goto_flag3)(zero)(go_back_to_flag0)(left)(left)(left)" + \
		            "(up)" * num + "-[+" + "(down)" * num + "(right)(right)(right)(off_flag0)<(on_flag0)" + \
		            "(goto_flag3)(inc)(go_back_to_flag0)(left)(left)(left)" + "(up)" * num + "-]+" + \
		            "(down)" * num + "(right)(right)(right)" + "(off_flag0)(goto_flag1)(off_flag1)" + rest
	return new_code


# loads the value of parameter flag into mem column at the flag's row
def load_flag_brainfuck(code, n, m):
	parts = code.split("(load_flag")
	new_code = parts[0]
	for part in parts[1:]:
		sub_parts = part.split(")")
		rest = ")".join(sub_parts[1:])
		num = int(sub_parts[0])
		new_code += "(up)" * num + "[-](left)(left)[-](left)[-(right)+(right)(right)+(left)(left)(left)](right)[-(left)+(right)](right)(right)" + "(down)" * num + rest
	return new_code


# syntax: (if_flag4)${do stuff}$
# the stuff only happens if flag 4 is on
def if_flag_brainfuck(code, n, m):
	parts = code.split("(if_flag")
	new_code = parts[0]
	for part in parts[1:]:
		sub_parts = part.split(")")
		rest = ")".join(sub_parts[1:])
		num = int(sub_parts[0])
		new_code += "(left)(left)" + "(up)" * num + "[-](left)[-(right)+" + "(down)" * num + "(right)+(left)(left)" + "(up)" * num + "]" + \
		            "(right)[-(left)+(right)](right)" + "(down)" * num + "[[-](right)" + \
		            rest[2:]
	new_code = new_code.replace("}$", "(left)](right)")
	return new_code


# syntax: (equate_b1001)${do stuff}$
# the stuff only happens if it was equal 1001
def equate_b_brainfuck(code, n, m):
	parts = code.split("(equate_b")
	new_code = parts[0]
	for part in parts[1:]:
		sub_parts = part.split(")")
		rest = ")".join(sub_parts[1:])
		num = sub_parts[0]
		new_code += "(save_all)(on_flag4)"
		for digit in num[::-1]:
			if (digit == '1'):
				new_code += "-"
			new_code += "(up)"
		new_code += "(down)" * len(num) + "{(off_flag4)}(load_all)(if_flag4)"
		rest = "${(off_flag4)" + rest[2:]
		new_code += rest
	return new_code


# syntax: like equate_b but the number is not binary ( so: (equate5)${do stuff}$ )
def equate_brainfuck(code, n, m):
	parts = code.split("(equate")
	new_code = parts[0]
	for part in parts[1:]:
		if part[0] != '_':
			sub_parts = part.split(")")
			rest = ")".join(sub_parts[1:])
			new_code += "(equate_b" + bin(int(sub_parts[0]))[2:] + ")" + rest
		else:
			new_code += '(equate' + part
	return new_code


# syntax: (while_not_flag4) do stuff (end_while_not_flag4)
def while_not_flag_brainfuck(code, n, m):
	parts = code.split("(while_not_flag")
	new_code = parts[0]
	for part in parts[1:]:
		sub_parts = part.split(")")
		rest = ")".join(sub_parts[1:])
		num = int(sub_parts[0])
		new_code += "(left)(left)(left)" + "(up)" * num + "-[+(right)(right)(right)" + "(down)" * num + rest
	parts = new_code.split("(end_while_not_flag")
	newer_code = parts[0]
	for part in parts[1:]:
		sub_parts = part.split(")")
		rest = ")".join(sub_parts[1:])
		num = int(sub_parts[0])
		newer_code += "(left)(left)(left)" + "(up)" * num + "-]+(right)(right)(right)" + "(down)" * num + rest
	return newer_code


def xor_brainfuck(code, n, m):
	xor_code = "(not)(save_all)(not)>(save_all)(zero)"
	for i in range(0, n):
		xor_code += "(load" + str(i) + "){<(load" + str(i) + ")>(zero)}"
	xor_code += '(load_all)<'
	return code.replace("(xor)", xor_code)


# sets flag number 5 to hold the negativity bit of the matrix value
def neg_flag(code, n, m):
	return code.replace("(neg_flag)",
	                    "(off_flag5)" + "(up)" * (n - 2) + "(right)(right)" +
	                    "[-](left)(left)" +
	                    "[-(left)(left)+(left)" + "(down)" * (n - 7) + "+" + "(up)" * (
			                    n - 7) + "(right)(right)(right)]" +
	                    "(left)(left)[-(right)(right)+(left)(left)](right)(right)" + "(down)" * (n - 2))


def negate_number_brainfuck(code, n, m):
	return code.replace("(negate_number)", "(not)(inc)")


def sub_brainfuck(code, n, m):
	return code.replace("(sub)", ">(negate_number)<(add)>(negate_number)<")


def shift_left_brainfuck(code, n, m):
	shift_left_code = "(up)" * (n - 2) + "[-]" + "(down)[-(up)+(down)]" * (n - 2)
	return code.replace("(shift_left)", shift_left_code)


def shift_right_brainfuck(code, n, m):
	shift_right_code = "[-]" + "(up)[-(down)+(up)]" * (n - 2) + "(down)" * (n - 2)
	return code.replace("(shift_right)", shift_right_code)


# destroys the second place after it!!!!!!!!!!!!!
def mult_brainfuck(code, n, m):
	mult_code = ">>(on_flag1)<(copy_to_flag1)>(off_flag1)<(on_flag1)<(copy_to_flag1)(zero)>(off_flag1)>(save_all)(zero)"
	for i in range(0, n - 1):
		mult_code += "(load" + str(i) + "){<<(add)>>(zero)}<(shift_left)>"
	mult_code += "(load_all)<(on_flag1)>(copy_behind_to_flag1)<<"
	return code.replace("(mult)", mult_code)


def copy_over_brainfuck(code, n, m):
	parts = code.split("(copy_over")
	new_code = parts[0]
	for part in parts[1:]:
		sub_parts = part.split(")")
		rest = ")".join(sub_parts[1:])
		num = int(sub_parts[0])
		new_code += '(save_all)'
		new_code += ('>' * num + '[-]' + '<' * num + '[[-]' + '>' * num + '+' + '<' * num + ']' + '(up)') * n
		new_code += '(down)' * n
		new_code += '(load_all)'
		new_code += rest
	return new_code


def copy_back_over_brainfuck(code, n, m):
	parts = code.split("(copy_back_over")
	new_code = parts[0]
	for part in parts[1:]:
		sub_parts = part.split(")")
		rest = ")".join(sub_parts[1:])
		num = int(sub_parts[0])
		new_code += '(save_all)'
		new_code += ('<' * num + '[-]' + '>' * num + '[[-]' + '<' * num + '+' + '>' * num + ']' + '(up)') * n
		new_code += '(down)' * n
		new_code += '(load_all)'
		new_code += rest
	return new_code


def decrement_brainfuck(code, n, m):
	return code.replace('(dec)', '(negate_number)(inc)(negate_number)')


def printb_brainfuck(code, n, m):
	save_code = "(left)(left)(left)(left)[-](right)(right)(right)(right)" + \
	            "[-(left)(left)+(left)(left)+(right)(right)(right)(right)]" \
	            + "(left)(left)[-(right)(right)+(left)(left)](right)(right)"
	load_code = "[-](left)(left)(left)(left)" + \
	            "[-(right)(right)+(right)(right)+(left)(left)(left)(left)]" + \
	            "(right)(right)[-(left)(left)+(right)(right)](right)(right)"
	print_code = '(save_all)' + '(up)' * n
	print_code += ('(down)-[[+]++++++++++++++++++++++++++++++++++++++++++++++++.' +
	               '[-]]' +
	               load_code +
	               '[[-]+++++++++++++++++++++++++++++++++++++++++++++++++.' +
	               '[-]]') * n
	print_code += '[-]++++++++++.[-]'
	print_code += '(load_all)'
	return code.replace('(printb)', print_code)


def print_ascii_brainfuck(code, n, m):
	print_code = '(save_all)' + '(up)' * 7
	print_code += '[-(down)++(up)](down)' * 7
	print_code += '.'
	print_code += '(load_all)'
	return code.replace('(print_ascii)', print_code)


def print_string_brainfuck(code, n, m):
	print_code = '(on_flag0)(while_not_flag1)'
	print_code += '(on_flag1){(off_flag1)(print_ascii)>}'
	print_code += '(end_while_not_flag1)(off_flag1)'
	print_code += '(go_back_to_flag0)(off_flag0)'

	return code.replace('(print_string)', print_code)
