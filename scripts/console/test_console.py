import pytest
from blessed import Terminal
import console as con


@pytest.fixture
def mock_console(mocker):
    terminal_mock = mocker.Mock(spec=Terminal)
    terminal_mock.home = "home_position"
    terminal_mock.clear = "clear_screen"
    terminal_mock.width = 36
    terminal_mock.reverse = lambda text: f"<reverse>{text}</reverse>"
    return terminal_mock


def test_clear_stdscr(mocker, mock_console):
    # Setup
    mock_print = mocker.patch("builtins.print")

    # Execute
    con.clear_stdscr(mock_console)

    # Verify
    mock_print.assert_called_once_with("home_position" + "clear_screen")


def test_put_script_banner(mocker, mock_console):
    # Setup
    mock_print = mocker.patch("builtins.print")
    script_name = "test_script"

    # Execute
    con.put_script_banner(mock_console, script_name)

    # Verify
    exp_out = "<reverse>Running test_script...              </reverse>"
    mock_print.assert_called_once_with(exp_out)
