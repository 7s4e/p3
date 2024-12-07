import pytest
from blessed import Terminal
from table import Table
import get_disk as gd


# Test getDisks
def test_get_disks(mocker):
    # Setup mock `lsblk` command
    lsblk_mock = mocker.patch("get_disk.cmd.list_block_devices")
    lsblk_mock.return_value = ("NAME       VENDOR              SIZE\n" + 
                               "sda        Seagate             500G\n" + 
                               "sdb        Western Digital     1T\n" + 
                               "sdc        Toshiba             2T\n" + 
                               "nvme0n1    Samsung             1.5T\n" + 
                               "sr0        ASUS                1024M")
    
    # Setup mock Table
    mock_table = mocker.patch("get_disk.Table")
    mock_instance = mock_table.return_value

    # Execute
    result = gd.get_disks()

    # Verify
    lsblk_mock.assert_called_once_with(columns=["NAME", "VENDOR", "SIZE"], 
                                       show_dependents=False)
    mock_table.assert_called_once_with(title="connected devices", 
                                       table_string=lsblk_mock.return_value, 
                                       rjust_columns="SIZE")
    mock_instance.filter_startswith.assert_called_once_with("NAME", "sd")
    assert result == mock_instance


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