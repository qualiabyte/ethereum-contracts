import os
import pytest
from pyethereum import tester
import serpent
import string

FILE = os.path.dirname(__file__)
SRC = os.path.abspath(os.path.join(FILE, '..'))


#
# HELPERS
#


# Compiles lll code and defines the given contract
def compile_lll(state, code):
    contract = state.contract('')
    bytecode = tester.serpent.compile_lll(code)
    state.block.set_code(contract, bytecode)
    return contract


def load(name):
    path = os.path.join(SRC, name)
    file = open(path, 'r')
    text = file.read()
    return text


def zpad(s):
    return string.ljust(s, 32, '\x00')


#
# TESTS
#


def test_keystore():
    code = load('contracts/keystore.se')
    state = tester.state()
    contract = state.contract(code)
    result1 = state.send(tester.k0, contract, 0, [zpad('set'), 'abc', 123])
    result2 = state.send(tester.k0, contract, 0, [zpad('get'), 'abc'])
    assert result1 == []
    assert result2 == [123]


def test_keystore_lll():
    code = load('contracts/keystore.lll')
    state = tester.state()
    contract = compile_lll(state, code)
    result1 = state.send(tester.k0, contract, 0, [zpad('set'), 'abc', 123])
    result2 = state.send(tester.k0, contract, 0, [zpad('get'), 'abc'])
    assert result1 == []
    assert result2 == [123]


test_keystore()
test_keystore_lll()
