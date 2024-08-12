# Specify ID or Name for pytest Parameter Set


In `pytest`, you can add a name or a message to a parameter set to make it easier to identify which parameter set is being run. This can be particularly useful when you have many parameter sets or complex test cases.

To achieve this, you can use the `pytest.param` function, which allows you to add a custom identifier to each parameter set. We will see how this can be done, but first let's first see how `pytest` is creating automatic identifiers:

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
    [pytest.param(input, expected, id=f"{input}_plus_{input}") for input, expected in test_data]
)
def test_addition_dynamic_id(input, expected):
    assert input + input == expected
```

## Conclusion

By using `pytest.param` with the `id` argument and including custom messages in assertions, you can make your `pytest` test outputs more informative and easier to understand.

