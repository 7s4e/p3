import pytest
from functools import partial
from menu import Menu


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

        # Test case 5: Isolated method on short menu with prompt
        (False, ["a", "b", "c", "d", "e"], "Mock prompt?"), 

        # Test case 6: Isolated method on short menu without prompt
        (False, ["a", "b", "c", "d", "e"], None), 

        # Test case 7: Isolated method on long menu with prompt
        (False, ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"], "Mock prompt?"), 

        # Test case 4: Isolated method on long menu without prompt
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
