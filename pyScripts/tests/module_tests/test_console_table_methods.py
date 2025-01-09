# import pytest
# from unittest.mock import call
# from blessed import Terminal
# from modules import ConsoleTable, Table


# ROW_ENDS = {"top": ("<blue>╔</blue>", "<blue>╗</blue>", ""), 
#             "inr": ("<blue>╟</blue>", "<blue>╢</blue>", ""), 
#             "btm": ("<blue>╚</blue>", "<blue>╝</blue>", ""), 
#             "txt": ("<blue>║</blue>", "<blue>║</blue>", " ")}

# ROW_CONTENT = {
#     "raw": {
#         "top": "═", 
#         "inr": "─", 
#         "btm": "═", 
#         "ttl": "Data Title", 
#         "hdg": {"COL A": "COL A", "COL B": "COL B"}, 
#         "rec": {"COL A": "abc", "COL B": "123"}
#     }, 
#     "prc": {
#         "top": "<blue>══════════════</blue>", 
#         "inr": "<blue>──────────────</blue>", 
#         "btm": "<blue>══════════════</blue>", 
#         "ttl": ["<reverse> Data Title </reverse>"], 
#         "hdg": ["<underline>COL A</underline>", 
#                 "<underline>COL B</underline>"], 
#         "rec": ["abc  ", "  123"]
#     }, 
#     "fin": {
#         "top": "<blue>╔</blue><blue>══════════════</blue><blue>╗</blue>\n", 
#         "inr": "<blue>╟</blue><blue>──────────────</blue><blue>╢</blue>\n", 
#         "btm": "<blue>╚</blue><blue>══════════════</blue><blue>╝</blue>\n", 
#         "ttl": "<blue>║</blue> <reverse> Data " + 
#                 "Title </reverse> <blue>║</blue>\n", 
#         "hdg": "<blue>║</blue> <underline>COL A</underline>  " + 
#                 "<underline>COL B</underline> <blue>║</blue>\n", 
#         "rec": "<blue>║</blue> abc      123 <blue>║</blue>\n"
#     }
# }


# @pytest.fixture
# def mck_Tm(mocker):
#     mck = mocker.Mock(spec=Terminal)
#     mck.blue = mocker.Mock(side_effect=lambda x: f"<blue>{x}</blue>")
#     mck.reverse = mocker.Mock(side_effect=lambda x: (f"<reverse>{x}" + 
#                                                      "</reverse>"))
#     mck.underline = mocker.Mock(side_effect=lambda x: (f"<underline>{x}" + 
#                                                        "</underline>"))
#     return mck

# @pytest.fixture
# def mck_Tb(mocker):
#     mck = mocker.Mock(spec=Table)
#     mck.get_title.return_value = ROW_CONTENT["raw"]["ttl"]
#     mck.get_headings.return_value = ROW_CONTENT["raw"]["hdg"]
#     mck.get_record.return_value = ROW_CONTENT["raw"]["rec"]
#     mck.get_rjust_columns.return_value = {"COL B"}
#     mck.get_column_widths.return_value = {"COL A": 5, "COL B": 5}
#     mck.get_table_width.return_value = 12
#     return mck

# @pytest.fixture
# def CT_inst(mck_Tb, mck_Tm):
#     inst = ConsoleTable(mck_Tb)
#     inst._trm = mck_Tm
#     inst._col_wds = mck_Tb.get_column_widths.return_value
#     inst._tbl_wd = mck_Tb.get_table_width.return_value
#     return inst


# # Test display
# @pytest.mark.parametrize("record_count", [0, 1, 9])
# def test_display(mocker, mck_Tb, record_count):
#     # Setup
#     CT_inst = ConsoleTable(mck_Tb)
#     mocker.patch.object(CT_inst, "_set_dims")
#     mocker.patch.object(CT_inst, "_drw_tbl")
#     mocker.patch.object(CT_inst._data, "count_records", return_value=record_count)

#     # Execute
#     CT_inst.display()

#     # Verify
#     CT_inst._set_dims.assert_called_once()
#     CT_inst._data.count_records.assert_called_once()
#     CT_inst._drw_tbl.assert_called_once_with(record_count)


# # Test drawRow
# @pytest.mark.parametrize(
#     "row_type, ends_in, raw_in, proc_in, record_idx, is_line_type, exp_out",
#     [
#         # Test case 1: Top border line
#         (
#             "top", 
#             ROW_ENDS["top"], 
#             ROW_CONTENT["raw"]["top"], 
#             ROW_CONTENT["prc"]["top"], 
#             None, 
#             True, 
#             ROW_CONTENT["fin"]["top"]
#         ), 
#         # Test case 2: Inner border line
#         (
#             "inner", 
#             ROW_ENDS["inr"], 
#             ROW_CONTENT["raw"]["inr"], 
#             ROW_CONTENT["prc"]["inr"], 
#             None, 
#             True, 
#             ROW_CONTENT["fin"]["inr"]
#         ), 
#         # Test case 3: Bottom border line
#         (
#             "bottom", 
#             ROW_ENDS["btm"], 
#             ROW_CONTENT["raw"]["btm"], 
#             ROW_CONTENT["prc"]["btm"], 
#             None, 
#             True, 
#             ROW_CONTENT["fin"]["btm"]
#         ), 
#         # Test case 4: Title row
#         (
#             "title", 
#             ROW_ENDS["txt"], 
#             ROW_CONTENT["raw"]["ttl"], 
#             ROW_CONTENT["prc"]["ttl"], 
#             None, 
#             False, 
#             ROW_CONTENT["fin"]["ttl"]
#         ), 
#         # Test case 5: Headings row
#         (
#             "headings", 
#             ROW_ENDS["txt"], 
#             ROW_CONTENT["raw"]["hdg"], 
#             ROW_CONTENT["prc"]["hdg"], 
#             None, 
#             False, 
#             ROW_CONTENT["fin"]["hdg"]
#         ), 
#         # Test case 6: Record rows
#         (
#             "record", 
#             ROW_ENDS["txt"], 
#             ROW_CONTENT["raw"]["rec"], 
#             ROW_CONTENT["prc"]["rec"], 
#             0, 
#             False, 
#             ROW_CONTENT["fin"]["rec"]
#         )
#     ]
# )
# def test_drw_rw(mocker, CT_inst, mck_Tb, row_type, ends_in, raw_in, proc_in, 
#                 record_idx, is_line_type, exp_out, capfd):
#     # Setup mock methods
#     mocker.patch.object(CT_inst, "_get_rw_ends", return_value=ends_in)
#     mocker.patch.object(CT_inst, "_get_rw_cntnt", return_value=raw_in)
#     mocker.patch.object(CT_inst, "_proc_rw_cntnt", return_value=proc_in)
    
#     # Setup attribute and method argument
#     CT_inst._mrg_sz = 0
#     rjust_col = (mck_Tb.get_rjust_columns.return_value 
#                  if row_type == "record" else {})

#     # Execute
#     CT_inst._drw_rw(row_type, record_idx)
#     out, err = capfd.readouterr()

#     # Verify method calls
#     if row_type == "record":
#         CT_inst._data.get_rjust_columns.assert_called_once()
#     CT_inst._get_rw_ends.assert_called_once_with(row_type, is_line_type)
#     if row_type in ["title", "headings", "record"]:
#         CT_inst._get_rw_cntnt.assert_called_once_with(row_type, record_idx)
#         CT_inst._proc_rw_cntnt.assert_called_once_with(row_type, raw_in, 
#                                                        rjust_col)
    
#     # Verify output    
#     assert out == exp_out
#     assert err == ""


# # Test drawTable
# @pytest.mark.parametrize("record_count", [0, 1, 9])
# def test_drw_tbl(mocker, CT_inst, record_count):
#     # Setup
#     mocker.patch.object(CT_inst, "_drw_rw")

#     # Execute
#     CT_inst._drw_tbl(record_count)

#     # Verify
#     exp_calls = [call("top"), 
#                  call("title"), 
#                  call("inner"), 
#                  call("headings"), 
#                  *[call("record", i) for i in range(record_count)], 
#                  call("bottom")]
#     CT_inst._drw_rw.assert_has_calls(exp_calls)
#     assert CT_inst._drw_rw.call_count == len(exp_calls)


# # Test getRowContent
# @pytest.mark.parametrize(
#     "row_type, record_idx", 
#     [
#         ("title", None),     # Test case 1: Title
#         ("headings", None),  # Test case 2: Headings
#         ("record", 0)        # Test case 3: Record
#     ]
# )
# def test_get_rw_cntnt(CT_inst, mck_Tb, row_type, record_idx):
#     # Execute
#     act_out = CT_inst._get_rw_cntnt(row_type, record_idx)

#     # Verify
#     match row_type:
#         case "title":
#             CT_inst._data.get_title.assert_called_once()
#             assert act_out == mck_Tb.get_title.return_value
#         case "headings":
#             CT_inst._data.get_headings.assert_called_once()
#             assert act_out == mck_Tb.get_headings.return_value
#         case "record":
#             CT_inst._data.get_record.assert_called_once_with(record_idx)
#             assert act_out == mck_Tb.get_record.return_value


# # Test getRowEnds
# @pytest.mark.parametrize(
#     "row_type, is_line_type, exp_out", 
#     [
#         # Test case 1: Top line
#         ("top", True, ROW_ENDS["top"]), 

#         # Test case 2: Inner line
#         ("inner", True, ROW_ENDS["inr"]), 

#         # Test case 3: Bottom line
#         ("bottom", True, ROW_ENDS["btm"]), 

#         # Test case 4: Text row
#         ("text", False, ROW_ENDS["txt"])
#     ]
# )
# def test_get_rw_ends(CT_inst, row_type, is_line_type, exp_out):
#     # Execute
#     act_out = CT_inst._get_rw_ends(row_type, is_line_type)

#     # Verify
#     assert act_out == exp_out


# # Test processRowContent
# @pytest.mark.parametrize(
#     "row_type, exp_out", 
#     [
#         # Test case 1: Title row
#         ("title", ROW_CONTENT["prc"]["ttl"]), 

#         # Test case 2: Headings row
#         ("headings", ROW_CONTENT["prc"]["hdg"]), 

#         # Test case 3: Record row
#         ("record", ROW_CONTENT["prc"]["rec"])
#     ]
# )
# def test_proc_rw_cntnt(mck_Tb, CT_inst, row_type, exp_out):
#     # Setup
#     match row_type:
#         case "title":
#             content = mck_Tb.get_title.return_value
#         case "headings":
#             content = mck_Tb.get_headings.return_value
#         case "record":
#             content = mck_Tb.get_record.return_value
#     rjust_col = mck_Tb.get_rjust_columns.return_value
    
#     # Execute
#     act_out = CT_inst._proc_rw_cntnt(row_type, content, rjust_col)

#     # Verify
#     assert act_out == exp_out


# # Test setDimensions
# @pytest.mark.parametrize(
#     "term_wd, tbl_wds, col_wds, dply_wd", 
#     [
#         (99, [64], [20, 20, 20], 79),      # Test case 1: Wide terminal
#         (59, [64, 55], [17, 17, 17], 59),  # Test case 2: Narrow terminal
#         (79, [94, 75], [24, 24, 23], 79),  # Test case 3: Wide table
#         (79, [34], [10, 10, 10], 79)       # Test case 4: Narrow table
#     ]
# )
# def test_set_dims(mck_Tm, mck_Tb, CT_inst, term_wd, tbl_wds, col_wds, 
#                   dply_wd):
#     # Setup
#     mck_Tm.width = term_wd
#     mck_Tb.get_table_width.side_effect = tbl_wds
#     mck_Tb.get_column_widths.return_value = col_wds

#     # Execute
#     CT_inst._set_dims()

#     # Verify function process
#     assert CT_inst._data.get_table_width.call_count == len(tbl_wds)
#     resize_called = CT_inst._data.resize_columns.call_count > 0
#     if resize_called:
#         CT_inst._data.resize_columns.assert_called_once_with(dply_wd - 4)
#     CT_inst._data.get_column_widths.assert_called_once()

#     # Verify function results
#     assert CT_inst._disp_wd == dply_wd
#     assert CT_inst._mrg_sz == (term_wd - dply_wd) // 2
#     assert CT_inst._tbl_wd == tbl_wds[-1]
#     assert CT_inst._col_wds == col_wds
