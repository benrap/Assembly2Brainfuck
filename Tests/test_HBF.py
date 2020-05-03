from converters.HBF2BF import *
from converters.main_converter import HBF2BF
import numpy as np
from BF import interpret
import sys

np.set_printoptions(threshold=sys.maxsize)


def problematic_bits(code):
    remove = '><+-[]., \n'
    for i in remove:
        code = code.replace(i, '')
    return code


def transform_data(data, m, n):
    m, n = n, m
    data += [0] * (n * m - (len(data) % (n * m)))
    data = np.reshape(data, (len(data) // (n * m), m, n))
    dat = []
    for i in range(len(data)):
        dat.append(data[i][::-1, ::-1])
    return np.asarray(dat)


def test_if_not_0_brainfuck():
    n = 4
    m = 5
    code = '(up)(up)+++(down)(down)(left)(right){-}'
    code = HBF2BF(code, n, m)
    data = interpret(code)
    return transform_data(data, m, n)


def test_save_load_brainfuck():
    n = 8
    m = 5
    code = '+(up)++(up)+++>' \
           '(left)(left)(left)(left)+++(down)++++(down)+++++(right)(right)(right)(right)<' \
           '(save_all)>(load_all)'
    code = HBF2BF(code, n, m)
    data = interpret(code)
    return transform_data(data, m, n)


def test_add_next_brainfuck():
    n = 8
    m = 5
    code = '+(up)+(up)+(up)+(up)+(up)+(up)+(down)(down)(down)(down)(down)(down)>+<(add)'  # 0: 11111110, 1: 10000000
    code = HBF2BF(code, n, m)
    data = interpret(code)
    return transform_data(data, m, n)


def test_go_to_flag_brainfuck():
    n = 8
    m = 5
    code = '''+(up)+(up)+>(left)(left)(left)>>>>(up)+(down)<<<<(right)(right)(right)(down)(down)<
    (goto_flag3)++++++++++++++'''
    code = HBF2BF(code, n, m)
    data = interpret(code)
    return transform_data(data, m, n)


def test_go_back_to_flag():
    n = 8
    m = 5
    code = '''(up)(up)(up)(left)(left)(left)+(down)(down)(down)(right)(right)(right)
    >>>>(go_back_to_flag3)+++++'''
    code = HBF2BF(code, n, m)
    data = interpret(code)
    return transform_data(data, m, n)


def test_set_flag_brainfuck():
    n = 8
    m = 5
    code = '''(on_flag3)>(on_flag2)>(on_flag2)<(off_flag2)'''
    code = HBF2BF(code, n, m)
    data = interpret(code)
    return transform_data(data, m, n)


def test_advance_flag_brainfuck():
    n = 8
    m = 5
    code = '''+(up)+(down)>(on_flag3)<(advance_flag3)
    '''
    code = HBF2BF(code, n, m)
    data = interpret(code)
    return transform_data(data, m, n)


def test_not_brainfuck():
    n = 8
    m = 5
    code = '''+(up)+(up)(up)(up)+(down)(down)(down)(down)(not)
    '''
    code = HBF2BF(code, n, m)
    data = interpret(code)
    return transform_data(data, m, n)


def test_zero_brainfuck():
    n = 8
    m = 5
    code = '''+(up)+(up)(up)(up)+(up)+(up)(up)+(down)(down)(down)(down)(down)(down)(down)(zero)
    '''
    code = HBF2BF(code, n, m)
    data = interpret(code)
    return transform_data(data, m, n)


def test_and_brainfuck():
    n = 8
    m = 5
    code = '''+(up)+(down)>+(up)(up)+(down)(down)<(and)'''  # and 1100 with 1010
    code = HBF2BF(code, n, m)
    data = interpret(code)
    return transform_data(data, m, n)


def test_or_brainfuck():
    n = 8
    m = 5
    code = '''+(up)+(down)>+(up)(up)+(down)(down)<(or)'''  # or 1100 with 1010
    code = HBF2BF(code, n, m)
    data = interpret(code)
    return transform_data(data, m, n)


def test_setb_brainfuck():
    n = 8
    m = 5
    code = '''(setb00100111)'''
    code = HBF2BF(code, n, m)
    data = interpret(code)
    return transform_data(data, m, n)


def test_set_brainfuck():
    n = 8
    m = 5
    code = '''(set31)'''
    code = HBF2BF(code, n, m)
    data = interpret(code)
    return transform_data(data, m, n)


# this one crashes
"""def test_copy_to_flag_brainfuck():
    n = 8
    m = 5
    code = '''+(up)++(down)>>>(on_flag3)<<<(copy_to_flag3)
    '''
    data = copy_to_flag_brainfuck(code, n, m)
    return transform_data(data, m, n)"""


def test_copy_behind_to_flag_brainfuck():
    n = 8
    m = 5
    code = '''(on_flag3)>>>+(up)++(down)<<<(copy_behind_to_flag3)
    '''
    code = HBF2BF(code, n, m)
    data = interpret(code)
    return transform_data(data, m, n)


def test_load_to_flag_brainfuck():
    n = 8
    m = 5
    code = '''+(up)+(down)(save_all)>(on_flag3)<
    (load_to_flag3)
    '''
    code = HBF2BF(code, n, m)
    data = interpret(code)
    return transform_data(data, m, n)


# doesn't work

def test_advance_behind_flag_brainfuck():
    n = 8
    m = 5
    code = '''+(on_flag3)>>>+(advance_behind_flag3)
    '''
    code = HBF2BF(code, n, m)
    data = interpret(code)
    return transform_data(data, m, n)


def test_inc_brainfuck():
    n = 8
    m = 5
    code = '''(inc)(inc)(inc)>(inc)(inc)(inc)(inc)(inc)(inc)
    '''
    code = HBF2BF(code, n, m)
    data = interpret(code)
    return transform_data(data, m, n)


def test_dist_from_flag_brainfuck():
    n = 8
    m = 5
    code = '''(on_flag5)>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>(on_flag3)<<(dist_to_flag5) +++++++++++++++++
    '''
    code = HBF2BF(code, n, m)
    data = interpret(code)
    return transform_data(data, m, n)


def test_load_flag_brainfuck():
    n = 8
    m = 5
    code = '''(on_flag3)(on_flag2)(on_flag4)(load_flag3)(load_flag2)'''
    code = HBF2BF(code, n, m)
    data = interpret(code)
    return transform_data(data, m, n)


def test_if_flag_brainfuck():
    n = 8
    m = 5
    code = '''(on_flag3)  (if_flag3)${+(up)++(down)}$  (if_flag2)${+(up)++(down)}$'''
    code = HBF2BF(code, n, m)
    data = interpret(code)
    return transform_data(data, m, n)


def test_equate_b_brainfuck():
    n = 8
    m = 5
    code = '''+(up)+(down)  (equate_b11)${-(up)-(up) +(down)(down)}$ 
                            (equate_b100)${+(up)+(up) +(down)(down)}$ 
    '''
    code = HBF2BF(code, n, m)
    data = interpret(code)
    return transform_data(data, m, n)


def test_equate_brainfuck():
    n = 8
    m = 6
    code = '''+ (up) (up)+(down) (down) (equate5)${++++}$
        '''
    code = HBF2BF(code, n, m)
    data = interpret(code)
    return transform_data(data, m, n)


def test_while_not_flag_brainfuck():
    n = 8
    m = 6
    code = '''>>>(on_flag3) <<<(while_not_flag3) > (end_while_not_flag3)'''
    code = HBF2BF(code, n, m)
    data = interpret(code)
    return transform_data(data, m, n)


def test_xor_brainfuck():
    n = 8
    m = 6
    code = '''+(up)+(down)>+(up)(up)+(down)(down)< (xor)'''  # xors 1100 with 1010
    code = HBF2BF(code, n, m)
    data = interpret(code)
    return transform_data(data, m, n)


def test_neg_flag():
    n = 10
    m = 6
    code = '''(up)(up)(up)(up)(up)(up)(up)+(up)+(down)(down)(down)(down)(down)(down)(down)(down)(neg_flag)'''
    code = HBF2BF(code, n, m)
    data = interpret(code)
    return transform_data(data, m, n)


def test_negate_number_brainfuck():
    n = 10
    m = 6
    code = '''(inc)(inc)(inc) (negate_number)'''
    code = HBF2BF(code, n, m)
    data = interpret(code)
    return transform_data(data, m, n)


def test_sub_brainfuck():
    n = 10
    m = 6
    code = '''(inc)(inc)(inc) > (inc)< (sub)'''
    code = HBF2BF(code, n, m)
    data = interpret(code)
    return transform_data(data, m, n)


def test_copy_over_brainfuck():
    n = 10
    m = 6
    code = '''(inc)(inc)(inc) > (inc)< (copy_over1)'''
    code = HBF2BF(code, n, m)
    data = interpret(code)
    return transform_data(data, m, n)


def test_copy_back_over_brainfuck():
    n = 10
    m = 6
    code = '''(inc)(inc)(inc) > (inc) (copy_back_over1)'''
    code = HBF2BF(code, n, m)
    data = interpret(code)
    return transform_data(data, m, n)


def test_decrement_brainfuck():
    n = 10
    m = 6
    code = '''(inc)(inc)(inc) (dec)(dec)'''
    code = HBF2BF(code, n, m)
    data = interpret(code)
    return transform_data(data, m, n)


def test_printb_brainfuck():
    n = 10
    m = 6
    code = '''(inc)(printb)(inc)(printb)(inc)(printb)'''
    code = HBF2BF(code, n, m)
    data = interpret(code)
    return transform_data(data, m, n)

def test_print_ascii_brainfuck():
    n = 10
    m = 6
    code = ''.join(''''(set{})(print_ascii)'''.format(ord(c)) for c in 'Hello World\n')
    code = HBF2BF(code, n, m)
    data = interpret(code)
    return transform_data(data, m, n)


def test_print_string_brainfuck():
    n = 10
    m = 6
    string = 'Hello World\n'
    code = ''.join(''''(set{})>'''.format(ord(c)) for c in string) + '<'*len(string) + '(print_string)'
    code = HBF2BF(code, n, m)
    data = interpret(code)
    return transform_data(data, m, n)


def get_tests():
    module = __import__(__name__)
    tests = []
    with open(module.__file__) as f:
        for line in f:
            if line.startswith('def test_'):
                test = globals()[line[4:][:-4]]
                tests.append(test)
    return tests


def __main__():
    tests = get_tests()
    for test in tests:
        print(test.__name__.replace('brainfuck', '').replace('_', ' ').strip())
        print(test())
        print('.....................')


if __name__ == '__main__':
    __main__()
