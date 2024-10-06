import pytest
import sys
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


@pytest.mark.parametrize(
    "prmt,                     exp_key,                 val_bool,                val_int,                 int_val,                 excep",
    # Check type errors
    # if not isinstance(prompt, str): raise TypeError("Expected `str` for 'prompt'.")
    # prmt                     exp_key                  val_bool                 val_int                  int_val                  excep"
    [(None,                    False,                   False,                   False,                   None,                    TypeError), 
     (bool(),                  False,                   False,                   False,                   None,                    TypeError), 
     (bytearray(),             False,                   False,                   False,                   None,                    TypeError), 
     (bytes(),                 False,                   False,                   False,                   None,                    TypeError), 
     (classmethod(mock_console),   False,                   False,                   False,                   None,                    TypeError), 
     (complex(),               False,                   False,                   False,                   None,                    TypeError), 
     (dict(),                  False,                   False,                   False,                   None,                    TypeError), 
     (enumerate(str()),        False,                   False,                   False,                   None,                    TypeError), 
     (filter(mock_console, str()), False,                   False,                   False,                   None,                    TypeError), 
     (float(),                 False,                   False,                   False,                   None,                    TypeError), 
     (frozenset(),             False,                   False,                   False,                   None,                    TypeError), 
     (int(),                   False,                   False,                   False,                   None,                    TypeError), 
     (list(),                  False,                   False,                   False,                   None,                    TypeError), 
     (map(mock_console, str()),    False,                   False,                   False,                   None,                    TypeError), 
     (memoryview(bytes()),     False,                   False,                   False,                   None,                    TypeError), 
     (object(),                False,                   False,                   False,                   None,                    TypeError), 
     (property(),              False,                   False,                   False,                   None,                    TypeError), 
     (range(int()),            False,                   False,                   False,                   None,                    TypeError), 
     (reversed(str()),         False,                   False,                   False,                   None,                    TypeError), 
     (set(),                   False,                   False,                   False,                   None,                    TypeError), 
     (slice(int()),            False,                   False,                   False,                   None,                    TypeError), 
     (staticmethod(mock_console),  False,                   False,                   False,                   None,                    TypeError), 
     (str(),                   False,                   False,                   False,                   None,                    None), 
     (tuple(),                 False,                   False,                   False,                   None,                    TypeError), 
     (type(object()),          False,                   False,                   False,                   None,                    TypeError), 
     (zip(),                   False,                   False,                   False,                   None,                    TypeError), 

    # if not isinstance(expect_keystroke, bool): raise TypeError("Expected `bool` for 'expect_keystroke'.")
    # prmt                     exp_key                  val_bool                 val_int                  int_val                  excep"
     ("",                      None,                    False,                   False,                   None,                    TypeError), 
     ("",                      bool(),                  False,                   False,                   None,                    None), 
     ("",                      bytearray(),             False,                   False,                   None,                    TypeError), 
     ("",                      bytes(),                 False,                   False,                   None,                    TypeError), 
     ("",                      classmethod(mock_console),   False,                   False,                   None,                    TypeError), 
     ("",                      complex(),               False,                   False,                   None,                    TypeError), 
     ("",                      dict(),                  False,                   False,                   None,                    TypeError), 
     ("",                      enumerate(str()),        False,                   False,                   None,                    TypeError), 
     ("",                      filter(mock_console, str()), False,                   False,                   None,                    TypeError), 
     ("",                      float(),                 False,                   False,                   None,                    TypeError), 
     ("",                      frozenset(),             False,                   False,                   None,                    TypeError), 
     ("",                      int(),                   False,                   False,                   None,                    TypeError), 
     ("",                      list(),                  False,                   False,                   None,                    TypeError), 
     ("",                      map(mock_console, str()),    False,                   False,                   None,                    TypeError), 
     ("",                      memoryview(bytes()),     False,                   False,                   None,                    TypeError), 
     ("",                      object(),                False,                   False,                   None,                    TypeError), 
     ("",                      property(),              False,                   False,                   None,                    TypeError), 
     ("",                      range(int()),            False,                   False,                   None,                    TypeError), 
     ("",                      reversed(str()),         False,                   False,                   None,                    TypeError), 
     ("",                      set(),                   False,                   False,                   None,                    TypeError), 
     ("",                      slice(int()),            False,                   False,                   None,                    TypeError), 
     ("",                      staticmethod(mock_console),  False,                   False,                   None,                    TypeError), 
     ("",                      str(),                   False,                   False,                   None,                    TypeError), 
     ("",                      tuple(),                 False,                   False,                   None,                    TypeError), 
     ("",                      type(object()),          False,                   False,                   None,                    TypeError), 
     ("",                      zip(),                   False,                   False,                   None,                    TypeError), 

    # if not isinstance(validate_bool, bool): raise TypeError("Expected `bool` for 'validate_bool'.")
    # prmt                     exp_key                  val_bool                 val_int                  int_val                  excep"
     ("",                      False,                   None,                    False,                   None,                    TypeError), 
     ("",                      False,                   bool(),                  False,                   None,                    None), 
     ("",                      False,                   bytearray(),             False,                   None,                    TypeError), 
     ("",                      False,                   bytes(),                 False,                   None,                    TypeError), 
     ("",                      False,                   classmethod(mock_console),   False,                   None,                    TypeError), 
     ("",                      False,                   complex(),               False,                   None,                    TypeError), 
     ("",                      False,                   dict(),                  False,                   None,                    TypeError), 
     ("",                      False,                   enumerate(str()),        False,                   None,                    TypeError), 
     ("",                      False,                   filter(mock_console, str()), False,                   None,                    TypeError), 
     ("",                      False,                   float(),                 False,                   None,                    TypeError), 
     ("",                      False,                   frozenset(),             False,                   None,                    TypeError), 
     ("",                      False,                   int(),                   False,                   None,                    TypeError), 
     ("",                      False,                   list(),                  False,                   None,                    TypeError), 
     ("",                      False,                   map(mock_console, str()),    False,                   None,                    TypeError), 
     ("",                      False,                   memoryview(bytes()),     False,                   None,                    TypeError), 
     ("",                      False,                   object(),                False,                   None,                    TypeError), 
     ("",                      False,                   property(),              False,                   None,                    TypeError), 
     ("",                      False,                   range(int()),            False,                   None,                    TypeError), 
     ("",                      False,                   reversed(str()),         False,                   None,                    TypeError), 
     ("",                      False,                   set(),                   False,                   None,                    TypeError), 
     ("",                      False,                   slice(int()),            False,                   None,                    TypeError), 
     ("",                      False,                   staticmethod(mock_console),  False,                   None,                    TypeError), 
     ("",                      False,                   str(),                   False,                   None,                    TypeError), 
     ("",                      False,                   tuple(),                 False,                   None,                    TypeError), 
     ("",                      False,                   type(object()),          False,                   None,                    TypeError), 
     ("",                      False,                   zip(),                   False,                   None,                    TypeError),

    # if not isinstance(validate_integer, bool): raise TypeError("Expected `bool` for 'validate_integer'.")
    # prmt                     exp_key                  val_bool                 val_int                  int_val                  excep"
     ("",                      False,                   False,                   None,                    None,                    TypeError), 
     ("",                      False,                   False,                   bool(),                  None,                    None), 
     ("",                      False,                   False,                   bytearray(),             None,                    TypeError), 
     ("",                      False,                   False,                   bytes(),                 None,                    TypeError), 
     ("",                      False,                   False,                   classmethod(mock_console),   None,                    TypeError), 
     ("",                      False,                   False,                   complex(),               None,                    TypeError), 
     ("",                      False,                   False,                   dict(),                  None,                    TypeError), 
     ("",                      False,                   False,                   enumerate(str()),        None,                    TypeError), 
     ("",                      False,                   False,                   filter(mock_console, str()), None,                    TypeError), 
     ("",                      False,                   False,                   float(),                 None,                    TypeError), 
     ("",                      False,                   False,                   frozenset(),             None,                    TypeError), 
     ("",                      False,                   False,                   int(),                   None,                    TypeError), 
     ("",                      False,                   False,                   list(),                  None,                    TypeError), 
     ("",                      False,                   False,                   map(mock_console, str()),    None,                    TypeError), 
     ("",                      False,                   False,                   memoryview(bytes()),     None,                    TypeError), 
     ("",                      False,                   False,                   object(),                None,                    TypeError), 
     ("",                      False,                   False,                   property(),              None,                    TypeError), 
     ("",                      False,                   False,                   range(int()),            None,                    TypeError), 
     ("",                      False,                   False,                   reversed(str()),         None,                    TypeError), 
     ("",                      False,                   False,                   set(),                   None,                    TypeError), 
     ("",                      False,                   False,                   slice(int()),            None,                    TypeError), 
     ("",                      False,                   False,                   staticmethod(mock_console),  None,                    TypeError), 
     ("",                      False,                   False,                   str(),                   None,                    TypeError), 
     ("",                      False,                   False,                   tuple(),                 None,                    TypeError), 
     ("",                      False,                   False,                   type(object()),          None,                    TypeError), 
     ("",                      False,                   False,                   zip(),                   None,                    TypeError),

    # if (integer_validation is not None and not (isinstance(integer_validation, int) and not isinstance(integer_validation, bool) or isinstance(integer_validation, tuple))):
    #   raise TypeError("Expected `int`, `tuple[int, int]`, or `None` for 'integer_validation'.")
    # prmt                     exp_key                  val_bool                 val_int                  int_val                  excep"
     ("",                      False,                   False,                   True,                    None,                    None), 
     ("",                      False,                   False,                   True,                    bool(),                  TypeError), 
     ("",                      False,                   False,                   True,                    bytearray(),             TypeError), 
     ("",                      False,                   False,                   True,                    bytes(),                 TypeError), 
     ("",                      False,                   False,                   True,                    classmethod(mock_console),   TypeError), 
     ("",                      False,                   False,                   True,                    complex(),               TypeError), 
     ("",                      False,                   False,                   True,                    dict(),                  TypeError), 
     ("",                      False,                   False,                   True,                    enumerate(str()),        TypeError), 
     ("",                      False,                   False,                   True,                    filter(mock_console, str()), TypeError), 
     ("",                      False,                   False,                   True,                    float(),                 TypeError), 
     ("",                      False,                   False,                   True,                    frozenset(),             TypeError), 
     ("",                      False,                   False,                   True,                    int(),                   None), 
     ("",                      False,                   False,                   True,                    list(),                  TypeError), 
     ("",                      False,                   False,                   True,                    map(mock_console, str()),    TypeError), 
     ("",                      False,                   False,                   True,                    memoryview(bytes()),     TypeError), 
     ("",                      False,                   False,                   True,                    object(),                TypeError), 
     ("",                      False,                   False,                   True,                    property(),              TypeError), 
     ("",                      False,                   False,                   True,                    range(int()),            TypeError), 
     ("",                      False,                   False,                   True,                    reversed(str()),         TypeError), 
     ("",                      False,                   False,                   True,                    set(),                   TypeError), 
     ("",                      False,                   False,                   True,                    slice(int()),            TypeError), 
     ("",                      False,                   False,                   True,                    staticmethod(mock_console),  TypeError), 
     ("",                      False,                   False,                   True,                    str(),                   TypeError), 
     ("",                      False,                   False,                   True,                    tuple([int(), int()]),   None), 
     ("",                      False,                   False,                   True,                    type(object()),          TypeError), 
     ("",                      False,                   False,                   True,                    zip(),                   TypeError),

    # Check value errors
    # if validate_bool and validate_integer: raise ValueError("Both 'validate_bool' and 'validate_integer' cannot be `True`.")
    # prmt                     exp_key                  val_bool                 val_int                  int_val                  excep"
     ("",                      False,                   True,                    False,                   None,                    None), 
     ("",                      False,                   False,                   True,                    None,                    None), 
     ("",                      False,                   True,                    True,                    None,                    ValueError),

    # if integer_validation is not None:
    #   if not validate_integer: raise ValueError("With 'integer_validation', 'validate_integer' must be `True`.")
     ("",                      False,                   False,                   True,                    int(),                   None),
     ("",                      False,                   False,                   False,                   int(),                   ValueError),

    #   if isinstance(integer_validation, int):
    #       if integer_validation < 0: raise ValueError("Range for 'integer_validation' must be positive.")
     ("",                      False,                   False,                   True,                    0,                       None),
     ("",                      False,                   False,                   True,                    1,                       None),
     ("",                      False,                   False,                   True,                    sys.maxsize,             None),
     ("",                      False,                   False,                   True,                    -1,                      ValueError),
     ("",                      False,                   False,                   True,                    -sys.maxsize,            ValueError),

    #   else:
    #       if len(integer_validation) != 2: raise ValueError("The 'integer_validation' `tuple` must have two elements.")
     ("",                      False,                   False,                   True,                    (1,),                    ValueError),
     ("",                      False,                   False,                   True,                    (1, 2),                  None),
     ("",                      False,                   False,                   True,                    (1, 2, 3),               ValueError),

    #       if integer_validation[0] > integer_validation[1]: 
    #           raise ValueError("The second value of the 'integer_validation' `tuple` cannot be less than the first.")
     ("",                      False,                   False,                   True,                    (0, 0),                  None),
     ("",                      False,                   False,                   True,                    (1, 2),                  None),
     ("",                      False,                   False,                   True,                    (-2, -1),                None),
     ("",                      False,                   False,                   True,                    (1, 0),                  ValueError)]
    )

def test_constructor(mock_console, prmt, exp_key, val_bool, val_int, int_val, excep):
    """Test the constructor of ConsolePrompt for with various parameters."""
    if excep:
        with pytest.raises(excep):
            ConsolePrompt(prmt, 
                          expect_keystroke=exp_key, 
                          validate_bool=val_bool, 
                          validate_integer=val_int, 
                          integer_validation=int_val)
    else:
        prompt = ConsolePrompt(prmt, 
                               expect_keystroke=exp_key, 
                               validate_bool=val_bool, 
                               validate_integer=val_int, 
                               integer_validation=int_val)
        assert prompt._prompt == prmt
        assert prompt._expect_keystroke == exp_key
        assert prompt._validate_bool == val_bool
        assert prompt._validate_integer == val_int
        assert prompt._integer_validation == int_val



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
