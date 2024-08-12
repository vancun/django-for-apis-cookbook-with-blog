from decimal import Decimal
import pytest


class BadWithdrawRequest(Exception):
    pass


class NegativeOrZeroAmount(BadWithdrawRequest):
    def __init__(self, message="Cannot withdraw negative or zero amount."):
        super().__init__(message)


class NegativeOrZeroBalance(BadWithdrawRequest):
    def __init__(self, message="Cannot withdraw from negative or zero balance."):
        super().__init__(message)


class InsufficientBalance(BadWithdrawRequest):
    def __init__(self, message="Insufficient balance to complete withdrawal."):
        super().__init__(message)


def withdraw(balance, amount):
    if not isinstance(balance, Decimal) or not isinstance(amount, Decimal):
        raise TypeError("Both balance and amount must be Decimal instances.")
    if amount <= 0:
        raise NegativeOrZeroAmount()
    if balance <= 0:
        raise NegativeOrZeroBalance()
    if balance < amount:
        raise InsufficientBalance()
    return balance - amount


params_for_test_withdraw_success = {
    "enough-balance": (Decimal(10), Decimal(5), Decimal(5)),
    "full-balance": (Decimal(5), Decimal(5), Decimal(0)),
    "rounding-error": (Decimal("0.3"), Decimal("0.1"), Decimal("0.20")),
}

params_for_test_withdraw_failure = {
    "non-decimal-balance": (5, Decimal(-5), TypeError, "(?i)both balance and amount must be decimal instances"),
    "non-decimal-amount": (5, Decimal(-5), TypeError, "(?i)both balance and amount must be decimal instances"),
    "negative-amount": (Decimal(5), Decimal(-5), NegativeOrZeroAmount, "negative or zero amount"),
    "insufficient-balance": (Decimal(5), Decimal(10), InsufficientBalance, "(?i)insufficient balance"),
    "zero-balance": (Decimal(0), Decimal(5), NegativeOrZeroBalance, "negative or zero balance"),
    "negative-balance": (Decimal(-5), Decimal(5), NegativeOrZeroBalance, "negative or zero balance"),
}


@pytest.mark.parametrize(
    "balance, amount, expect",
    params_for_test_withdraw_success.values(),
    ids=params_for_test_withdraw_success.keys(),
)
def test_withdraw_success(balance, amount, expect):
    new_balance = withdraw(balance, amount)
    assert new_balance == expect


@pytest.mark.parametrize(
    "balance, amount, expect_raises, raise_matches",
    params_for_test_withdraw_failure.values(),
    ids=params_for_test_withdraw_failure.keys(),
)
def test_withdraw_failure(balance, amount, expect_raises, raise_matches):
    with pytest.raises(expect_raises, match=raise_matches):
        withdraw(balance, amount)
