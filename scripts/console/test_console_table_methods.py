import pytest
from blessed import Terminal
from console_table import ConsoleTable
from table import Table


ROW_ENDS = {"top": ("<blue>╔</blue>", "<blue>╗</blue>", ""), 
            "inr": ("<blue>╟</blue>", "<blue>╢</blue>", ""), 
            "btm": ("<blue>╚</blue>", "<blue>╝</blue>", ""), 
            "txt": ("<blue>║</blue>", "<blue>║</blue>", " ")}

ROW_CONTENT = {
    "top": {"raw": "═", "prc": "<blue>══════════════</blue>"}, 
    "inr": {"raw": "─", "prc": "<blue>──────────────</blue>"}, 
    "btm": {"raw": "═", "prc": "<blue>══════════════</blue>"}, 
    "ttl": {"raw": "Data Title", "prc": ["<reverse> Data Title </reverse>"]}, 
    "hdg": {"raw": {"COL A": "COL A", "COL B": "COL B"}, 
            "prc": ["<underline>COL A</underline>", 
                    "<underline>COL B</underline>"]}, 
    "rec": {"raw": {"COL A": "abc", "COL B": "123"}, "prc": ["abc  ", "  123"]}
}


@pytest.fixture
def console_mock(mocker):
    mock = mocker.Mock(spec=Terminal)
    mock.blue = mocker.Mock(side_effect=lambda x: f"<blue>{x}</blue>")
    mock.reverse = mocker.Mock(side_effect=lambda x: f"<reverse>{x}</reverse>")
    mock.underline = mocker.Mock(side_effect=lambda x: f"<underline>{x}</underline>")
    return mock

@pytest.fixture
def data_mock(mocker):
    mock = mocker.Mock(spec=Table)
    mock.get_title.return_value = ROW_CONTENT["ttl"]["raw"]
    mock.get_headings.return_value = ROW_CONTENT["hdg"]["raw"]
    mock.get_record.return_value = ROW_CONTENT["rec"]["raw"]
    mock.get_rjust_columns.return_value = {"COL B"}
    mock.get_column_widths.return_value = {"COL A": 5, "COL B": 5}
    mock.get_table_width.return_value = 12
    return mock

@pytest.fixture
def con_tbl_inst(data_mock, console_mock):
    instance = ConsoleTable(data_mock)
    instance._con = console_mock
    return instance


#7 Test display


# Test drawRow
@pytest.mark.parametrize(
    "row_type, ends, raw, processed, index, is_line_type, exp_out",
    [
        (
            "top", 
            ROW_ENDS["top"], 
            ROW_CONTENT["top"]["raw"], 
            ROW_CONTENT["top"]["prc"], 
            None, 
            True, 
            "<blue>╔</blue><blue>══════════════</blue><blue>╗</blue>\n"
        ), 
        (
            "inner", 
            ROW_ENDS["inr"], 
            ROW_CONTENT["inr"]["raw"], 
            ROW_CONTENT["inr"]["prc"], 
            None, 
            True, 
            "<blue>╟</blue><blue>──────────────</blue><blue>╢</blue>\n"
        ), 
        (
            "bottom", 
            ROW_ENDS["btm"], 
            ROW_CONTENT["btm"]["raw"], 
            ROW_CONTENT["btm"]["prc"], 
            None, 
            True, 
            "<blue>╚</blue><blue>══════════════</blue><blue>╝</blue>\n"
        ), 
        (
            "title", 
            ROW_ENDS["txt"], 
            ROW_CONTENT["ttl"]["raw"], 
            ROW_CONTENT["ttl"]["prc"], 
            None, 
            False,
            "<blue>║</blue> <reverse> Data Title </reverse> <blue>║</blue>\n"
        ), 
        (
            "headings", 
            ROW_ENDS["txt"], 
            ROW_CONTENT["hdg"]["raw"], 
            ROW_CONTENT["hdg"]["prc"], 
            None, 
            False,
            "<blue>║</blue> <underline>COL A</underline>  " + 
            "<underline>COL B</underline> <blue>║</blue>\n"
        ), 
        (
            "record", 
            ROW_ENDS["txt"], 
            ROW_CONTENT["rec"]["raw"], 
            ROW_CONTENT["rec"]["prc"], 
            0, 
            False,
            "<blue>║</blue> abc      123 <blue>║</blue>\n"
        )
    ]
)
def test_draw_row(mocker, con_tbl_inst, data_mock, row_type, ends, raw, 
                  processed, index, is_line_type, exp_out, capfd):
    # Setup attributes
    con_tbl_inst._margin_size = 0
    con_tbl_inst._column_widths = data_mock.get_column_widths.return_value
    con_tbl_inst._table_width = data_mock.get_table_width.return_value

    # Setup methods
    mocker.patch.object(con_tbl_inst, "_get_row_ends", return_value=ends)
    mocker.patch.object(con_tbl_inst, "_get_row_content", return_value=raw)
    mocker.patch.object(con_tbl_inst, "_process_row_content", 
                        return_value=processed)
    
    # Setup method argument
    rjust_col = (data_mock.get_rjust_columns.return_value 
                 if row_type == "record" else {})

    # Execute
    con_tbl_inst._draw_row(row_type, index)
    out, err = capfd.readouterr()

    # Verify method calls
    if row_type == "record":
        data_mock.get_rjust_columns.assert_called_once()
    con_tbl_inst._get_row_ends.assert_called_once_with(row_type, is_line_type)
    if row_type in ["title", "headings", "record"]:
        con_tbl_inst._get_row_content.assert_called_once_with(row_type, index)
        con_tbl_inst._process_row_content.assert_called_once_with(row_type, 
                                                                  raw, 
                                                                  rjust_col)
    
    # Verify output    
    assert out == exp_out
    assert err == ""


#6 Test drawTable


# Test getRowContent
@pytest.mark.parametrize(
    "row_type, index", 
    [
        ("title", None),     # Test case 1: Title
        ("headings", None),  # Test case 2: Headings
        ("record", 0)        # Test case 3: Record
    ]
)
def test_get_row_content(con_tbl_inst, data_mock, row_type, index):
    # Execute
    result = con_tbl_inst._get_row_content(row_type, index)

    # Verify
    match row_type:
        case "title":
            con_tbl_inst._data.get_title.assert_called_once()
            assert result == data_mock.get_title.return_value
        case "headings":
            con_tbl_inst._data.get_headings.assert_called_once()
            assert result == data_mock.get_headings.return_value
        case "record":
            con_tbl_inst._data.get_record.assert_called_once_with(index)
            assert result == data_mock.get_record.return_value


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
def test_get_row_ends(con_tbl_inst, row_type, is_line_type, expected):
    # Execute
    result = con_tbl_inst._get_row_ends(row_type, is_line_type)

    # Verify
    assert result == expected


# Test processRowContent
@pytest.mark.parametrize(
    "row_type, expected", 
    [
        # Test case 1: Title line
        ("title", ROW_CONTENT["ttl"]["prc"]), 

        # Test case 2: Headings line
        ("headings", ROW_CONTENT["hdg"]["prc"]), 

        # Test case 3: Record line
        ("record", ROW_CONTENT["rec"]["prc"])
    ]
)
def test_process_row_content(data_mock, con_tbl_inst, row_type, expected):
    # Setup
    match row_type:
        case "title":
            content = data_mock.get_title.return_value
        case "headings":
            content = data_mock.get_headings.return_value
        case "record":
            content = data_mock.get_record.return_value
    rjust_col = data_mock.get_rjust_columns.return_value
    con_tbl_inst._column_widths = data_mock.get_column_widths.return_value
    con_tbl_inst._table_width = data_mock.get_table_width.return_value
    
    # Execute
    result = con_tbl_inst._process_row_content(row_type, content, rjust_col)

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
