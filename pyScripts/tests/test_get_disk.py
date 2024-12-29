import pytest
import scripts.get_disk_scr as gd


@pytest.fixture
def con_prmpt_fxtrs(mocker):
    ptch = mocker.patch("scripts.get_disk_scr.ConsolePrompt")
    mck = ptch.return_value
    return ptch, mck

@pytest.fixture
def lsblk_mock(mocker):
    mck =  mocker.patch("scripts.get_disk_scr.cmd.list_block_devices")
    mck.return_value = "mock table string"
    return mck

@pytest.fixture
def table_fxtrs(mocker):
    ptch = mocker.patch("scripts.get_disk_scr.Table")
    mck = ptch.return_value
    return ptch, mck


# Test confirmDisk
@pytest.mark.parametrize("user_response", [True, False])
def test_confirm_disk(mocker, lsblk_mock, table_fxtrs, con_prmpt_fxtrs, 
                      user_response):
    # Setup argument
    prompt = "Are you sure you want to select the disk 'sda'? (y/n) "
    
    # Setup Table and ConsolePrompt mocks
    tbl_patch, tbl_mock = table_fxtrs
    mocker.patch.object(tbl_mock, "put_table")
    con_prmpt_patch, con_prmpt_mock = con_prmpt_fxtrs
    con_prmpt_mock.call.return_value = user_response

    # Execute
    result = gd.confirm_disk("sda")
    
    # Verify lsblk call
    lsblk_mock.assert_called_once_with("sda", columns=["NAME", "TYPE", 
                                                       "FSTYPE", "LABEL", 
                                                       "MOUNTPOINTS"])
    
    # Verify Table calls
    tbl_patch.assert_called_once_with(title="selected device", 
                                      table_string=lsblk_mock.return_value)
    tbl_mock.put_table.assert_called_once()
    
    # Verify ConsolePrompt calls
    con_prmpt_patch.assert_called_once_with(prompt, expect_keystroke=True, 
                                            validate_bool=True)
    con_prmpt_mock.call.assert_called_once()

    # Verify method return    
    assert result == user_response


# Test getDisks
def test_get_disks(lsblk_mock, table_fxtrs):
    # Setup
    tbl_patch, tbl_mock = table_fxtrs

    # Execute
    result = gd.get_disks()

    # Verify
    lsblk_mock.assert_called_once_with(columns=["NAME", "VENDOR", "SIZE"], 
                                       show_dependents=False)
    tbl_patch.assert_called_once_with(title="connected devices", 
                                      table_string=lsblk_mock.return_value, 
                                      rjust_columns="SIZE")
    tbl_mock.filter_startswith.assert_called_once_with("NAME", "sd")
    assert result == tbl_mock


# # # Test selectDisk
# # def test_select_disk(mocker, console_mock):
# #     # Setup mock Table
# #     mock_table = mocker.Mock(spec=Table)

# #     # Setup mock Menu
# #     mock_menu = mocker.patch("get_disk.Menu")
# #     menu_instance = mock_menu.return_value
# #     menu_instance.get_selection.return_value = "sda"

# #     # Execute
# #     result = gd.select_disk(console_mock, mock_table)

# #     # Verify
# #     mock_menu.assert_called_once_with(mock_table)
# #     menu_instance.run.assert_called_once_with(console_mock)
# #     assert result == "sda"


# # Test getDisk
# def test_get_disk(mocker, con_prmpt_fxtrs, console_mock):
#     # Setup mock dependencies
#     mock_disks = mocker.Mock(spec=Table)
#     confirm_disk_mock = mocker.patch("get_disk.confirm_disk")
#     get_disks_mock = mocker.patch("get_disk.get_disks")
#     put_script_banner_mock = mocker.patch("get_disk.con.put_script_banner")
#     select_disk_mock = mocker.patch("get_disk.select_disk")
#     unmount_disk_mock = mocker.patch("get_disk.cmd.unmount_disk")
#     con_prmpt_patch, con_prmpt_mock = con_prmpt_fxtrs

#     # Setup mock behavior
#     get_disks_mock.return_value = mock_disks
#     mock_disks.count_records.side_effect = [0,  # Iteration 1: No disks
#                                             1,  # Iteration 2: One disk
#                                             2]  # Iteration 3: Two disks
#     mock_disks.get_record.return_value = {"NAME": "sda1"}  # Iteration 2
#     select_disk_mock.return_value = "sda2"                 # Iteration 3
#     confirm_disk_mock.side_effect = [False,  # Iteration 2: Reject disk
#                                      True]   # Iteration 3: Accept disk
#     con_prmpt_mock.call.side_effect = [None,  # Iter 1: No disk
#                                                 True,  # Iter 2: Unmount
#                                                 True]  # Iter 2: Check disk
    
#     # Execute
#     result = gd.get_disk(console_mock)
    
#     # Verify first loop call
#     put_script_banner_mock.assert_called_once_with(console_mock, "get_disk")

#     # Verify second loop calls
#     confirm_disk_mock.assert_any_call(console_mock, "sda1")
#     unmount_disk_mock.assert_called_once_with("sda1")
    
#     # Verify iteration 3 calls
#     select_disk_mock.assert_called_once_with(console_mock, mock_disks)
#     confirm_disk_mock.assert_any_call(console_mock, "sda2")

#     # Verify call counts and result
#     assert get_disks_mock.call_count == 3
#     assert con_prmpt_patch.call_count == 3
#     assert confirm_disk_mock.call_count == 2
#     assert result == "sda2"
