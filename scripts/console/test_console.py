import pytest
from blessed import Terminal
import console as c


@pytest.fixture
def mock_console(mocker):
    terminal_mock = mocker.Mock(spec=Terminal)
    terminal_mock.home = "home_position"
    terminal_mock.clear = "clear_screen"
    terminal_mock.width = 36
    terminal_mock.reverse = lambda text: f"<reverse>{text}</reverse>"
    return terminal_mock


def test_clear_stdscr(mock_console, mocker):
    # Setup
    mock_print = mocker.patch("builtins.print")

    # Execute
    c.clear_stdscr(mock_console)

    # Verify
    mock_print.assert_called_once_with("home_position" + "clear_screen")


def test_put_script_banner(mock_console, mocker):
    # Setup
    mock_print = mocker.patch("builtins.print")
    script_name = "test_script"

    # Execute
    c.put_script_banner(mock_console, script_name)

    # Verify
    expected_output = "<reverse>Running test_script...              </reverse>"
    mock_print.assert_called_once_with(expected_output)
