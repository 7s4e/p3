from blessed import Terminal
import console as c

def test_clear_stdscr(mocker):
    # Create a mock Terminal object
    mock_console = mocker.Mock(spec=Terminal)

    # Mock the attributes that clear_stdscr uses
    mock_console.home = 'home_position'
    mock_console.clear = 'clear_screen'

    # Spy on the print function to see if it's called with the correct 
    # argument
    mock_print = mocker.patch("builtins.print")

    # Call the function under test
    c.clear_stdscr(mock_console)

    # Assert that print was called with the right arguments (home + 
    # clear)
    mock_print.assert_called_once_with('home_position' + 'clear_screen')

def test_put_script_banner(mocker):
    # Create a mock Terminal object
    mock_console = mocker.Mock(spec=Terminal)

    # Assume terminal width is 36 characters
    mock_console.width = 36

    # Simulate reverse formatting
    mock_console.reverse = lambda text: f"<reverse>{text}</reverse>"

    # Patch the print function to verify what is printed
    mock_print = mocker.patch("builtins.print")

    # Call the function under test with a sample script name
    script_name = "test_script"
    c.put_script_banner(mock_console, script_name)

    # Create the expected banner text, padded to the terminal width
    expected_output = "<reverse>Running test_script...              </reverse>"

    # Assert that print was called once with the expected output
    mock_print.assert_called_once_with(expected_output)