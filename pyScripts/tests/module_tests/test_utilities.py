import pytest
from modules import utilities as utl


# Test abort
@pytest.mark.parametrize("signal", [True, False])
def test_abort(mocker, signal):
    # Setup
    mck_script = "mock_script.py"
    exit_code = 10
    mck_print = mocker.patch("builtins.print")
    mck_exit = mocker.patch("sys.exit")

    # Execute
    utl.abort(signal, mck_script)

    # Verify
    if signal:
        mck_print.assert_called_once_with(f"Aborted {mck_script}")
        mck_exit.assert_called_once_with(exit_code)
    else:
        mck_print.assert_not_called()
        mck_exit.assert_not_called()


# Test getCallerInfo
@pytest.mark.parametrize(
    "call_level, expected_function",
    [
        # Test case 1: Non-recursive call
        (0, "test_get_caller_info"), 

        # Test case 2: 1 level of recursion
        (1, "helper"), 

        # Test case 3: 2 levels of recursion
        (2, "helper")
    ]
)
def test_get_caller_info(call_level, expected_function):
    # Setup import as inspect relies on actual stack frame at runtime
    from inspect import currentframe
    current_frame = currentframe()
    call_line = current_frame.f_lineno + 9  # Line count?

    # Recursive helper function
    def helper(level):
        if level > 1:
            return helper(level - 1)
        return utl.get_caller_info()

    # Execute the function
    result = helper(call_level) if call_level > 0 else utl.get_caller_info()

    # Verify the calling function details
    assert result["function"] == expected_function
    assert result["file"].endswith("test_utilities.py")
    assert result["line"].isdigit() and int(result["line"]) > 0

    # Additional verification for non-recursive calls
    if call_level == 0:
        assert current_frame is not None
        assert result["line"] == str(call_line)


# Test snakeToCamel
@pytest.mark.parametrize("str_in, exp_out", [("get_disk", "getDisk")])
def test_snake_to_camel(str_in, exp_out):
    # Execute
    result = utl.snake_to_camel(str_in)

    # Veriry
    assert result == exp_out


# Test truncateString
@pytest.mark.parametrize(
    "max, exp_out", 
    [
        (79, "Lorem ipsum odor amet, consectetuer adipiscing elit."), 
        (52, "Lorem ipsum odor amet, consectetuer adipiscing elit."), 
        (51, "Lorem ipsum odor amet, consectetuer adipiscing e..."), 
        (3, "..."), 
        (1, "."), 
        (0, ""), 
    ]
)
def test_truncate_string(max, exp_out):
    # Setup
    string = "Lorem ipsum odor amet, consectetuer adipiscing elit."

    # Execute
    result = utl.truncate_string(string, max)

    # Verify
    assert result == exp_out
