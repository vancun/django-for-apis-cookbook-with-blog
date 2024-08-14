import pytest




@pytest.fixture(name="f")
def given_f():
    return lambda a, b: a + b


params_test_addition = ((1, 1, 2),)


@pytest.mark.parametrize(
    "a, b, expected",
    params_test_addition,
    ids=[f"{a} + {b} == {c}" for a, b, c in params_test_addition],
)
def test_addition(a, b, expected, f):
    assert a + b == expected
