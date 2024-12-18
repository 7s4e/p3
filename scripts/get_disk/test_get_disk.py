import pytest
from blessed import Terminal
from table import Table
import get_disk as gd


@pytest.fixture
def console_mock(mocker):
    return mocker.Mock(spec=Terminal)

@pytest.fixture
def console_prompt_mocks(mocker):
    mock_class = mocker.patch("get_disk.ConsolePrompt")
    mock_instance = mock_class.return_value
    return mock_class, mock_instance

@pytest.fixture
def lsblk_mock(mocker):
    return mocker.patch("get_disk.cmd.list_block_devices")

@pytest.fixture
def table_mocks(mocker):
    mock_class = mocker.patch("get_disk.Table")
    mock_instance = mock_class.return_value
    return mock_class, mock_instance


# Test confirmDisk
def test_confirm_disk(lsblk_mock, table_mocks, console_prompt_mocks, 
                      console_mock):
    # Setup arguments
    mock_prompt = "Are you sure you want to select the disk 'sda'? (y/n) "
    lsblk_mock.return_value = ("NAME   TYPE  FSTYPE LABEL   MOUNTPOINTS\n" + 
                               "sda    disk\n" + 
                               "├─sda1 part  ext4   rootfs  /\n" + 
                               "├─sda2 part  swap           [SWAP]\n" + 
                               "└─sda3 part  ext4   data    /data")
    
    # Setup Table and ConsolePrompt mocks
    table_class, table_instance = table_mocks
    console_prompt_class, console_prompt_instance = console_prompt_mocks
    console_prompt_instance.call.return_value = True

    # Execute
    result = gd.confirm_disk(console_mock, "sda")

    # Verify lsblk call
    lsblk_mock.assert_called_once_with("sda", columns=["NAME", "TYPE", 
                                                       "FSTYPE", "LABEL", 
                                                       "MOUNTPOINTS"])
    
    # Verify Table calls
    table_class.assert_called_once_with(title="selected device", 
                                        table_string=lsblk_mock.return_value)
    table_instance.put_table.assert_called_once_with(console_mock)
    
    # Verify ConsolePrompt calls
    console_prompt_class.assert_called_once_with(mock_prompt, 
                                                 expect_keystroke=True, 
                                                 validate_bool=True)
    console_prompt_instance.call.assert_called_once_with(console_mock)

    # Verify method return    
    assert result == True


# Test getDisk
def test_get_disk(mocker, console_prompt_mocks, console_mock):
    # Setup mock dependencies
    mock_disks = mocker.Mock(spec=Table)
    confirm_disk_mock = mocker.patch("get_disk.confirm_disk")
    get_disks_mock = mocker.patch("get_disk.get_disks")
    put_script_banner_mock = mocker.patch("get_disk.con.put_script_banner")
    select_disk_mock = mocker.patch("get_disk.select_disk")
    unmount_disk_mock = mocker.patch("get_disk.cmd.unmount_disk")
    console_prompt_class, console_prompt_instance = console_prompt_mocks

    # Setup mock behavior
    get_disks_mock.return_value = mock_disks
    mock_disks.count_records.side_effect = [0,  # Iteration 1: No disks
                                            1,  # Iteration 2: One disk
                                            2]  # Iteration 3: Two disks
    mock_disks.get_record.return_value = {"NAME": "sda1"}  # Iteration 2
    select_disk_mock.return_value = "sda2"                 # Iteration 3
    confirm_disk_mock.side_effect = [False,  # Iteration 2: Reject disk
                                     True]   # Iteration 3: Accept disk
    console_prompt_instance.call.side_effect = [None,  # Iter 1: No disk
                                                True,  # Iter 2: Unmount
                                                True]  # Iter 2: Check disk
    
    # Execute
    result = gd.get_disk(console_mock)
    
    # Verify first loop call
    put_script_banner_mock.assert_called_once_with(console_mock, "get_disk")

    # Verify second loop calls
    confirm_disk_mock.assert_any_call(console_mock, "sda1")
    unmount_disk_mock.assert_called_once_with("sda1")
    
    # Verify iteration 3 calls
    select_disk_mock.assert_called_once_with(console_mock, mock_disks)
    confirm_disk_mock.assert_any_call(console_mock, "sda2")

    # Verify call counts and result
    assert get_disks_mock.call_count == 3
    assert console_prompt_class.call_count == 3
    assert confirm_disk_mock.call_count == 2
    assert result == "sda2"


# Test getDisks
def test_get_disks(lsblk_mock, table_mocks):
    # Setup return value for mock `lsblk` command
    lsblk_mock.return_value = ("NAME       VENDOR              SIZE\n" + 
                               "sda        Seagate             500G\n" + 
                               "sdb        Western Digital     1T\n" + 
                               "sdc        Toshiba             2T\n" + 
                               "nvme0n1    Samsung             1.5T\n" + 
                               "sr0        ASUS                1024M")
    
    # Unpack Table mocks
    table_class, table_instance = table_mocks

    # Execute
    result = gd.get_disks()

    # Verify
    lsblk_mock.assert_called_once_with(columns=["NAME", "VENDOR", "SIZE"], 
                                       show_dependents=False)
    table_class.assert_called_once_with(title="connected devices", 
                                        table_string=lsblk_mock.return_value, 
                                        rjust_columns="SIZE")
    table_instance.filter_startswith.assert_called_once_with("NAME", "sd")
    assert result == table_instance


# Test selectDisk
def test_select_disk(mocker, console_mock):
    # Setup mock Table
    mock_table = mocker.Mock(spec=Table)

    # Setup mock Menu
    mock_menu = mocker.patch("get_disk.Menu")
    menu_instance = mock_menu.return_value
    menu_instance.get_selection.return_value = "sda"

    # Execute
    result = gd.select_disk(console_mock, mock_table)

    # Verify
    mock_menu.assert_called_once_with(mock_table)
    menu_instance.run.assert_called_once_with(console_mock)
    assert result == "sda"