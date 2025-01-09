# import pytest
# from functools import partial
# from modules import ConsolePrompt, Menu, Table


# # Test run
# @pytest.mark.parametrize(
#     "option_count, user_response", 
#     [
#         (1, 1),   # Test case 1: Single record, first option
#         (7, 1),   # Test case 2: Multiple records, first option
#         (7, 7),   # Test case 3: Multiple records, last option
#         (10, 5),  # Test case 4: Double-digit records, middle option
#     ]
# )
# def test_run_and_get_selection(mocker, option_count, user_response):
#     # Setup mock Table for Menu initialization and run() call
#     mck_T = mocker.Mock(spec=Table)
#     mck_T.count_records.return_value = option_count
#     mck_T.get_record.return_value = {"OPTION": "Mock option"}

#     # Setup mock ConsolePrompt for Menu instance and mock user response
#     mck_CP = mocker.Mock(spec=ConsolePrompt)
#     mck_CP.call.return_value = user_response

#     # Setup Menu instance
#     M_inst = Menu(mck_T)
#     M_inst._prmt = mck_CP

#     M_inst.run()
#     result = M_inst.get_selection("option")

#     # Verify run method
#     M_inst._opts.put_table.assert_called_once_with(is_menu=True)
#     M_inst._prmt.call.assert_called_once()
#     M_inst._opts.get_record.called_once_with(user_response - 1)
#     assert M_inst._sel == {"OPTION": "Mock option"}

#     # Verify getSelection method
#     assert result == "Mock option"


# # Test setPrompt
# @pytest.mark.parametrize(
#     "mock_menu, options, prompt_param", 
#     [
#         # Test case 1: Isolated method on short menu with prompt
#         (True, 7, "Mock prompt?"), 

#         # Test case 2: Isolated method on short menu without prompt
#         (True, 7, None), 

#         # Test case 3: Isolated method on long menu with prompt
#         (True, 55, "Mock prompt?"), 

#         # Test case 4: Isolated method on long menu without prompt
#         (True, 55, None), 

#         # Test case 5: Integrated method on short menu with prompt
#         (False, ["a", "b", "c", "d", "e"], "Mock prompt?"), 

#         # Test case 6: Integrated method on short menu without prompt
#         (False, ["a", "b", "c", "d", "e"], None), 

#         # Test case 7: Integrated method on long menu with prompt
#         (False, 
#          ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"], "Mock prompt?"), 

#         # Test case 8: Integrated method on long menu without prompt
#         (False, ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"], None), 
#     ]
# )
# def test_set_prompt(mocker, mock_menu, options, prompt_param):
#     # Setup mock Menu to isolate method as if called in __init__; use of 
#     # partial binds the real setPrompt method to the mock instance
#     if mock_menu:
#         M_obj = mocker.Mock(spec=Menu)
#         M_obj._ct = options
#         method = getattr(M_obj, "set_prompt")
#         method.side_effect = partial(getattr(Menu, "set_prompt"), M_obj)
    
#     # Setup Menu instance to integrate method as if called on real 
#     # instance
#     else:
#         M_obj = Menu(options)

#     # Setup ConsolePrompt, patch, and parameter
#     mck_CP = mocker.Mock(spec=ConsolePrompt)
#     CP_ptch = mocker.patch("modules.menu.ConsolePrompt", return_value=mck_CP)
#     prompt_arg = (prompt_param if prompt_param is not None 
#                   else f"Enter number (1-{options}) for selection:")

#     # Execute
#     M_obj.set_prompt(prompt_arg)
    
#     # Verify
#     count = M_obj._ct
#     CP_ptch.assert_called_once_with(prompt_arg, expect_keystroke=count<10, 
#                                     validate_integer=True, 
#                                     integer_validation=(1, count))
