import random
from constants import *


def chaos_roller(choice):
    ret_string = None
    array_choice = None
    if choice == "Basic":
        array_choice = BASIC_MAGIC
    elif choice == "Advanced":
        array_choice = ADVANCED_MAGIC
    elif choice == "Fluff":
        array_choice = FLUFF_CHAOS_MAGIC
    elif choice == "Combat":
        array_choice = CHAOS_COMBAT
    elif choice == "Status":
        array_choice = CHAOS_STATUS
    else:
        ret_string = "No chaos could be summoned. Please try again."
        return ret_string
    array_length = len(array_choice)
    index = random.randint(0, array_length)
    ret_string = array_choice[index]['type'] + array_choice[index]['effect']
    return ret_string


def fossil_roller():
    array_length = len(FOSSIL)
    index = random.randint(0, array_length)
    ret_string = FOSSIL[index]['fossil'] + ", which revives into a(n) " + FOSSIL[index]['poke']
    return ret_string
