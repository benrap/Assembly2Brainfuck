import sys
from inspect import getmembers, isfunction, getsource

import converters.ASM2HBF
import converters.HBF2BF
from constants.CONSTANTS import CASM, HBF, BF, N, M


def ASM2HBF(code):
	return converters.ASM2HBF.ASM2HBF(code)


def HBF2BF(code, n, m):
	source = getsource(converters.HBF2BF)
	functions_list = [o for o in getmembers(converters.HBF2BF) if isfunction(o[1])]
	functions_list.sort(key=lambda x: source.find(x[0]))
	for f in functions_list[::-1]:
		code = f[1](code, n, m)
	return code


def convert(start, end, code, **kwargs):
	if start == CASM:
		if end == HBF:
			return ASM2HBF(code)
		elif end == BF:
			return HBF2BF(ASM2HBF(code), N, M)
	elif start == HBF:
		if end == BF:
			if 'n' in kwargs and 'm' in kwargs:
				return HBF2BF(code, N, M)
			else:
				return HBF2BF(code, N, M)


if __name__ == '__main__':
	print(convert(HBF, BF, "(dec)", n=4, m=5))
