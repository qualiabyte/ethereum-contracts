from math import *
import os
import pytest
import pyethereum
from pyethereum import tester
import serpent
import string
import subprocess

t = tester

FILE = os.path.dirname(__file__)
SRC = os.path.abspath(os.path.join(FILE, '..'))


#
# HELPERS
#


# Runs a command
def run(cmd):
    return subprocess.check_output(cmd, shell=True)


# Creates an lll contract
def lll(state, path):
    code = run('lllc ' + path).rstrip().decode('hex')
    contract = state.evm(code)
    return contract


# Loads a project file
def load(name):
    path = os.path.join(SRC, name)
    file = open(path, 'r')
    text = file.read()
    return text


# Right-pads a string
def zpad(s):
    return string.ljust(s, 32, '\x00')


# Serpent number to string
def num2str(num):
    string = ''
    length = int(floor(1 + log(num, 256)))
    for i in reversed(range(0, length)):
        string += chr((num >> i*8) & 0xff)
    return string


# Serpent string to number
def str2num(string):
    num = 0
    length = len(string)
    for i in range(0, length):
        num += ord(string[length-i-1]) * 256**i
    return num


# Aliases
z = zpad
zn = lambda s: str2num(zpad(s))
