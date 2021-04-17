# standard imports
import logging
import json
import os

# external imports
from chainlib.eth.tx import (
        TxFactory,
        TxFormat,
        )
from chainlib.eth.contract import (
        ABIContractEncoder,
        ABIContractDecoder,
        ABIContractType,
        abi_decode_single,
        )
from chainlib.eth.constant import ZERO_ADDRESS
from chainlib.jsonrpc import (
        jsonrpc_template,
        )
from hexathon import add_0x

logg = logging.getLogger()

moddir = os.path.dirname(__file__)
datadir = os.path.join(moddir, 'data')


class Owned(TxFactory):

    interfaces = None

    def owner(self, contract_address, sender_address=ZERO_ADDRESS):
        o = jsonrpc_template()
        o['method'] = 'eth_call'
        enc = ABIContractEncoder()
        enc.method('owner')
        data = add_0x(enc.get())
        tx = self.template(sender_address, contract_address)
        tx = self.set_code(tx, data)
        o['params'].append(self.normalize(tx))
        return o


    def transfer_ownership(self, sender_address, contract_address, address, tx_format=TxFormat.JSONRPC):
        enc = ABIContractEncoder()
        enc.method('transferOwnership')
        enc.typ(ABIContractType.ADDRESS)
        enc.address(address)
        data = enc.get()
        tx = self.template(sender_address, contract_address, use_nonce=True)
        tx = self.set_code(tx, data)
        tx = self.finalize(tx, tx_format)        
        return tx


    def accept_ownership(self, sender_address, contract_address, tx_format=TxFormat.JSONRPC):
        enc = ABIContractEncoder()
        enc.method('acceptOwnership')
        data = enc.get()
        tx = self.template(sender_address, contract_address, use_nonce=True)
        tx = self.set_code(tx, data)
        tx = self.finalize(tx, tx_format)        
        return tx


    @classmethod
    def parse_owner(self, v):
        return abi_decode_single(ABIContractType.ADDRESS, v)

