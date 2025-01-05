import pytest
from modules import Table


@pytest.fixture
def T_inst():
    tbl_data = [{"First": "abc", "Second": "123"}, 
                {"First": "", "Second": "456"}, 
                {"First": "xyz", "Second": "789"}]
    title = "Mock Table"
    rj_col = "Second"
    return Table(table_data=tbl_data, title=title, rjust_columns=rj_col)

@pytest.fixture
def T_wth_wds(T_inst):
    T_inst._col_wds = {"FIRST": 5, "SECOND": 6}
    T_inst._tbl_wd = 13
    return T_inst


"""Modify Table Methods"""
# Test filterNonempty
@pytest.mark.parametrize(
    "filter_key, exp_dataset, exp_count",
    [
        # Test case 1: Key present, record filtered
        (
            "First", 
            [{"FIRST": "abc", "SECOND": "123"}, 
             {"FIRST": "xyz", "SECOND": "789"}], 
            2
        ),
        # Test case 2: Key present, no record filtered
        (
            "Second", 
            [{"FIRST": "abc", "SECOND": "123"}, 
             {"FIRST": "", "SECOND": "456"}, 
             {"FIRST": "xyz", "SECOND": "789"}], 
            3
        ),
        # Test case 3: Key not present
        (
            "Third", 
            [{"FIRST": "abc", "SECOND": "123"}, 
             {"FIRST": "", "SECOND": "456"}, 
             {"FIRST": "xyz", "SECOND": "789"}], 
            3
        )
    ]
)
def test_filter_nonempty(T_inst, filter_key, exp_dataset, exp_count):
    # Execute
    T_inst.filter_nonempty(filter_key)

    # Verify
    assert T_inst._ds == exp_dataset
    assert T_inst._rec_ct == exp_count


# Test filterStartwith
@pytest.mark.parametrize(
    "filter_key, value_prefix, exp_dataset, exp_count",
    [
        # Test case 1: Key and prefix present
        (
            "First", 
            "xy", 
            [{"FIRST": "xyz", "SECOND": "789"}], 
            1
        ),
        # Test case 2: Key present but no prefix match
        (
            "First", 
            "qr", 
            [], 
            0
        ),
        # Test case 3: Key not present
        (
            "Third", 
            "no", 
            [], 
            0
        )
    ]
)
def test_filter_startswith(T_inst, filter_key, value_prefix, exp_dataset, 
                           exp_count):
    # Execute
    T_inst.filter_startswith(filter_key, value_prefix)

    # Verify
    assert T_inst._ds == exp_dataset
    assert T_inst._rec_ct == exp_count


# Test resizeColumns
@pytest.mark.parametrize(
    "width_limit, exp_col_wds, exp_tbl_wd",
    [
        # Test case 1: Trim table width by 1
        (12, {"FIRST": 5, "SECOND": 5}, 12),

        # Test case 2: Trim table width by 2
        (11, {"FIRST": 4, "SECOND": 5}, 11),
    
        # Test case 3: Trim table width by 3
        (10, {"FIRST": 4, "SECOND": 4}, 10),
    
        # Test case 4: Trim table width by 4
        (9, {"FIRST": 3, "SECOND": 4}, 9),

        # Test case 5: Trim table width by 5
        (8, {"FIRST": 3, "SECOND": 3}, 8)
    ]
)
def test_resize_columns(T_wth_wds, width_limit, exp_col_wds, exp_tbl_wd):
    # Execute
    T_wth_wds.resize_columns(width_limit)

    # Verify
    assert T_wth_wds._col_wds == exp_col_wds
    assert T_wth_wds._tbl_wd == exp_tbl_wd


"""Display Table Methods"""
# Test putTable
@pytest.mark.parametrize(
    "menu_flag, record_number",
    [
        # Test case 1: Table is a menu
        (True, 3),

        # Test case 2: Table is not a menu
        # (False, "")
    ]
)
def test_put_table(mocker, T_wth_wds, menu_flag, record_number):
    # Setup patches
    mocker.patch.object(T_wth_wds, "_num_recs", return_value=record_number)
    mocker.patch.object(T_wth_wds, "_set_wds")
    mck_CT = mocker.patch("modules.table.ConsoleTable")
    mocker.patch.object(mck_CT.return_value, "display")

    # Execute
    T_wth_wds.put_table(menu_flag)

    # Verify calls
    if menu_flag:
        T_wth_wds._num_recs.assert_called_once()
    T_wth_wds._set_wds.assert_called_once()
    mck_CT.assert_called_once_with(T_wth_wds)
    mck_CT.return_value.display.assert_called_once()


# Test setWidths
def test_set_wds(T_inst):
    # Execute
    T_inst._set_wds()

    # Verify
    assert T_inst._col_wds == {"FIRST": 5, "SECOND": 6}
    assert T_inst._tbl_wd == 13


# Test numberRecords
def test_num_recs(T_inst):
    # Execute
    T_inst._num_recs()

    # Verify
    assert T_inst._ds == [{"#": 1, "FIRST": "abc", "SECOND": "123"}, 
                          {"#": 2, "FIRST": "", "SECOND": "456"}, 
                          {"#": 3, "FIRST": "xyz", "SECOND": "789"}]
    assert T_inst._rj_cols == {"#", "SECOND"}


"""Getter Methods"""
# Test countRecords, getColumnWidths, getHeadings, getRjustColumns, 
#   getTableWidth, and getTitle
def test_basic_getters(T_inst):
    # Setup
    T_inst._set_wds()

    # Execute
    records_count = T_inst.count_records()
    column_widths = T_inst.get_column_widths()
    headings = T_inst.get_headings()
    rjust_cols = T_inst.get_rjust_columns()
    table_width = T_inst.get_table_width()
    title = T_inst.get_title()

    # Verify
    assert records_count == 3
    assert column_widths == {"FIRST": 5, "SECOND": 6}
    assert headings == {"FIRST": "FIRST", "SECOND": "SECOND"}
    assert rjust_cols == {"SECOND"}
    assert table_width == 13
    assert title == "MOCK TABLE"


# Test getRecords
@pytest.mark.parametrize(
    "index_in, exp_record, exception", 
    [
        # Test case 1: First record
        (0, {"FIRST": "abc", "SECOND": "123"}, False), 

        # Test case 2: Middle record
        (1, {"FIRST": "", "SECOND": "456"}, False), 

        # Test case 3: Last record
        (2, {"FIRST": "xyz", "SECOND": "789"}, False), 

        # Test case 4: Above range
        (3, {"FIRST": "", "SECOND": ""}, True), 

        # Test case 5: Below range
        (-1, {"FIRST": "", "SECOND": ""}, True)
    ]
)
def test_get_record(T_inst, index_in, exp_record, exception):
    # Execute with exception
    if exception:
        with pytest.raises(IndexError):
            T_inst.get_record(index_in)
    
    # Execute without acception
    else:
        result = T_inst.get_record(index_in)
        assert result == exp_record
