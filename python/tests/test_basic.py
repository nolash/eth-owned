# standard imports
import os
import unittest
import json
import logging

# external imports
from chainlib.eth.unittest.ethtester import EthTesterCase
from chainlib.connection import RPCConnection
from chainlib.eth.address import to_checksum_address
from chainlib.eth.nonce import RPCNonceOracle
from chainlib.eth.tx import (
        receipt,
        transaction,
        TxFormat,
        TxFactory,
        )
from chainlib.eth.contract import (
        abi_decode_single,
        ABIContractType,
        )
from chainlib.jsonrpc import jsonrpc_template
from chainlib.eth.contract import (
        ABIContractEncoder,
        )
from hexathon import add_0x

# local imports
from eth_void_owner import (
        VoidOwner,
        data_dir,
        )

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()

testdir = os.path.dirname(__file__)


class Test(EthTesterCase):


    def setUp(self):
        super(Test, self).setUp()
        self.conn = RPCConnection.connect(self.chain_spec, 'default')
        nonce_oracle = RPCNonceOracle(self.accounts[0], self.conn)
        self.o = VoidOwner(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash_hex, o) = self.o.constructor(self.accounts[0])
        r = self.conn.do(o)
        logg.debug('deployed with hash {}'.format(r))

        o = receipt(tx_hash_hex)
        r = self.conn.do(o)
        self.address = r['contract_address']

        f = open(os.path.join(data_dir, 'Owned.bin'), 'r')
        b = f.read()
        f.close()
       
        txf = TxFactory(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        tx = txf.template(self.accounts[0], None, use_nonce=True)
        tx = txf.set_code(tx, b)
        (tx_hash_hex, o) = txf.build(tx)
        r = self.conn.do(o)

        o = receipt(tx_hash_hex)
        r = self.conn.do(o)
        self.owned_demo_address = r['contract_address']


    def test_takeover(self):
        
        nonce_oracle = RPCNonceOracle(self.accounts[0], self.conn)
        txf = TxFactory(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)

        enc = ABIContractEncoder()
        enc.method('transferOwnership')
        enc.typ(ABIContractType.ADDRESS)
        enc.address(self.address)
        data = enc.get()
        tx = txf.template(self.accounts[0], self.owned_demo_address, use_nonce=True)
        tx = txf.set_code(tx, data)
        (tx_hash_hex, o) = txf.finalize(tx)

        r = self.conn.do(o)

        o = receipt(tx_hash_hex)
        r = self.conn.do(o)
        self.assertEqual(r['status'], 1)

        c = VoidOwner(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash_hex, o) = c.take_ownership(self.accounts[0], self.address, self.owned_demo_address)

        r = self.conn.do(o)

        o = receipt(tx_hash_hex)
        r = self.conn.do(o)
        self.assertEqual(r['status'], 1)

        o = jsonrpc_template()
        o['method'] = 'eth_call'
        enc = ABIContractEncoder()
        enc.method('owner')
        data = add_0x(enc.get())
        tx = txf.template(self.accounts[0], self.owned_demo_address)
        tx = txf.set_code(tx, data)
        o['params'].append(txf.normalize(tx))

        r = self.conn.do(o)
        owner_address = abi_decode_single(ABIContractType.ADDRESS, r)
        self.assertEqual(owner_address, self.address)


if __name__ == '__main__':
    unittest.main()
