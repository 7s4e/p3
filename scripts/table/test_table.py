import pytest
from unittest.mock import MagicMock
from functools import partial
from table import Table


@pytest.fixture
def mock_instance():
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
def test_capitalize_keys(mock_instance, data_input, exp_dataset, exp_count):
    # Setup
    mock_instance._dataset = []
    mock_instance._records_count = 0
    mock_instance._capitalize_keys.side_effect = partial(
        Table._capitalize_keys, mock_instance)

    # Execute
    mock_instance._capitalize_keys(data_input)

    # Verify
    assert mock_instance._dataset == exp_dataset
    assert mock_instance._records_count == exp_count


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
def test_find_column_positions(mock_instance, header_line, keys, 
                               exp_positions, exception):
    # Setup
    mock_instance._find_column_positions.side_effect = partial(
        Table._find_column_positions, mock_instance)

    # Execute and Verify
    if exception:
        with pytest.raises(exception, 
                           match="Column '.*' not found in header line."):
            mock_instance._find_column_positions(header_line, keys)
    else:
        result = mock_instance._find_column_positions(header_line, keys)
        assert result == exp_positions


# Tests parameters for findBoundaries and getSlice
params = [
    # Test case 1: Left-justified column
    (0, [0, 11, 15], "Name       Age Location", (0, 4), "Name"), 

    # Test case 2: Last column boundary case
    (2, [0, 11, 15], "Name       Age Location", (15, 23), "Location"), 

    # Test case 3: Positions applied to truncated line
    (2, [0, 11, 15], "Name", (4, 4), ""), 
    
    # Test case 4: Whitespace at start
    (1, [0, 11, 15], "Baby        6w Nursery", (12, 14), "6w"), 
    
    # Test case 5: No whitespace before start
    (1, [0, 11, 15], "Methusela 969y Genesis", (10, 14), "969y"), 
    
    # Test case 6: No whitespace before end
    (0, [0, 11, 15], "Methusela 969y Genesis", (0, 9), "Methusela"), 
    
    # Test case 7: Column with no content
    (0, [0, 11, 15], "                       ", (11, 11), ""), 
    
    # Test case 8: Edge case with empty line
    (0, [0, 11, 15], "", (0, 0), "")
]

# Test findBoundaries
@pytest.mark.parametrize("col_idx, pos_list, line, exp_boundaries, _", 
                         params)
def test_find_boundaries(mock_instance, col_idx, pos_list, line, 
                         exp_boundaries, _):
    # Setup
    mock_instance._find_boundaries.side_effect = partial(
        Table._find_boundaries, mock_instance)

    # Execute
    result_start, result_end = mock_instance._find_boundaries(col_idx, 
                                                              pos_list, line)

    # Verify
    assert result_start == exp_boundaries[0]
    assert result_end == exp_boundaries[1]

# Test getSlice
@pytest.mark.parametrize("col_idx, pos_list, line, _, exp_slice", params)
def test_get_slice(mock_instance, col_idx, pos_list, line, _, exp_slice):
    # Setup
    mock_instance._find_boundaries.side_effect = partial(
        Table._find_boundaries, mock_instance)
    mock_instance._get_slice.side_effect = partial(Table._get_slice, 
                                                   mock_instance)

    # Execute
    result = mock_instance._get_slice(col_idx, pos_list, line)

    # Verify
    assert result == exp_slice
