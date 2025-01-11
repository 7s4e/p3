import pytest
import sys
from blessed import Terminal
from modules import ConsoleAnyKeyPrompt, ConsoleBooleanPrompt
from modules import ConsoleFreeFormPrompt, ConsoleIntegerPrompt


# Test ConsolePrompt
@pytest.mark.parametrize(
    "cue, exception",
    [
        # Test series: TypeError if 'cue' not `string`
        (bool(), TypeError), 
        (bytearray(), TypeError), 
        (bytes(), TypeError), 
        (classmethod(lambda: None), TypeError), 
        (complex(), TypeError), 
        (dict(), TypeError), 
        (enumerate(str()), TypeError), 
        (filter(lambda: None, str()), TypeError), 
        (float(), TypeError), 
        (frozenset(), TypeError), 
        (int(), TypeError), 
        (list(), TypeError), 
        (map(lambda: None, str()), TypeError), 
        (memoryview(bytes()), TypeError), 
        (object(), TypeError), 
        (property(), TypeError), 
        (range(int()), TypeError), 
        (reversed(str()), TypeError), 
        (set(), TypeError), 
        (slice(int()), TypeError), 
        (staticmethod(lambda: None), TypeError), 
        (str(), None), 
        (tuple(), TypeError), 
        (type(object()), TypeError), 
        (zip(), TypeError), 
    ]
)
def test_console_prompt_constructors(cue, exception):
    # Setup
    prompt_classes = [(ConsoleAnyKeyPrompt, []), 
                      (ConsoleBooleanPrompt, []), 
                      (ConsoleFreeFormPrompt, []), 
                      (ConsoleIntegerPrompt, [None])]
    CIP_reset_val = {"NaN": 0, "OOR": 0, "OOL": 0}
    other_reset_val = 0
    exp_user_resp = ""
    exp_vldtd_resp = None
    
    # Execute
    if exception:
        for prompt_class, args in prompt_classes:
            if args:
                with pytest.raises(exception):
                    prompt_class(cue, *args)
    else:
        CP_instances = [clss(cue, *args) for clss, args in prompt_classes]

    # Verify
        for inst in CP_instances:
            assert isinstance(inst._trm, Terminal)
            assert inst._cue == cue
            exp_reset_val = exp_error_ct = (CIP_reset_val 
                                            if isinstance(inst, 
                                                          ConsoleIntegerPrompt)
                                            else other_reset_val)
            assert inst._reset_value == exp_reset_val
            assert inst._error_count == exp_error_ct
            assert inst._user_response == exp_user_resp
            assert inst._validated_response == exp_vldtd_resp


# Test ConsoleAnyKeyPrompt
@pytest.mark.parametrize("cue_is_custom", [True, False])
def test_console_any_key_prompt_constructor(cue_is_custom):
    # Setup
    custom_cue = "test cue"
    default_cue = "Press any key to continue..."
    exp_exp_kst = True

    # Execute
    CAKP_inst = (ConsoleAnyKeyPrompt(custom_cue) if cue_is_custom 
                 else ConsoleAnyKeyPrompt())
    
    # Verify
    exp_cue = custom_cue if cue_is_custom else default_cue
    assert CAKP_inst._cue == exp_cue
    assert CAKP_inst._expect_keystroke == exp_exp_kst


# Test ConsoleBooleanPrompt
@pytest.mark.parametrize("cue_is_custom", [True, False])
def test_console_boolean_prompt_constructor(cue_is_custom):
    # Setup
    custom_cue = "test cue"
    default_cue = "(y/n)?"
    exp_exp_kst = True

    # Execute
    CBP_inst = (ConsoleBooleanPrompt(custom_cue) if cue_is_custom 
                else ConsoleBooleanPrompt())
    
    # Verify
    exp_cue = custom_cue if cue_is_custom else default_cue
    assert CBP_inst._cue == exp_cue
    assert CBP_inst._expect_keystroke == exp_exp_kst


# Test ConsoleFreeFormPrompt
@pytest.mark.parametrize("cue_is_custom", [True, False])
def test_console_free_form_prompt_constructor(cue_is_custom):
    # Setup
    custom_cue = "test cue"
    default_cue = "> "
    exp_exp_kst = False

    # Execute
    CFFP_inst = (ConsoleFreeFormPrompt(custom_cue) if cue_is_custom 
                else ConsoleFreeFormPrompt())
    
    # Verify
    exp_cue = custom_cue if cue_is_custom else default_cue
    assert CFFP_inst._cue == exp_cue
    assert CFFP_inst._expect_keystroke == exp_exp_kst


# Test ConsoleIntegerPrompt
@pytest.mark.parametrize(
    "cue_is_custom, constraint, exception, exp_exp_kst",
    [
        # Test series 1: Test cue assignment
        (True, None, None, False), 
        (False, None, None, False), 

        # Test series 2: TypeError if 'constraint' not `None`, `int`, 
        #   or `tuple`
        (False, bool(), TypeError, False), 
        (False, bytearray(), TypeError, False), 
        (False, bytes(), TypeError, False), 
        (False, classmethod(lambda: None), TypeError, False), 
        (False, complex(), TypeError, False), 
        (False, dict(), TypeError, False), 
        (False, enumerate(str()), TypeError, False), 
        (False, filter(lambda: None, str()), TypeError, False), 
        (False, float(), TypeError, False), 
        (False, frozenset(), TypeError, False), 
        (False, int(), None, True), 
        (False, list(), TypeError, False), 
        (False, map(lambda: None, str()), TypeError, False), 
        (False, memoryview(bytes()), TypeError, False), 
        (False, object(), TypeError, False), 
        (False, property(), TypeError, False), 
        (False, range(int()), TypeError, False), 
        (False, reversed(str()), TypeError, False), 
        (False, set(), TypeError, False), 
        (False, slice(int()), TypeError, False), 
        (False, staticmethod(lambda: None), TypeError, False), 
        (False, str(), TypeError, False), 
        (False, tuple([int(), int()]), None, True), 
        (False, type(object()), TypeError, False), 
        (False, zip(), TypeError, False), 
        
        # Test series 3: ValueError if 'constraint' is an integer that 
        #   is negative
        (False, 0, None, True), 
        (False, 1, None, True), 
        (False, sys.maxsize, None, False), 
        (False, -1, ValueError, False), 
        (False, -sys.maxsize, ValueError, False), 

        # Test series 4: ValueError if 'constraint' is a tuple without 
        #   two elements
        (False, (1,), ValueError, False), 
        (False, (1, 2), None, True), 
        (False, (1, 2, 3), ValueError, False), 

        # Test series 5: ValueError is second tuple value less than the 
        #   first
        (False, (0, 0), None, True), 
        (False, (1, 2), None, True), 
        (False, (-2, -1), None, False), 
        (False, (1, 0), ValueError, False), 

        # Test series 6: Boundary conditions for `_expect_keystroke`
        (False, 10, None, True), 
        (False, 11, None, False), 
        (False, (-1, 9), None, False), 
        (False, (0, 9), None, True), 
        (False, (0, 10), None, False) 
    ]
)
def test_console_integer_prompt_constructor(cue_is_custom, constraint, 
                                            exception, exp_exp_kst):
    # Setup
    custom_cue = "test cue"
    default_cue = "> "

    # Execute
    if exception:
        with pytest.raises(exception):
            ConsoleIntegerPrompt(constraint=constraint)
    else:
        CIP_inst = (ConsoleIntegerPrompt(custom_cue, constraint) 
                    if cue_is_custom 
                    else ConsoleIntegerPrompt(constraint=constraint))

    # Verify
        exp_cue = custom_cue if cue_is_custom else default_cue
        assert CIP_inst._cue == exp_cue
        assert CIP_inst._expect_keystroke == exp_exp_kst
