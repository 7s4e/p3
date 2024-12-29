import pytest
from src import Table


@pytest.fixture
def table_inst():
    tbl_data = [{"First": "abc", "Second": "123"}, 
                {"First": "", "Second": "456"}, 
                {"First": "xyz", "Second": "789"}]
    title = "Mock Table"
    rj_col = "Second"
    return Table(table_data=tbl_data, title=title, rjust_columns=rj_col)

@pytest.fixture
def tbl_inst_with_wds(table_inst):
    table_inst._column_widths = {"FIRST": 5, "SECOND": 6}
    table_inst._table_width = 13
    return table_inst


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
def test_filter_nonempty(table_inst, filter_key, exp_dataset, exp_count):
    # Execute
    table_inst.filter_nonempty(filter_key)

    # Verify
    assert table_inst._dataset == exp_dataset
    assert table_inst._records_count == exp_count


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
def test_filter_startswith(table_inst, filter_key, value_prefix, exp_dataset, 
                           exp_count):
    # Execute
    table_inst.filter_startswith(filter_key, value_prefix)

    # Verify
    assert table_inst._dataset == exp_dataset
    assert table_inst._records_count == exp_count


# Test resizeColumns
@pytest.mark.parametrize(
    "width_limit, exp_col_widths, exp_tbl_width",
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
def test_resize_columns(tbl_inst_with_wds, width_limit, exp_col_widths, 
                        exp_tbl_width):
    # Execute
    tbl_inst_with_wds.resize_columns(width_limit)

    # Verify
    assert tbl_inst_with_wds._column_widths == exp_col_widths
    assert tbl_inst_with_wds._table_width == exp_tbl_width


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
def test_put_table(mocker, tbl_inst_with_wds, menu_flag, record_number):
    # Setup patches
    mocker.patch.object(tbl_inst_with_wds, "_number_records", 
                        return_value=record_number)
    mocker.patch.object(tbl_inst_with_wds, "_calculate_widths")
    mock_con_tbl = mocker.patch("src.table.ConsoleTable")
    mocker.patch.object(mock_con_tbl.return_value, "display")

    # Execute
    tbl_inst_with_wds.put_table(is_menu=menu_flag)

    # Verify calls
    if menu_flag:
        tbl_inst_with_wds._number_records.assert_called_once()
    tbl_inst_with_wds._calculate_widths.assert_called_once()
    mock_con_tbl.assert_called_once_with(tbl_inst_with_wds)
    mock_con_tbl.return_value.display.assert_called_once()


# Test calculateWidths
def test_calculate_widths(table_inst):
    # Execute
    table_inst._calculate_widths()

    # Verify
    assert table_inst._column_widths == {"FIRST": 5, "SECOND": 6}
    assert table_inst._table_width == 13


# Test numberRecords
def test_number_records(table_inst):
    # Execute
    table_inst._number_records()

    # Verify
    assert table_inst._dataset == [{"#": 1, "FIRST": "abc", "SECOND": "123"}, 
                                   {"#": 2, "FIRST": "", "SECOND": "456"}, 
                                   {"#": 3, "FIRST": "xyz", "SECOND": "789"}]
    assert table_inst._right_justified_columns == {"#", "SECOND"}


"""Getter Methods"""
# Test countRecords, getColumnWidths, getHeadings, getRjustColumns, 
#   getTableWidth, and getTitle
def test_basic_getters(table_inst):
    # Setup
    table_inst._calculate_widths()

    # Execute
    records_count = table_inst.count_records()
    column_widths = table_inst.get_column_widths()
    headings = table_inst.get_headings()
    rjust_cols = table_inst.get_rjust_columns()
    table_width = table_inst.get_table_width()
    title = table_inst.get_title()

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
def test_get_record(table_inst, index_in, exp_record, exception):
    # Execute with exception
    if exception:
        with pytest.raises(IndexError):
            table_inst.get_record(index_in)
    
    # Execute without acception
    else:
        result = table_inst.get_record(index_in)
        assert result == exp_record
