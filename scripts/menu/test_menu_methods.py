import pytest
from functools import partial
from blessed import Terminal
from console_prompt import ConsolePrompt
from menu import Menu
from table import Table


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
def test_run(mocker, option_count, user_response):
    # Setup mock Table for Menu initialization and run() call
    mock_table = mocker.Mock(spec=Table)
    mock_table.count_records.return_value = option_count
    mock_table.get_record.return_value = {"OPTION": "Mock option"}

    # Setup mock ConsolePrompt for Menu instance and mock user response
    mock_prompt = mocker.Mock(spec=ConsolePrompt)
    mock_prompt.call.return_value = user_response

    # Setup Menu instance
    menu_instance = Menu(mock_table)
    menu_instance._prompt = mock_prompt

    # Setup mock Terminal as test argument
    mock_console = mocker.Mock(spec=Terminal)

    # Execute
    menu_instance.run(mock_console)

    # Verify
    menu_instance._options.put_table.assert_called_once_with(mock_console, 
                                                             is_menu=True)
    menu_instance._prompt.call.assert_called_once_with(mock_console)
    menu_instance._options.get_record.called_once_with(user_response - 1)
    assert menu_instance._selection == {"OPTION": "Mock option"}


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
    # Setup method isolating instance
    if mock_menu:
        menu = mocker.Mock(spec=Menu)
        menu._count = options
        method = getattr(menu, "set_prompt")
        method.side_effect = partial(getattr(Menu, "set_prompt"), menu)
    
    # Setup method integrated instance
    else:
        menu = Menu(options)
    
    # Setup ConsolePrompt mock and its prompt argument
    mock_console_prompt = mocker.patch("menu.ConsolePrompt")
    prompt_arg = (prompt_param if prompt_param is not None 
                  else f"Enter number (1-{options}) for selection:")

    # Execute
    menu.set_prompt(prompt_arg)
    
    # Verify
    count = menu._count
    mock_console_prompt.assert_called_once_with(prompt_arg, 
                                                expect_keystroke=count<10, 
                                                validate_integer=True, 
                                                integer_validation=(1, count))
