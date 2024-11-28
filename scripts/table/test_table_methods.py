import pytest
from table import Table


@pytest.fixture
def mock_table(mocker):
    tbl_data = [{"First": "abc", "Second": "123"}, 
                {"First": "", "Second": "456"}, 
                {"First": "xyz", "Second": "789"}]
    title = "Mock Table"
    rj_col = "Second"
    return Table(table_data=tbl_data, title=title, rjust_columns=rj_col)


"""Modify Table Methods"""
# Test filterNonempty
@pytest.mark.parametrize("filter_key, exp_dataset, exp_count",
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
def test_filter_nonempty(mock_table, filter_key, exp_dataset, exp_count):
    mock_table.filter_nonempty(filter_key)
    assert mock_table._dataset == exp_dataset
    assert mock_table._records_count == exp_count


# # Test findColumnPositions
# @pytest.mark.parametrize(
#     "header_line, keys, exp_positions, exception",
#     [
#         # Test case 1: All keys found
#         ("Name Age Location", ["Name", "Age", "Location"], [0, 5, 9], None),

#         # Test case 2: Keys with varying positions
#         ("ID Name Dept", ["ID", "Name"], [0, 3], None),

#         # Test case 3: Single key
#         ("Header1 Header2 Header3", ["Header2"], [8], None),

#         # Test case 4: No keys to search
#         ("Column1 Column2 Column3", [], [], None),

#         # Test case 5: Duplicate keys
#         ("A B A C", ["A", "C"], [0, 6], None),

#         # Test case 6: Key not found
#         ("Col1 Col2 Col3", ["Col4"], None, ValueError),

#         # Test case 7: Mixed valid and invalid keys
#         ("X Y Z", ["X", "W"], None, ValueError),

#         # Test case 8: Empty header line
#         ("", ["Column"], None, ValueError)
#     ]
# )
# def test_find_column_positions(mock_table, header_line, keys, 
#                                exp_positions, exception):
#     if exception:
#         with pytest.raises(exception, 
#                            match="Column '.*' not found in header line."):
#             mock_table._find_column_positions(header_line, keys)
#     else:
#         result = mock_table._find_column_positions(header_line, keys)
#         assert result == exp_positions


# # Tests parameters for findBoundaries and getSlice
# params = [
#     # Test case 1: Left-justified column
#     (0, [0, 11, 15], "Name       Age Location", (0, 4), "Name"), 

#     # Test case 2: Last column boundary case
#     (2, [0, 11, 15], "Name       Age Location", (15, 23), "Location"), 

#     # Test case 3: Positions applied to truncated line
#     (2, [0, 11, 15], "Name", (4, 4), ""), 
    
#     # Test case 4: Whitespace at start
#     (1, [0, 11, 15], "Baby        6w Nursery", (12, 14), "6w"), 
    
#     # Test case 5: No whitespace before start
#     (1, [0, 11, 15], "Methusela 969y Genesis", (10, 14), "969y"), 
    
#     # Test case 6: No whitespace before end
#     (0, [0, 11, 15], "Methusela 969y Genesis", (0, 9), "Methusela"), 
    
#     # Test case 7: Column with no content
#     (0, [0, 11, 15], "                       ", (11, 11), ""), 
    
#     # Test case 8: Edge case with empty line
#     (0, [0, 11, 15], "", (0, 0), "")
# ]

# # Test findBoundaries
# @pytest.mark.parametrize("col_idx, pos_list, line, exp_boundaries, _", 
#                          params)
# def test_find_boundaries(mock_table, col_idx, pos_list, line, 
#                          exp_boundaries, _):
#     result_start, result_end = mock_table._find_boundaries(col_idx, 
#                                                               pos_list, line)
#     assert result_start == exp_boundaries[0]
#     assert result_end == exp_boundaries[1]

# # Test getSlice
# @pytest.mark.parametrize("col_idx, pos_list, line, _, exp_slice", params)
# def test_get_slice(mock_table, col_idx, pos_list, line, _, exp_slice):
#     result = mock_table._get_slice(col_idx, pos_list, line)
#     assert result == exp_slice


# # Test readTable
# @pytest.mark.parametrize(
#     "table_string, exp_dataset, exp_count",
#     [
#         # Test case 1: Simple table with two columns
#         (
#             "Name Age\nJohn 25\nJane 30\n", 
#             [{'NAME': 'John', 'AGE': '25'}, {'NAME': 'Jane', 'AGE': '30'}], 
#             2
#         ),

#         # Test case 2: Table with multiple columns and different lengths of data
#         (
#             "Name Age Location\nJohn 25 USA\nJane 30 Canada\n", 
#             [{'NAME': 'John', 'AGE': '25', 'LOCATION': 'USA'}, 
#              {'NAME': 'Jane', 'AGE': '30', 'LOCATION': 'Canada'}], 
#             2
#         ),
    
#         # Test case 3: Empty table
#         (
#             "Name Age\n", 
#             [], 
#             0
#         ),
    
#         # Test case 4: Table with extra spaces
#         (
#             "Name    Age\nJohn   25\nJane    30\n", 
#             [{'NAME': 'John', 'AGE': '25'}, {'NAME': 'Jane', 'AGE': '30'}], 
#             2
#         )
#     ]
# )
# def test_read_table(mock_table, table_string, exp_dataset, exp_count):
#     mock_table._read_table(table_string)
#     assert mock_table._dataset == exp_dataset
#     assert mock_table._records_count == exp_count


# # Test addRjustColLabel
# @pytest.mark.parametrize(
#     "initial_set, label_input, exp_labels", 
#     [
#         # Test case 1: Single string label
#         (set(), "Column1", {"Column1"}), 

#         # Test case 2: Adding a list of labels
#         (set(), ["Column1", "Column2"], {"Column1", "Column2"}), 
        
#         # Test case 3: Adding a set of labels
#         (set(), {"Column1", "Column3"}, {"Column1", "Column3"}), 
        
#         # Test case 4: Adding a label that already exists
#         ({"Column1"}, "Column1", {"Column1"}), 
        
#         # Test case 5: Adding a mix of existing and new labels
#         ({"Column1"}, ["Column1", "Column4"], {"Column1", "Column4"}), 
#     ]
# )
# def test_add_rjust_col_label(mock_table, initial_set, label_input, 
#                              exp_labels):
#     mock_table._right_justified_columns = initial_set
#     mock_table._add_rjust_col_label(label_input)
#     assert mock_table._right_justified_columns == exp_labels
