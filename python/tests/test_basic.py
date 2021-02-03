# standard imports
import os
import unittest
import json
import logging

# third-party imports
import web3
import eth_tester
import eth_abi

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()

logging.getLogger('web3').setLevel(logging.WARNING)
logging.getLogger('eth.vm').setLevel(logging.WARNING)

testdir = os.path.dirname(__file__)


class Test(unittest.TestCase):

    contract = None

    def setUp(self):
        eth_params = eth_tester.backends.pyevm.main.get_default_genesis_params({
            'gas_limit': 9000000,
            })

        f = open(os.path.join(testdir, '../../solidity/Owned.bin'), 'r')
        self.bytecode_owned = f.read()
        f.close()

        f = open(os.path.join(testdir, '../../solidity/Owned.json'), 'r')
        self.abi_owned = json.load(f)
        f.close()

        f = open(os.path.join(testdir, '../../solidity/VoidOwner.bin'), 'r')
        self.bytecode_void = f.read()
        f.close()

        f = open(os.path.join(testdir, '../../solidity/VoidOwner.json'), 'r')
        self.abi_void = json.load(f)
        f.close()

        backend = eth_tester.PyEVMBackend(eth_params)
        self.eth_tester =  eth_tester.EthereumTester(backend)
        provider = web3.Web3.EthereumTesterProvider(self.eth_tester)
        self.w3 = web3.Web3(provider)

        c = self.w3.eth.contract(abi=self.abi_owned, bytecode=self.bytecode_owned)
        tx_hash = c.constructor().transact()
        r = self.w3.eth.getTransactionReceipt(tx_hash)
        self.assertEqual(r.status, 1)
        self.contract_owned = self.w3.eth.contract(abi=self.abi_owned, address=r.contractAddress)

        c = self.w3.eth.contract(abi=self.abi_void, bytecode=self.bytecode_void)
        tx_hash = c.constructor().transact()
        r = self.w3.eth.getTransactionReceipt(tx_hash)
        self.assertEqual(r.status, 1)
        self.contract_void = self.w3.eth.contract(abi=self.abi_void, address=r.contractAddress)


    def tearDown(self):
        pass


    def test_hello(self):
        owner = self.contract_owned.functions.owner().call()
        self.assertEqual(self.w3.eth.accounts[0], owner)


    def test_accept(self):
        owner = self.contract_owned.functions.owner().call()
    
        tx_hash = self.contract_owned.functions.transferOwnership(self.contract_void.address).transact()
        r = self.w3.eth.getTransactionReceipt(tx_hash)
        self.assertEqual(r.status, 1)

        tx_hash = self.contract_void.functions.omNom(self.contract_owned.address).transact()
        r = self.w3.eth.getTransactionReceipt(tx_hash)
        self.assertEqual(r.status, 1)
        logged = False
        for l in r.logs:
            logg.debug('log {}'.format(l))
            if l.topics[0].hex() == '0xdc3c82f4776932041f15a08f769aadd6ed44c2a975e64bbf0fde8cf812f8b6b8':
                matchLogAddress = '0x{:>064}'.format(self.contract_owned.address[2:].lower()
                self.assertEqual(l.data, matchLogAddress))
                logged = True

        self.assertTrue(logged)

        owner = self.contract_owned.functions.owner().call()
        self.assertEqual(owner, self.contract_void.address)
    
        tx = self.contract_owned.functions.transferOwnership(self.contract_void.address)
        self.assertRaises(eth_tester.exceptions.TransactionFailed, tx.transact)


if __name__ == '__main__':
    unittest.main()
