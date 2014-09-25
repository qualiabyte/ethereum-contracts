from helpers import *

#
# OBJECTDB
#

def test_objectdb_serpent():
    source = load('contracts/objectdb.se')
    state = tester.state()
    contract = state.contract(source)
    objectdb_tests(state, contract)


def objectdb_tests(s, c):

    # Create a 20-byte (160-bit) object id
    id_hex = '0123456789' * 4
    id_bin = id_hex.decode('hex')

    # Define first account as object owner
    owner = int(t.a0, 16)

    # Verify the contract creator
    creator = owner
    assert s.send(t.k0, c, 0, [z('get'), 0, 0]) == [creator]

    # Add an object, verify the owner
    assert s.send(t.k0, c, 0, [z('add'), id_bin]) == []
    assert s.send(t.k0, c, 0, [z('get'), id_bin]) == [owner]

    # Add object with existing id fails
    assert s.send(t.k1, c, 0, [z('add'), id_bin]) == [1]
    assert s.send(t.k0, c, 0, [z('get'), id_bin]) == [owner]

    # Add object with id 0 fails (owned by creator)
    assert s.send(t.k1, c, 0, [z('add'), 0]) == [1]
    assert s.send(t.k0, c, 0, [z('get'), 0]) == [owner]

    # Add object with invalid id fails
    min_id = 0
    max_id = 256**20 - 1
    assert s.send(t.k0, c, 0, [z('add'), (min_id - 1)]) == [2]
    assert s.send(t.k0, c, 0, [z('add'), (max_id + 1)]) == [3]
    assert s.send(t.k0, c, 0, [z('get'), (min_id - 1)]) == [0]
    assert s.send(t.k0, c, 0, [z('get'), (max_id + 1)]) == [0]

    # Set a numeric property
    assert s.send(t.k0, c, 0, [z('set'), id_bin, 'abc', 123]) == []
    assert s.send(t.k0, c, 0, [z('get'), id_bin, 'abc']) == [123]

    # Set a string property
    assert s.send(t.k0, c, 0, [z('set'), id_bin, 'foo', z('bar')]) == []
    assert s.send(t.k0, c, 0, [z('get'), id_bin, 'foo']) == [zn('bar')]

    # Setting by non-owner fails
    assert s.send(t.k1, c, 0, [z('set'), id_bin, 'abc', 456]) == [1]
    assert s.send(t.k0, c, 0, [z('get'), id_bin, 'abc']) == [123]

    # Setting an invalid key fails
    min_key = 1
    max_key = 256**12 - 1
    assert s.send(t.k0, c, 0, [z('set'), id_bin, (min_key - 1), 123]) == [2]
    assert s.send(t.k0, c, 0, [z('set'), id_bin, (max_key + 1), 123]) == [3]

    # Creator kills the contract
    assert s.send(t.k0, c, 0, [z('kill')]) == []
    assert s.send(t.k0, c, 0, [z('get'), 0, 0]) == []
