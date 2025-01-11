import pytest
import sys
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


@pytest.mark.parametrize(
    "n_lines, exception", 
    [
        (1., TypeError), 
        (-1, ValueError), 
        (-sys.maxsize, ValueError), 
        (0, None), 
        (1, None), 
        (9, None), 
        (sys.maxsize, None)
    ]
)
def test_back_n_lines(mocker, mck_T, mck_CB, n_lines, exception):
    # Setup
    mck_T.height = 99
    write_mck = mocker.patch("sys.stdout.write")
    flush_mck = mocker.patch("sys.stdout.flush")
    mv_up_cll = mocker.call("\033[F")
    clr_ln_cll = mocker.call("\033[K")

    # Execute
    if exception:
        with pytest.raises(exception):
            Console.back_n_lines(n_lines)
    else:
        Console.back_n_lines(n_lines)

    # Verify
        mck_CB.assert_called_once()
        exp_calls = [mv_up_cll, clr_ln_cll] * min(n_lines, mck_T.height)
        write_mck.assert_has_calls(exp_calls)
        flush_mck.assert_called_once()


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
