import pytest
import sys
from src import commands as cmd


@pytest.fixture
def run_cmmnd_mock(mocker):
    return mocker.patch("src.commands.run_command")


# Test listBlockDevices
@pytest.mark.parametrize("disk, cols, shw_deps, exp_cmnd", 
    [
        # Test case 1: Command to list block devices
        (None, [], True, "lsblk"),

        # Test case 2: Command to list /dev/sda disk and partitions
        ("sda", [], True, "lsblk /dev/sda"), 

        # Test case 3: Command to print specified output columns
        (None, ["NAME", "SIZE"], True, "lsblk --output NAME,SIZE"), 

        # Test case 4: Command to not print slaves
        (None, [], False, "lsblk --nodeps"), 

        # Test case 5: Command to print with columns and without slaves
        ("sda", ["NAME", "TYPE"], False, 
         "lsblk --nodeps --output NAME,TYPE /dev/sda")
    ]
)
def test_list_block_devices(run_cmmnd_mock, disk, cols, shw_deps, exp_cmnd):
    # Setup
    run_cmmnd_mock.return_value = "Mock Block Devices List"

    # Execute
    result = cmd.list_block_devices(disk, cols, shw_deps)

    # Verify
    run_cmmnd_mock.assert_called_once_with(exp_cmnd)
    assert result == "Mock Block Devices List"


# Test runBadblocks
@pytest.mark.parametrize(
    "non_destruct, capt_out, exp_cmnd, mock_out",
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
def test_run_badblocks(run_cmmnd_mock, non_destruct, capt_out, exp_cmnd, 
                       mock_out):
    # Setup
    run_cmmnd_mock.return_value = mock_out

    # Execute
    result = cmd.run_badblocks("sda", non_destruct, capt_out)

    # Verify
    run_cmmnd_mock.assert_called_once_with(exp_cmnd, capture_output=capt_out)
    assert result == mock_out


# Test runCommand
@pytest.mark.parametrize(
    "cmnd, capt_out, mock_rtn, exp_out, should_raise",
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
def test_run_command(mocker, cmnd, mock_rtn, capt_out, exp_out, should_raise):
    # Setup
    run_mock = mocker.patch("subprocess.run")
    run_mock.return_value = mocker.MagicMock(**mock_rtn)

    # Execute exception
    if should_raise:
        with pytest.raises(RuntimeError, match=mock_rtn.get("stderr", "")):
            cmd.run_command(cmnd, capt_out, use_shell=True)
    
    # Execute without exception
    else:
        result = cmd.run_command(cmnd, capt_out, use_shell=True)
        
        # Verify method output
        assert result == exp_out
    
    # Verify method process
    run_mock.assert_called_once_with(cmnd, capture_output=capt_out, 
                                     shell=True, text=True, 
                                     stdout=(sys.stdout if not capt_out 
                                             else None),
                                     stderr=(sys.stderr if not capt_out 
                                             else None))


# Test unmountDisk
def test_unmount_disk(mocker, run_cmmnd_mock):
    # Setup runCommand mock
    mock_lsblk_out = ("PATH       MOUNTPOINT\n"
                      "/dev/sda1  /mnt/point1\n"
                      "/dev/sda2  /mnt/point2\n")
    run_cmmnd_mock.side_effect = [mock_lsblk_out,  # First call for lsblk
                                  None,            # Second call for umount
                                  None]            # Third call for umount
    
    # Setup mock Table
    tbl_patch = mocker.patch("src.commands.Table")
    mock_tbl = tbl_patch.return_value
    mock_tbl.filter_nonempty.return_value = None
    mock_tbl.count_records.return_value = 2
    mock_tbl.get_record.side_effect = [{"PATH": "/dev/sda1", 
                                        "MOUNTPOINT": "/mnt/point1"}, 
                                       {"PATH": "/dev/sda2", 
                                        "MOUNTPOINT": "/mnt/point2"}]

    # Execute
    cmd.unmount_disk("sda")

    # Verify runCommand calls
    run_cmmnd_mock.assert_any_call("lsblk --output PATH,MOUNTPOINT /dev/sda")
    run_cmmnd_mock.assert_any_call("sudo umount --verbose /dev/sda1", 
                                     capture_output=False)
    run_cmmnd_mock.assert_any_call("sudo umount --verbose /dev/sda2", 
                                     capture_output=False)
    assert run_cmmnd_mock.call_count == 3

    # Verify Table method calls
    tbl_patch.assert_called_once_with(table_string=mock_lsblk_out)
    mock_tbl.filter_nonempty.assert_called_once_with("MOUNTPOINT")
    pass
