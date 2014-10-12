from helpers import *

#
# OBJECTDB
#

def test_objectdb_serpent():
    source = load('contracts/objectdb.se')
    state = tester.state()
    contract = state.contract(source)
    objectdb_tests(state, contract)


def test_objectdb_lll():
    path = 'contracts/objectdb.lll'
    state = tester.state()
    contract = lll(state, path)
    objectdb_tests(state, contract)


def objectdb_tests(s, c):
    config_tests(s, c)
    private_tests(s, c)
    public_tests(s, c)
    id_tests(s, c)
    key_tests(s, c)
    value_tests(s, c)
    cleanup_tests(s, c)


def config_tests(s, c):

    # Storage address
    PARENT = 0

    # Define users
    user0 = int(t.a0, 16)
    user1 = int(t.a1, 16)

    # Change the parent
    assert s.send(t.k0, c, 0, [z('config'), z('parent'), user1]) == []
    assert s.block.get_storage_data(c, PARENT) == user1

    # Reset the parent
    assert s.send(t.k1, c, 0, [z('config'), z('parent'), user0]) == []
    assert s.block.get_storage_data(c, PARENT) == user0


def private_tests(s, c):

    # Storage address
    PUBLIC = 1

    # Disable public mode
    assert s.send(t.k0, c, 0, [z('config'), z('public'), 0]) == []
    assert s.block.get_storage_data(c, PUBLIC) == 0

    # Object id
    id = 33

    # Add by non-parent should fail
    assert s.send(t.k1, c, 0, [z('add'), id]) == [0]
    assert s.send(t.k1, c, 0, [z('get'), id, 0]) == [0]

    # Add by parent should succeed
    parent = int(t.a0, 16)
    assert s.send(t.k0, c, 0, [z('add'), id]) == []
    assert s.send(t.k0, c, 0, [z('get'), id, 0]) == [parent]

    # Set by parent should succeed
    assert s.send(t.k0, c, 0, [z('set'), id, 'abc', 123]) == []
    assert s.send(t.k0, c, 0, [z('get'), id, 'abc']) == [123]


def public_tests(s, c):

    # Storage address
    PUBLIC = 1

    # Create a 20-byte (160-bit) object id
    id_hex = '0123456789' * 4
    id_bin = id_hex.decode('hex')

    # Enable public mode
    assert s.send(t.k0, c, 0, [z('config'), z('public'), 1]) == []
    assert s.block.get_storage_data(c, PUBLIC) == 1

    # Define first account as object owner
    owner = int(t.a0, 16)

    # Verify the contract parent
    parent = owner
    assert s.send(t.k0, c, 0, [z('get'), 0, 0]) == [parent]

    # Add an object, verify the owner
    assert s.send(t.k0, c, 0, [z('add'), id_bin]) == []
    assert s.send(t.k0, c, 0, [z('get'), id_bin]) == [owner]

    # Add object with existing id fails
    assert s.send(t.k1, c, 0, [z('add'), id_bin]) == [1]
    assert s.send(t.k0, c, 0, [z('get'), id_bin]) == [owner]

    # Add object with id 0 fails (owned by parent)
    assert s.send(t.k1, c, 0, [z('add'), 0]) == [1]
    assert s.send(t.k0, c, 0, [z('get'), 0]) == [owner]

    # Set a numeric property
    assert s.send(t.k0, c, 0, [z('set'), id_bin, 'abc', 123]) == []
    assert s.send(t.k0, c, 0, [z('get'), id_bin, 'abc']) == [123]

    # Setting by non-owner fails
    assert s.send(t.k1, c, 0, [z('set'), id_bin, 'abc', 456]) == [1]
    assert s.send(t.k0, c, 0, [z('get'), id_bin, 'abc']) == [123]


def id_tests(s, c):

    # Define first account as object owner
    owner = int(t.a0, 16)

    # Add object with invalid id fails
    min_id = 0
    max_id = 256**20 - 1
    assert s.send(t.k0, c, 0, [z('add'), (min_id - 1)]) == [2]
    assert s.send(t.k0, c, 0, [z('add'), (max_id + 2)]) == [3]
    assert s.send(t.k0, c, 0, [z('get'), (min_id - 1)]) == [0]
    assert s.send(t.k0, c, 0, [z('get'), (max_id + 2)]) == [0]

    # Create medium length (10-byte) object id
    id_hex = '01234567890123456789'
    id_bin = id_hex.decode('hex')

    # Add object, verify the owner
    assert s.send(t.k0, c, 0, [z('add'), id_bin]) == []
    assert s.send(t.k0, c, 0, [z('get'), id_bin]) == [owner]

    # Verify id format
    index_hex = '0000000000000000000001234567890123456789000000000000000000000000'
    assert s.block.get_storage_data(c, index_hex.decode('hex')) == owner


def key_tests(s, c):

    # Create a 20-byte (160-bit) object id
    id_hex = '0123456789' * 4
    id_bin = id_hex.decode('hex')

    # Setting an invalid key fails
    min_key = 1
    max_key = 256**12 - 1
    assert s.send(t.k0, c, 0, [z('set'), id_bin, (min_key - 1), 123]) == [2]
    assert s.send(t.k0, c, 0, [z('set'), id_bin, (max_key + 1), 123]) == [3]

    # Set a medium key (6 bytes)
    key_hex = 'aabbccddeeff'
    key_bin = key_hex.decode('hex')
    assert s.send(t.k0, c, 0, [z('set'), id_bin, key_bin, 456]) == []
    assert s.send(t.k0, c, 0, [z('get'), id_bin, key_bin]) == [456]

    # Verify index format
    index_hex = '0123456789012345678901234567890123456789000000000000aabbccddeeff'
    assert s.block.get_storage_data(c, index_hex.decode('hex')) == 456

    # Set a long key (12 bytes)
    key_hex = 'aabbccddeeff' * 2
    key_bin = key_hex.decode('hex')
    assert s.send(t.k0, c, 0, [z('set'), id_bin, key_bin, 789]) == []
    assert s.send(t.k0, c, 0, [z('get'), id_bin, key_bin]) == [789]

    # Verify index format
    index_hex = '0123456789012345678901234567890123456789aabbccddeeffaabbccddeeff'
    assert s.block.get_storage_data(c, index_hex.decode('hex')) == 789


def value_tests(s, c):

    # Object owner
    owner = int(t.a0, 16)

    # Object id
    id = str2num('value-test')

    # Add object, verify the owner
    assert s.send(t.k0, c, 0, [z('add'), id]) == []
    assert s.send(t.k0, c, 0, [z('get'), id]) == [owner]

    # Set a numeric property
    assert s.send(t.k0, c, 0, [z('set'), id, 'abc', 123]) == []
    assert s.send(t.k0, c, 0, [z('get'), id, 'abc']) == [123]

    # Set a string property
    assert s.send(t.k0, c, 0, [z('set'), id, 'foo', z('bar')]) == []
    assert s.send(t.k0, c, 0, [z('get'), id, 'foo']) == [zn('bar')]


def cleanup_tests(s, c):

    # Parent kills the contract
    assert s.send(t.k0, c, 0, [z('kill')]) == []
    assert s.send(t.k0, c, 0, [z('get'), 0, 0]) == []
