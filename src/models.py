from dataclasses import dataclass
from enum import Enum
from typing import TypedDict

@dataclass
class ClientData:
    name: str
    surname: str

class AccountStatus(Enum):
    ACTIVE = 'active'
    FROZEN = 'frozen'
    CLOSED = 'closed'

class ClientStatus(Enum):
    ACTIVE = 'active'
    BLOCKED = 'blocked'
    DEPRECATED = 'deprecated'

class Currencies(Enum):
    RUB = 'RUB'
    USD = 'USD'
    EUR = 'EUR'
    KZT = 'KZT'
    CNY = 'CNY'

class Assets(Enum):
    stocks = 'stocks'
    bonds = 'bonds'
    etf = 'etf'

class Portfolio(TypedDict):
    bonds: float
    stocks: float
    etf: float