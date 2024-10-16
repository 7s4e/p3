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
@pytest.mark.parametrize(" expected, sequence", 
                         [('',       [keyboard.Keystroke('\n', 10)]), 
                          (' ',      [keyboard.Keystroke(' ', 32)]), 
                          ('!',      [keyboard.Keystroke('!', 33)]), 
                          ('1',      [keyboard.Keystroke('1', 49)]), 
                          ('A',      [keyboard.Keystroke('A', 65)]), 
                          ('a',      [keyboard.Keystroke('a', 97)]), 
                          ('~',      [keyboard.Keystroke('~', 126)]), 
                          ('a',      [keyboard.Keystroke('\x08', 8), 
                                      keyboard.Keystroke('\x09', 9), 
                                      keyboard.Keystroke('\x1b', 27), 
                                      keyboard.Keystroke('a', 97)])])

def test_read_keystroke(mock_prompt, sequence, expected):
    # Setup
    mock_prompt._con.cbreak = MagicMock()
    mock_prompt._con.cbreak.return_value.__enter__ = MagicMock()
    mock_prompt._con.cbreak.return_value.__exit__ = MagicMock()
    mock_prompt._con.hidden_cursor = MagicMock()
    mock_prompt._con.hidden_cursor.return_value.__enter__ = MagicMock()
    mock_prompt._con.hidden_cursor.return_value.__exit__ = MagicMock()

    key_iterator = iter(sequence)
    mock_prompt._con.inkey = lambda: next(key_iterator)

    # Execute
    mock_prompt._read_keystroke()

    # Verify
    assert mock_prompt._user_response == expected


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
@pytest.mark.parametrize(" response, expected", 
                         [('!',      False), 
                          ('1',      False), 
                          ('a',      False), 
                          ('A',      False), 
                          ('y',      True), 
                          ('Y',      True), 
                          ('n',      True), 
                          ('N',      True)])

def test_check_bool_validation(mock_prompt, response, expected):
    # Setup
    mock_prompt._user_response = response

    with patch.object(mock_prompt, '_put_alert') as mock_put_alert:

        # Execute
        result = mock_prompt._check_bool_validation()

        # Verify
        assert result == expected
        
        if expected == False:
            mock_put_alert.assert_called_once_with("Respond with 'y' or 'n'.")
        else:
            mock_put_alert.assert_not_called()


# Test _check_integer_validation
@pytest.mark.parametrize(
    " validation, response, expected,  alert", 
    [(None,       "123",    True,      ""), 
     (None,       "-123",   True,      ""), 
     (None,       "1.23",   False,     "Enter a valid number."), 
     (None,       "abc",    False,     "Enter a valid number."), 
     (9,          "0",      True,      ""), 
     (9,          "9",      False,     "Response is out of range."), 
     (9,          "-1",     False,     "Response is out of range."), 
     ((-7, 7),    "0",      True,      ""), 
     ((-7, 7),    "7",      True,      ""), 
     ((-7, 7),    "9",      False,     "Enter a number between -7 and 7."), 
     ((-7, 7),    "-7",     True,      ""), 
     ((-7, 7),    "-9",     False,     "Enter a number between -7 and 7.")])

def test_check_integer_validation(mock_prompt, validation, response, expected, 
                                  alert):
    # Setup
    mock_prompt._integer_validation = validation
    mock_prompt._user_response = response

    with patch.object(mock_prompt, '_put_alert') as mock_put_alert:

        # Execute
        result = mock_prompt._check_integer_validation()

        # Verify
        assert result == expected
        
        if expected == True:
            assert mock_prompt._validated_response == response
        else:
            mock_put_alert.assert_called_once_with(alert)


#Test _get_response
@pytest.mark.parametrize("keystroke, cursor", [(True, False), (False, True)])

def test_get_response(mock_prompt, keystroke, cursor):
    # Setup
    mock_prompt._expect_keystroke = keystroke

    with patch.object(mock_prompt, '_put_prompt') as mock_put_prompt, \
         patch.object(mock_prompt, '_read_keystroke') as mock_read_keystroke, \
         patch.object(mock_prompt, '_read_string') as mock_read_string:

        # Execute
        mock_prompt._get_response()

        # Verify
        mock_put_prompt.assert_called_once_with(leave_cursor_inline=cursor)
        
        if keystroke:
            mock_read_keystroke.assert_called_once()
            mock_read_string.assert_not_called()
        else:
            mock_read_keystroke.assert_not_called()
            mock_read_string.assert_called_once()


# Test _validate_response
@pytest.mark.parametrize(" boolean, integer, bool_rtn, int_rtn, expected", 
                         [(True,    False,   True,     None,    True), 
                          (True,    False,   False,    None,    False), 
                          (False,   True,    None,     True,    True), 
                          (False,   True,    None,     False,   False), 
                          (False,   False,   None,     None,    True)])

def test_get_validate_reponse(mock_prompt, boolean, integer, bool_rtn, int_rtn, 
                              expected):
    # Setup
    mock_prompt._validate_bool = boolean
    mock_prompt._validate_integer = integer

    with patch.object(mock_prompt, '_check_bool_validation', 
                      return_value=bool_rtn) as mock_check_bool_validation, \
         patch.object(mock_prompt, '_check_integer_validation', 
                      return_value=int_rtn) as mock_check_integer_validation:

        # Execute
        result = mock_prompt._validate_response()
        
        # Verify
        assert result == expected

        if boolean:
            mock_check_bool_validation.assert_called_once()
            mock_check_integer_validation.assert_not_called()
        elif integer:
            mock_check_bool_validation.assert_not_called()
            mock_check_integer_validation.assert_called_once()
        else:
            mock_check_bool_validation.assert_not_called()
            mock_check_integer_validation.assert_not_called()


# Test call
def test_call(mock_console):
    # Setup
    mock_prompt = ConsolePrompt("Mocked prompt")
    mock_prompt._validated_response = "mocked response"
    with patch.object(mock_prompt, '_get_response') as mock_get_response, \
         patch.object(mock_prompt, '_validate_response', 
                      side_effect=[False, True]) as mock_validate_response:
        
    # Execute
        result = mock_prompt.call(mock_console)

    # Verify
        assert result == "mocked response"
        assert mock_prompt._con == mock_console
        assert mock_get_response.call_count == 2
        assert mock_validate_response.call_count == 2
