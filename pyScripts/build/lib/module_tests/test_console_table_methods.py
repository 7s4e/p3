import pytest
from unittest.mock import call
from blessed import Terminal
from modules import ConsoleTable, Table


ROW_ENDS = {"top": ("<blue>╔</blue>", "<blue>╗</blue>", ""), 
            "inr": ("<blue>╟</blue>", "<blue>╢</blue>", ""), 
            "btm": ("<blue>╚</blue>", "<blue>╝</blue>", ""), 
            "txt": ("<blue>║</blue>", "<blue>║</blue>", " ")}

ROW_CONTENT = {
    "raw": {
        "top": "═", 
        "inr": "─", 
        "btm": "═", 
        "ttl": "Data Title", 
        "hdg": {"COL A": "COL A", "COL B": "COL B"}, 
        "rec": {"COL A": "abc", "COL B": "123"}
    }, 
    "prc": {
        "top": "<blue>══════════════</blue>", 
        "inr": "<blue>──────────────</blue>", 
        "btm": "<blue>══════════════</blue>", 
        "ttl": ["<reverse> Data Title </reverse>"], 
        "hdg": ["<underline>COL A</underline>", 
                "<underline>COL B</underline>"], 
        "rec": ["abc  ", "  123"]
    }, 
    "fin": {
        "top": "<blue>╔</blue><blue>══════════════</blue><blue>╗</blue>\n", 
        "inr": "<blue>╟</blue><blue>──────────────</blue><blue>╢</blue>\n", 
        "btm": "<blue>╚</blue><blue>══════════════</blue><blue>╝</blue>\n", 
        "ttl": "<blue>║</blue> <reverse> Data " + 
                "Title </reverse> <blue>║</blue>\n", 
        "hdg": "<blue>║</blue> <underline>COL A</underline>  " + 
                "<underline>COL B</underline> <blue>║</blue>\n", 
        "rec": "<blue>║</blue> abc      123 <blue>║</blue>\n"
    }
}


@pytest.fixture
def mock_console(mocker):
    mck = mocker.Mock(spec=Terminal)
    mck.blue = mocker.Mock(side_effect=lambda x: f"<blue>{x}</blue>")
    mck.reverse = mocker.Mock(side_effect=lambda x: (f"<reverse>{x}" + 
                                                     "</reverse>"))
    mck.underline = mocker.Mock(side_effect=lambda x: (f"<underline>{x}" + 
                                                       "</underline>"))
    return mck

@pytest.fixture
def mock_data(mocker):
    mck = mocker.Mock(spec=Table)
    mck.get_title.return_value = ROW_CONTENT["raw"]["ttl"]
    mck.get_headings.return_value = ROW_CONTENT["raw"]["hdg"]
    mck.get_record.return_value = ROW_CONTENT["raw"]["rec"]
    mck.get_rjust_columns.return_value = {"COL B"}
    mck.get_column_widths.return_value = {"COL A": 5, "COL B": 5}
    mck.get_table_width.return_value = 12
    return mck

@pytest.fixture
def table_inst(mock_data, mock_console):
    instnc = ConsoleTable(mock_data)
    instnc._trm = mock_console
    instnc._column_widths = mock_data.get_column_widths.return_value
    instnc._table_width = mock_data.get_table_width.return_value
    return instnc


# Test display
@pytest.mark.parametrize("record_count", [0, 1, 9])
def test_display(mocker, mock_data, record_count):
    # Setup
    con_tbl = ConsoleTable(mock_data)
    mocker.patch.object(con_tbl, "_set_dimensions")
    mocker.patch.object(con_tbl, "_draw_table")
    mocker.patch.object(con_tbl._data, "count_records", 
                        return_value=record_count)

    # Execute
    con_tbl.display()

    # Verify
    con_tbl._set_dimensions.assert_called_once()
    con_tbl._data.count_records.assert_called_once()
    con_tbl._draw_table.assert_called_once_with(record_count)


# Test drawRow
@pytest.mark.parametrize(
    "row_type, ends_in, raw_in, proc_in, record_idx, is_line_type, exp_out",
    [
        # Test case 1: Top border line
        (
            "top", 
            ROW_ENDS["top"], 
            ROW_CONTENT["raw"]["top"], 
            ROW_CONTENT["prc"]["top"], 
            None, 
            True, 
            ROW_CONTENT["fin"]["top"]
        ), 
        # Test case 2: Inner border line
        (
            "inner", 
            ROW_ENDS["inr"], 
            ROW_CONTENT["raw"]["inr"], 
            ROW_CONTENT["prc"]["inr"], 
            None, 
            True, 
            ROW_CONTENT["fin"]["inr"]
        ), 
        # Test case 3: Bottom border line
        (
            "bottom", 
            ROW_ENDS["btm"], 
            ROW_CONTENT["raw"]["btm"], 
            ROW_CONTENT["prc"]["btm"], 
            None, 
            True, 
            ROW_CONTENT["fin"]["btm"]
        ), 
        # Test case 4: Title row
        (
            "title", 
            ROW_ENDS["txt"], 
            ROW_CONTENT["raw"]["ttl"], 
            ROW_CONTENT["prc"]["ttl"], 
            None, 
            False, 
            ROW_CONTENT["fin"]["ttl"]
        ), 
        # Test case 5: Headings row
        (
            "headings", 
            ROW_ENDS["txt"], 
            ROW_CONTENT["raw"]["hdg"], 
            ROW_CONTENT["prc"]["hdg"], 
            None, 
            False, 
            ROW_CONTENT["fin"]["hdg"]
        ), 
        # Test case 6: Record rows
        (
            "record", 
            ROW_ENDS["txt"], 
            ROW_CONTENT["raw"]["rec"], 
            ROW_CONTENT["prc"]["rec"], 
            0, 
            False, 
            ROW_CONTENT["fin"]["rec"]
        )
    ]
)
def test_draw_row(mocker, table_inst, mock_data, row_type, ends_in, raw_in, 
                  proc_in, record_idx, is_line_type, exp_out, capfd):
    # Setup mock methods
    mocker.patch.object(table_inst, "_get_row_ends", return_value=ends_in)
    mocker.patch.object(table_inst, "_get_row_content", return_value=raw_in)
    mocker.patch.object(table_inst, "_process_row_content", 
                        return_value=proc_in)
    
    # Setup attribute and method argument
    table_inst._margin_size = 0
    rjust_col = (mock_data.get_rjust_columns.return_value 
                 if row_type == "record" else {})

    # Execute
    table_inst._draw_row(row_type, record_idx)
    out, err = capfd.readouterr()

    # Verify method calls
    if row_type == "record":
        table_inst._data.get_rjust_columns.assert_called_once()
    table_inst._get_row_ends.assert_called_once_with(row_type, is_line_type)
    if row_type in ["title", "headings", "record"]:
        table_inst._get_row_content.assert_called_once_with(row_type, 
                                                            record_idx)
        table_inst._process_row_content.assert_called_once_with(row_type, 
                                                                raw_in, 
                                                                rjust_col)
    
    # Verify output    
    assert out == exp_out
    assert err == ""


# Test drawTable
@pytest.mark.parametrize("record_count", [0, 1, 9])
def test_draw_table(mocker, table_inst, record_count):
    # Setup
    mocker.patch.object(table_inst, "_draw_row")

    # Execute
    table_inst._draw_table(record_count)

    # Verify
    exp_calls = [call("top"), 
                 call("title"), 
                 call("inner"), 
                 call("headings"), 
                 *[call("record", i) for i in range(record_count)], 
                 call("bottom")]
    table_inst._draw_row.assert_has_calls(exp_calls)
    assert table_inst._draw_row.call_count == len(exp_calls)


# Test getRowContent
@pytest.mark.parametrize(
    "row_type, record_idx", 
    [
        ("title", None),     # Test case 1: Title
        ("headings", None),  # Test case 2: Headings
        ("record", 0)        # Test case 3: Record
    ]
)
def test_get_row_content(table_inst, mock_data, row_type, record_idx):
    # Execute
    result = table_inst._get_row_content(row_type, record_idx)

    # Verify
    match row_type:
        case "title":
            table_inst._data.get_title.assert_called_once()
            assert result == mock_data.get_title.return_value
        case "headings":
            table_inst._data.get_headings.assert_called_once()
            assert result == mock_data.get_headings.return_value
        case "record":
            table_inst._data.get_record.assert_called_once_with(record_idx)
            assert result == mock_data.get_record.return_value


# Test getRowEnds
@pytest.mark.parametrize(
    "row_type, is_line_type, expected", 
    [
        # Test case 1: Top line
        ("top", True, ROW_ENDS["top"]), 

        # Test case 2: Inner line
        ("inner", True, ROW_ENDS["inr"]), 

        # Test case 3: Bottom line
        ("bottom", True, ROW_ENDS["btm"]), 

        # Test case 4: Text row
        ("text", False, ROW_ENDS["txt"])
    ]
)
def test_get_row_ends(table_inst, row_type, is_line_type, expected):
    # Execute
    result = table_inst._get_row_ends(row_type, is_line_type)

    # Verify
    assert result == expected


# Test processRowContent
@pytest.mark.parametrize(
    "row_type, expected", 
    [
        # Test case 1: Title row
        ("title", ROW_CONTENT["prc"]["ttl"]), 

        # Test case 2: Headings row
        ("headings", ROW_CONTENT["prc"]["hdg"]), 

        # Test case 3: Record row
        ("record", ROW_CONTENT["prc"]["rec"])
    ]
)
def test_process_row_content(mock_data, table_inst, row_type, expected):
    # Setup
    match row_type:
        case "title":
            content = mock_data.get_title.return_value
        case "headings":
            content = mock_data.get_headings.return_value
        case "record":
            content = mock_data.get_record.return_value
    rjust_col = mock_data.get_rjust_columns.return_value
    
    # Execute
    result = table_inst._process_row_content(row_type, content, rjust_col)

    # Verify
    assert result == expected


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
def test_set_dimensions(mock_console, mock_data, table_inst, term_wd, 
                        tbl_wds, col_wds, dply_wd):
    # Setup
    mock_console.width = term_wd
    mock_data.get_table_width.side_effect = tbl_wds
    mock_data.get_column_widths.return_value = col_wds

    # Execute
    table_inst._set_dimensions()

    # Verify function process
    assert table_inst._data.get_table_width.call_count == len(tbl_wds)
    resize_called = table_inst._data.resize_columns.call_count > 0
    if resize_called:
        table_inst._data.resize_columns.assert_called_once_with(dply_wd - 4)
    table_inst._data.get_column_widths.assert_called_once()

    # Verify function results
    assert table_inst._display_width == dply_wd
    assert table_inst._margin_size == (term_wd - dply_wd) // 2
    assert table_inst._table_width == tbl_wds[-1]
    assert table_inst._column_widths == col_wds
