# import pytest
# import sys
# from blessed import Terminal
# from modules import ConsolePrompt


# @pytest.mark.parametrize(
#     "prompt, exp_key, validate_bool, validate_int, int_validation, exception",
#     [
#         # Test series 1: TypeError if 'prompt' not `string`
#         (None, False, False, False, None, TypeError), 
#         (bool(), False, False, False, None, TypeError), 
#         (bytearray(), False, False, False, None, TypeError), 
#         (bytes(), False, False, False, None, TypeError), 
#         (classmethod(lambda: None), False, False, False, None, TypeError), 
#         (complex(), False, False, False, None, TypeError), 
#         (dict(), False, False, False, None, TypeError), 
#         (enumerate(str()), False, False, False, None, TypeError), 
#         (filter(lambda: None, str()), False, False, False, None, TypeError), 
#         (float(), False, False, False, None, TypeError), 
#         (frozenset(), False, False, False, None, TypeError), 
#         (int(), False, False, False, None, TypeError), 
#         (list(), False, False, False, None, TypeError), 
#         (map(lambda: None, str()), False, False, False, None, TypeError), 
#         (memoryview(bytes()), False, False, False, None, TypeError), 
#         (object(), False, False, False, None, TypeError), 
#         (property(), False, False, False, None, TypeError), 
#         (range(int()), False, False, False, None, TypeError), 
#         (reversed(str()), False, False, False, None, TypeError), 
#         (set(), False, False, False, None, TypeError), 
#         (slice(int()), False, False, False, None, TypeError), 
#         (staticmethod(lambda: None), False, False, False, None, TypeError), 
#         (str(), False, False, False, None, None), 
#         (tuple(), False, False, False, None, TypeError), 
#         (type(object()), False, False, False, None, TypeError), 
#         (zip(), False, False, False, None, TypeError), 

#         # Test series 2: TypeError if 'expect_keystroke' not `bool`
#         ("", None, False, False, None, TypeError), 
#         ("", bool(), False, False, None, None), 
#         ("", bytearray(), False, False, None, TypeError), 
#         ("", bytes(), False, False, None, TypeError), 
#         ("", classmethod(lambda: None), False, False, None, TypeError), 
#         ("", complex(), False, False, None, TypeError), 
#         ("", dict(), False, False, None, TypeError), 
#         ("", enumerate(str()), False, False, None, TypeError), 
#         ("", filter(lambda: None, str()), False, False, None, TypeError), 
#         ("", float(), False, False, None, TypeError), 
#         ("", frozenset(), False, False, None, TypeError), 
#         ("", int(), False, False, None, TypeError), 
#         ("", list(), False, False, None, TypeError), 
#         ("", map(lambda: None, str()), False, False, None, TypeError), 
#         ("", memoryview(bytes()), False, False, None, TypeError), 
#         ("", object(), False, False, None, TypeError), 
#         ("", property(), False, False, None, TypeError), 
#         ("", range(int()), False, False, None, TypeError), 
#         ("", reversed(str()), False, False, None, TypeError), 
#         ("", set(), False, False, None, TypeError), 
#         ("", slice(int()), False, False, None, TypeError), 
#         ("", staticmethod(lambda: None), False, False, None, TypeError), 
#         ("", str(), False, False, None, TypeError), 
#         ("", tuple(), False, False, None, TypeError), 
#         ("", type(object()), False, False, None, TypeError), 
#         ("", zip(), False, False, None, TypeError), 

#         # Test series 3: TypeError if 'validate_bool' not `bool`
#         ("", False, None, False, None, TypeError), 
#         ("", False, bool(), False, None, None), 
#         ("", False, bytearray(), False, None, TypeError), 
#         ("", False, bytes(), False, None, TypeError), 
#         ("", False, classmethod(lambda: None), False, None, TypeError), 
#         ("", False, complex(), False, None, TypeError), 
#         ("", False, dict(), False, None, TypeError), 
#         ("", False, enumerate(str()), False, None, TypeError), 
#         ("", False, filter(lambda: None, str()), False, None, TypeError), 
#         ("", False, float(), False, None, TypeError), 
#         ("", False, frozenset(), False, None, TypeError), 
#         ("", False, int(), False, None, TypeError), 
#         ("", False, list(), False, None, TypeError), 
#         ("", False, map(lambda: None, str()), False, None, TypeError), 
#         ("", False, memoryview(bytes()), False, None, TypeError), 
#         ("", False, object(), False, None, TypeError), 
#         ("", False, property(), False, None, TypeError), 
#         ("", False, range(int()), False, None, TypeError), 
#         ("", False, reversed(str()), False, None, TypeError), 
#         ("", False, set(), False, None, TypeError), 
#         ("", False, slice(int()), False, None, TypeError), 
#         ("", False, staticmethod(lambda: None), False, None, TypeError), 
#         ("", False, str(), False, None, TypeError), 
#         ("", False, tuple(), False, None, TypeError), 
#         ("", False, type(object()), False, None, TypeError), 
#         ("", False, zip(), False, None, TypeError), 

#         # Test series 4: TypeError if 'validate_int' not `bool`
#         ("", False, False, None, None, TypeError), 
#         ("", False, False, bool(), None, None), 
#         ("", False, False, bytearray(), None, TypeError), 
#         ("", False, False, bytes(), None, TypeError), 
#         ("", False, False, classmethod(lambda: None), None, TypeError), 
#         ("", False, False, complex(), None, TypeError), 
#         ("", False, False, dict(), None, TypeError), 
#         ("", False, False, enumerate(str()), None, TypeError), 
#         ("", False, False, filter(lambda: None, str()), None, TypeError), 
#         ("", False, False, float(), None, TypeError), 
#         ("", False, False, frozenset(), None, TypeError), 
#         ("", False, False, int(), None, TypeError), 
#         ("", False, False, list(), None, TypeError), 
#         ("", False, False, map(lambda: None, str()), None, TypeError), 
#         ("", False, False, memoryview(bytes()), None, TypeError), 
#         ("", False, False, object(), None, TypeError), 
#         ("", False, False, property(), None, TypeError), 
#         ("", False, False, range(int()), None, TypeError), 
#         ("", False, False, reversed(str()), None, TypeError), 
#         ("", False, False, set(), None, TypeError), 
#         ("", False, False, slice(int()), None, TypeError), 
#         ("", False, False, staticmethod(lambda: None), None, TypeError), 
#         ("", False, False, str(), None, TypeError), 
#         ("", False, False, tuple(), None, TypeError), 
#         ("", False, False, type(object()), None, TypeError), 
#         ("", False, False, zip(), None, TypeError),

#         # Test series 5: TypeError if 'int_validation' not `None`, `int`,
#         #     or `tuple`
#         ("", False, False, True, None, None), 
#         ("", False, False, True, bool(), TypeError), 
#         ("", False, False, True, bytearray(), TypeError), 
#         ("", False, False, True, bytes(), TypeError), 
#         ("", False, False, True, classmethod(lambda: None), TypeError), 
#         ("", False, False, True, complex(), TypeError), 
#         ("", False, False, True, dict(), TypeError), 
#         ("", False, False, True, enumerate(str()), TypeError), 
#         ("", False, False, True, filter(lambda: None, str()), TypeError), 
#         ("", False, False, True, float(), TypeError), 
#         ("", False, False, True, frozenset(), TypeError), 
#         ("", False, False, True, int(), None), 
#         ("", False, False, True, list(), TypeError), 
#         ("", False, False, True, map(lambda: None, str()), TypeError), 
#         ("", False, False, True, memoryview(bytes()), TypeError), 
#         ("", False, False, True, object(), TypeError), 
#         ("", False, False, True, property(), TypeError), 
#         ("", False, False, True, range(int()), TypeError), 
#         ("", False, False, True, reversed(str()), TypeError), 
#         ("", False, False, True, set(), TypeError), 
#         ("", False, False, True, slice(int()), TypeError), 
#         ("", False, False, True, staticmethod(lambda: None), TypeError), 
#         ("", False, False, True, str(), TypeError), 
#         ("", False, False, True, tuple([int(), int()]), None), 
#         ("", False, False, True, type(object()), TypeError), 
#         ("", False, False, True, zip(), TypeError), 
        
#         # Test series 6: ValueError if both 'validate_bool' and 
#         #     'validate_int' are `True`
#         ("", False, True, False, None, None), 
#         ("", False, False, True, None, None), 
#         ("", False, True, True, None, ValueError),
#         ("", False, False, False, None, None),
        
#         # Test series 7: ValueError if 'int_validation' is not `None` 
#         #     and 'validate_int' is `False`
#         ("", False, False, True, int(), None), 
#         ("", False, False, False, int(), ValueError), 
#         ("", False, False, False, None, None), 
        
#         # Test series 8: ValueError if 'int_validation' is an integer 
#         #     that is negative
#         ("", False, False, True, 0, None), 
#         ("", False, False, True, 1, None), 
#         ("", False, False, True, sys.maxsize, None), 
#         ("", False, False, True, -1, ValueError), 
#         ("", False, False, True, -sys.maxsize, ValueError), 

#         # Test series 9: ValueError if 'int_validation' is a tuple 
#         #     without two elements
#         ("", False, False, True, (1,), ValueError), 
#         ("", False, False, True, (1, 2), None), 
#         ("", False, False, True, (1, 2, 3), ValueError), 

#         # Test series 10: ValueError is second tuple value less than the 
#         #     first
#         ("", False, False, True, (0, 0), None), 
#         ("", False, False, True, (1, 2), None), 
#         ("", False, False, True, (-2, -1), None), 
#         ("", False, False, True, (1, 0), ValueError)
#     ]
# )
# def test_console_prompt_constructor(prompt, exp_key, validate_bool, 
#                                     validate_int, int_validation, exception):
#     # Execute
#     if exception:
#         with pytest.raises(exception):
#             ConsolePrompt(prompt, expect_keystroke=exp_key, 
#                           validate_bool=validate_bool, 
#                           validate_integer=validate_int, 
#                           integer_validation=int_validation)
#     else:
#         CP_inst = ConsolePrompt(prompt, expect_keystroke=exp_key, 
#                                 validate_bool=validate_bool, 
#                                 validate_integer=validate_int, 
#                                 integer_validation=int_validation)
    
#     # Verify
#         assert isinstance(CP_inst._trm, Terminal)
#         assert CP_inst._cue == prompt
#         assert CP_inst._exp_kst == exp_key
#         assert CP_inst._val_bool == validate_bool
#         assert CP_inst._val_int == validate_int
#         assert CP_inst._int_vld == int_validation
