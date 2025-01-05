import pytest
from functools import partial
from modules import Table


# Tests parameters for findBoundaries and getSlice
PARAMS = [
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


@pytest.fixture
def mck_T(mocker):
    mck = mocker.Mock(spec=Table)
    for name in ["_add_rj_col_lbl", "_cap_keys", "_fnd_bnds", "_fnd_col_pos", 
                 "_get_slc", "_rd_tbl"]:
        method = getattr(mck, name)
        method.side_effect = partial(getattr(Table, name), mck)
    return mck


# Test addRjustColLabel
@pytest.mark.parametrize(
    "initial_set, label_in, exp_labels", 
    [
        # Test case 1: Single string label
        (set(), "Column1", {"COLUMN1"}), 

        # Test case 2: Adding a list of labels
        (set(), ["Column1", "Column2"], {"COLUMN1", "COLUMN2"}), 
        
        # Test case 3: Adding a set of labels
        (set(), {"Column1", "Column3"}, {"COLUMN1", "COLUMN3"}), 
        
        # Test case 4: Adding a label that already exists
        ({"COLUMN1"}, "Column1", {"COLUMN1"}), 
        
        # Test case 5: Adding a mix of existing and new labels
        ({"COLUMN1"}, ["Column1", "Column4"], {"COLUMN1", "COLUMN4"}), 
    ]
)
def test_add_rj_col_lbl(mck_T, initial_set, label_in, exp_labels):
    # Setup
    mck_T._rj_cols = initial_set

    # Execute
    mck_T._add_rj_col_lbl(label_in)

    # Verify
    assert mck_T._rj_cols == exp_labels


# Test capitalizeKeys
@pytest.mark.parametrize("data_input, exp_dataset, exp_count",
    [
        # Test case 1: Simple case with one dictionary
        (
            [{"key1": "value1", "key2": "value2"}],
            [{"KEY1": "value1", "KEY2": "value2"}],
            1
        ), 
        # Test case 2: Multiple dictionaries with mixed keys
        (
            [{"key1": "value1"}, {"Key2": "value2"}],
            [{"KEY1": "value1"}, {"KEY2": "value2"}],
            2
        ), 
        # Test case 3: Empty list
        ([], [], 0),

        # Test case 4: Empty dictionaries
        ([{}], [{}], 1), 

        # Test case 5: Special characters and numbers in keys
        (
            [{"k3y!": "v@lue", "123": "456"}],
            [{"K3Y!": "v@lue", "123": "456"}],
            1
        )
    ]
)
def test_cap_keys(mck_T, data_input, exp_dataset, exp_count):
    # Execute
    mck_T._cap_keys(data_input)

    # Verify
    assert mck_T._ds == exp_dataset
    assert mck_T._rec_ct == exp_count


# Test findBoundaries
@pytest.mark.parametrize("col_idx, pos_list, line, exp_boundaries, _", 
                         PARAMS)
def test_fnd_bnds(mck_T, col_idx, pos_list, line, exp_boundaries, _):
    # Execute
    act_start, act_end = mck_T._fnd_bnds(col_idx, pos_list, line)
    
    # Verify
    assert act_start == exp_boundaries[0]
    assert act_end == exp_boundaries[1]


# Test findColumnPositions
@pytest.mark.parametrize(
    "header_ln, keys, exp_out",
    [
        # Test case 1: All keys found
        ("Name Age Location", ["Name", "Age", "Location"], [0, 5, 9]),

        # Test case 2: Keys with varying positions
        ("ID Name Dept", ["ID", "Name"], [0, 3]),

        # Test case 3: Single key
        ("Header1 Header2 Header3", ["Header2"], [8]),

        # Test case 4: No keys to search
        ("Column1 Column2 Column3", [], []),

        # Test case 5: Duplicate keys
        ("A B A C", ["A", "C"], [0, 6])
    ]
)
def test_fnd_col_pos(mck_T, header_ln, keys, exp_out):
    # Execute
    act_out = mck_T._fnd_col_pos(header_ln, keys)
    
    # Verify
    assert act_out == exp_out


# Test getSlice
@pytest.mark.parametrize("col_idx, pos_list, line, _, exp_slice", PARAMS)
def test_get_slice(mck_T, col_idx, pos_list, line, _, exp_slice):
    # Execute
    act_out = mck_T._get_slc(col_idx, pos_list, line)

    # Verify
    assert act_out == exp_slice


# Test readTable
@pytest.mark.parametrize(
    "table_string, exp_dataset, exp_count",
    [
        # Test case 1: Simple table with two columns
        (
            "Name Age\nJohn 25\nJane 30\n", 
            [{'NAME': 'John', 'AGE': '25'}, {'NAME': 'Jane', 'AGE': '30'}], 
            2
        ), 
        # Test case 2: Table with multiple columns and different lengths of data
        (
            "Name Age Location\nJohn 25 USA\nJane 30 Canada\n", 
            [{'NAME': 'John', 'AGE': '25', 'LOCATION': 'USA'}, 
             {'NAME': 'Jane', 'AGE': '30', 'LOCATION': 'Canada'}], 
            2
        ), 
        # Test case 3: Empty table
        ("Name Age\n", [], 0),
    
        # Test case 4: Table with extra spaces
        (
            "Name    Age\nJohn   25\nJane    30\n", 
            [{'NAME': 'John', 'AGE': '25'}, {'NAME': 'Jane', 'AGE': '30'}], 
            2
        )
    ]
)
def test_read_table(mck_T, table_string, exp_dataset, exp_count):
    # Execute
    mck_T._rd_tbl(table_string)
    
    # Verify
    assert mck_T._ds == exp_dataset
    assert mck_T._rec_ct == exp_count
