import pytest
from blessed import Terminal
from console import ConsolePrompt

@pytest.fixture
def mock_console(mocker):
    """Fixture to create a mock Terminal object."""
    return mocker.Mock(spec=Terminal)

@pytest.mark.parametrize("exp_key, val_bool, val_int, int_val", 
                          # no parameters
                         [(False, False, False, None),
                          # expect keystroke
                          (True, False, False, None),
                          # validate bool
                          (False, True, False, None),
                          # validate any integer
                          (False, False, True, None),
                          # validate within range
                          (False, False, True, 7),
                          # validate within limits
                          (False, False, True, (1, 9))])

def test_constructor(mock_console, exp_key, val_bool, val_int, int_val):
    """Test the constructor of ConsolePrompt with various parameters."""
    prompt = ConsolePrompt(">>> ", 
                           expect_keystroke=exp_key, 
                           validate_bool=val_bool, 
                           validate_integer=val_int, 
                           integer_validation=int_val)
    
    assert prompt._prompt == ">>> "
    assert prompt._expect_keystroke == exp_key
    assert prompt._validate_bool == val_bool
    assert prompt._validate_integer == val_int
    assert prompt._integer_validation == int_val

# def test_boolean_validation_yes(mock_console, mocker):
#     prompt = ConsolePrompt("Do you want to continue? (y/n)", validate_bool=True)
#     prompt._response = "y"  # Simulate user input

#     mocker.patch.object(prompt, '_put_alert')  # Mock alert method
#     assert prompt.call(mock_console) is True  # Expecting valid response

# def test_boolean_validation_no(mock_console, mocker):
#     prompt = ConsolePrompt("Do you want to continue? (y/n)", validate_bool=True)
#     prompt._response = "n"  # Simulate user input

#     mocker.patch.object(prompt, '_put_alert')
#     assert prompt.call(mock_console) is False  # Expecting valid response

# def test_invalid_boolean_input(mock_console, mocker):
#     prompt = ConsolePrompt("Do you want to continue? (y/n)", validate_bool=True)
#     prompt._response = "maybe"  # Simulate invalid user input

#     mocker.patch.object(prompt, '_put_alert')  # Mock alert method
#     assert prompt.call(mock_console) is None  # Expecting re-prompt

# def test_integer_validation_valid(mock_console, mocker):
#     prompt = ConsolePrompt("Enter a number (0-10):", validate_integer=True, integer_validation=(0, 10))
#     prompt._response = "5"  # Simulate user input

#     mocker.patch.object(prompt, '_put_alert')
#     assert prompt.call(mock_console) == "5"  # Expecting valid response

# def test_integer_validation_invalid(mock_console, mocker):
#     prompt = ConsolePrompt("Enter a number (0-10):", validate_integer=True, integer_validation=(0, 10))
#     prompt._response = "15"  # Simulate invalid user input

#     mocker.patch.object(prompt, '_put_alert')
#     assert prompt.call(mock_console) is None  # Expecting re-prompt

# def test_keystroke_input(mock_console, mocker):
#     prompt = ConsolePrompt("Press any key:", expect_keystroke=True)
#     prompt._response = "a"  # Simulate keystroke input

#     mocker.patch.object(prompt, '_put_alert')
#     result = prompt.call(mock_console)

#     assert result == repr("a")  # Expecting the keystroke representation

# def test_read_string(mock_console, mocker):
#     prompt = ConsolePrompt("Enter a string:")
#     prompt._response = "test input"  # Simulate user input

#     mocker.patch.object(prompt, '_put_alert')
#     result = prompt.call(mock_console)

#     assert result == "test input"  # Expecting the string input
