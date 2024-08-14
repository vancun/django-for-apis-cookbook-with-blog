# Pytest Structure and Naming

## Organize `pytest` Tests

How to organize unit and functional tests for python application. Directories, test files, test functions, test classes, test methods, fixtures etc. Test framework is pytest.

Organizing unit and functional tests in a Python application using pytest can be done in a structured and logical manner to make it easy to manage and scale as the application grows. Here’s a suggested approach:

### Directory Structure

A common practice is to mirror the application’s directory structure in the `tests` directory. Here’s an example structure:

```
my_project/
│
├── my_app/
│   ├── __init__.py
│   ├── module1.py
│   ├── module2.py
│   └── ...
│
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_module1.py
│   │   ├── test_module2.py
│   │   └── ...
│   ├── functional/
│   │   ├── __init__.py
│   │   ├── test_feature1.py
│   │   ├── test_feature2.py
│   │   └── ...
│   └── conftest.py
│
├── requirements.txt
└── setup.py
```

### Test Files

- **Unit tests** should be placed in the `tests/unit/` directory and should focus on testing individual functions or classes.
- **Functional tests** should be placed in the `tests/functional/` directory and should test the application’s behavior by simulating user interactions or system operations.

### Test Functions

Each test function should test a small, isolated piece of functionality. By convention, test function names should start with `test_`.

```python
# tests/unit/test_module1.py

def test_function1_behavior():
    # Arrange
    # Act
    # Assert
```

### Test Classes

Group related tests into test classes. Use setup and teardown methods to prepare the test environment.

```python
# tests/unit/test_module1.py

import pytest

class TestModule1:
    def setup_method(self):
        # Setup before each test method
        pass

    def teardown_method(self):
        # Teardown after each test method
        pass

    def test_function1_behavior(self):
        # Arrange
        # Act
        # Assert
```

### Test Methods

Within test classes, each method should test a specific aspect of the functionality.

```python
# tests/unit/test_module1.py

class TestModule1:
    def test_function1_behavior(self):
        # Test specific behavior of function1
        pass

    def test_function1_edge_case(self):
        # Test edge cases of function1
        pass
```

### Fixtures

Use fixtures to provide a fixed baseline upon which tests can reliably and repeatedly execute. Define fixtures in `conftest.py` to make them available across multiple test files.

```python
# tests/conftest.py

import pytest

@pytest.fixture
def sample_fixture():
    # Setup
    data = {"key": "value"}
    yield data
    # Teardown (optional)
```

```python
# tests/unit/test_module1.py

def test_function_with_fixture(sample_fixture):
    assert sample_fixture["key"] == "value"
```

### Example of a Functional Test

Functional tests can follow a similar structure but focus on higher-level application behavior.

```python
# tests/functional/test_feature1.py

def test_feature1_behavior():
    # Simulate user interaction or system operation
    # Assert expected behavior
    pass
```

### Running Tests

You can run all tests using the `pytest` command:

```
pytest
```

To run only unit tests or functional tests:

```
pytest tests/unit/
pytest tests/functional/
```

### Summary

- **Directory Structure**: Mirror the application structure within the `tests` directory.
- **Test Files**: Separate unit and functional tests into different subdirectories.
- **Test Functions**: Use descriptive function names that start with `test_`.
- **Test Classes**: Group related tests and use setup/teardown methods.
- **Fixtures**: Define reusable fixtures in `conftest.py` for shared test setup.

By organizing your tests in this manner, you can maintain a clean and scalable test suite that is easy to navigate and extend.

Notes:

- Unit tests could be placed directly under the `tests/` directory.
- Unit tests could be marked with a `unit` mark
- Functional tests could be marked with a `functional` mark

## Naming Conventions

When naming test methods, it's important to create a convention that ensures clarity, consistency, and readability. Below are four different conventions for structuring test method names, each emphasizing different parts of the test:

### **1. Action-Based Convention**
   - **Format**: `test_<Action>__<ConditionOrScenario>`
   - **Parts**:
     - **Action**: The method or behavior being tested.
     - **Condition or Scenario**: The specific condition or scenario under which the action is being tested.
   - **Example**:
     - `test_add_item__when_cart_is_empty`
     - `test_save_user__with_valid_data`
     - `test_remove_item__when_item_not_in_cart`

### **2. Given-When-Then Convention**
   - **Format**: `test_given<Condition>__when<MethodName>__then<ExpectedOutcome>`
   - **Parts**:
     - **Given Condition**: The initial setup or state before the action.
     - **When Method Name**: The method being tested.
     - **Then Expected Outcome**: The expected result of the test.
   - **Example**:
     - `test_given_empty_cart__when_add_item__then_item_count_increases`
     - `test_given_existing_user__when_login__then_successful_login`
     - `test_given_out_of_stock_item__when_add_to_cart__then_raises_error`

### **3. Behavior-Driven Convention**
   - **Format**: `test_<MethodName>__should<ExpectedBehavior>__when<Condition>`
   - **Parts**:
     - **Method Name**: The name of the method being tested.
     - **Expected Behavior**: What the method is expected to do.
     - **Condition**: The condition under which the behavior is expected.
   - **Example**:
     - `test_add_item__should_increase_item_count__when_item_in_stock`
     - `test_calculate_total__should_include_tax__when_tax_applies`
     - `test_login__should_fail__when_password_is_incorrect`

### **4. Context-Outcome Convention**
   - **Format**: `test_<MethodName>__on<ConditionOrContext>__returns<ExpectedOutcome>`
   - **Parts**:
     - **Method Name**: The name of the method under test.
     - **Condition or Context**: The specific scenario or context.
     - **Expected Outcome**: The result or behavior expected from the method.
   - **Example**:
     - `test_create_user__on_valid_input__returns_user_instance`
     - `test_get_balance__on_insufficient_funds__returns_error`
     - `test_process_payment__on_invalid_card__returns_declined_status`

### **5. Outcome-Based Convention**
   - **Format**: `test_<ExpectedOutcome>__when_<MethodName>__with_<Condition>`
   - **Parts**:
     - **Expected Outcome**: The result or state expected after the test.
     - **Method Name**: The method being tested.
     - **Condition**: The specific condition or input being used.
   - **Example**:
     - `test_success__when_user_registers__with_valid_data`
     - `test_error__when_calculating_total__with_negative_values`
     - `test_empty_list__when_search__with_no_results`

### **6. Validation Convention**
   - **Format**: `test_<MethodName>__validates_<ExpectedBehavior>__under_<Condition>`
   - **Parts**:
     - **Method Name**: The method being tested.
     - **Validates Expected Behavior**: What the method should validate.
     - **Under Condition**: The scenario or context under which the validation happens.
   - **Example**:
     - `test_login__validates_user_authentication__under_correct_credentials`
     - `test_save_item__validates_unique_constraint__under_duplicate_entries`
     - `test_process_order__validates_inventory_update__under_successful_payment`

### **7. Scenario-Based Convention**
   - **Format**: `test_<MethodName>__in_scenario_<ScenarioDescription>`
   - **Parts**:
     - **Method Name**: The method or function being tested.
     - **Scenario Description**: A brief description of the scenario or context.
   - **Example**:
     - `test_calculate_discount__in_scenario_large_order`
     - `test_delete_account__in_scenario_user_has_active_subscription`
     - `test_generate_report__in_scenario_no_data_available`

### **8. Operation-Expectation Convention**
   - **Format**: `test_<Operation>__expects_<ExpectedResult>__for_<InputOrCondition>`
   - **Parts**:
     - **Operation**: The operation or method being tested.
     - **Expected Result**: The result expected from the operation.
     - **Input or Condition**: The input data or specific condition.
   - **Example**:
     - `test_add_item__expects_success__for_in_stock_product`
     - `test_login__expects_failure__for_invalid_password`
     - `test_update_profile__expects_no_change__for_invalid_email_format`

### **9. Input-Output Convention**
   - **Format**: `test_<MethodName>__input_<InputDescription>__output_<ExpectedOutput>`
   - **Parts**:
     - **Method Name**: The method or function being tested.
     - **Input Description**: A description of the input data.
     - **Expected Output**: The expected result or state.
   - **Example**:
     - `test_calculate_total__input_discounted_items__output_correct_total`
     - `test_filter_list__input_empty_list__output_empty_list`
     - `test_sort_array__input_unsorted_numbers__output_sorted_numbers`

### **10. Condition-Effect Convention**
   - **Format**: `test_<MethodName>__under_<Condition>__yields_<Effect>`
   - **Parts**:
     - **Method Name**: The method being tested.
     - **Condition**: The situation or input being tested.
     - **Effect**: The result or effect of that condition.
   - **Example**:
     - `test_save_user__under_duplicate_username__yields_validation_error`
     - `test_generate_report__under_no_data__yields_empty_report`
     - `test_process_payment__under_insufficient_funds__yields_transaction_failure`

### **11. Status-Behavior Convention**
   - **Format**: `test_<MethodName>__status_<InitialStatus>__behavior_<ExpectedBehavior>`
   - **Parts**:
     - **Method Name**: The method being tested.
     - **Initial Status**: The initial state or status before the method execution.
     - **Expected Behavior**: The behavior expected after the method is executed.
   - **Example**:
     - `test_checkout__status_cart_empty__behavior_redirect_to_shop`
     - `test_update_profile__status_user_logged_in__behavior_save_changes`
     - `test_delete_file__status_file_locked__behavior_raise_permission_error`

### **12. Contextual Behavior Convention**
   - **Format**: `test_<MethodName>__in_context_of_<SpecificContext>__does_<ExpectedBehavior>`
   - **Parts**:
     - **Method Name**: The method being tested.
     - **Specific Context**: The context or situation under which the test is conducted.
     - **Expected Behavior**: What the method is expected to do in this context.
   - **Example**:
     - `test_send_email__in_context_of_user_signup__does_send_welcome_email`
     - `test_upload_file__in_context_of_large_file__does_split_and_upload_in_parts`
     - `test_process_order__in_context_of_invalid_credit_card__does_fail_gracefully`

### **Choosing the Right Convention**:
- **Consistency**: Stick to one convention across your test suite for uniformity.
- **Readability**: Choose the convention that best balances detail with clarity.
- **Project Fit**: Some conventions may be more suited to certain types of projects or testing methodologies (e.g., behavior-driven vs. action-oriented).
- **Project Needs**: Consider the type of project and what convention aligns with the team's understanding.
- **Complexity**: More complex systems might benefit from conventions that include context, scenarios, or expected outcomes.
- **Team Agreement**: Ensure the chosen convention is agreed upon by the team to maintain consistency.

Each of these conventions ensures that your test method names are descriptive, making it easier for anyone reading the code to understand what is being tested and under what conditions.

These conventions offer a variety of ways to emphasize different aspects of your tests, such as the action being tested, the input/output, the context, or the expected outcome. The goal is to choose or adapt a convention that best fits the nature of your tests and the needs of your project.

## The Three-Part Test Naming Convention

The **three-part naming convention** for test function names is a structured approach that ensures each test name clearly communicates:

1. **The Method or Function Being Tested** - the **U**nit
2. **The Specific Condition or Scenario**  - the **S**cenario
3. **The Expected Outcome or Behavior** - the **E**xpected behavior or **E**xit Point 

**U**nit + **S**cenario + **E**xpected behavior == USE naming


### **Format**:
`test_<MethodName>__<ConditionOrScenario>__<ExpectedOutcome>`

### **Breakdown**:
1. **Method Name**: The specific method or function being tested.
2. **Condition or Scenario**: The particular condition, input, or scenario under which the test is performed.
3. **Expected Outcome**: The result or behavior that is expected when the method is invoked under the given condition.

### **Examples**:
- **Testing a User Login Method:**
  - `test_login__with_valid_credentials__returns_success`
  - `test_login__with_invalid_password__returns_error`
  
- **Testing a Cart’s Add Item Method:**
  - `test_add_item__when_item_in_stock__increases_item_count`
  - `test_add_item__when_item_out_of_stock__raises_out_of_stock_error`
  
- **Testing a Payment Processing Method:**
  - `test_process_payment__with_valid_card__completes_transaction`
  - `test_process_payment__with_expired_card__declines_payment`

- **Testing a File Upload Method:**
  - `test_upload_file__with_valid_format__saves_file`
  - `test_upload_file__with_unsupported_format__raises_error`

### **Benefits of Three-Part Naming**:
- **Clarity**: The test name clearly communicates what is being tested, under what conditions, and what the expected result is.
- **Readability**: The format makes it easy for developers to quickly understand the purpose of the test just by reading the function name.
- **Consistency**: Following this pattern across a codebase makes the tests more predictable and easier to navigate.

This convention is particularly useful in larger projects where tests need to be highly descriptive to ensure that every possible scenario is covered and understood.

