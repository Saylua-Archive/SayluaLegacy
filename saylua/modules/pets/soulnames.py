import random
from namelist import name_list
from badwords import bad_words


def soulname(min_length=7):
    start = ""
    while len(start) < 3:
        start = random.choice(name_list)
    start = start[0:random.randint(2, len(start) - 1)]
    while len(start) < min_length:
        start = extend_name(start)
    if is_bad(start):
        return soulname(min_length) # try again if fails the check
    return start.lower()


def extend_name(name):
    returnname = name
    name_end = name[len(name) - 1]
    while returnname == name:
        nextbit = ""
        while name_end not in nextbit:
            nextbit = random.choice(name_list)
        returnname = name[:-1] + nextbit[nextbit.index(name_end):]
    return returnname


def is_bad(word):
    word = word.lower()
    for testword in bad_words:
        if testword in word:
            return True
    return False
