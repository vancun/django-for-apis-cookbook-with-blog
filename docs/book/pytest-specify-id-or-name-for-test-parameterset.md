# Specify ID or Name for pytest Parameter Set


In `pytest`, you can add a name or a message to a parameter set to make it easier to identify which parameter set is being run. This can be particularly useful when you have many parameter sets or complex test cases.

Custom identifiers for `pytest` parametrization could be specified in different ways:

- Using a callback function passed as `ids` argument to `pytest.mark.parametrize`.
- Using a list of ids, passed as `ids` argument to `pytest.mark.parametrize`.
- Using `pytest.param`

First let's see how `pytest` is creating automatic identifiers:

## Parameterization with automatic identifiers

If you do not specify parameterset identifier, pytest will generate automatically such identifiers dinamically, based on the parameter values. Here’s an example of how this works:

```python
import pytest

test_data = [
    (1, 2),
    (2, 4),
    (3, 6)
]

@pytest.mark.parametrize(
    "input, expected", 
    test_data
)
def test_addition_automatic_param_ids(input, expected):
    assert input + input == expected
```

Running this test produces following result:

```
============================= test session starts ==============================
platform linux -- Python 3.10.13, pytest-8.3.2, pluggy-1.5.0 -- /home/codespace/.python/current/bin/python3
cachedir: .pytest_cache
django: version: 5.1, settings: blogapi.settings (from ini)
rootdir: /workspaces/django-for-apis-cookbook-with-blog
configfile: pytest.ini
plugins: anyio-4.4.0, cov-5.0.0, django-4.8.0
collecting ... collected 3 items

src/tests/recipes/test_custom_parameterset_identifiers.py::test_addition_automatic_param_ids[1-2] PASSED [ 33%]
src/tests/recipes/test_custom_parameterset_identifiers.py::test_addition_automatic_param_ids[2-4] PASSED [ 66%]
src/tests/recipes/test_custom_parameterset_identifiers.py::test_addition_automatic_param_ids[3-6] PASSED [100%]

============================== 3 passed in 0.05s ===============================
```

Each test parameterset has been assigned name/identifier by pytest.


## Provide custom identifiers with `pytest.param`


```python
import pytest

@pytest.mark.parametrize(
    "input, expected", 
    [
        pytest.param(1, 2, id="one_plus_one"),
        pytest.param(2, 4, id="two_plus_two"),
        pytest.param(3, 6, id="three_plus_three")
    ]
)
def test_addition_custom_id(input, expected):
    assert input + input == expected
```

The result from running above test function is:

```
============================= test session starts ==============================
platform linux -- Python 3.10.13, pytest-8.3.2, pluggy-1.5.0 -- /home/codespace/.python/current/bin/python3
cachedir: .pytest_cache
django: version: 5.1, settings: blogapi.settings (from ini)
rootdir: /workspaces/django-for-apis-cookbook-with-blog
configfile: pytest.ini
plugins: anyio-4.4.0, cov-5.0.0, django-4.8.0
collecting ... collected 3 items

src/tests/recipes/test_custom_parameterset_identifiers.py::test_addition_custom_id[one_plus_one] PASSED [ 33%]
src/tests/recipes/test_custom_parameterset_identifiers.py::test_addition_custom_id[two_plus_two] PASSED [ 66%]
src/tests/recipes/test_custom_parameterset_identifiers.py::test_addition_custom_id[three_plus_three] PASSED [100%]

============================== 3 passed in 0.06s ===============================
```

As you can see the identifiers we provided in the `pytest.param` decorator are being used by `pytest`.


## Provide custom identifiers with `ids` parameter

You can spcify explicit identifiers for parametersets using the `ids` parameter of the `pytest.mark.parametrize` fixture:

```python
@pytest.mark.parametrize(
    "input, expected", 
    test_data,
    ids = ("one_plus_one", "two_plus_two", "three_plus_three")
)
def test_addition_custom_ids_list(input, expected):
    assert input + input == expected
```

Produces following result:

```
============================= test session starts ==============================
platform linux -- Python 3.10.13, pytest-8.3.2, pluggy-1.5.0 -- /home/codespace/.python/current/bin/python3
cachedir: .pytest_cache
django: version: 5.1, settings: blogapi.settings (from ini)
rootdir: /workspaces/django-for-apis-cookbook-with-blog
configfile: pytest.ini
plugins: anyio-4.4.0, cov-5.0.0, django-4.8.0
collecting ... collected 3 items

src/tests/recipes/test_custom_parameterset_identifiers.py::test_addition_custom_ids_list[one_plus_one] PASSED [ 33%]
src/tests/recipes/test_custom_parameterset_identifiers.py::test_addition_custom_ids_list[two_plus_two] PASSED [ 66%]
src/tests/recipes/test_custom_parameterset_identifiers.py::test_addition_custom_ids_list[three_plus_three] PASSED [100%]

============================== 3 passed in 0.07s ===============================
```

## Good Practice: Use Dictionary to Define Test Parameters

Let's assume we need to test a function which can be used to withdraw money from a bank account.

```python
from decimal import Decimal


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
```

We can create two test functions - one for testing success and one for testing failure. The two functions are parametrized.

We could use dictionary to define the function parameters. The keys of the dictionary are the ids of the parameter set, expressing the behavior being tested and the value is
the actual parameterset.

```python
import pytest

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

```
Running the tests produces following output:

```
============================= test session starts ==============================
platform linux -- Python 3.10.13, pytest-8.3.2, pluggy-1.5.0 -- /home/codespace/.python/current/bin/python3
cachedir: .pytest_cache
django: version: 5.1, settings: blogapi.settings (from ini)
rootdir: /workspaces/django-for-apis-cookbook-with-blog
configfile: pytest.ini
plugins: anyio-4.4.0, cov-5.0.0, django-4.8.0
collecting ... collected 9 items

src/tests/sandbox/test_parametrize_with_dictionary.py::test_withdraw_success[enough-balance] PASSED [ 11%]
src/tests/sandbox/test_parametrize_with_dictionary.py::test_withdraw_success[full-balance] PASSED [ 22%]
src/tests/sandbox/test_parametrize_with_dictionary.py::test_withdraw_success[rounding-error] PASSED [ 33%]
src/tests/sandbox/test_parametrize_with_dictionary.py::test_withdraw_failure[non-decimal-balance] PASSED [ 44%]
src/tests/sandbox/test_parametrize_with_dictionary.py::test_withdraw_failure[non-decimal-amount] PASSED [ 55%]
src/tests/sandbox/test_parametrize_with_dictionary.py::test_withdraw_failure[negative-amount] PASSED [ 66%]
src/tests/sandbox/test_parametrize_with_dictionary.py::test_withdraw_failure[insufficient-balance] PASSED [ 77%]
src/tests/sandbox/test_parametrize_with_dictionary.py::test_withdraw_failure[zero-balance] PASSED [ 88%]
src/tests/sandbox/test_parametrize_with_dictionary.py::test_withdraw_failure[negative-balance] PASSED [100%]

============================== 9 passed in 0.10s ===============================
```

## Generate Dynamic Identifiers

You might also want to generate identifiers dynamically based on the parameter values. Here’s an example of how you can do that:

```python
import pytest

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
```
And the output:

```
============================= test session starts ==============================
platform linux -- Python 3.10.13, pytest-8.3.2, pluggy-1.5.0 -- /home/codespace/.python/current/bin/python3
cachedir: .pytest_cache
django: version: 5.1, settings: blogapi.settings (from ini)
rootdir: /workspaces/django-for-apis-cookbook-with-blog
configfile: pytest.ini
plugins: anyio-4.4.0, cov-5.0.0, django-4.8.0
collecting ... collected 3 items

src/tests/sandbox/test_custom_parameterset_identifiers.py::test_addition_dynamic_id1[1_plus_1_expected_2] PASSED [ 33%]
src/tests/sandbox/test_custom_parameterset_identifiers.py::test_addition_dynamic_id1[2_plus_2_expected_4] PASSED [ 66%]
src/tests/sandbox/test_custom_parameterset_identifiers.py::test_addition_dynamic_id1[3_plus_3_expected_6] PASSED [100%]

============================== 3 passed in 0.06s ===============================
```

## Assign Custom Idenfiers for Parameterized `pytest` Fixutres

For parametrized fixtures, you could use the `ids` parameter of the fixture decorator and access the current parameter value by inspecting `request.param`:

```python
@pytest.fixture(params=["done", "in prog", "todo"], ids=["State: Done", "State: In Progress", "State: To Do"])
def start_state(request):
    return request.param

def test_finish(cards_db, start_state):
    c = Card('write a book', state=start_sate)
    index = cards_db.add_card(c)
    cards_db.finish(index)
    card = cards_db.get_card(index)
    assert card.state == "done"
```


## Conclusion

By using `pytest.param` with the `id` argument and including custom messages in assertions, you can make your `pytest` test outputs more informative and easier to understand.

