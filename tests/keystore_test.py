from math import *
import os
import pytest
import pyethereum
from pyethereum import tester
import serpent
import string
import subprocess

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


#
# TESTS
#


def test_num2str():
    assert num2str(1) == '\x01'
    assert num2str(256) == '\x01\x00'
    assert num2str(65536) == '\x01\x00\x00'
    assert num2str(6382179) == 'abc'
    assert num2str(113685359126373) == 'george'


def test_str2num():
    assert str2num('\x01') == 1
    assert str2num('\x01\x00') == 256
    assert str2num('\x01\x00\x00') == 65536
    assert str2num('abc') == 97*256**2 + 98*256 + 99
    assert str2num('george') == 113685359126373


def keystore_tests(state, contract):
    result1 = state.send(tester.k0, contract, 0, [zpad('set'), 'abc', 123])
    result2 = state.send(tester.k0, contract, 0, [zpad('get'), 'abc'])
    result3 = state.send(tester.k0, contract, 0, [zpad('set'), 'foo', 'bar'])
    result4 = state.send(tester.k0, contract, 0, [zpad('get'), 'foo'])
    assert result1 == []
    assert result2 == [123]
    assert result3 == []
    assert result4 == [str2num('bar')]


def test_keystore_serpent():
    source = load('contracts/keystore.se')
    state = tester.state()
    contract = state.contract(source)
    keystore_tests(state, contract)


def test_keystore_lll():
    path = 'contracts/keystore.lll'
    state = tester.state()
    contract = lll(state, path)
    keystore_tests(state, contract)
