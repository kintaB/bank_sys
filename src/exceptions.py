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

class TransactionCancelledError(Exception):
    pass

class TransactionDeclinedError(Exception):
    pass

class TransactionRefundedError(Exception):
    pass

class TransactionRejectedError(Exception):
    pass
