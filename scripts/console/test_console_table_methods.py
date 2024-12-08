import pytest
from blessed import Terminal
from console_table import ConsoleTable
from table import Table


#7 Test display
#5 Test drawRow
#6 Test drawTable
#2 Test getRowEnds
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
def test_set_dimensions(mocker, term_wd, tbl_wds, col_wds, dply_wd):
    # Setup console mock
    mock_console = mocker.Mock(spec=Terminal)
    mock_console.width = term_wd
    
    # Setup data mock
    mock_data = mocker.Mock(spec=Table)
    mock_data.get_table_width.side_effect = tbl_wds
    mock_data.get_column_widths.return_value = col_wds

    # Setup ConsoleTable instance
    console_table = ConsoleTable(mock_data)
    console_table._con = mock_console

    # Execute
    console_table._set_dimensions()

    # Verify function results
    assert console_table._display_width == dply_wd
    assert console_table._margin_size == (term_wd - dply_wd) // 2
    assert console_table._table_width == tbl_wds[-1]
    assert console_table._column_widths == col_wds
    
    # Verify function process
    assert console_table._data.get_table_width.call_count == len(tbl_wds)
    resize_called = console_table._data.resize_columns.call_count > 0
    if resize_called:
        console_table._data.resize_columns.assert_called_once_with(dply_wd - 4)
    console_table._data.get_column_widths.assert_called_once()
