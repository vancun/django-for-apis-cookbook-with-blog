import pytest

test_data = [(1, 2), (2, 4), (3, 6)]


def idfn(value):
    if isinstance(value, tuple):
        input, output = value
        return f"{input}_plus_{output}"
    return str(value)



@pytest.mark.parametrize(
    "input, expected",
    [
        pytest.param(1, 2, id="one_plus_one"),
        pytest.param(2, 4, id="two_plus_two"),
        pytest.param(3, 6, id="three_plus_three"),
    ],
)
def test_addition_custom_id(input, expected):
    assert input + input == expected


@pytest.mark.parametrize(
    "input, expected",
    test_data,
    ids=("one_plus_one", "two_plus_two", "three_plus_three"),
)
def test_addition_custom_ids_list(input, expected):
    assert input + input == expected


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
    if amount <= 0:
        raise NegativeOrZeroAmount()
    if balance <= 0:
        raise NegativeOrZeroBalance()
    if balance < amount:
        raise InsufficientBalance()
    return balance - amount


params_for_test_withdraw_success = {
    "withdrawal-enough-balance": (10, 5, 5),
    "withdrawal-all-balance": (5, 5, 0),
}

params_for_test_withdraw_failure = {
    "negative-amount": (5, -5, NegativeOrZeroAmount, "negative or zero amount"),
    "insufficient-balance": (5, 10, InsufficientBalance, "(?i)insufficient balance"),
    "zero-balance": (0, 5, NegativeOrZeroBalance, "negative or zero balance"),
    "negative-balance": (-5, 5, NegativeOrZeroBalance, "negative or zero balance"),
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


test_data = [
    (1, 2),
    (2, 4),
    (3, 6)
]

@pytest.mark.parametrize(
    "input, expected",
    test_data,
    ids = (f"{input}_plus_{input}_expected_{expected}" for input, expected in test_data)
)
def test_addition_dynamic_id1(input, expected):
    assert input + input == expected
