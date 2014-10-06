from helpers import *

#
# NOTARY
#

def test_notary_lll():
    path = 'contracts/notary.lll'
    dbpath = 'contracts/objectdb.lll'
    state = tester.state()
    db = lll(state, dbpath)
    contract = lll(state, path)
    notary_tests(state, contract, db)


def notary_tests(s, c, db):

    # Storage addresses
    CREATOR = 0

    # Set database address
    assert s.send(t.k0, c, 0, [z('database'), db]) == []
    assert s.block.get_storage_data(c, 1) == int(db, 16)

    # Set notary as db creator
    assert s.send(t.k0, db, 0, [z('config'), z('creator'), c]) == []
    assert s.block.get_storage_data(db, CREATOR) == int(c, 16)

    # Define first account as submitter
    submitter = int(t.a0, 16)

    # Create a 20-byte (160-bit) hash
    hash_hex = '0123456789' * 4
    hash = hash_hex.decode('hex')

    # Notarise a hash, verify the account and timestamp
    assert s.send(t.k0, c, 0, [z('record'), hash]) == []
    assert s.send(t.k0, c, 0, [z('get'), hash, "account"]) == [submitter]
    assert s.send(t.k0, c, 0, [z('get'), hash, "timestamp"]) == [s.block.timestamp]

    # Set a custom property
    assert s.send(t.k0, c, 0, [z('set'), hash, "author", "Alice"]) == []
    assert s.send(t.k0, c, 0, [z('get'), hash, "author"]) == [str2num("Alice")]

    # Setting by non-submitters should fail
    assert s.send(t.k1, c, 0, [z('set'), hash, "author2", "Eve"]) == [1]
    assert s.send(t.k0, c, 0, [z('get'), hash, "author2"]) == [0]

    # Setting reserved keys should fail
    assert s.send(t.k0, c, 0, [z('set'), hash, "account", 0xff]) == [2]
    assert s.send(t.k0, c, 0, [z('set'), hash, "timestamp", 1234]) == [2]
    assert s.send(t.k0, c, 0, [z('get'), hash, "account"]) == [submitter]
    assert s.send(t.k0, c, 0, [z('get'), hash, "timestamp"]) == [s.block.timestamp]

    # Creator kills the contract
    assert s.send(t.k0, c, 0, [z('kill')]) == []
    assert s.send(t.k0, c, 0, [z('get'), 0, 0]) == []

    # Verify database also killed
    assert s.block.get_storage_data(db, CREATOR) == 0
