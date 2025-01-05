import pytest
from blessed import Terminal
from modules import Console


@pytest.fixture
def mck_T(mocker):
    return mocker.Mock(spec=Terminal)

@pytest.fixture
def mck_CB(mocker, mck_T):
    base_class = mocker.patch("modules.console.ConsoleBase")
    base_class.return_value._trm = mck_T
    return base_class

@pytest.fixture
def pnt_mck(mocker):
    return mocker.patch("builtins.print")


def test_clear_screen(mck_T, mck_CB, pnt_mck):
    # Setup
    mck_T.home = "home_position"
    mck_T.clear = "clear_screen"

    # Execute
    Console.clear_screen()

    # Verify
    mck_CB.assert_called_once()
    pnt_mck.assert_called_once_with("home_position" + "clear_screen")


def test_put_script_banner(mck_T, mck_CB, pnt_mck):
    # Setup
    mck_T.width = 36
    mck_T.reverse = lambda text: f"<reverse>{text}</reverse>"
    exp_pnt_arg = "<reverse>Running mockScript...               </reverse>"

    # Execute
    Console.put_script_banner("mock_script")

    # Verify
    mck_CB.assert_called_once()
    pnt_mck.assert_called_once_with(exp_pnt_arg)
