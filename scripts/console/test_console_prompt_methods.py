import pytest
from unittest.mock import MagicMock
from blessed import Terminal
from console import ConsolePrompt

@pytest.fixture
def mock_console(mocker):
    """Fixture to create a mock Terminal object."""
    return mocker.Mock(spec=Terminal)


# Test _print_message
@pytest.mark.parametrize(
    "width, padding,  is_inline, message", 
    [(1,    " " * 0,  False,     "Lorem ipsum odor amet, consectetuer adipiscing elit."),
     (79,   " " * 0,  False,     "Lorem ipsum odor amet, consectetuer adipiscing elit."),
     (99,   " " * 10, False,     "Lorem ipsum odor amet, consectetuer adipiscing elit."),
     (79,   " " * 0,  True,      "Lorem ipsum odor amet, consectetuer adipiscing elit."),
     (79,   " " * 0,  True,      "Lorem ipsum odor amet, consectetuer adipiscing elit. Torquent leo consectetur sodales etiam ex gravida eleifend interdum.")])

def test_print_message(mock_console, capfd, width, padding, message, is_inline):
    """Test the _print_message method with mocked terminal and output 
        capture.
    """
    # Setup
    mock_console.width = width
    cp = ConsolePrompt("Test prompt")
    cp._con = mock_console

    # Execute
    cp._print_message(message, leave_cursor_inline=is_inline)
    out, err = capfd.readouterr()

    # Verify
    text = padding + message
    ln_break = text.rfind(" ", 0, min(width, 79))
    assert out.startswith(text[:ln_break if ln_break > 0 else width])
    assert out.endswith("\n") != is_inline
    assert err == ""


# Test _put_prompt
@pytest.mark.parametrize("is_inline, end", [(True, " "), (False, "\n")])

def test_put_prompt(mock_console, capfd, is_inline, end):
    # Setup
    mock_console.width = 79
    mock_console.bright_yellow = lambda x: f"[yellow]{x}[/yellow]"
    cp = ConsolePrompt("Test prompt")
    cp._con = mock_console

    # Execute
    cp._put_prompt(leave_cursor_inline=is_inline)
    out, err = capfd.readouterr()

    # Verify
    assert out.startswith("[yellow]Test prompt[/yellow]")
    assert out.endswith(end)
    assert err == ""


# Test _put_alert
def test_put_alert(mock_console, capfd):
    # Setup
    mock_console.width = 79
    mock_console.red = lambda x: f"[red]{x}[/red]"
    cp = ConsolePrompt("Test prompt")
    cp._con = mock_console

    # Execute
    cp._put_alert("Alert message")
    out, err = capfd.readouterr()

    # Verify
    assert out == "[red]Alert message[/red]\n"
    assert err == ""


# Test _read_keystroke
@pytest.mark.parametrize("key", ['a', 'A', '1', '!', '\n', '\x08'])

def test_read_keystroke(mock_console, key):
    # Setup
    mock_console.cbreak = MagicMock()
    mock_console.cbreak.return_value.__enter__ = MagicMock()
    mock_console.cbreak.return_value.__exit__ = MagicMock()
    mock_console.hidden_cursor = MagicMock()
    mock_console.hidden_cursor.return_value.__enter__ = MagicMock()
    mock_console.hidden_cursor.return_value.__exit__ = MagicMock()
    mock_console.inkey = lambda: key
    cp = ConsolePrompt("Test prompt")
    cp._con = mock_console

    # Execute
    result = cp._read_keystroke()

    # Verify
    assert result == str(key)


# Test _read_string
# @pytest.mark.parametrize(
#     "expected_output, input_sequence", 
#     [
#      ("ab",           ['a', 'b', MagicMock(is_sequence=True, name='KEY_ENTER')]), 
#     #  ("a",            ['a', 'b', MagicMock(is_sequence=True, name='KEY_BACKSPACE'), MagicMock(is_sequence=True, name='KEY_ENTER')]), 
#     #  ("",             ['a', 'b', MagicMock(is_sequence=True, name='KEY_BACKSPACE'), MagicMock(is_sequence=True, name='KEY_BACKSPACE'), MagicMock(is_sequence=True, name='KEY_ENTER')])
#      ])

# def test_read_string(mock_console, input_sequence, expected_output):
#     # Setup
#     mock_console.cbreak = MagicMock()
#     mock_console.cbreak.return_value.__enter__ = MagicMock()
#     mock_console.cbreak.return_value.__exit__ = MagicMock()
#     mock_input_sequence = []
#     for char in input_sequence:
#         if isinstance(char, str):
#             key_mock = MagicMock(is_sequence=False)
#             key_mock.__str__.return_value = char
#             mock_input_sequence.append(key_mock)
#         else:
#             mock_input_sequence.append(char)
#     mock_console.inkey.side_effect = mock_input_sequence
#     # mock_console.green = lambda x: f"[green]{x}[/green]"
#     cp = ConsolePrompt("Test prompt")
#     cp._con = mock_console
#     cp._put_prompt = MagicMock()

#     # Execute
#     result = cp._read_string()

#     # Verify
#     assert result == expected_output
#     # mock_console.inkey.assert_called()
#     # mock_console.green.assert_called()
#     # cp._put_prompt.assert_called()

# # Parametrized test for _read_string
# @pytest.mark.parametrize(
#     "expected_output, input_sequence", 
#     [
#         # ("ab", ['a', 'b', MagicMock(is_sequence=True, name='KEY_ENTER')]),  # Test without backspace
#         ("a", ['a', 'b', 
#                 MagicMock(is_sequence=True, name='KEY_BACKSPACE'),  # Remove 'b'
#                 MagicMock(is_sequence=True, name='KEY_ENTER')])    # Press enter
#     ]
# )
# def test_read_string(mock_console, expected_output, input_sequence):
#     # Setup the mock console and behavior
#     mock_console.cbreak = MagicMock()
#     mock_console.cbreak.return_value.__enter__ = MagicMock()
#     mock_console.cbreak.return_value.__exit__ = MagicMock()
    
#     # Create a list to hold the mock input sequence
#     mock_input_sequence = []
    
#     for char in input_sequence:
#         if isinstance(char, str):
#             # Mock regular characters
#             key_mock = MagicMock(is_sequence=False)
#             key_mock.__str__.return_value = char  # Returns the character when printed or appended
#             mock_input_sequence.append(key_mock)
#         else:
#             # Mock control keys (e.g., KEY_ENTER, KEY_BACKSPACE)
#             mock_input_sequence.append(char)
    
#     # Simulate user input sequence via inkey side effect
#     mock_console.inkey.side_effect = mock_input_sequence
    
#     # Create an instance of the class with the method _read_string
#     cp = ConsolePrompt("Test prompt")
#     cp._con = mock_console
#     cp._put_prompt = MagicMock()

#     # Execute the method
#     result = cp._read_string()

#     # Verify the result matches the expected output
#     assert result == expected_output



@pytest.mark.parametrize(
    "expected_output, input_sequence", 
    [
        ("ab", ['a', 'b', MagicMock(is_sequence=False, name='a'), 
                MagicMock(is_sequence=False, name='b'),
                MagicMock(is_sequence=True, name='KEY_ENTER')]),  # Test without backspace
        ("a", ['a', 'b', 
               MagicMock(is_sequence=True, name='KEY_BACKSPACE'),  # Remove 'b'
               MagicMock(is_sequence=True, name='KEY_ENTER')])  # Press enter
    ]
)
def test_read_string(mock_console, expected_output, input_sequence):
    # Setup the mock console and behavior
    mock_console.cbreak = MagicMock()
    mock_console.cbreak.return_value.__enter__ = MagicMock()
    mock_console.cbreak.return_value.__exit__ = MagicMock()

    # Create a list to hold the mock input sequence
    mock_input_sequence = []
    
    for char in input_sequence:
        if isinstance(char, str):
            # Mock regular characters
            key_mock = MagicMock(is_sequence=False)
            key_mock.__str__.return_value = char  # Return the character when printed
            mock_input_sequence.append(key_mock)
        else:
            # Mock control keys (e.g., KEY_ENTER, KEY_BACKSPACE)
            key_mock = MagicMock(is_sequence=True)
            if 'BACKSPACE' in char.name:
                key_mock.name = 'KEY_BACKSPACE'  # Set backspace name
            elif 'ENTER' in char.name:
                key_mock.name = 'KEY_ENTER'  # Set enter name
            mock_input_sequence.append(key_mock)

    # Simulate user input sequence via inkey side effect
    mock_console.inkey.side_effect = mock_input_sequence
    
    # Create an instance of the class with the method _read_string
    cp = ConsolePrompt("Test prompt")
    cp._con = mock_console
    cp._put_prompt = MagicMock()

    # Execute the method
    result = cp._read_string()

    # Verify the result matches the expected output
    assert result == expected_output



# Test _check_bool_validation
# Test _check_int_validation
# Test _get_response
# Test _validate_response
# Test call




# def test_boolean_validation_yes(mock_consolesole, mocker):
#     prompt = ConsolePrompt("Do you want to continue? (y/n)", validate_bool=True)
#     prompt._response = "y"  # Simulate user input

#     mocker.patch.object(prompt, '_put_alert')  # Mock alert method
#     assert prompt.call(mock_consolesole) is True  # Expecting valid response

# def test_boolean_validation_no(mock_consolesole, mocker):
#     prompt = ConsolePrompt("Do you want to continue? (y/n)", validate_bool=True)
#     prompt._response = "n"  # Simulate user input

#     mocker.patch.object(prompt, '_put_alert')
#     assert prompt.call(mock_consolesole) is False  # Expecting valid response

# def test_invalid_boolean_input(mock_consolesole, mocker):
#     prompt = ConsolePrompt("Do you want to continue? (y/n)", validate_bool=True)
#     prompt._response = "maybe"  # Simulate invalid user input

#     mocker.patch.object(prompt, '_put_alert')  # Mock alert method
#     assert prompt.call(mock_consolesole) is None  # Expecting re-prompt

# def test_integer_validation_valid(mock_consolesole, mocker):
#     prompt = ConsolePrompt("Enter a number (0-10):", validate_integer=True, integer_validation=(0, 10))
#     prompt._response = "5"  # Simulate user input

#     mocker.patch.object(prompt, '_put_alert')
#     assert prompt.call(mock_consolesole) == "5"  # Expecting valid response

# def test_integer_validation_invalid(mock_consolesole, mocker):
#     prompt = ConsolePrompt("Enter a number (0-10):", validate_integer=True, integer_validation=(0, 10))
#     prompt._response = "15"  # Simulate invalid user input

#     mocker.patch.object(prompt, '_put_alert')
#     assert prompt.call(mock_consolesole) is None  # Expecting re-prompt

# def test_keystroke_input(mock_consolesole, mocker):
#     prompt = ConsolePrompt("Press any key:", expect_keystroke=True)
#     prompt._response = "a"  # Simulate keystroke input

#     mocker.patch.object(prompt, '_put_alert')
#     result = prompt.call(mock_consolesole)

#     assert result == repr("a")  # Expecting the keystroke representation

# def test_read_string(mock_consolesole, mocker):
#     prompt = ConsolePrompt("Enter a string:")
#     prompt._response = "test input"  # Simulate user input

#     mocker.patch.object(prompt, '_put_alert')
#     result = prompt.call(mock_consolesole)

#     assert result == "test input"  # Expecting the string input
