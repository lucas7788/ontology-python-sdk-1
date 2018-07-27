from unittest import TestCase


from binascii import a2b_hex
from unittest import TestCase

from ontology.account.account import Account
from ontology.crypto.SignatureScheme import SignatureScheme
from ontology.rpc.rpc import RpcClient
from ontology.smart_contract.native_contract import asset
import time

rpc_address = "http://polaris3.ont.io:20336"
rest_address = "http://polaris1.ont.io:20334"
cli = RpcClient(0, rpc_address)
private_key = "523c5fcf74823831756f0bcb3634234f10b3beb1c05595058534577752ad2d9f"
private_key2 = "75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf"
private_key3 = "1383ed1fe570b6673351f1a30a66b21204918ef8f673e864769fa2a653401114"
acc = Account(a2b_hex(private_key.encode()), SignatureScheme.SHA256withECDSA)
acc2 = Account(a2b_hex(private_key2.encode()), SignatureScheme.SHA256withECDSA)
acc3 = Account(a2b_hex(private_key3.encode()), SignatureScheme.SHA256withECDSA)


class TestAsset(TestCase):

    def test_new_transfer_transaction(self):
        tx = asset.new_transfer_transaction("ont", acc.get_address().to_base58(), acc2.get_address_base58(),
                                            1, 20000, 500)
        tx = cli.sign_to_transaction(tx, acc)
        print(tx.hash256().hex())
        print(tx.serialize().hex())
        b = cli.get_balance(acc.get_address_base58())
        b2 = cli.get_balance(acc2.get_address_base58())
        cli.send_raw_transaction(tx)
        time.sleep(6)
        bs = cli.get_balance(acc.get_address_base58())
        b2s = cli.get_balance(acc2.get_address_base58())
        assert int(b["ont"])-int(bs["ont"]) == int(b2s["ont"])-int(b2["ont"])
        aa = asset.unboundong(cli,acc.get_address_base58())
        if aa != "0":
            bb = int(aa)
            tx = asset.new_withdraw_ong_transaction(acc.get_address_base58(),acc.get_address_base58(),bb,20000,500)
            cli.sign_to_transaction(tx,acc)
            cli.send_raw_transaction(tx)
            time.sleep(6)
            aa2 = asset.unboundong(cli,acc.get_address_base58())
            assert aa2 == "0"

    def test_new_get_balance_transaction(self):
        tx = asset.new_get_balance_transaction("ont", acc.get_address_base58())
        result = cli.send_raw_transaction_preexec(tx)
        assert int(result) >= 0
        tx = asset.new_get_name_transaction("ont")
        result = cli.send_raw_transaction_preexec(tx)
        assert result != ""
        tx = asset.new_get_symbol_transaction("ont")
        result = cli.send_raw_transaction_preexec(tx)
        assert result != ""
        tx = asset.new_get_decimals_transaction("ont")
        result = cli.send_raw_transaction_preexec(tx)
        assert int(result) >= 0

    def test_new_approve_transaction(self):
        tx = asset.new_get_allowance_transaction("ont", acc.get_address_base58(), acc2.get_address_base58())
        allowance = cli.send_raw_transaction_preexec(tx)
        amount = 10
        tx2 = asset.new_approve_transaction("ont", acc.get_address_base58(), acc2.get_address_base58(), amount, 20000, 500)
        cli.sign_to_transaction(tx2, acc)
        cli.send_raw_transaction(tx2)
        time.sleep(6)
        tx = asset.new_get_allowance_transaction("ont", acc.get_address_base58(), acc2.get_address_base58())
        allowance2 = cli.send_raw_transaction_preexec(tx)
        if allowance == "":
            allowance = "0"
        assert int(allowance2,16) - int(allowance,16) == amount
        tx2 = asset.new_transferfrom_transaction("ont", acc2.get_address_base58(), acc.get_address_base58(), acc2.get_address_base58(), amount, 20000, 500)
        cli.sign_to_transaction(tx2, acc2)
        cli.send_raw_transaction(tx2)
        time.sleep(6)
        tx = asset.new_get_allowance_transaction("ont", acc.get_address_base58(), acc2.get_address_base58())
        allowance3 = cli.send_raw_transaction_preexec(tx)
        if allowance3 == "":
            allowance3 = "0"
        assert allowance == allowance3