import pytest

test_data = [
    (1, 2),
    (2, 4),
    (3, 6)
]

@pytest.mark.parametrize(
    "input, expected", 
    [pytest.param(input, expected, id=f"{input}_plus_{input}") for input, expected in test_data]
)
def test_addition_dynamic_id(input, expected):
    assert input + input == expected

@pytest.mark.parametrize(
    "input, expected", 
    test_data
)
def test_addition_automatic_param_ids(input, expected):
    assert input + input == expected



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
