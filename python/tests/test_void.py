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
from chainlib.eth.contract import (
        ABIContractEncoder,
        )
from hexathon import (
        add_0x,
        strip_0x,
        )

# local imports
from eth_owned.void import VoidOwner
from eth_owned.owned import Owned
from eth_owned import data_dir

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


    def test_accept(self):
        nonce_oracle = RPCNonceOracle(self.accounts[0], self.conn)
        txf = TxFactory(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)

        c = Owned(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash_hex, o) = c.transfer_ownership(self.owned_demo_address, self.accounts[0], self.accounts[1])
        r = self.conn.do(o)

        o = receipt(tx_hash_hex)
        r = self.conn.do(o)
        self.assertEqual(r['status'], 1)

        nonce_oracle = RPCNonceOracle(self.accounts[1], self.conn)
        c = Owned(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash_hex, o) = c.accept_ownership(self.owned_demo_address, self.accounts[1])
       
        r = self.conn.do(o)

        o = receipt(tx_hash_hex)
        r = self.conn.do(o)
        self.assertEqual(r['status'], 1)

        o = c.owner(self.owned_demo_address, sender_address=self.accounts[0])
        r = self.conn.do(o)
        owner_address = abi_decode_single(ABIContractType.ADDRESS, r)
        self.assertEqual(owner_address, strip_0x(self.accounts[1]))


    def test_void(self):
        nonce_oracle = RPCNonceOracle(self.accounts[0], self.conn)
        txf = TxFactory(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)

        c = Owned(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash_hex, o) = c.transfer_ownership(self.owned_demo_address, self.accounts[0], self.address)
        r = self.conn.do(o)

        o = receipt(tx_hash_hex)
        r = self.conn.do(o)
        self.assertEqual(r['status'], 1)

        (tx_hash_hex, o) = c.take_ownership(self.address, self.accounts[0], self.owned_demo_address)
        r = self.conn.do(o)

        o = receipt(tx_hash_hex)
        r = self.conn.do(o)
        self.assertEqual(r['status'], 1)

        o = c.owner(self.owned_demo_address, sender_address=self.accounts[0])
        r = self.conn.do(o)

        owner_address = abi_decode_single(ABIContractType.ADDRESS, r)
        self.assertEqual(owner_address, strip_0x(self.address))


if __name__ == '__main__':
    unittest.main()
