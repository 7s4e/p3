import pytest
from blessed import keyboard, Terminal
from console import ConsolePrompt


@pytest.fixture
def mock_console(mocker):
    return mocker.Mock(spec=Terminal)

@pytest.fixture
def mock_prompt(mock_console):
    mock = ConsolePrompt("Test prompt")
    mock._con = mock_console
    mock._con.width = 79
    return mock

@pytest.fixture
def cbreak_mock(mocker, mock_prompt):
    mock = mocker.patch.object(mock_prompt._con, "cbreak", mocker.MagicMock())
    mock.return_value.__enter__ = mocker.MagicMock()
    mock.return_value.__exit__ = mocker.MagicMock()
    return mock

@pytest.fixture
def hidden_cursor_mock(mocker, mock_prompt):
    mock = mocker.patch.object(mock_prompt._con, "hidden_cursor", 
                               mocker.MagicMock())
    mock.return_value.__enter__ = mocker.MagicMock()
    mock.return_value.__exit__ = mocker.MagicMock()
    return mock

@pytest.fixture
def put_alert_mock(mocker, mock_prompt):
    return mocker.patch.object(mock_prompt, "_put_alert")


# Test printMessage
@pytest.mark.parametrize(
    "width, padding, is_inline, message", 
    [
        # Test case 1: Minimum width
        (
            1, " " * 0, False, 
            "Lorem ipsum odor amet, consectetuer adipiscing elit."
        ), 
        # Test case 2: Standard width
        (
            79, " " * 0, False, 
            "Lorem ipsum odor amet, consectetuer adipiscing elit."
        ), 
        # Test case 3: Large width
        (
            99, " " * 10, False, 
            "Lorem ipsum odor amet, consectetuer adipiscing elit."
        ), 
        # Test case 4: Standard width, inline
        (
            79," " * 0, True, 
            "Lorem ipsum odor amet, consectetuer adipiscing elit."
        ), 
        # Test case 5: Standard width, text
        (
            79," " * 0, True, 
            "Lorem ipsum odor amet, consectetuer adipiscing elit. Torquent leo consectetur sodales etiam ex gravida eleifend interdum."
        )
    ]
)
def test_print_message(mock_prompt, capfd, width, padding, message, is_inline):
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


# Test putPrompt
@pytest.mark.parametrize("is_inline, end", 
                         [(True, " "),     # Test case 1: Inline
                          (False, "\n")])  # Test case 2: New line
def test_put_prompt(mock_prompt, capfd, is_inline, end):
    # Setup
    mock_prompt._con.bright_yellow = lambda x: f"[yellow]{x}[/yellow]"

    # Execute
    mock_prompt._put_prompt(leave_cursor_inline=is_inline)
    out, err = capfd.readouterr()

    # Verify
    assert out.startswith("[yellow]Test prompt[/yellow]")
    assert out.endswith(end)
    assert err == ""


# Test putAlert
def test_put_alert(mock_prompt, capfd):
    # Setup
    mock_prompt._con.red = lambda x: f"[red]{x}[/red]"

    # Execute
    mock_prompt._put_alert("Alert message")
    out, err = capfd.readouterr()

    # Verify
    assert out == "[red]Alert message[/red]\n"
    assert err == ""


# Test readKeystroke
@pytest.mark.parametrize(
    "exp_result, input_sequence", 
    [
        ('', [keyboard.Keystroke('\n', 10)]),   # Test case 1
        (' ', [keyboard.Keystroke(' ', 32)]),   # Test case 2
        ('!', [keyboard.Keystroke('!', 33)]),   # Test case 3
        ('1', [keyboard.Keystroke('1', 49)]),   # Test case 4
        ('A', [keyboard.Keystroke('A', 65)]),   # Test case 5
        ('a', [keyboard.Keystroke('a', 97)]),   # Test case 6
        ('~', [keyboard.Keystroke('~', 126)]),  # Test case 7

        # Test case 8: Non-printable keystrokes
        ('a', [keyboard.Keystroke('\x08', 8), keyboard.Keystroke('\x09', 9), 
            keyboard.Keystroke('\x1b', 27), keyboard.Keystroke('a', 97)])
    ]
)
def test_read_keystroke(mocker, mock_prompt, cbreak_mock, hidden_cursor_mock, 
                        input_sequence, exp_result):
    # Setup
    key_iterator = iter(input_sequence)
    mocker.patch.object(mock_prompt._con, "inkey", lambda: next(key_iterator))

    # Execute
    mock_prompt._read_keystroke()

    # Verify
    assert mock_prompt._user_response == exp_result


# Test readString
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


# Test checkBoolValidity
@pytest.mark.parametrize(
    "response, expected", 
    [
        # Test series 1: Invalid
        ('!', False), ('1', False), ('a', False), ('A', False), 

        # Test series 2: Valid
        ('y', True), ('Y', True), ('n', True), ('N', True)
    ]
)
def test_check_bool_validity(mock_prompt, put_alert_mock, response, expected):
    # Setup
    mock_prompt._user_response = response

    # Execute
    result = mock_prompt._check_bool_validity()

    # Verify
    assert result == expected
    if not expected:
        put_alert_mock.assert_called_once_with("Respond with 'y' or 'n'.")
    else:
        put_alert_mock.assert_not_called()


# Test checkIntegerValidity
@pytest.mark.parametrize(
    "validation, response, expected, alert", 
    [
        # Test series 1: No extra validation of integer
        (None, "123", True, ""), 
        (None, "-123", True, ""), 
        (None, "1.23", False, "Enter a valid number."), 
        (None, "abc", False, "Enter a valid number."), 

        # Test series 2: Valid range defined by single integer
        (9, "0", True, ""), 
        (9, "9", False, "Response is out of range."), 
        (9, "-1", False, "Response is out of range."), 

        # Test series 3: Valid range defined by tuple
        ((-7, 7), "0", True, ""), 
        ((-7, 7), "7", True, ""), 
        ((-7, 7), "9", False, "Enter a number between -7 and 7."), 
        ((-7, 7), "-7", True, ""), 
        ((-7, 7), "-9", False, "Enter a number between -7 and 7.")
    ]
)
def test_check_integer_validity(mock_prompt, put_alert_mock, validation, 
                                response, expected, alert):
    # Setup
    mock_prompt._integer_validation = validation
    mock_prompt._user_response = response

    # Execute
    result = mock_prompt._check_integer_validity()

    # Verify
    assert result == expected
    if expected == True:
        assert mock_prompt._validated_response == response
    else:
        put_alert_mock.assert_called_once_with(alert)


#Test _get_response
@pytest.mark.parametrize(
    "keystroke, cursor", 
    [(True, False),  # Test case 1: readKeystroke path
     (False, True)]  # Test case 2: readString path
)
def test_get_response(mocker, mock_prompt, keystroke, cursor):
    # Setup
    put_prompt_mock = mocker.patch.object(mock_prompt, "_put_prompt")
    read_keystroke_mock = mocker.patch.object(mock_prompt, "_read_keystroke")
    read_string_mock = mocker.patch.object(mock_prompt, "_read_string")
    mock_prompt._expect_keystroke = keystroke

    # Execute
    mock_prompt._get_response()

    # Verify
    put_prompt_mock.assert_called_once_with(leave_cursor_inline=cursor)
    if keystroke:
        read_keystroke_mock.assert_called_once()
        read_string_mock.assert_not_called()
    else:
        read_keystroke_mock.assert_not_called()
        read_string_mock.assert_called_once()


# Test _validate_response
@pytest.mark.parametrize(
    "bool_path, int_path, bool_rtn, int_rtn, exp_result", 
    [
        # Test case 1: True on checkBoolValidity path
        (True, False, True, None, True), 

        # Test case 2: False on checkBoolValidity path
        (True, False, False, None, False), 

        # Test case 3: True on checkIntegerValidity path
        (False, True, None, True, True), 

        # Test case 4: False on checkIntegerValidity path
        (False, True, None, False, False), 

        # Test case 5: No validation required
        (False, False, None, None, True)]
)
def test_get_validate_reponse(mocker, mock_prompt, bool_path, int_path, 
                              bool_rtn, int_rtn, exp_result):
    # Setup
    check_bool_validity_mock = mocker.patch.object(mock_prompt, 
                                                   "_check_bool_validity", 
                                                   return_value=bool_rtn)
    check_int_validity_mock = mocker.patch.object(mock_prompt, 
                                                  "_check_integer_validity", 
                                                  return_value=int_rtn)
    mock_prompt._validate_bool = bool_path
    mock_prompt._validate_integer = int_path

    # Execute
    result = mock_prompt._validate_response()

    # Verify
    assert result == exp_result
    if bool_path:
        check_bool_validity_mock.assert_called_once()
        check_int_validity_mock.assert_not_called()
    elif int_path:
        check_bool_validity_mock.assert_not_called()
        check_int_validity_mock.assert_called_once()
    else:
        check_bool_validity_mock.assert_not_called()
        check_int_validity_mock.assert_not_called()


# Test call
def test_call(mocker, mock_console):
    # Setup
    mock_prompt = ConsolePrompt("Mocked prompt")
    get_response_mock = mocker.patch.object(mock_prompt, "_get_response")
    validate_response_mock = mocker.patch.object(mock_prompt, 
                                                 "_validate_response", 
                                                 side_effect=[False, True])
    mock_prompt._validated_response = "mocked response"
    
    # Execute
    result = mock_prompt.call(mock_console)

    # Verify
    assert mock_prompt._con == mock_console
    assert get_response_mock.call_count == 2
    assert validate_response_mock.call_count == 2
    assert result == "mocked response"
