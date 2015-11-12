#!/usr/bin/env python 

import testlib 

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

    # will all be rejected trivially, since the first import must come from the importer's address
    testlib.blockstore_name_import( "foo.test", wallets[4].addr, "11" * 20, wallets[2].privkey )
    testlib.blockstore_name_import( "bar.test", wallets[2].addr, "22" * 20, wallets[3].privkey )
    testlib.blockstore_name_import( "baz.test", wallets[3].addr, "33" * 20, wallets[4].privkey )
    testlib.next_block( **kw )
   
    # will be accepted 
    testlib.blockstore_name_import( "goo.test", wallets[2].addr, "11" * 20, wallets[1].privkey )
    
    # will all be rejected because they weren't sent from a importer-derived key
    testlib.blockstore_name_import( "foo.test", wallets[4].addr, "11" * 20, wallets[2].privkey )
    testlib.blockstore_name_import( "bar.test", wallets[2].addr, "22" * 20, wallets[3].privkey )
    testlib.blockstore_name_import( "baz.test", wallets[3].addr, "33" * 20, wallets[4].privkey )
    testlib.next_block( **kw )
    
    testlib.blockstore_namespace_ready( "test", wallets[1].privkey )
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

    # these names can't exist
    foo = state_engine.get_name( "foo.test" )
    bar = state_engine.get_name( "bar.test" )
    baz = state_engine.get_name( "baz.test" )

    if foo is not None:
        return False 

    if bar is not None:
        return False 

    if baz is not None:
        return False

    # this name was valid
    goo = state_engine.get_name( "goo.test" )
    if goo is None:
        return False 

    return True
