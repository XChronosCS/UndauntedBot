import random
import dice
import re
from constants import *

GENDER = ["Male", "Female"]


def nature():
    index = random.randint(0, len(NATURES))
    return NATURES[index]


def gender():
    index = random.randint(0, 2)
    return GENDER[index]


def roll_vals(match):
    a, b = match.group(1).split('d')
    ret_array = []
    for i in range(int(a)):
        ret_array.append(str(random.randint(1, 1 * int(b))))
    ret_string = '[' + ', '.join(ret_array) + ']'
    return ret_string


def roll_result(match):
    ret_val = 0
    arr = match.group(0)
    num_string = ''
    for x in list(arr):
        if x.isnumeric():
            num_string += x
        else:
            if num_string == '':
                ret_val += 0
            else:
                ret_val += int(num_string)
                num_string = ''
    return str(ret_val)
