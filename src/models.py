from dataclasses import dataclass

@dataclass
class ClientData:
    name: str
    surname: str
    account_number: str | None = None
