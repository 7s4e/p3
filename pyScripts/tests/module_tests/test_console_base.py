from blessed import Terminal
from modules.console import ConsoleBase


def test_console_base_constructor(mocker):
    # Setup
    mck_T = mocker.Mock(spec=Terminal)
    mocker.patch("modules.console.Terminal", return_value=mck_T)

    # Execute
    CB_inst = ConsoleBase()

    # Verify
    assert CB_inst._trm == mck_T
