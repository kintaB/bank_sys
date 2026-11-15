class AccountFrozenError(Exception):
    pass

class AccountClosedError(Exception):
    pass

class InvalidOperationError(Exception):
    pass

class InsufficientFundsError(Exception):
    pass

class YoungClientError(Exception):
    pass

class AuthentificateFailedError(Exception):
    pass

class TooManyAttemptsError(Exception):
    pass

class DayTimeOperationError(Exception):
    pass