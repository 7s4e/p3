import pytest
import sys
from modules import commands as cmd


@pytest.fixture
def rc_mck(mocker):
    return mocker.patch("modules.commands.run_command")


# Test listBlockDevices
@pytest.mark.parametrize(
    "disk, cols, shw_deps, exp_cmnd", 
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
def test_list_block_devices(rc_mck, disk, cols, shw_deps, exp_cmnd):
    # Setup
    rc_mck.return_value = "Mock Block Devices List"

    # Execute
    act_out = cmd.list_block_devices(disk, cols, shw_deps)

    # Verify
    rc_mck.assert_called_once_with(exp_cmnd)
    assert act_out == "Mock Block Devices List"


# Test runBadblocks
@pytest.mark.parametrize(
    "non_destruct, capt_out, exp_cmnd, exp_out",
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
def test_run_badblocks(rc_mck, non_destruct, capt_out, exp_cmnd, exp_out):
    # Setup
    rc_mck.return_value = exp_out

    # Execute
    act_out = cmd.run_badblocks("sda", non_destruct, capt_out)

    # Verify
    rc_mck.assert_called_once_with(exp_cmnd, capture_output=capt_out)
    assert act_out == exp_out


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
    r_mck = mocker.patch("modules.commands.run")
    r_mck.return_value = mocker.MagicMock(**mock_rtn)

    # Execute exception
    if should_raise:
        with pytest.raises(RuntimeError, match=mock_rtn.get("stderr", "")):
            cmd.run_command(cmnd, capt_out, use_shell=True)
    
    # Execute without exception
    else:
        act_out = cmd.run_command(cmnd, capt_out, use_shell=True)
        
        # Verify method output
        assert act_out == exp_out
    
    # Verify method process
    r_mck.assert_called_once_with(cmnd, capture_output=capt_out, shell=True, 
                                  text=True, 
                                  stdout=(sys.stdout if not capt_out 
                                          else None),
                                  stderr=(sys.stderr if not capt_out 
                                          else None))


# Test unmountDisk
def test_unmount_disk(mocker, rc_mck):
    # Setup runCommand mock
    mck_lsblk_out = ("PATH       MOUNTPOINT\n"
                     "/dev/sda1  /mnt/point1\n"
                     "/dev/sda2  /mnt/point2\n")
    rc_mck.side_effect = [mck_lsblk_out,  # First call for lsblk
                          None,           # Second call for umount
                          None]           # Third call for umount
    
    # Setup mock Table
    T_pch = mocker.patch("modules.commands.Table")
    mck_T = T_pch.return_value
    mck_T.filter_nonempty.return_value = None
    mck_T.count_records.return_value = 2
    mck_T.get_record.side_effect = [{"PATH": "/dev/sda1", 
                                     "MOUNTPOINT": "/mnt/point1"}, 
                                    {"PATH": "/dev/sda2", 
                                     "MOUNTPOINT": "/mnt/point2"}]

    # Execute
    cmd.unmount_disk("sda")

    # Verify runCommand calls
    rc_mck.assert_any_call("lsblk --output PATH,MOUNTPOINT /dev/sda")
    rc_mck.assert_any_call("sudo umount --verbose /dev/sda1", 
                                     capture_output=False)
    rc_mck.assert_any_call("sudo umount --verbose /dev/sda2", 
                                     capture_output=False)
    assert rc_mck.call_count == 3

    # Verify Table method calls
    T_pch.assert_called_once_with(table_string=mck_lsblk_out)
    mck_T.filter_nonempty.assert_called_once_with("MOUNTPOINT")
