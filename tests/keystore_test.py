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
    contract = evm_contract(state, code)
    return contract


# Creates an evm contract
def evm_contract(state, evm, sender=tester.k0, endowment=0):
    from pyethereum import utils, processblock, transactions
    nonce = state.block.get_nonce(utils.privtoaddr(sender))
    tx = transactions.contract(nonce, 1, 10000, endowment, evm)
    tx.sign(sender)
    (success, address) = processblock.apply_transaction(state.block, tx)
    if not success:
        raise Exception("Contract creation failed")
    return address


# Loads a project file
def load(name):
    path = os.path.join(SRC, name)
    file = open(path, 'r')
    text = file.read()
    return text


# Right-pads a string
def zpad(s):
    return string.ljust(s, 32, '\x00')


#
# TESTS
#


def test_keystore():
    source = load('contracts/keystore.se')
    state = tester.state()
    contract = state.contract(source)
    result1 = state.send(tester.k0, contract, 0, [zpad('set'), 'abc', 123])
    result2 = state.send(tester.k0, contract, 0, [zpad('get'), 'abc'])
    assert result1 == []
    assert result2 == [123]


def test_keystore_lll():
    path = 'contracts/keystore.lll'
    state = tester.state()
    contract = lll(state, path)
    result1 = state.send(tester.k0, contract, 0, [zpad('set'), 'abc', 123])
    result2 = state.send(tester.k0, contract, 0, [zpad('get'), 'abc'])
    assert result1 == []
    assert result2 == [123]


test_keystore()
test_keystore_lll()
