import os
from random import randint
from string import ascii_letters

try:
    FileExistsError
except NameError:
    FileExistsError = OSError

def mkdir(fn):
    'Make a directory that will contain the file.'
    try:
        os.makedirs(os.path.split(fn)[0])
    except FileExistsError:
        pass

def mktemp(tempdir):
    return os.path.join(tempdir, _random_file_name())

def _random_file_name():
    n = len(ascii_letters)
    return ''.join(ascii_letters[randint(0, n)] for _ in range(10))
