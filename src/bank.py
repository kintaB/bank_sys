from dataclasses import dataclass, field
from typing import TypedDict

from src.accounts.base import BankAccount
from src.exceptions import AuthentificateFailedError, TooManyAttemptsError, YoungClientError
from src.models import AccountStatus, ClientData, ClientStatus

class Contacts(TypedDict):
    mail: str
    phone: str
    address: str | None

@dataclass
class Client:
    id: str
    full_name: ClientData
    age: int
    _password: str
    client_status: ClientStatus
    accounts: list[str]
    contacts: Contacts
    _auth_attempts: int = 0
    _susp_operations: list[str] = field(default_factory=list)

class Bank:

    def __init__(self):
        self.clients = {}
        self.accounts = {}

    def add_client(self, client: Client):
        if client.age < 18:
            raise YoungClientError('Age of suggested client is lower than 18')
        self.clients[client.id] = client

    def open_account(self, client_id, account: BankAccount):
        number = account.account_number
        self.accounts[number] = account
        self.clients[client_id].accounts.append(number)

    def close_account(self, account_number):
        if self.accounts[account_number].account_status != AccountStatus.CLOSED:
            self.accounts[account_number].account_status = AccountStatus.CLOSED
        
    def freeze_account(self, account_number):
        if self.accounts[account_number].account_status != AccountStatus.FROZEN:
            self.accounts[account_number].account_status = AccountStatus.FROZEN
        
    def unfreeze_account(self, account_number):
        if self.accounts[account_number].account_status == AccountStatus.FROZEN:
            self.accounts[account_number].account_status = AccountStatus.ACTIVE
        
    def authenticate_client(self, login, password, client_id):
        client_login = self.clients[client_id].contacts['phone']
        client_password = self.clients[client_id]._password

        if self.clients[client_id].client_status == ClientStatus.BLOCKED:
            raise AuthentificateFailedError(f'Account blocked')

        if client_login != login or client_password != password:
            self.clients[client_id]._auth_attempts += 1
            self.mark_suspicious(client_id, 'failed login')
            if self.clients[client_id]._auth_attempts >= 3:
                self.clients[client_id].client_status = ClientStatus.BLOCKED
                self.mark_suspicious(client_id, 'account blocked after too many login attempts')
                raise TooManyAttemptsError('Account has been blocked due to a lot of attempts of log in')
            raise AuthentificateFailedError(f'Wrong credentials, try again, attempts left {2 - self.clients[client_id]._auth_attempts}')

        else:
            self.clients[client_id]._auth_attempts = 0

    def search_accounts(self, accounts_number):
        seen_accs = {}

        for account in accounts_number:
            if account in self.accounts:
                seen_accs[account] = self.accounts[account]
        return seen_accs

    def mark_suspicious(self, client_id, reason):
        self.clients[client_id]._susp_operations.append(reason)

    def get_total_balance(self, client_id):
        total_balance = 0.00
        accounts = self.clients[client_id].accounts
        for acc in accounts:
            total_balance += self.accounts[acc]._balance

        return total_balance

    def get_bank_total_balance(self):
        total = 0.0
        for account_number in self.accounts:
            total = total + self.accounts[account_number]._balance
        return total

    def get_clients_ranking(self):
        ranking = []
        for client_id in self.clients:
            ranking.append((client_id, self.get_total_balance(client_id)))

        # simple sort: highest balance first
        i = 0
        while i < len(ranking):
            j = i + 1
            while j < len(ranking):
                if ranking[j][1] > ranking[i][1]:
                    temp = ranking[i]
                    ranking[i] = ranking[j]
                    ranking[j] = temp
                j = j + 1
            i = i + 1
        return ranking
