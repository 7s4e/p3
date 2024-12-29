import pytest
import scripts.get_disk_scr as gd
from src import Table


@pytest.fixture
def con_prmpt_fxtrs(mocker):
    ptch = mocker.patch("scripts.get_disk_scr.ConsolePrompt")
    inst = ptch.return_value
    return {"patch": ptch, "instance": inst}

@pytest.fixture
def lsblk_mck(mocker):
    mck =  mocker.patch("scripts.get_disk_scr.cmd.list_block_devices")
    mck.return_value = "mock table string"
    return mck

@pytest.fixture
def mnu_fxtrs(mocker):
    ptch = mocker.patch("scripts.get_disk_scr.Menu")
    inst = ptch.return_value
    return {"patch": ptch, "instance": inst}

@pytest.fixture
def tbl_fxtrs(mocker):
    ptch = mocker.patch("scripts.get_disk_scr.Table")
    inst = ptch.return_value
    mck = mocker.Mock(spec=Table)
    return {"patch": ptch, "instance": inst, "mock": mck}


# Test confirmDisk
@pytest.mark.parametrize("user_response", [True, False])
def test_confirm_disk(lsblk_mck, tbl_fxtrs, con_prmpt_fxtrs, user_response):
    # Setup
    prompt = "Are you sure you want to select the disk 'sda'? (y/n) "
    tbl_str = lsblk_mck.return_value
    con_prmpt_fxtrs["instance"].call.return_value = user_response

    # Execute
    result = gd.confirm_disk("sda")
    
    # Verify lsblk call
    lsblk_mck.assert_called_once_with("sda", columns=["NAME", "TYPE", 
                                                      "FSTYPE", "LABEL", 
                                                      "MOUNTPOINTS"])
    
    # Verify Table calls
    tbl_fxtrs["patch"].assert_called_once_with(title="selected device", 
                                               table_string=tbl_str)
    tbl_fxtrs["instance"].put_table.assert_called_once()
    
    # Verify ConsolePrompt calls
    con_prmpt_fxtrs["patch"].assert_called_once_with(prompt, 
                                                     expect_keystroke=True, 
                                                     validate_bool=True)
    con_prmpt_fxtrs["instance"].call.assert_called_once()

    # Verify method return    
    assert result == user_response


# Test getDisks
def test_get_disks(lsblk_mck, tbl_fxtrs):
    # Setup
    tbl_str = lsblk_mck.return_value

    # Execute
    result = gd.get_disks()

    # Verify
    lsblk_mck.assert_called_once_with(columns=["NAME", "VENDOR", "SIZE"], 
                                      show_dependents=False)
    tbl_fxtrs["patch"].assert_called_once_with(title="connected devices", 
                                               table_string=tbl_str, 
                                               rjust_columns="SIZE")
    tbl_fxtrs["instance"].filter_startswith.assert_called_once_with("NAME", 
                                                                    "sd")
    assert result == tbl_fxtrs["instance"]


# Test selectDisk
def test_select_disk(mnu_fxtrs, tbl_fxtrs):
    # Setup
    mnu_fxtrs["instance"].get_selection.return_value = "sda"

    # Execute
    result = gd.select_disk(tbl_fxtrs["mock"])

    # Verify
    mnu_fxtrs["patch"].assert_called_once_with(tbl_fxtrs["mock"])
    mnu_fxtrs["instance"].run.assert_called_once()
    mnu_fxtrs["instance"].get_selection.assert_called_once_with("NAME")
    assert result == "sda"


# Test getDisk
def test_get_disk(mocker, tbl_fxtrs, con_prmpt_fxtrs):
    # Setup putScriptBanner mock
    mck_code = mocker.MagicMock()
    mck_code.co_name = "get_disk"
    mck_frame = mocker.MagicMock()
    mck_frame.f_code = mck_code
    currentframe_mck = mocker.patch("inspect.currentframe")
    currentframe_mck.return_value = mck_frame
    mck_con = mocker.patch("scripts.get_disk_scr.Console")

    # Setup getDisks mock and disks behavior
    gt_dsks_mck = mocker.patch("scripts.get_disk_scr.get_disks")
    gt_dsks_mck.return_value = tbl_fxtrs["mock"]
    tbl_fxtrs["mock"].count_records.side_effect = [0,  # Iter 1: 0 disks
                                                   1,  # Iter 2: 1 disk
                                                   2]  # Iter 3: 2 disks
    tbl_fxtrs["mock"].get_record.return_value = {"NAME": "sda1"}  # Iter 2

    # Setup selectDisk mock
    slct_dsk_mck = mocker.patch("scripts.get_disk_scr.select_disk")
    slct_dsk_mck.return_value = "sda2"  # Iter 3

    # Setup confirmDisk mock
    cfrm_dsk_mck = mocker.patch("scripts.get_disk_scr.confirm_disk")
    cfrm_dsk_mck.side_effect = [False,  # Iter 2: Reject disk
                                True]   # Iter 3: Accept disk
    
    # Setup unmountDisk mock
    umnt_dsk_mck = mocker.patch("scripts.get_disk_scr.cmd.unmount_disk")

    # Setup ConsolePrompt mock
    con_prmpt_fxtrs["instance"].call.side_effect = [None,  # Iter 1: No disk
                                                    True,  # Iter 2: Unmount
                                                    True]  # Iter 2: Check disk
    
    # Execute
    result = gd.get_disk()

    # Verify first iteration call
    mck_con.put_script_banner.called_once_with(currentframe_mck)
    
    # Verify second iteration calls
    cfrm_dsk_mck.assert_any_call("sda1")
    umnt_dsk_mck.assert_called_once_with("sda1")
    
    # Verify third iteration calls
    slct_dsk_mck.assert_called_once_with(tbl_fxtrs["mock"])
    cfrm_dsk_mck.assert_any_call("sda2")

    # Verify call counts and result
    assert gt_dsks_mck.call_count == 3
    assert con_prmpt_fxtrs["patch"].call_count == 3
    assert cfrm_dsk_mck.call_count == 2
    assert result == "sda2"
