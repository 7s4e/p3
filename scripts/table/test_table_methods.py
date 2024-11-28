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
def test_filter_nonempty(mock_table, filter_key, exp_dataset, exp_count):
    mock_table.filter_nonempty(filter_key)
    assert mock_table._dataset == exp_dataset
    assert mock_table._records_count == exp_count


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
def test_filter_startswith(mock_table, filter_key, value_prefix, exp_dataset, 
                           exp_count):
    mock_table.filter_startswith(filter_key, value_prefix)
    assert mock_table._dataset == exp_dataset
    assert mock_table._records_count == exp_count


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
def test_resize_columns(mock_table, width_limit, exp_col_widths, exp_tbl_width):
    mock_table._column_widths = {"FIRST": 5, "SECOND": 6}
    mock_table._table_width = 13
    mock_table.resize_columns(width_limit)
    assert mock_table._column_widths == exp_col_widths
    assert mock_table._table_width == exp_tbl_width


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
