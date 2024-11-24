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

@pytest.fixture
def mock_table():
    with patch("table.Table") as table:
        yield table


# Test runCommand
@pytest.mark.parametrize(
    "command, capture_output, mock_return, expected_output, should_raise",
    [
        # Test case 1: Command success with output.
        (
            "echo 'Hello, World!'", 
            True, 
            MagicMock(returncode=0, stdout="Hello, World!\n"), 
            "Hello, World!", 
            False
        ), 
        # Test case 2: Command fail.
        (
            "exit 1", 
            True, 
            MagicMock(returncode=1, stderr="Command failed"), 
            None, 
            True
        ),
        # Test case 3: Command success without output.
        (
            "echo 'No Capture'", 
            False, 
            MagicMock(returncode=0), 
            None, 
            False
        )
    ]
)
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


# Test listBlockDevices
@pytest.mark.parametrize("disk, columns, show_dependents, expected_command", 
    [
        # Test case 1: Command to list block devices
        (
            None, 
            [], 
            True, 
            "lsblk"
        ),
        # Test case 2: Command to list /dev/sda disk and partitions
        (
            "sda", 
            [], 
            True, 
            "lsblk /dev/sda"
        ),
        # Test case 3: Command to print specified output columns
        (
            None, 
            ["NAME", "SIZE"], 
            True, 
            "lsblk --output NAME,SIZE"
        ),
        # Test case 4: Command to not print slaves
        (
            None, 
            [], 
            False, 
            "lsblk --nodeps"
        ),
        # Test case 5: Command to print with columns and without slaves
        (
            "sda", 
            ["NAME", "TYPE"], 
            False, 
            "lsblk --nodeps --output NAME,TYPE /dev/sda"
        )
    ]
)
def test_list_block_devices(mock_run_command, disk, columns, show_dependents, 
                            expected_command):
    # Setup
    mock_run_command.return_value = "Mock Output"

    # Execute
    result = c.list_block_devices(disk=disk, columns=columns, 
                                  show_dependents=show_dependents)

    # Verify
    mock_run_command.assert_called_once_with(expected_command)
    assert result == "Mock Output"


@pytest.mark.parametrize(
    "non_destructive, capture_output, exp_command, mock_output, exp_result",
    [
        # Test case 1: Non-destructive command with output
        (
            True, 
            True, 
            "sudo badblocks --non-destructive --show-progress --verbose /dev/sda", 
            "Mock Output", 
            "Mock Output"
        ),
        # Test case 2: Destructive command with output
        (
            False, 
            True, 
            "sudo badblocks --write-mode --show-progress --verbose /dev/sda", 
            "Mock Output", 
            "Mock Output"
        ),
        # Test case 3: Non-destructive commmand without output
        (
            True, 
            False, 
            "sudo badblocks --non-destructive --show-progress --verbose /dev/sda", 
            None, 
            None
        ),
        # Test case 4: Destructive command without output
        (
            False, 
            False, 
            "sudo badblocks --write-mode --show-progress --verbose /dev/sda", 
            None, 
            None
        )
    ]
)
def test_run_badblocks(mock_run_command, non_destructive, capture_output, 
                       exp_command, mock_output, exp_result):
    # Setup
    mock_run_command.return_value = mock_output

    # Execute
    result = c.run_badblocks("sda", non_destructive, capture_output)

    # Verify
    mock_run_command.assert_called_once_with(exp_command, 
                                             capture_output=capture_output)
    assert result == exp_result


# def test_unmount_disk(mock_run_command, mock_table):
#     # Setup
#     mock_lsblk_output = ("PATH       MOUNTPOINT\n"
#                          "/dev/sda1  /mnt/point1\n"
#                          "/dev/sda2  /mnt/point2\n")
#     mock_run_command.side_effect = [mock_lsblk_output,  # First call for lsblk
#                                     None,               # Second call for umount
#                                     None]               # Third call for umount
#     mock_table_instance = mock_table.return_value
#     mock_table_instance.filter_nonempty.return_value = None
#     mock_table_instance.count_records.return_value = 2
#     mock_table_instance.get_record.side_effect = [{"PATH": "/dev/sda1", 
#                                                    "MOUNTPOINT": "/mnt/point1"},
#                                                   {"PATH": "/dev/sda2", 
#                                                    "MOUNTPOINT": "/mnt/point2"}]

#     # Execute
#     c.unmount_disk("sda")

#     # Verify
#     mock_run_command.assert_any_call("lsblk --output PATH,MOUNTPOINT /dev/sda")
#     mock_run_command.assert_any_call("sudo umount --verbose /mnt/point1", 
#                                      capture_output=False)
#     mock_run_command.assert_any_call("sudo umount --verbose /mnt/point2", 
#                                      capture_output=False)
#     assert mock_run_command.call_count == 3
#     mock_table.assert_called_once_with(table_string=mock_lsblk_output)
#     mock_table_instance.filter_nonempty.assert_called_once_with("MOUNTPOINT")
