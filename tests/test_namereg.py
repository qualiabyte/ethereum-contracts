from helpers import *

#
# NAMEREG
#

def test_namereg_serpent():
    source = load('contracts/namereg.se')
    state = tester.state()
    contract = state.contract(source)
    namereg_tests(state, contract)


def test_namereg_lll():
    path = 'contracts/namereg.lll'
    state = tester.state()
    contract = lll(state, path)
    namereg_tests(state, contract)


def namereg_tests(s, c):

    # Register users
    assert s.send(t.k0, c, 0, [z('register'), z('leonardo')]) == []
    assert s.send(t.k1, c, 0, [z('register'), z('donatello')]) == []

    # Get addresses by names
    assert s.send(t.k0, c, 0, [z('leonardo')]) == [int(t.a0, 16)]
    assert s.send(t.k0, c, 0, [z('donatello')]) == [int(t.a1, 16)]

    # Get name by address
    assert s.send(t.k0, c, 0, [t.a0]) == [zn('leonardo')]

    # Register existing name
    assert s.send(t.k1, c, 0, [z('register'), z('leonardo')]) == []
    assert s.send(t.k0, c, 0, [z('leonardo')]) == [int(t.a0, 16)]

    # Second user unregisters
    assert s.send(t.k1, c, 0, [z('unregister')]) == []
    assert s.send(t.k0, c, 0, [z('donatello')]) == [0]

    # First user kills contract
    assert s.send(t.k0, c, 0, [z('kill')]) == []
    assert s.send(t.k0, c, 0, [z('leonardo')]) == []
