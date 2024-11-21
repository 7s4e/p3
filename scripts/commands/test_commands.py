import pytest
from unittest.mock import patch, MagicMock
import sys
import commands as c


@pytest.fixture
def mock_run():
    with patch("commands.subprocess.run") as run:
        yield run


@pytest.fixture
def mock_run_command():
    with patch("commands.run_command") as command:
        yield command


@pytest.mark.parametrize(
    " command,                capture_output, mock_return,                                       expected_output, should_raise",
    [("echo 'Hello, World!'", True,           MagicMock(returncode=0, stdout="Hello, World!\n"), "Hello, World!", False),
     ("exit 1",               True,           MagicMock(returncode=1, stderr="Command failed"),  None,            True),
     ("echo 'No Capture'",    False,          MagicMock(returncode=0),                           None,            False)])

def test_run_command(mock_run, command, capture_output, mock_return, 
                     expected_output, should_raise):
    # Setup
    mock_run.return_value = mock_return

    # Execute
    if should_raise:
        with pytest.raises(RuntimeError, match=mock_return.stderr):
            c.run_command(command, capture_output=capture_output, 
                          use_shell=True)
    else:
        output = c.run_command(command, capture_output=capture_output, 
                               use_shell=True)
        
    # Verify
        assert output == expected_output
    mock_run.assert_called_once_with(
        command, capture_output=capture_output, shell=True, text=True, 
        stdout=sys.stdout if not capture_output else None,
        stderr=sys.stderr if not capture_output else None)


@pytest.mark.parametrize(
    " disk,  columns,          show_dependents, expected_command",
    [(None,  [],               True,            "lsblk"),
     ("sda", [],               True,            "lsblk /dev/sda"),
     (None,  ["NAME", "SIZE"], True,            "lsblk --output NAME,SIZE"),
     (None,  [],               False,           "lsblk --nodeps"),
     ("sda", ["NAME", "TYPE"], False,           "lsblk --nodeps --output NAME,TYPE /dev/sda")])

def test_list_block_devices(mock_run_command, disk, columns, show_dependents, 
                            expected_command):
    # Setup
    mock_run_command.return_value = "MOCK OUTPUT"

    # Execute
    result = c.list_block_devices(disk=disk, columns=columns, 
                                  show_dependents=show_dependents)

    # Verify
    mock_run_command.assert_called_once_with(expected_command)
    assert result == "MOCK OUTPUT"


# def test_run_badblocks():
#     pass

# def test_unmount_disk():
#     pass