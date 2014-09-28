
# Ethereum Contracts

A collection of contracts for Ethereum

+ [ObjectDB](#objectdb-serpent)
+ [Keystore](#keystore-serpent-lll)
+ [NameReg](#namereg-serpent-lll)

## ObjectDB ([Serpent](contracts/objectdb.se), [LLL](contracts/objectdb.lll))

An object database contract for Ethereum

### Overview

    In public mode, anyone can add objects to the database.
    The first account to add an object becomes its owner.
    Only the object's owner can modify its properties.

    In private mode, only the database creator may add objects.
    Thus, only they will own (and be able to modify) objects.

    By default, public mode is enabled.
    In either mode, any account can read object properties.

### API

    "add" <id>                  # Add empty object    (20-byte id)
    "get" <id> <key>            # Get object property (12-byte key)
    "set" <id> <key> <value>    # Set object property (32-byte value)
    "kill"                      # Kill the database   (Creator only)

## KeyStore ([Serpent](contracts/keystore.se), [LLL](contracts/keystore.lll))

A key-value store contract for Ethereum

### API

    "get" <key>                # Get a value
    "set" <key> <value>        # Set a value
    "kill"                     # Kill keystore (creator only)

## NameReg ([Serpent](contracts/namereg.se), [LLL](contracts/namereg.lll))

A name registration contract for Ethereum

### Overview

    Simply a re-implementation of the classic in Serpent and LLL.
    For science!

### API

    "register" <name>         # Register name
    <name>                    # Get address by name
    <address>                 # Get name by address
    "unregister"              # Unregister the caller
    "kill"                    # Kill registry (creator only)

<!--
## TODO

### Voteable

    "election" <title> <duration>   # Members only, Create new election
               <contract> <data>... # (Calls contract with data on success)
    "vote" <election> <boolean>     # Members only, Vote for-or-against
    "call" <election>               # Members only, Call a vote count
    "add-member" <name> <address>   # Contract only, After election!

### Notary
-->

## UNLICENSE

Released into the public domain with the [Unlicense](http://unlicense.org/).  
Please consider [Lightness, nonviolence and the Unlicense](http://adrianshort.org/lightness-nonviolence-unlicense/).  
