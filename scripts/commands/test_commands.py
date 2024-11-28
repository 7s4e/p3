import pytest
import commands
from sys import stdout, stderr


@pytest.fixture
def mock_run(mocker):
    return mocker.patch("commands.run")

@pytest.fixture
def mock_command_run(mocker):
    return mocker.patch("commands.run_command")

@pytest.fixture
def mock_table(mocker):
    return mocker.patch("commands.Table")


# Test runCommand
@pytest.mark.parametrize(
    "command, capture_output, mock_return, exp_output, should_raise",
    [
        # Test case 1: Command success with output.
        (
            "echo 'Hello, World!'", 
            True, 
            {"returncode": 0, "stdout": "Hello, World!\n"}, 
            "Hello, World!", 
            False
        ), 
        # Test case 2: Command fail.
        (
            "exit 1", 
            True, 
            {"returncode": 1, "stderr": "Command failed"}, 
            None, 
            True
        ),
        # Test case 3: Command success without output.
        (
            "echo 'No Capture'", 
            False, 
            {"returncode": 0}, 
            None, 
            False
        )
    ]
)
def test_run_command(mocker, mock_run, command, mock_return, capture_output, 
                     exp_output, should_raise):
    # Setup
    mock_run.return_value = mocker.MagicMock(**mock_return)

    # Execute
    if should_raise:
        with pytest.raises(RuntimeError, match=mock_return.get("stderr", "")):
            commands.run_command(command, capture_output, use_shell=True)
    else:
        result = commands.run_command(command, capture_output, use_shell=True)
        
        # Verify method output
        assert result == exp_output
    
    # Verify method process
    mock_run.assert_called_once_with(command, capture_output=capture_output, 
                                     shell=True, text=True, 
                                     stdout=stdout 
                                     if not capture_output else None,
                                     stderr=stderr 
                                     if not capture_output else None)


# Test listBlockDevices
@pytest.mark.parametrize("disk, columns, show_dependents, exp_command", 
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
def test_list_block_devices(mock_command_run, disk, columns, show_dependents, 
                            exp_command):
    # Setup
    mock_command_run.return_value = "Mock Block Devices List"

    # Execute
    result = commands.list_block_devices(disk, columns, show_dependents)

    # Verify
    mock_command_run.assert_called_once_with(exp_command)
    assert result == "Mock Block Devices List"


# Test runBadblocks
@pytest.mark.parametrize(
    "non_destructive, capture_output, exp_command, mock_output",
    [
        # Test case 1: Non-destructive command with output
        (
            True, 
            True, 
            "sudo badblocks --non-destructive --show-progress --verbose /dev/sda", 
            "Mock Badblocks Report", 
        ),
        # Test case 2: Destructive command with output
        (
            False, 
            True, 
            "sudo badblocks --write-mode --show-progress --verbose /dev/sda", 
            "Mock Badblocks Report", 
        ),
        # Test case 3: Non-destructive commmand without output
        (
            True, 
            False, 
            "sudo badblocks --non-destructive --show-progress --verbose /dev/sda", 
            None
        ),
        # Test case 4: Destructive command without output
        (
            False, 
            False, 
            "sudo badblocks --write-mode --show-progress --verbose /dev/sda", 
            None
        )
    ]
)
def test_run_badblocks(mock_command_run, non_destructive, capture_output, 
                       exp_command, mock_output):
    # Setup
    mock_command_run.return_value = mock_output

    # Execute
    result = commands.run_badblocks("sda", non_destructive, capture_output)

    # Verify
    mock_command_run.assert_called_once_with(exp_command, 
                                             capture_output=capture_output)
    assert result == mock_output


# Test unmountDisk
def test_unmount_disk(mock_command_run, mock_table):
    # Setup
    mock_lsblk_output = ("PATH       MOUNTPOINT\n"
                         "/dev/sda1  /mnt/point1\n"
                         "/dev/sda2  /mnt/point2\n")
    mock_command_run.side_effect = [mock_lsblk_output,  # First call for lsblk
                                    None,               # Second call for umount
                                    None]               # Third call for umount
    mock_table_instance = mock_table.return_value
    mock_table_instance.filter_nonempty.return_value = None
    mock_table_instance.count_records.return_value = 2
    mock_table_instance.get_record.side_effect = [{"PATH": "/dev/sda1", 
                                                   "MOUNTPOINT": "/mnt/point1"},
                                                  {"PATH": "/dev/sda2", 
                                                   "MOUNTPOINT": "/mnt/point2"}]

    # Execute
    commands.unmount_disk("sda")

    # Verify
    mock_command_run.assert_any_call("lsblk --output PATH,MOUNTPOINT /dev/sda")
    mock_command_run.assert_any_call("sudo umount --verbose /dev/sda1", 
                                     capture_output=False)
    mock_command_run.assert_any_call("sudo umount --verbose /dev/sda2", 
                                     capture_output=False)
    assert mock_command_run.call_count == 3
    mock_table.assert_called_once_with(table_string=mock_lsblk_output)
    mock_table_instance.filter_nonempty.assert_called_once_with("MOUNTPOINT")
