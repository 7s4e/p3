import pytest
import get_disk as gd


@pytest.fixture
def mock_lsblk(mocker):
    return mocker.patch("get_disk.cmd.list_block_devices")

@pytest.fixture
def mock_table(mocker):
    return mocker.patch("get_disk.Table")


# Test getDisks
def test_get_disks(mock_lsblk, mock_table):
    # Setup
    mock_lsblk.return_value = ("NAME       VENDOR              SIZE\n" + 
                               "sda        Seagate             500G\n" + 
                               "sdb        Western Digital     1T\n" + 
                               "sdc        Toshiba             2T\n" + 
                               "nvme0n1    Samsung             1.5T\n" + 
                               "sr0        ASUS                1024M")
    mock_table_instance = mock_table.return_value

    # Execute
    result = gd.get_disks()

    # Verify
    mock_lsblk.assert_called_once_with(columns=["NAME", "VENDOR", "SIZE"], 
                                       show_dependents=False)
    mock_table.assert_called_once_with(title="connected devices", 
                                       table_string=mock_lsblk.return_value, 
                                       rjust_columns="SIZE")
    mock_table_instance.filter_startswith.assert_called_once_with("NAME", 
                                                                  "sd")
    assert result == mock_table_instance
