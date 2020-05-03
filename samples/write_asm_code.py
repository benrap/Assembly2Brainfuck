from constants.MIPS_instruction_set import instructions

with open('Test.asm', 'wb') as f:
    code = ''
    # 0
    code += instructions['NOOP']
    # 1
    code += instructions['ADDIU'].replace('t' * 5, '00000').replace('s' * 5, '00001').replace('i' * 16, '1' * 14 + '01')
    # 2
    # code += NOOP[:-2] + '11'
    # 3
    # code += NOOP[:-3] + '100'

    a = []
    for i in range(len(code) // 8):
        a.append(int(code[i * 8:(i + 1) * 8], 2))
    towrite = (''.join(chr(i) for i in a)).encode('charmap')
    print(towrite)
    print(list(str(c) for c in towrite))
    f.write(towrite)
