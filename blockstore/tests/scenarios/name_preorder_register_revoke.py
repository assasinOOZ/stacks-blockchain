#!/usr/bin/env python 

import testlib
import pybitcoin
import json

wallets = [
    testlib.Wallet( "5JesPiN68qt44Hc2nT8qmyZ1JDwHebfoh9KQ52Lazb1m1LaKNj9", 100000000000 ),
    testlib.Wallet( "5KHqsiU9qa77frZb6hQy9ocV7Sus9RWJcQGYYBJJBb2Efj1o77e", 100000000000 ),
    testlib.Wallet( "5Kg5kJbQHvk1B64rJniEmgbD83FpZpbw2RjdAZEzTefs9ihN3Bz", 100000000000 ),
    testlib.Wallet( "5JuVsoS9NauksSkqEjbUZxWwgGDQbMwPsEfoRBSpLpgDX1RtLX7", 100000000000 ),
    testlib.Wallet( "5KEpiSRr1BrT8vRD7LKGCEmudokTh1iMHbiThMQpLdwBwhDJB1T", 100000000000 )
]

consensus = "17ac43c1d8549c3181b200f1bf97eb7d"

def scenario( wallets, **kw ):

    testlib.blockstore_namespace_preorder( "test", wallets[1].addr, wallets[0].privkey )
    testlib.next_block( **kw )

    testlib.blockstore_namespace_reveal( "test", wallets[1].addr, 52595, 250, 4, [6,5,4,3,2,1,0,0,0,0,0,0,0,0,0,0], 10, 10, wallets[0].privkey )
    testlib.next_block( **kw )

    testlib.blockstore_namespace_ready( "test", wallets[1].privkey )
    testlib.next_block( **kw )

    testlib.blockstore_name_preorder( "foo.test", wallets[2].privkey, wallets[3].addr )
    testlib.next_block( **kw )
    
    testlib.blockstore_name_register( "foo.test", wallets[2].privkey, wallets[3].addr )
    testlib.next_block( **kw )
    
    resp = testlib.blockstore_name_revoke( "foo.test", wallets[3].privkey )
    testlib.next_block( **kw )


def check( state_engine ):

    # not revealed, but ready 
    ns = state_engine.get_namespace_reveal( "test" )
    if ns is not None:
        return False 

    ns = state_engine.get_namespace( "test" )
    if ns is None:
        return False 

    if ns['namespace_id'] != 'test':
        return False 

    # not preordered
    preorder = state_engine.get_name_preorder( "foo.test", pybitcoin.make_pay_to_address_script(wallets[2].addr), wallets[3].addr )
    if preorder is not None:
        return False
    
    # registered 
    name_rec = state_engine.get_name( "foo.test" )
    if name_rec is None:
        return False 

    # owned by
    if name_rec['address'] != wallets[3].addr or name_rec['sender'] != pybitcoin.make_pay_to_address_script(wallets[3].addr):
        return False 

    # revoked 
    if not name_rec['revoked']:
        return False 

    return True
