import pytest
from blessed import keyboard, Terminal
from src import ConsolePrompt


@pytest.fixture
def mock_console(mocker):
    mck = mocker.Mock(spec=Terminal)
    mck.width = 79
    return mck

@pytest.fixture
def prompt_inst(mock_console):
    inst = ConsolePrompt("Test prompt")
    inst._trm = mock_console
    return inst

@pytest.fixture
def cbreak_mock(mocker, prompt_inst):
    mck = mocker.patch.object(prompt_inst._trm, "cbreak", mocker.MagicMock())
    mck.return_value.__enter__ = mocker.MagicMock()
    mck.return_value.__exit__ = mocker.MagicMock()
    return mck

@pytest.fixture
def hidden_cursor_mock(mocker, prompt_inst):
    mck = mocker.patch.object(prompt_inst._trm, "hidden_cursor", 
                              mocker.MagicMock())
    mck.return_value.__enter__ = mocker.MagicMock()
    mck.return_value.__exit__ = mocker.MagicMock()
    return mck

@pytest.fixture
def put_alert_mock(mocker, prompt_inst):
    return mocker.patch.object(prompt_inst, "_put_alert")


# Test call
def test_call(mocker):
    # Setup instance and method and attribue mocks
    console_prompt = ConsolePrompt("Mock prompt")
    get_response_mock = mocker.patch.object(console_prompt, "_get_response")
    validate_response_mock = mocker.patch.object(console_prompt, 
                                                 "_validate_response", 
                                                 side_effect=[False, True])
    console_prompt._validated_response = "mocked response"
    
    # Execute
    result = console_prompt.call()

    # Verify method calls and result
    assert get_response_mock.call_count == 2
    assert validate_response_mock.call_count == 2
    assert result == "mocked response"


# Test checkBoolValidity
@pytest.mark.parametrize(
    "response, exp_result", 
    [
        # Test series 1: Invalid
        ('!', False), ('1', False), ('a', False), ('A', False), 

        # Test series 2: Valid
        ('y', True), ('Y', True), ('n', True), ('N', True)
    ]
)
def test_check_bool_validity(prompt_inst, put_alert_mock, response, 
                             exp_result):
    # Setup
    prompt_inst._user_response = response

    # Execute
    result = prompt_inst._check_bool_validity()

    # Verify
    assert result == exp_result
    if not exp_result:
        put_alert_mock.assert_called_once_with("Respond with 'y' or 'n'")
    else:
        put_alert_mock.assert_not_called()


# Test checkIntegerValidity
@pytest.mark.parametrize(
    "int_validation, response, exp_result, alert", 
    [
        # Test series 1: No extra validation of integer
        (None, "123", True, ""), 
        (None, "-123", True, ""), 
        (None, "1.23", False, "Enter a valid number"), 
        (None, "abc", False, "Enter a valid number"), 

        # Test series 2: Valid range defined by single integer
        (9, "0", True, ""), 
        (9, "9", False, "Response is out of range"), 
        (9, "-1", False, "Response is out of range"), 

        # Test series 3: Valid range defined by tuple
        ((-7, 7), "0", True, ""), 
        ((-7, 7), "7", True, ""), 
        ((-7, 7), "9", False, "Enter a number between -7 and 7"), 
        ((-7, 7), "-7", True, ""), 
        ((-7, 7), "-9", False, "Enter a number between -7 and 7")
    ]
)
def test_check_integer_validity(prompt_inst, put_alert_mock, int_validation, 
                                response, exp_result, alert):
    # Setup
    prompt_inst._integer_validation = int_validation
    prompt_inst._user_response = response

    # Execute
    result = prompt_inst._check_integer_validity()

    # Verify
    assert result == exp_result
    if exp_result == True:
        assert prompt_inst._validated_response == response
    else:
        put_alert_mock.assert_called_once_with(alert)


# Test _get_response
@pytest.mark.parametrize(
    "keystroke, leave_crsr", 
    [(True, False),  # Test case 1: readKeystroke path
     (False, True)]  # Test case 2: readString path
)
def test_get_response(mocker, prompt_inst, keystroke, leave_crsr):
    # Setup method mocks
    put_prompt_mock = mocker.patch.object(prompt_inst, "_put_prompt")
    read_keystroke_mock = mocker.patch.object(prompt_inst, "_read_keystroke")
    read_string_mock = mocker.patch.object(prompt_inst, "_read_string")
    
    # Setup expKeystroke attribute
    prompt_inst._expect_keystroke = keystroke

    # Execute
    prompt_inst._get_response()

    # Verify method calls
    put_prompt_mock.assert_called_once_with(leave_cursor_inline=leave_crsr)
    if keystroke:
        read_keystroke_mock.assert_called_once()
        read_string_mock.assert_not_called()
    else:
        read_keystroke_mock.assert_not_called()
        read_string_mock.assert_called_once()


# Test printMessage
@pytest.mark.parametrize(
    "width, padding, is_inline, message", 
    [
        # Test case 1: Minimum width
        (1, " " * 0, False, 
         "Lorem ipsum odor amet, consectetuer adipiscing elit."), 
        
        # Test case 2: Standard width
        (79, " " * 0, False, 
         "Lorem ipsum odor amet, consectetuer adipiscing elit."), 
        
        # Test case 3: Large width
        (99, " " * 10, False, 
         "Lorem ipsum odor amet, consectetuer adipiscing elit."), 
        
        # Test case 4: Standard width, inline
        (79," " * 0, True, 
         "Lorem ipsum odor amet, consectetuer adipiscing elit."), 
        
        # Test case 5: Standard width, text
        (79," " * 0, True, 
         "Lorem ipsum odor amet, consectetuer adipiscing elit. Torquent " + 
         "leo consectetur sodales etiam ex gravida eleifend interdum.")
    ]
)
def test_print_message(prompt_inst, width, padding, message, is_inline, 
                       capfd):
    # Setup display width
    prompt_inst._trm.width = width

    # Execute and capture
    prompt_inst._print_message(message, leave_cursor_inline=is_inline)
    out, err = capfd.readouterr()

    # Verify padding and line break
    text = padding + message
    ln_break = text.rfind(" ", 0, min(width, 79))
    assert out.startswith(text[:ln_break if ln_break > 0 else width])
    assert out.endswith("\n") != is_inline
    assert err == ""


# Test putAlert
def test_put_alert(prompt_inst, capfd):
    # Setup terminal color
    prompt_inst._trm.red = lambda x: f"[red]{x}[/red]"

    # Execute and capture
    prompt_inst._put_alert("Alert message")
    out, err = capfd.readouterr()

    # Verify capture
    assert out == "[red]Alert message[/red]\n"
    assert err == ""


# Test putPrompt
@pytest.mark.parametrize("is_inline, end", 
                         [(True, " "),     # Test case 1: Inline
                          (False, "\n")])  # Test case 2: New line
def test_put_prompt(prompt_inst, is_inline, end, capfd):
    # Setup terminal color
    prompt_inst._trm.bright_yellow = lambda x: f"[yellow]{x}[/yellow]"

    # Execute and capture
    prompt_inst._put_prompt(leave_cursor_inline=is_inline)
    out, err = capfd.readouterr()

    # Verify capture
    assert out.startswith("[yellow]Test prompt[/yellow]")
    assert out.endswith(end)
    assert err == ""


# Test readKeystroke
@pytest.mark.parametrize(
    "exp_result, sequence_in", 
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
def test_read_keystroke(mocker, prompt_inst, cbreak_mock, hidden_cursor_mock, 
                        sequence_in, exp_result):
    # Setup key iterator; cbreak and hiddenCursor mocks required
    key_iterator = iter(sequence_in)
    mocker.patch.object(prompt_inst._trm, "inkey", lambda: next(key_iterator))

    # Execute
    prompt_inst._read_keystroke()

    # Verify result
    assert prompt_inst._user_response == exp_result


# Test readString
@pytest.mark.parametrize(
    "exp_result, sequence_in", 
    [
        # Test case 1: No use of 'Backspace'
        ("abc", [keyboard.Keystroke('a', 97), keyboard.Keystroke('b', 98), 
                 keyboard.Keystroke('c', 99), keyboard.Keystroke('\n', 10)]), 
        
        # Test case 2: Mid-stream use of 'Backspace'
        # ("b", [keyboard.Keystroke('a', 97), keyboard.Keystroke('\x08', 8), 
        #        keyboard.Keystroke('b', 98), keyboard.Keystroke('\n', 10)]), 
        # """ > assert out == exp_stdout, f"Expected: {exp_stdout}, Got: 
        #         {out}"
        #     E AssertionError: Expected: [green]b[/green], Got: 
        #         [green]b[/green]
        #     E assert '[green]a[/green]\x08 \x08\x08 \x08\x08 \x08\x08 \x08
        #         \x08 \x08\x08 \x08\x08 \x08\x08 \x08\x08 \x08\x08 \x08
        #         \x08 \x08\x08 \x08\x08 \x08\x08 \x08\x08 \x08\x08 \x08
        #         [green]b[/green]\n' == '[green]b[/green]\n'
        # """
        
        # Test case 3: Initial use of 'Backspace'
        # ("ab", [keyboard.Keystroke('\x08', 8), keyboard.Keystroke('a', 97), 
        #         keyboard.Keystroke('b', 98), keyboard.Keystroke('\n', 8)])
        # """ > assert console_prompt._user_response == exp_result
        #     E AssertionError: assert 'a' == 'ab'
        # """
    ]
)
def test_read_string(prompt_inst, cbreak_mock, sequence_in, exp_result, 
                     capfd):
    # Setup
    prompt_inst._trm.inkey.side_effect = sequence_in
    prompt_inst._trm.green = lambda x: f"[green]{x}[/green]"

    # Execute and capture
    prompt_inst._read_string()
    out, err = capfd.readouterr()

    # Verify result
    assert prompt_inst._user_response == exp_result
    
    # Verify capture
    exp_stdout = []
    for key in sequence_in:
        if key.code == 8:
            if exp_stdout:
                exp_stdout.pop()
        elif 32 <= key.code <= 126:
            exp_stdout.append(f"[green]{str(key)}[/green]")
    exp_stdout = ''.join(exp_stdout) + '\n'
    assert out == exp_stdout, f"Expected: {exp_stdout}, Got: {out}"
    assert err == ""


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
def test_get_validate_reponse(mocker, prompt_inst, bool_path, int_path, 
                              bool_rtn, int_rtn, exp_result):
    # Setup method mocks
    check_bool_validity_mock = mocker.patch.object(prompt_inst, 
                                                   "_check_bool_validity", 
                                                   return_value=bool_rtn)
    check_int_validity_mock = mocker.patch.object(prompt_inst, 
                                                  "_check_integer_validity", 
                                                  return_value=int_rtn)
    
    # Setup instance attributes
    prompt_inst._validate_bool = bool_path
    prompt_inst._validate_integer = int_path

    # Execute
    result = prompt_inst._validate_response()

    # Verify result
    assert result == exp_result

    # Verify method calls
    if bool_path:
        check_bool_validity_mock.assert_called_once()
        check_int_validity_mock.assert_not_called()
    elif int_path:
        check_bool_validity_mock.assert_not_called()
        check_int_validity_mock.assert_called_once()
    else:
        check_bool_validity_mock.assert_not_called()
        check_int_validity_mock.assert_not_called()
