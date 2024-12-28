import pytest
from functools import partial
from src import ConsolePrompt, Menu, Table


# Test run
@pytest.mark.parametrize(
    "option_count, user_response", 
    [
        (1, 1),   # Test case 1: Single record, first option
        (7, 1),   # Test case 2: Multiple records, first option
        (7, 7),   # Test case 3: Multiple records, last option
        (10, 5),  # Test case 4: Double-digit records, middle option
    ]
)
def test_run_and_get_selection(mocker, option_count, user_response):
    # Setup mock Table for Menu initialization and run() call
    mock_tbl = mocker.Mock(spec=Table)
    mock_tbl.count_records.return_value = option_count
    mock_tbl.get_record.return_value = {"OPTION": "Mock option"}

    # Setup mock ConsolePrompt for Menu instance and mock user response
    mock_prmpt = mocker.Mock(spec=ConsolePrompt)
    mock_prmpt.call.return_value = user_response

    # Setup Menu instance
    mnu = Menu(mock_tbl)
    mnu._prompt = mock_prmpt

    mnu.run()
    result = mnu.get_selection("option")

    # Verify run method
    mnu._options.put_table.assert_called_once_with(is_menu=True)
    mnu._prompt.call.assert_called_once()
    mnu._options.get_record.called_once_with(user_response - 1)
    assert mnu._selection == {"OPTION": "Mock option"}

    # Verify getSelection method
    assert result == "Mock option"


# Test setPrompt
@pytest.mark.parametrize(
    "mock_menu, options, prompt_param", 
    [
        # Test case 1: Isolated method on short menu with prompt
        (True, 7, "Mock prompt?"), 

        # Test case 2: Isolated method on short menu without prompt
        (True, 7, None), 

        # Test case 3: Isolated method on long menu with prompt
        (True, 55, "Mock prompt?"), 

        # Test case 4: Isolated method on long menu without prompt
        (True, 55, None), 

        # Test case 5: Integrated method on short menu with prompt
        (False, ["a", "b", "c", "d", "e"], "Mock prompt?"), 

        # Test case 6: Integrated method on short menu without prompt
        (False, ["a", "b", "c", "d", "e"], None), 

        # Test case 7: Integrated method on long menu with prompt
        (False, 
         ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"], "Mock prompt?"), 

        # Test case 4: Integrated method on long menu without prompt
        (False, ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"], None), 
    ]
)
def test_set_prompt(mocker, mock_menu, options, prompt_param):
    # Setup mock Menu to isolate method as if called in __init__; use of 
    # partial binds the real setPrompt method to the mock instance
    if mock_menu:
        mnu = mocker.Mock(spec=Menu)
        mnu._count = options
        method = getattr(mnu, "set_prompt")
        method.side_effect = partial(getattr(Menu, "set_prompt"), mnu)
    
    # Setup Menu instance to integrate method as if called on real 
    # instance
    else:
        mnu = Menu(options)

    # Setup ConsolePrompt, patch, and parameter
    mock_con_prmpt = mocker.Mock(spec=ConsolePrompt)
    cprmpt_patch = mocker.patch("src.ConsolePrompt", 
                                return_value=mock_con_prmpt)
    prompt_arg = (prompt_param if prompt_param is not None 
                  else f"Enter number (1-{options}) for selection:")

    # Execute
    mnu.set_prompt(prompt_arg)
    
    # Verify
    cnt = mnu._count
    cprmpt_patch.assert_called_once_with(prompt_arg, 
                                         expect_keystroke=cnt<10, 
                                         validate_integer=True, 
                                         integer_validation=(1, cnt))
