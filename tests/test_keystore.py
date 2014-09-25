from helpers import *

#
# KEYSTORE
#

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


def keystore_tests(s, c):

    # Set a number value
    assert s.send(t.k0, c, 0, [z('set'), 'abc', 123]) == []
    assert s.send(t.k0, c, 0, [z('get'), 'abc']) == [123]

    # Set a string value
    assert s.send(t.k0, c, 0, [z('set'), 'foo', z('bar')]) == []
    assert s.send(t.k0, c, 0, [z('get'), 'foo']) == [zn('bar')]
