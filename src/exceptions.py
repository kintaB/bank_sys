class AccountFrozenError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None
    
    def __str__(self):
        print('calling magic method str')
        if self.message:
            return f'AccountFrozenError'
        else:
            return 'AccountFrozenError has been raised'


class AccountClosedError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None
    
    def __str__(self):
        print('calling magic method str')
        if self.message:
            return f'AccountFrozenError, '
        else:
            return 'AccountFrozenError has been raised'

class InvalidOperationError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None
    
    def __str__(self):
        print('calling magic method str')
        if self.message:
            return f'InvalidOperationError, '
        else:
            return 'InvalidOperationError has been raised'

class InsufficientFundsError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None
    
    def __str__(self):
        print('calling magic method str')
        if self.message:
            return f'InsufficientFundsError'
        else:
            return 'InsufficientFundsError has been raised'