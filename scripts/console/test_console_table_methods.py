import pytest
from blessed import Terminal
from console_table import ConsoleTable
from table import Table


@pytest.fixture
def console_mock(mocker):
    mock = mocker.Mock(spec=Terminal)
    mock.blue = mocker.Mock(side_effect=lambda x: f"<blue>{x}</blue>")
    return mock

@pytest.fixture
def data_mock(mocker):
    return mocker.Mock(spec=Table)

@pytest.fixture
def con_tbl_inst(data_mock, console_mock):
    instance = ConsoleTable(data_mock)
    instance._con = console_mock
    return instance


#7 Test display
#5 Test drawRow
#6 Test drawTable


# Test getRowEnds
@pytest.mark.parametrize(
    "row_type, is_line_type, expected", 
    [
        # Test case 1: Top line
        ("top", True, ("<blue>╔</blue>", "<blue>╗</blue>", "")), 

        # Test case 2: Inner line
        ("inner", True, ("<blue>╟</blue>", "<blue>╢</blue>", "")), 

        # Test case 3: Bottom line
        ("bottom", True, ("<blue>╚</blue>", "<blue>╝</blue>", "")), 

        # Test case 4: Text row
        ("text", False, ("<blue>║</blue>", "<blue>║</blue>", " ")), 

    ]
)
def test_get_row_ends(con_tbl_inst, row_type, is_line_type, expected):
    # Execute
    result = con_tbl_inst._get_row_ends(row_type, is_line_type)

    # Verify
    assert result == expected


#3 Test getTextContent
#4 Test processTextContent


# Test setDimensions
@pytest.mark.parametrize(
    "term_wd, tbl_wds, col_wds, dply_wd", 
    [
        (99, [64], [20, 20, 20], 79),      # Test case 1: Wide terminal
        (59, [64, 55], [17, 17, 17], 59),  # Test case 2: Narrow terminal
        (79, [94, 75], [24, 24, 23], 79),  # Test case 3: Wide table
        (79, [34], [10, 10, 10], 79)       # Test case 4: Narrow table
    ]
)
def test_set_dimensions(console_mock, data_mock, con_tbl_inst, term_wd, 
                        tbl_wds, col_wds, dply_wd):
    # Setup
    console_mock.width = term_wd
    data_mock.get_table_width.side_effect = tbl_wds
    data_mock.get_column_widths.return_value = col_wds

    # Execute
    con_tbl_inst._set_dimensions()

    # Verify function results
    assert con_tbl_inst._display_width == dply_wd
    assert con_tbl_inst._margin_size == (term_wd - dply_wd) // 2
    assert con_tbl_inst._table_width == tbl_wds[-1]
    assert con_tbl_inst._column_widths == col_wds
    
    # Verify function process
    assert con_tbl_inst._data.get_table_width.call_count == len(tbl_wds)
    resize_called = con_tbl_inst._data.resize_columns.call_count > 0
    if resize_called:
        con_tbl_inst._data.resize_columns.assert_called_once_with(dply_wd - 4)
    con_tbl_inst._data.get_column_widths.assert_called_once()
