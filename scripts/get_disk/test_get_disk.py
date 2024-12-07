import pytest
from blessed import Terminal
from table import Table
import get_disk as gd


@pytest.fixture
def lsblk_mock(mocker):
    return mocker.patch("get_disk.cmd.list_block_devices")

@pytest.fixture
def table_mocks(mocker):
    mock_class = mocker.patch("get_disk.Table")
    mock_instance = mock_class.return_value
    return mock_class, mock_instance


# Test confirmDisk
def test_confirm_disk(mocker, lsblk_mock, table_mocks):
    # Setup arguments
    mock_prompt = "Are you sure you want to select the disk 'sda'? (y/n) "
    mock_console = mocker.Mock(spec=Terminal)
    lsblk_mock.return_value = ("NAME   TYPE  FSTYPE LABEL   MOUNTPOINTS\n" + 
                               "sda    disk\n" + 
                               "├─sda1 part  ext4   rootfs  /\n" + 
                               "├─sda2 part  swap           [SWAP]\n" + 
                               "└─sda3 part  ext4   data    /data")
    
    # Setup Table and ConsolePrompt mocks
    table_class, table_instance = table_mocks
    console_prompt_class = mocker.patch("get_disk.ConsolePrompt")
    console_prompt_instance = console_prompt_class.return_value
    console_prompt_instance.call.return_value = "y"

    # Execute
    result = gd.confirm_disk(mock_console, "sda")

    # Verify lsblk call
    lsblk_mock.assert_called_once_with("sda", columns=["NAME", "TYPE", 
                                                       "FSTYPE", "LABEL", 
                                                       "MOUNTPOINTS"])
    
    # Verify Table calls
    table_class.assert_called_once_with(title="selected device", 
                                        table_string=lsblk_mock.return_value)
    table_instance.put_table.assert_called_once_with(mock_console)
    
    # Verify ConsolePrompt calls
    console_prompt_class.assert_called_once_with(mock_prompt, 
                                                 expect_keystroke=True, 
                                                 validate_bool=True)
    console_prompt_instance.call.assert_called_once_with(mock_console)

    # Verify method return    
    assert result == "y"


# Test getDisks
def test_get_disks(mocker, lsblk_mock, table_mocks):
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
def test_select_disk(mocker):
    # Setup function arguments
    mock_console = mocker.Mock(spec=Terminal)
    mock_table = mocker.Mock(spec=Table)

    # Setup mock Menu
    mock_menu = mocker.patch("get_disk.Menu")
    menu_instance = mock_menu.return_value
    menu_instance.get_selection.return_value = "sda"

    # Execute
    result = gd.select_disk(mock_console, mock_table)

    # Verify
    mock_menu.assert_called_once_with(mock_table)
    menu_instance.run.assert_called_once_with(mock_console)
    assert result == "sda"