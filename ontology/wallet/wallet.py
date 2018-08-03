from ontology.crypto.scrypt import Scrypt
from ontology.wallet.account import AccountData
from ontology.wallet.identity import Identity


class WalletData(object):
    def __init__(self, name="MyWallet", version="1.1", create_time="", default_ontid="", default_account_address="",
                 scrypt=Scrypt(), identities=[], accounts=[]):
        self.name = name
        self.version = version
        self.createTime = create_time
        self.defaultOntid = default_ontid
        self.defaultAccountAddress = default_account_address
        self.scrypt = scrypt  # Scrypt class
        self.identities = identities  # a list of Identity class
        self.accounts = accounts  # a list of AccountData class

    def clone(self):
        wallet = WalletData()
        wallet.name = self.name
        wallet.version = self.version
        wallet.createTime = self.createTime
        wallet.defaultOntid = self.defaultOntid
        wallet.defaultAccountAddress = self.defaultAccountAddress
        wallet.scrypt = self.scrypt
        wallet.accounts = self.accounts
        wallet.identities = self.identities
        return wallet

    def add_account(self, acc: AccountData):
        self.accounts.append(acc)

    def remove_account(self, address: str):
        account = self.get_account_by_address(address)
        if account is None:
            raise Exception("no the account")
        return self.accounts.remove(account)

    def get_account_by_index(self, index: int):
        if index < 0 or index >= len(self.accounts):
            return ValueError("wrong account index")
        return self.accounts[index]

    def get_account_by_address(self, address: str):
        for index in range(len(self.accounts)):
            if self.accounts[index].address == address:
                return self.accounts[index]
        return None

    def add_identity(self, id: Identity):
        for identity in self.identities:
            if identity.ontid == id.ontid:
                raise Exception("")
        self.identities.append(id)

    def remove_identity(self, ontid):
        for index in range(len(self.identities)):
            if self.identities[index].ontid == ontid:
                del self.identities[index]
                break

    def get_identity_by_ontid(self, ontid: str):
        for identity in self.identities:
            if identity.ontid == ontid:
                return identity
        return None
