from blessed import Terminal
from modules.console import ConsoleBase


def test_console_base_constructor(mocker):
    # Setup
    mock_terminal = mocker.Mock(spec=Terminal)
    mocker.patch("modules.console.Terminal", 
                 return_value=mock_terminal)

    # Execute
    instance = ConsoleBase()

    # Verify
    assert instance._trm == mock_terminal
