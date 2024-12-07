import pytest
from table import Table
from blessed import Terminal


@pytest.fixture
def table_instance():
    tbl_data = [{"First": "abc", "Second": "123"}, 
                {"First": "", "Second": "456"}, 
                {"First": "xyz", "Second": "789"}]
    title = "Mock Table"
    rj_col = "Second"
    return Table(table_data=tbl_data, title=title, rjust_columns=rj_col)


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
def test_filter_nonempty(table_instance, filter_key, exp_dataset, exp_count):
    table_instance.filter_nonempty(filter_key)
    assert table_instance._dataset == exp_dataset
    assert table_instance._records_count == exp_count


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
def test_filter_startswith(table_instance, filter_key, value_prefix, 
                           exp_dataset, exp_count):
    table_instance.filter_startswith(filter_key, value_prefix)
    assert table_instance._dataset == exp_dataset
    assert table_instance._records_count == exp_count


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
def test_resize_columns(table_instance, width_limit, exp_col_widths, 
                        exp_tbl_width):
    table_instance._column_widths = {"FIRST": 5, "SECOND": 6}
    table_instance._table_width = 13
    table_instance.resize_columns(width_limit)
    assert table_instance._column_widths == exp_col_widths
    assert table_instance._table_width == exp_tbl_width


"""Display Table Methods"""
# Test numberRecords
def test_number_records(table_instance):
    table_instance._number_records()
    assert table_instance._dataset == [{"#": 1, "FIRST": "abc", 
                                        "SECOND": "123"}, 
                                       {"#": 2, "FIRST": "", 
                                        "SECOND": "456"}, 
                                       {"#": 3, "FIRST": "xyz", 
                                        "SECOND": "789"}]
    assert table_instance._right_justified_columns == {"#", "SECOND"}


# Test calculateWidths
def test_calculate_widths(table_instance):
    table_instance._calculate_widths()
    assert table_instance._column_widths == {"FIRST": 5, "SECOND": 6}
    assert table_instance._table_width == 13


# Test putTable
@pytest.mark.parametrize(
    "menu_flag, record_number",
    [
        # Test case 1: Table is a menu
        (True, 3),

        # Test case 2: Table is not a menu
        (False, "")
    ]
)
def test_put_table(mocker, table_instance, menu_flag, record_number):
    # Setup console mocks
    mock_console = mocker.Mock(spec=Terminal)
    mock_console_table = mocker.patch("table.ConsoleTable")
    display_mock = mock_console_table.return_value.display

    # Execute
    table_instance.put_table(console=mock_console, is_menu=menu_flag)
    
    # Verify numberRecords called, pending menuFlag
    assert table_instance._dataset[2].get("#", "") == record_number

    # Verify calculateWidth called
    assert hasattr(table_instance, "_column_widths")
    assert hasattr(table_instance, "_table_width")

    # Verify ConsoleTable called
    mock_console_table.assert_called_once_with(table_instance)
    display_mock.assert_called_once_with(mock_console)


"""Getter Methods"""
# Test countRecords, getColumnWidths, getHeadings, getRjustColumns, 
#   getTableWidth, and getTitle
def test_basic_getters(table_instance):
    # Setup
    table_instance._calculate_widths()

    # Execute
    records_count = table_instance.count_records()
    column_widths = table_instance.get_column_widths()
    headings = table_instance.get_headings()
    rjust_cols = table_instance.get_rjust_columns()
    table_width = table_instance.get_table_width()
    title = table_instance.get_title()

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
def test_get_record(table_instance, index_in, exp_record, exception):
    # Execute with exception
    if exception:
        with pytest.raises(IndexError):
            table_instance.get_record(index_in)
    
    # Execute without acception
    else:
        result = table_instance.get_record(index_in)
        assert result == exp_record