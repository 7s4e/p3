import pytest
from blessed import Terminal
from modules import Console


@pytest.fixture
def mock_console(mocker):
    return mocker.Mock(spec=Terminal)

@pytest.fixture
def mock_base(mocker, mock_console):
    base_class = mocker.patch("modules.console.ConsoleBase")
    base_class.return_value._trm = mock_console
    return base_class

@pytest.fixture
def print_mock(mocker):
    return mocker.patch("builtins.print")


def test_clear_stdscr(mock_console, mock_base, print_mock):
    # Setup
    mock_console.home = "home_position"
    mock_console.clear = "clear_screen"

    # Execute
    Console.clear_stdscr()

    # Verify
    mock_base.assert_called_once()
    print_mock.assert_called_once_with("home_position" + "clear_screen")


def test_put_script_banner(mock_console, mock_base, print_mock):
    # Setup
    mock_console.width = 36
    mock_console.reverse = lambda text: f"<reverse>{text}</reverse>"

    # Execute
    Console.put_script_banner("mock_script")

    # Verify
    mock_base.assert_called_once()
    exp_out = "<reverse>Running mock_script...              </reverse>"
    print_mock.assert_called_once_with(exp_out)
