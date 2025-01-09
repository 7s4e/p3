import pytest
import sys
from blessed import Terminal
from modules.console import ConsolePrompt
from modules import ConsoleAnyKeyPrompt, ConsoleBooleanPrompt
from modules import ConsoleFreeFormPrompt, ConsoleIntegerPrompt


@pytest.mark.parametrize(
    "cue, constraint, exception",
    [
        # Test series 1: TypeError if 'cue' not `string`
        (None, None, TypeError), 
        (bool(), None, TypeError), 
        (bytearray(), None, TypeError), 
        (bytes(), None, TypeError), 
        (classmethod(lambda: None), None, TypeError), 
        (complex(), None, TypeError), 
        (dict(), None, TypeError), 
        (enumerate(str()), None, TypeError), 
        (filter(lambda: None, str()), None, TypeError), 
        (float(), None, TypeError), 
        (frozenset(), None, TypeError), 
        (int(), None, TypeError), 
        (list(), None, TypeError), 
        (map(lambda: None, str()), None, TypeError), 
        (memoryview(bytes()), None, TypeError), 
        (object(), None, TypeError), 
        (property(), None, TypeError), 
        (range(int()), None, TypeError), 
        (reversed(str()), None, TypeError), 
        (set(), None, TypeError), 
        (slice(int()), None, TypeError), 
        (staticmethod(lambda: None), None, TypeError), 
        (str(), None, None), 
        (tuple(), None, TypeError), 
        (type(object()), None, TypeError), 
        (zip(), None, TypeError), 

        # Test series 2: TypeError if 'constraint' not `None`, `int`, 
        #   or `tuple`
        ("", None, None), 
        ("", bool(), TypeError), 
        # ("", bytearray(), TypeError), 
        # ("", bytes(), TypeError), 
        # ("", classmethod(lambda: None), TypeError), 
        # ("", complex(), TypeError), 
        # ("", dict(), TypeError), 
        # ("", enumerate(str()), TypeError), 
        # ("", filter(lambda: None, str()), TypeError), 
        # ("", float(), TypeError), 
        # ("", frozenset(), TypeError), 
        # ("", int(), None), 
        # ("", list(), TypeError), 
        # ("", map(lambda: None, str()), TypeError), 
        # ("", memoryview(bytes()), TypeError), 
        # ("", object(), TypeError), 
        # ("", property(), TypeError), 
        # ("", range(int()), TypeError), 
        # ("", reversed(str()), TypeError), 
        # ("", set(), TypeError), 
        # ("", slice(int()), TypeError), 
        # ("", staticmethod(lambda: None), TypeError), 
        # ("", str(), TypeError), 
        # ("", tuple([int(), int()]), None), 
        # ("", type(object()), TypeError), 
        # ("", zip(), TypeError), 
        
        # # Test series 3: ValueError if 'constraint' is an integer that 
        # #   is negative
        # ("", 0, None), 
        # ("", 1, None), 
        # ("", sys.maxsize, None), 
        # ("", -1, ValueError), 
        # ("", -sys.maxsize, ValueError), 

        # # Test series 4: ValueError if 'constraint' is a tuple without 
        # #   two elements
        # ("", (1,), ValueError), 
        # ("", (1, 2), None), 
        # ("", (1, 2, 3), ValueError), 

        # # Test series 5: ValueError is second tuple value less than the 
        # #   first
        # ("", (0, 0), None), 
        # ("", (1, 2), None), 
        # ("", (-2, -1), None), 
        # ("", (1, 0), ValueError)
    ]
)
def test_console_prompt_constructors(cue, constraint, exception):
    # Setup
    prompt_classes = [(ConsoleAnyKeyPrompt, []), 
                      (ConsoleBooleanPrompt, []), 
                      (ConsoleFreeFormPrompt, []), 
                      (ConsoleIntegerPrompt, [constraint])]
    
    # Execute
    if exception:
        for prompt_class, args in prompt_classes:
            if args:
                with pytest.raises(exception):
                    prompt_class(cue, *args)
            # else:
            #     with pytest.raises(exception):
            #         prompt_class(cue)
    else:
        instances = [cls(cue, *args) for cls, args in prompt_classes]

        # Verify
        for instance in instances:
            assert isinstance(instance._trm, Terminal)
            assert instance._cue == cue
