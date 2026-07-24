class BusinessException(Exception):
    """
    Base class for all business exceptions.
    """

    default_message = "Business operation failed."

    def __init__(self, message=None):
        self.message = message or self.default_message
        super().__init__(self.message)


class InsufficientBalanceException(BusinessException):
    default_message = "Insufficient balance."


class AccountFrozenException(BusinessException):
    default_message = "Account is frozen."


class AccountNotFoundException(BusinessException):
    default_message = "Account not found."


class DuplicateAccountException(BusinessException):
    default_message = "User already has a bank account."


class ReceiverAccountInactiveException(BusinessException):
    default_message = "Receiver account is not active."


class SelfBeneficiaryException(BusinessException):
    default_message = (
        "You cannot add your own account as a beneficiary."
    )

class BeneficiaryAlreadyExistsException(BusinessException):
    default_message = "Beneficiary already exists."