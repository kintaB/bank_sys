from dataclasses import dataclass
from enum import Enum

@dataclass
class ClientData:
    name: str
    surname: str
    account_number: str | None = None

class AccountStatus(Enum):
    ACTIVE = 'active'
    FROZEN = 'frozen'
    CLOSED = 'closed'

class Currencies(Enum):
    RUB = 'RUB'
    USD = 'USD'
    EUR = 'EUR'
    KZT = 'KZT'
    CNY = 'CNY'