import pytest
from unittest.mock import MagicMock
from table import Table


@pytest.fixture
def mock_table():
    return MagicMock(spec=Table)


# Test capitalizeKeys
@pytest.mark.parametrize("data_input, exp_dataset, exp_count",
    [
        # Test case 1: Simple case with one dictionary
        (
            [{"key1": "value1", "key2": "value2"}],
            [{"KEY1": "value1", "KEY2": "value2"}],
            1,
        ),
        # Test case 2: Multiple dictionaries with mixed keys
        (
            [{"key1": "value1"}, {"Key2": "value2"}],
            [{"KEY1": "value1"}, {"KEY2": "value2"}],
            2,
        ),
        # Test case 3: Empty list
        (
            [],
            [],
            0,
        ),
        # Test case 4: Empty dictionaries
        (
            [{}],
            [{}],
            1,
        ),
        # Test case 5: Special characters and numbers in keys
        (
            [{"k3y!": "v@lue", "123": "456"}],
            [{"K3Y!": "v@lue", "123": "456"}],
            1,
        ),
    ],
)
def test_capitalize_keys(mock_table, data_input, exp_dataset, exp_count):
    # Setup
    mock_table._dataset = []
    mock_table._records_count = 0
    mock_table._capitalize_keys.side_effect = Table._capitalize_keys

    # Execute
    mock_table._capitalize_keys(mock_table, data_input)

    # Verify
    assert mock_table._dataset == exp_dataset
    assert mock_table._records_count == exp_count


# Test findColumnPositions
@pytest.mark.parametrize(
    "header_line, keys, exp_positions, exception",
    [
        # Test case 1: All keys found
        ("Name Age Location", ["Name", "Age", "Location"], [0, 5, 9], None),

        # Test case 2: Keys with varying positions
        ("ID Name Dept", ["ID", "Name"], [0, 3], None),

        # Test case 3: Single key
        ("Header1 Header2 Header3", ["Header2"], [8], None),

        # Test case 4: No keys to search
        ("Column1 Column2 Column3", [], [], None),

        # Test case 5: Duplicate keys
        ("A B A C", ["A", "C"], [0, 6], None),

        # Test case 6: Key not found
        ("Col1 Col2 Col3", ["Col4"], None, ValueError),

        # Test case 7: Mixed valid and invalid keys
        ("X Y Z", ["X", "W"], None, ValueError),

        # Test case 8: Empty header line
        ("", ["Column"], None, ValueError)
    ]
)
def test_find_column_positions(mock_table, header_line, keys, exp_positions, 
                               exception):
    # Setup
    mock_table._find_column_positions.side_effect = Table._find_column_positions

    # Execute and Verify
    if exception:
        with pytest.raises(exception, 
                           match="Column '.*' not found in header line."):
               mock_table._find_column_positions(mock_table, header_line, 
                                                 keys)
    else:
        result = mock_table._find_column_positions(mock_table, header_line, 
                                                   keys)
        assert result == exp_positions


# Test findBoundaries
@pytest.mark.parametrize(
    "column_idx, positions_list, line, exp_start, exp_end",
    [
        # Test case 1: No whitespace adjustment needed
        (0, [0, 5, 9], "Name Age Location", 0, 4), 

        # Test case 2: Last column boundary case
        (2, [0, 5, 9], "Name Age Location", 9, 17), 

        # Test case 3: Positions applied to truncated line
        (2, [0, 5, 9], "Name", 4, 4), 

        # Test case 4: Whitespace at the start of the column ('Age')
        (1, [0, 5, 11], "Name   Age Location", 7, 10), 

        # Test case 4: Column with trailing whitespace
        # (0, [0, 5, 10], "   Name Age Location", 3, 7),  # 'Name' column, leading whitespace adjusted

        # Test case 5: No whitespace adjustment needed, column index is last in list
        # (1, [0, 6, 12], "ID Name Location", 6, 10),  # 'Name' column

        # Test case 6: Column with no characters
        # (0, [0, 5, 10], "    ", 0, 0),  # 'ID' column (no content)

        # Test case 7: Edge case with empty line
        (0, [0, 5], "", 0, 0),  # Empty line, no columns
    ]
)
def test_find_boundaries(mock_table, column_idx, positions_list, line, 
                         exp_start, exp_end):
    # Setup
    mock_table._find_boundaries.side_effect = Table._find_boundaries

    # Execute
    result_start, result_end = mock_table._find_boundaries(mock_table, 
                                                           column_idx, 
                                                           positions_list, 
                                                           line)

    # Verify
    assert result_start == exp_start
    assert result_end == exp_end
