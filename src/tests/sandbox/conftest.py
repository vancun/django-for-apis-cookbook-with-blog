import pytest

@pytest.fixture(name="a")
def given_a():
    raise NotImplementedError()


def b():
    raise NotImplementedError()
