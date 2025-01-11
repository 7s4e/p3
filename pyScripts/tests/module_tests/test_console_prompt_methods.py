import pytest
from blessed import keyboard, Terminal
from modules import ConsoleAnyKeyPrompt, ConsoleBooleanPrompt
from modules import ConsoleFreeFormPrompt, ConsoleIntegerPrompt


PROMPT_CLASSES = [(ConsoleAnyKeyPrompt, ["Mock cue"]), 
                  (ConsoleBooleanPrompt, ["Mock cue"]), 
                  (ConsoleFreeFormPrompt, ["Mock cue"]), 
                  (ConsoleIntegerPrompt, ["Mock cue", None])]


@pytest.fixture
def mck_T(mocker):
    mck = mocker.Mock(spec=Terminal)
    mck.width = 79
    return mck

@pytest.fixture
def CP_insts(mck_T):
    insts = [clss(*args) for clss, args in PROMPT_CLASSES]
    for inst in insts: inst._trm = mck_T
    return insts

# @pytest.fixture
# def cb_mck(mocker, CP_insts):
#     mck = mocker.patch.object(CP_insts._trm, "cbreak", mocker.MagicMock())
#     mck.return_value.__enter__ = mocker.MagicMock()
#     mck.return_value.__exit__ = mocker.MagicMock()
#     return mck

# @pytest.fixture
# def hc_mck(mocker, CP_insts):
#     mck = mocker.patch.object(CP_insts._trm, "hidden_cursor", 
#                               mocker.MagicMock())
#     mck.return_value.__enter__ = mocker.MagicMock()
#     mck.return_value.__exit__ = mocker.MagicMock()
#     return mck

# @pytest.fixture
# def pa_mck(mocker, CP_insts):
#     return mocker.patch.object(CP_insts, "_put_alrt")


# Test call
def test_call(mocker):
    # Setup subclass instances
    CP_insts = [clss(*args) for clss, args in PROMPT_CLASSES]

    # Setup mock methods for each instance
    grms = [mocker.patch.object(inst, "_get_response") for inst in CP_insts]
    vrms = [mocker.patch.object(inst, "_validate_response", 
                                side_effect=[False, True]) 
            for inst in CP_insts]
    recms = [mocker.patch.object(inst, "_reset_error_count") 
             for inst in CP_insts]
    
    # Setup common state for all instances
    for inst in CP_insts: inst._validated_response = "mocked response"
    
    # Execute
    for inst, gr_mck, vr_mck, rec_mck in zip(CP_insts, grms, vrms, recms):
        act_out = inst.call()
    
    # Verify call counts and results
        assert gr_mck.call_count == 2
        assert vr_mck.call_count == 2
        assert rec_mck.call_count == 1
        assert act_out == "mocked response"


# Test getResponse
@pytest.mark.parametrize(
    "exp_kst, leave_cur", 
    [(True, False),  # Test case 1: readKeystroke path
     (False, True)]  # Test case 2: readString path
)
def test_get_response(mocker, CP_insts, exp_kst, leave_cur):
    # Setup mock methods for each instance
    ppms = [mocker.patch.object(inst, "_put_prompt") for inst in CP_insts]
    rkms = [mocker.patch.object(inst, "_read_keystroke") for inst in CP_insts]
    rsms = [mocker.patch.object(inst, "_read_string") for inst in CP_insts]
    
    # Setup common state for all instances
    for inst in CP_insts:
        mocker.patch.object(inst.__class__, "_expect_keystroke", 
                            new_callable=mocker.PropertyMock, 
                            return_value=exp_kst)

    # Execute
    for inst, pp_mck, rk_mck, rs_mck in zip(CP_insts, ppms, rkms, rsms):
        inst._get_response()

    # Verify method calls
        pp_mck.assert_called_once_with(kp_cur_inline=leave_cur)
        assert rk_mck.call_count == (1 if exp_kst else 0)
        assert rs_mck.call_count == (0 if exp_kst else 1)


# # Test checkBoolValidity
# @pytest.mark.parametrize(
#     "response, exp_out", 
#     [
#         # Test series 1: Invalid
#         ('!', False), ('1', False), ('a', False), ('A', False), 

#         # Test series 2: Valid
#         ('y', True), ('Y', True), ('n', True), ('N', True)
#     ]
# )
# def test_chk_bool_vld(CP_insts, pa_mck, response, exp_out):
#     # Setup
#     CP_insts._user_resp = response
#     pa_alert_arg = "Respond with 'y' or 'n'"

#     # Execute
#     act_out = CP_insts._chk_bool_vld()

#     # Verify
#     assert act_out == exp_out
#     if not exp_out:
#         pa_mck.assert_called_once_with(pa_alert_arg, CP_insts._e_ct["yes/no"])
#     else:
#         pa_mck.assert_not_called()


# # Test checkIntegerValidity
# @pytest.mark.parametrize(
#     "int_validation, response, exp_out, alert, error_cat", 
#     [
#         # Test series 1: No extra validation of integer
#         (None, "123", True, None, None), 
#         (None, "-123", True, None, None), 
#         (None, "1.23", False, "Enter a valid number", "NaN"), 
#         (None, "abc", False, "Enter a valid number", "NaN"), 

#         # Test series 2: Valid range defined by single integer
#         (9, "0", True, None, None), 
#         (9, "9", False, "Response is out of range", "OOR"), 
#         (9, "-1", False, "Response is out of range", "OOR"), 

#         # Test series 3: Valid range defined by tuple
#         ((-7, 7), "0", True, None, None), 
#         ((-7, 7), "7", True, None, None), 
#         ((-7, 7), "9", False, "Enter a number between -7 and 7", "OOL"), 
#         ((-7, 7), "-7", True, None, None), 
#         ((-7, 7), "-9", False, "Enter a number between -7 and 7", "OOL")
#     ]
# )
# def test_chk_int_vld(CP_insts, pa_mck, int_validation, response, exp_out, 
#                      alert, error_cat):
#     # Setup
#     CP_insts._int_vld = int_validation
#     CP_insts._user_resp = response

#     # Execute
#     act_out = CP_insts._chk_int_vld()

#     # Verify
#     assert act_out == exp_out
#     if exp_out == True:
#         assert CP_insts._vld_resp == response
#     else:
#         pa_mck.assert_called_once_with(alert, CP_insts._e_ct[error_cat])


# # Test printMessage
# @pytest.mark.parametrize(
#     "width, padding, is_inline, message", 
#     [
#         # Test case 1: Minimum width
#         (1, " " * 0, False, 
#          "Lorem ipsum odor amet, consectetuer adipiscing elit."), 
        
#         # Test case 2: Standard width
#         (79, " " * 0, False, 
#          "Lorem ipsum odor amet, consectetuer adipiscing elit."), 
        
#         # Test case 3: Large width
#         (99, " " * 10, False, 
#          "Lorem ipsum odor amet, consectetuer adipiscing elit."), 
        
#         # Test case 4: Standard width, inline
#         (79," " * 0, True, 
#          "Lorem ipsum odor amet, consectetuer adipiscing elit."), 
        
#         # Test case 5: Standard width, text
#         (79," " * 0, True, 
#          "Lorem ipsum odor amet, consectetuer adipiscing elit. Torquent " + 
#          "leo consectetur sodales etiam ex gravida eleifend interdum.")
#     ]
# )
# def test_pnt_msg(CP_insts, width, padding, message, is_inline, capfd):
#     # Setup display width
#     CP_insts._trm.width = width

#     # Execute and capture
#     CP_insts._pnt_msg(message, fmt_alloc=0, kp_cur_inline=is_inline)
#     out, err = capfd.readouterr()

#     # Verify padding and line break
#     text = padding + message
#     ln_break = text.rfind(" ", 0, min(width, 79))
#     assert out.startswith(text[:ln_break if ln_break > 0 else width])
#     assert out.endswith("\n") != is_inline
#     assert err == ""


# # Test putAlert
# def test_put_alrt(CP_insts, capfd):
#     # Setup terminal color
#     CP_insts._trm.red = lambda x: f"[red]{x}[/red]"

#     # Execute and capture
#     CP_insts._put_alrt("Alert message", 1)
#     out, err = capfd.readouterr()

#     # Verify capture
#     assert out == "[red]Alert message[/red]\n"
#     assert err == ""


# # Test putPrompt
# @pytest.mark.parametrize("is_inline, end", 
#                          [(True, " "),     # Test case 1: Inline
#                           (False, "\n")])  # Test case 2: New line
# def test_put_prompt(CP_insts, is_inline, end, capfd):
#     # Setup terminal color
#     CP_insts._trm.yellow = lambda x: f"[yellow]{x}[/yellow]"

#     # Execute and capture
#     CP_insts._put_prompt(kp_cur_inline=is_inline)
#     out, err = capfd.readouterr()

#     # Verify capture
#     assert out.startswith("[yellow]Test prompt[/yellow]")
#     assert out.endswith(end)
#     assert err == ""


# # Test readKeystroke
# @pytest.mark.parametrize(
#     "exp_out, sequence_in", 
#     [
#         ('', [keyboard.Keystroke('\n', 10)]),   # Test case 1
#         (' ', [keyboard.Keystroke(' ', 32)]),   # Test case 2
#         ('!', [keyboard.Keystroke('!', 33)]),   # Test case 3
#         ('1', [keyboard.Keystroke('1', 49)]),   # Test case 4
#         ('A', [keyboard.Keystroke('A', 65)]),   # Test case 5
#         ('a', [keyboard.Keystroke('a', 97)]),   # Test case 6
#         ('~', [keyboard.Keystroke('~', 126)]),  # Test case 7

#         # Test case 8: Non-printable keystrokes
#         ('a', [keyboard.Keystroke('\x08', 8), keyboard.Keystroke('\x09', 9), 
#             keyboard.Keystroke('\x1b', 27), keyboard.Keystroke('
#a', 97)])
#     ]
# ]
# def test_read_keystroke(mocker, CP_insts, cb_mck, hc_mck, sequence_in, exp_out):
#     # Setup key iterator; cbreak and hiddenCursor mocks required
#     key_iter = iter(sequence_in)
#     mocker.patch.object(CP_insts._trm, "inkey", lambda: next(key_iter))

#     # Execut
#e
#     CP_instsecute_read_keystroke()

#     # Verify output
#     assert CP_insts._user_resp == exp_out


# # Test readString
# @pytest.mark.parametrize(
#     "exp_out, sequence_in", 
#     [
#         # Test case 1: No use of 'Backspace'
#         ("abc", [keyboard.Keystroke('a', 97), keyboard.Keystroke('b', 98), 
#                  keyboard.Keystroke('c', 99), keyboard.Keystroke('\n', 10)]), 
        
#         # Test case 2: Mid-stream use of 'Backspace'
#         # ("b", [keyboard.Keystroke('a', 97), keyboard.Keystroke('\x08', 8), 
#         #        keyboard.Keystroke('b', 98), keyboard.Keystroke('\n', 10)]), 
#         # """ > assert out == exp_stdout, f"Expected: {exp_stdout}, Got: 
#         #         {out}"
#         #     E AssertionError: Expected: [green]b[/green], Got: 
#         #         [green]b[/green]
#         #     E assert '[green]a[/green]\x08 \x08\x08 \x08\x08 \x08\x08 \x08
#         #         \x08 \x08\x08 \x08\x08 \x08\x08 \x08\x08 \x08\x08 \x08
#         #         \x08 \x08\x08 \x08\x08 \x08\x08 \x08\x08 \x08\x08 \x08
#         #         [green]b[/green]\n' == '[green]b[/green]\n'
#         # """
        
#         # Test case 3: Initial use of 'Backspace'
#         # ("ab", [keyboard.Keystroke('\x08', 8), keyboard.Keystroke('a', 97), 
#         #         keyboard.Keystroke('b', 98), keyboard.Keystroke('\n', 8)])
#         # """ > assert console_prompt._user_response == exp_out
#         #     E AssertionError: assert 'a' == 'ab'
#         # """
#     ]
# )
# def test_read_str(CP_insts, cb_mck, sequence_in, exp_out, capfd):
#     # Setup
#     CP_insts._trm.inkey.side_effect = sequence_in
#     CP_insts._trm.green = lambda x: f"[green]{x}[/green]"

#     # Execute and capture
#     CP_insts._read_str()
#     out, err = capfd.readouterr()

#     # Verify result
#     assert CP_insts._user_resp == exp_out
    
#     # Verify capture
#     exp_stdout = []
#     for key in sequence_in:
#         if key.code == 8:
#             if exp_stdout:
#                 exp_stdout.pop()
#         elif 32 <= key.code <= 126:
#             exp_stdout.append(f"[green]{str(key)}[/green]")
#     exp_stdout = ''.join(exp_stdout) + '\n'
#     assert out == exp_stdout, f"Expected: {exp_stdout}, Got: {out}"
#     assert err == ""


# # Test validateResponse
# @pytest.mark.parametrize(
#     "bool_path, int_path, bool_rtn, int_rtn, exp_out", 
#     [
#         # Test case 1: True on checkBoolValidity path
#         (True, False, True, None, True), 

#         # Test case 2: False on checkBoolValidity path
#         (True, False, False, None, False), 

#         # Test case 3: True on checkIntegerValidity path
#         (False, True, None, True, True), 

#         # Test case 4: False on checkIntegerValidity path
#         (False, True, None, False, False), 

#         # Test case 5: No validation required
#         (False, False, None, None, True)]
# )
# def test_validate_response(mocker, CP_insts, bool_path, int_path, bool_rtn, int_rtn, 
#                   exp_out):
#     # Setup method mocks
#     cbv_mck = mocker.patch.object(CP_insts, "_chk_bool_vld", 
#                                   return_value=bool_rtn)
#     civ_mck = mocker.patch.object(CP_insts, "_chk_int_vld", 
#                                   return_value=int_rtn)
    
#     # Setup instance attributes
#     CP_insts._val_bool = bool_path
#     CP_insts._val_int = int_path
#     CP_insts._user_resp = "mock response"

#     # Execute
#     act_out = CP_insts._validate_response()

#     # Verify result
#     assert act_out == exp_out

#     # Verify method calls
#     if bool_path:
#         cbv_mck.assert_called_once()
#         civ_mck.assert_not_called()
#     elif int_path:
#         cbv_mck.assert_not_called()
#         civ_mck.assert_called_once()
#     else:
#         cbv_mck.assert_not_called()
#         civ_mck.assert_not_called()
#         assert CP_insts._vld_resp == CP_insts._user_resp
