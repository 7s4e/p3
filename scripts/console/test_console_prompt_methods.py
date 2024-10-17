import pytest
from unittest.mock import patch, MagicMock
from blessed import keyboard, Terminal
from console import ConsolePrompt


@pytest.fixture
def mock_console(mocker):
    """Fixture to create a mock Terminal object."""
    return mocker.Mock(spec=Terminal)

@pytest.fixture
def mock_prompt(mock_console):
    """Fixture to create a mock ConsolePrompt instance."""
    prompt = ConsolePrompt("Test prompt")
    prompt._con = mock_console
    return prompt


# Test _print_message
@pytest.mark.parametrize(
    " width, padding,  is_inline, message", 
    [(1,     " " * 0,  False,     "Lorem ipsum odor amet, consectetuer adipiscing elit."),
     (79,    " " * 0,  False,     "Lorem ipsum odor amet, consectetuer adipiscing elit."),
     (99,    " " * 10, False,     "Lorem ipsum odor amet, consectetuer adipiscing elit."),
     (79,    " " * 0,  True,      "Lorem ipsum odor amet, consectetuer adipiscing elit."),
     (79,    " " * 0,  True,      "Lorem ipsum odor amet, consectetuer adipiscing elit. Torquent leo consectetur sodales etiam ex gravida eleifend interdum.")])

def test_print_message(mock_prompt, capfd, width, padding, message, is_inline):
    """Test the _print_message method with mocked terminal and output 
        capture.
    """
    # Setup
    mock_prompt._con.width = width

    # Execute
    mock_prompt._print_message(message, leave_cursor_inline=is_inline)
    out, err = capfd.readouterr()

    # Verify
    text = padding + message
    ln_break = text.rfind(" ", 0, min(width, 79))
    assert out.startswith(text[:ln_break if ln_break > 0 else width])
    assert out.endswith("\n") != is_inline
    assert err == ""


# Test _put_prompt
@pytest.mark.parametrize("is_inline, end", [(True, " "), (False, "\n")])

def test_put_prompt(mock_prompt, capfd, is_inline, end):
    # Setup
    mock_prompt._con.width = 79
    mock_prompt._con.bright_yellow = lambda x: f"[yellow]{x}[/yellow]"

    # Execute
    mock_prompt._put_prompt(leave_cursor_inline=is_inline)
    out, err = capfd.readouterr()

    # Verify
    assert out.startswith("[yellow]Test prompt[/yellow]")
    assert out.endswith(end)
    assert err == ""


# Test _put_alert
def test_put_alert(mock_prompt, capfd):
    # Setup
    mock_prompt._con.width = 79
    mock_prompt._con.red = lambda x: f"[red]{x}[/red]"

    # Execute
    mock_prompt._put_alert("Alert message")
    out, err = capfd.readouterr()

    # Verify
    assert out == "[red]Alert message[/red]\n"
    assert err == ""


# Test _read_keystroke
@pytest.mark.parametrize(" expected_output, key_sequence", 
                         [('',              [keyboard.Keystroke('\n', 10)]), 
                          (' ',             [keyboard.Keystroke(' ', 32)]), 
                          ('!',             [keyboard.Keystroke('!', 33)]), 
                          ('1',             [keyboard.Keystroke('1', 49)]), 
                          ('A',             [keyboard.Keystroke('A', 65)]), 
                          ('a',             [keyboard.Keystroke('a', 97)]), 
                          ('~',             [keyboard.Keystroke('~', 126)]), 
                          ('a',             [keyboard.Keystroke('\x08', 8), 
                                             keyboard.Keystroke('\x09', 9), 
                                             keyboard.Keystroke('\x1b', 27), 
                                             keyboard.Keystroke('a', 97)])])

def test_read_keystroke(mock_prompt, key_sequence, expected_output):
    # Setup
    mock_prompt._con.cbreak = MagicMock()
    mock_prompt._con.cbreak.return_value.__enter__ = MagicMock()
    mock_prompt._con.cbreak.return_value.__exit__ = MagicMock()
    mock_prompt._con.hidden_cursor = MagicMock()
    mock_prompt._con.hidden_cursor.return_value.__enter__ = MagicMock()
    mock_prompt._con.hidden_cursor.return_value.__exit__ = MagicMock()
    key_iterator = iter(key_sequence)
    mock_prompt._con.inkey = lambda: next(key_iterator)

    # Execute
    mock_prompt._read_keystroke()

    # Verify
    assert mock_prompt._user_response == expected_output


# Test _read_string
"""Needs work"""
# @pytest.mark.parametrize(
#     " expected_output, input_sequence", 
#     [
#      ("abc",           [keyboard.Keystroke('a', 97), 
#                         keyboard.Keystroke('b', 98), 
#                         keyboard.Keystroke('c', 99), 
#                         keyboard.Keystroke('\n', 10)]), 
#      ("b",             [keyboard.Keystroke('a', 97), 
#                         keyboard.Keystroke('\x08', 8), 
#                         keyboard.Keystroke('b', 98), 
#                         keyboard.Keystroke('\n', 10)]), 
#      ("ab",            [keyboard.Keystroke('\x08', 8), 
#                         keyboard.Keystroke('a', 97), 
#                         keyboard.Keystroke('b', 98), 
#                         keyboard.Keystroke('\n', 8)])
#                         ])

# def test_read_string(mock_prompt, input_sequence, expected_output, capfd):
#     # Setup
#     mock_prompt._con.cbreak = MagicMock()
#     mock_prompt._con.cbreak.return_value.__enter__ = MagicMock()
#     mock_prompt._con.cbreak.return_value.__exit__ = MagicMock()
#     mock_prompt._con.inkey.side_effect = input_sequence
#     mock_prompt._con.green = lambda x: f"[green]{x}[/green]"

#     # Execute the method
#     mock_prompt._read_string()
#     out, err = capfd.readouterr()

#     # Verify the final response captured in _user_response
#     assert mock_prompt._user_response == expected_output

#     # Build expected printed output with proper handling of backspace
#     expected_stdout = []
#     for key in input_sequence:
#         if key.code == 8:  # Backspace
#             if expected_stdout:
#                 # Simulate the backspace visual effect in terminal (\b \b)
#                 expected_stdout.pop()  # Remove the last character from the visible output
#         elif 32 <= key.code <= 126:  # Printable characters
#             expected_stdout.append(f"[green]{str(key)}[/green]")  # Add colored char

#     # Join expected printed output with color and backspace handling
#     expected_stdout = ''.join(expected_stdout) + '\n'

#     # Verify captured stdout matches the expected printed output with color
#     assert out == expected_stdout, f"Expected: {expected_stdout}, Got: {out}"
#     assert err == ""


# Test _check_bool_validation
@pytest.mark.parametrize(" response, valid", 
                         [('!',      False), 
                          ('1',      False), 
                          ('a',      False), 
                          ('A',      False), 
                          ('y',      True), 
                          ('Y',      True), 
                          ('n',      True), 
                          ('N',      True)])

def test_check_bool_validation(mock_prompt, response, valid):
    # Setup
    mock_prompt._user_response = response
    with patch.object(mock_prompt, '_put_alert') as mock_put_alert:

    # Execute
        result = mock_prompt._check_bool_validation()

    # Verify
        assert result == valid
        if not valid:
            mock_put_alert.assert_called_once_with("Respond with 'y' or 'n'.")
        else:
            mock_put_alert.assert_not_called()


# Test _check_intger_validation
@pytest.mark.parametrize(
    " validation, response, valid,  alert", 
    [(None,       "123",    True,   ""), 
     (None,       "-123",   True,   ""), 
     (None,       "1.23",   False,  "Enter a valid number."), 
     (None,       "abc",    False,  "Enter a valid number."), 
     (9,          "0",      True,   ""), 
     (9,          "9",      False,  "Response is out of range."), 
     (9,          "-1",     False,  "Response is out of range."), 
     ((-7, 7),    "0",      True,   ""), 
     ((-7, 7),    "7",      True,   ""), 
     ((-7, 7),    "9",      False,  "Enter a number between -7 and 7."), 
     ((-7, 7),    "-7",     True,   ""), 
     ((-7, 7),    "-9",     False,  "Enter a number between -7 and 7.")])

def test_check_integer_validation(mock_prompt, capfd, validation, response, 
                                  valid, alert):
    # Setup
    mock_prompt._integer_validation = validation
    mock_prompt._user_response = response
    with patch.object(mock_prompt, '_put_alert') as mock_put_alert:

    # Execute
        result = mock_prompt._check_integer_validation()

    # Verify
        assert result == valid
        if valid:
            assert mock_prompt._validated_response == response
        else:
            mock_put_alert.assert_called_once_with(alert)


#Test _get_response
# @pytest.mark.parametrize(
#     " expect_keystroke", 
#     [(None,       "123",    True,   ""), 
#      ((-7, 7),    "-9",     False,  "Enter a number between -7 and 7.")])

# def test_get_response(mock_prompt, expect_keystroke):
#     # Setup
#     mock_prompt._expect_keystroke = expect_keystroke
#     mock_prompt._integer_validation = validation
#     mock_prompt._user_response = response
        
#     # Execute
#     result = mock_prompt._check_integer_validation()
#     message = "" if valid else f"[red]{alert}[/red]\n"
#     out, err = capfd.readouterr()

#     # Verify
#     if valid:
#         assert mock_prompt._validated_response == response
#     assert result == valid
#     assert out == message
#     assert err == ""

"""
getResponse()
    GET self.expectKeystroke
    IF expectKeystroke
        putPrompt(inlineCursor=False)
        SET userResponse <- readKeystroke()
    ELSE
        putPrompt(inlineCursor=True)
        SET userResponse <- readString()
END
"""


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

