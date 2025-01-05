import pytest
import scripts.get_disk_script as gd
from modules import Table


@pytest.fixture
def CP_fxtrs(mocker):
    ptch = mocker.patch("scripts.get_disk_script.ConsolePrompt")
    inst = ptch.return_value
    return {"patch": ptch, "instance": inst}

@pytest.fixture
def lsblk_mck(mocker):
    mck =  mocker.patch("scripts.get_disk_script.cmd.list_block_devices")
    mck.return_value = "mock table string"
    return mck

@pytest.fixture
def M_fxtrs(mocker):
    ptch = mocker.patch("scripts.get_disk_script.Menu")
    inst = ptch.return_value
    return {"patch": ptch, "instance": inst}

@pytest.fixture
def T_fxtrs(mocker):
    ptch = mocker.patch("scripts.get_disk_script.Table")
    inst = ptch.return_value
    mck = mocker.Mock(spec=Table)
    return {"patch": ptch, "instance": inst, "mock": mck}


# Test confirmDisk
@pytest.mark.parametrize("user_response", [True, False])
def test_confirm_disk(lsblk_mck, T_fxtrs, CP_fxtrs, user_response):
    # Setup
    prompt = "Are you sure you want to select the disk 'sda'? (y/n) "
    tbl_str = lsblk_mck.return_value
    CP_fxtrs["instance"].call.return_value = user_response

    # Execute
    result = gd.confirm_disk("sda")
    
    # Verify lsblk call
    lsblk_mck.assert_called_once_with("sda", columns=["NAME", "TYPE", 
                                                      "FSTYPE", "LABEL", 
                                                      "MOUNTPOINTS"])
    
    # Verify Table calls
    T_fxtrs["patch"].assert_called_once_with(title="selected device", 
                                             table_string=tbl_str)
    T_fxtrs["instance"].put_table.assert_called_once()
    
    # Verify ConsolePrompt calls
    CP_fxtrs["patch"].assert_called_once_with(prompt, expect_keystroke=True, 
                                              validate_bool=True)
    CP_fxtrs["instance"].call.assert_called_once()

    # Verify method return    
    assert result == user_response


# Test getDisks
def test_get_disks(lsblk_mck, T_fxtrs):
    # Setup
    tbl_str = lsblk_mck.return_value

    # Execute
    result = gd.get_disks()

    # Verify
    lsblk_mck.assert_called_once_with(columns=["NAME", "VENDOR", "SIZE"], 
                                      show_dependents=False)
    T_fxtrs["patch"].assert_called_once_with(title="connected devices", 
                                             table_string=tbl_str, 
                                             rjust_columns="SIZE")
    T_fxtrs["instance"].filter_startswith.assert_called_once_with("NAME", 
                                                                  "sd")
    assert result == T_fxtrs["instance"]


# Test selectDisk
def test_select_disk(M_fxtrs, T_fxtrs):
    # Setup
    M_fxtrs["instance"].get_selection.return_value = "sda"

    # Execute
    result = gd.select_disk(T_fxtrs["mock"])

    # Verify
    M_fxtrs["patch"].assert_called_once_with(T_fxtrs["mock"])
    M_fxtrs["instance"].run.assert_called_once()
    M_fxtrs["instance"].get_selection.assert_called_once_with("NAME")
    assert result == "sda"


# Test getDisk
def test_get_disk(mocker, T_fxtrs, CP_fxtrs):
    # Setup putScriptBanner mock
    mck_code = mocker.MagicMock()
    mck_code.co_name = "get_disk"
    mck_frame = mocker.MagicMock()
    mck_frame.f_code = mck_code
    cf_mck = mocker.patch("inspect.currentframe")
    cf_mck.return_value = mck_frame
    mck_con = mocker.patch("scripts.get_disk_script.Console")

    # Setup getDisks mock and disks behavior
    gd_mck = mocker.patch("scripts.get_disk_script.get_disks")
    gd_mck.return_value = T_fxtrs["mock"]
    T_fxtrs["mock"].count_records.side_effect = [0,  # Iter 1: 0 disks
                                                 1,  # Iter 2: 1 disk
                                                 2]  # Iter 3: 2 disks
    T_fxtrs["mock"].get_record.return_value = {"NAME": "sda1"}  # Iter 2

    # Setup selectDisk mock
    sd_mck = mocker.patch("scripts.get_disk_script.select_disk")
    sd_mck.return_value = "sda2"  # Iter 3

    # Setup confirmDisk mock
    cd_mck = mocker.patch("scripts.get_disk_script.confirm_disk")
    cd_mck.side_effect = [False,  # Iter 2: Reject disk
                          True]   # Iter 3: Accept disk
    
    # Setup unmountDisk mock
    ud_mck = mocker.patch("scripts.get_disk_script.cmd.unmount_disk")

    # Setup ConsolePrompt mock
    CP_fxtrs["instance"].call.side_effect = [None,  # Iter 1: No disk
                                             True,  # Iter 2: Unmount
                                             True]  # Iter 2: Check disk
    
    # Execute
    result = gd.get_disk()

    # Verify first iteration call
    mck_con.put_script_banner.called_once_with(cf_mck)
    
    # Verify second iteration calls
    cd_mck.assert_any_call("sda1")
    ud_mck.assert_called_once_with("sda1")
    
    # Verify third iteration calls
    sd_mck.assert_called_once_with(T_fxtrs["mock"])
    cd_mck.assert_any_call("sda2")

    # Verify call counts and result
    assert gd_mck.call_count == 3
    assert CP_fxtrs["patch"].call_count == 3
    assert cd_mck.call_count == 2
    assert result == "sda2"
