import pytest
from modules import Menu, Table


@pytest.mark.parametrize(
    "options, title, prompt, exp_count, exception",
    [
        # Test series 1: TypeError if 'options' not `Table` or `list`
        (None, None, None, 0, TypeError), 
        (bool(), None, None, 0, TypeError), 
        (bytearray(), None, None, 0, TypeError), 
        (bytes(), None, None, 0, TypeError), 
        (classmethod(lambda: None), None, None, 0, TypeError), 
        (complex(), None, None, 0, TypeError), 
        (dict(), None, None, 0, TypeError), 
        (enumerate(str()), None, None, 0, TypeError), 
        (filter(lambda: None, str()), None, None, 0, TypeError), 
        (float(), None, None, 0, TypeError), 
        (frozenset(), None, None, 0, TypeError), 
        (int(), None, None, 0, TypeError), 
        (list(), None, None, 0, ValueError), 
        (map(lambda: None, str()), None, None, 0, TypeError), 
        (memoryview(bytes()), None, None, 0, TypeError), 
        (object(), None, None, 0, TypeError), 
        (property(), None, None, 0, TypeError), 
        (range(int()), None, None, 0, TypeError), 
        (reversed(str()), None, None, 0, TypeError), 
        (set(), None, None, 0, TypeError), 
        (slice(int()), None, None, 0, TypeError), 
        (staticmethod(lambda: None), None, None, 0, TypeError), 
        (str(), None, None, 0, TypeError), 
        (tuple(), None, None, 0, TypeError), 
        (type(object()), None, None, 0, TypeError), 
        (zip(), None, None, 0, TypeError), 
        (Table(table_string=""), None, None, 0, None), 

        # Test series 2: TypeError if 'title' not `str` or `None`
        (Table(table_string=""), None, None, 0, None), 
        (Table(table_string=""), bool(), None, 0, TypeError), 
        (Table(table_string=""), bytearray(), None, 0, TypeError), 
        (Table(table_string=""), bytes(), None, 0, TypeError), 
        (Table(table_string=""), classmethod(lambda: None), None, 0, 
         TypeError), 
        (Table(table_string=""), complex(), None, 0, TypeError), 
        (Table(table_string=""), dict(), None, 0, TypeError), 
        (Table(table_string=""), enumerate(str()), None, 0, TypeError), 
        (Table(table_string=""), filter(lambda: None, str()), None, 0, 
         TypeError), 
        (Table(table_string=""), float(), None, 0, TypeError), 
        (Table(table_string=""), frozenset(), None, 0, TypeError), 
        (Table(table_string=""), int(), None, 0, TypeError), 
        (Table(table_string=""), list(), None, 0, TypeError), 
        (Table(table_string=""), map(lambda: None, str()), None, 0, 
         TypeError), 
        (Table(table_string=""), memoryview(bytes()), None, 0, TypeError), 
        (Table(table_string=""), object(), None, 0, TypeError), 
        (Table(table_string=""), property(), None, 0, TypeError), 
        (Table(table_string=""), range(int()), None, 0, TypeError), 
        (Table(table_string=""), reversed(str()), None, 0, TypeError), 
        (Table(table_string=""), set(), None, 0, TypeError), 
        (Table(table_string=""), slice(int()), None, 0, TypeError), 
        (Table(table_string=""), staticmethod(lambda: None), None, 0, 
         TypeError), 
        (Table(table_string=""), str(), None, 0, None), 
        (Table(table_string=""), tuple(), None, 0, TypeError), 
        (Table(table_string=""), type(object()), None, 0, TypeError), 
        (Table(table_string=""), zip(), None, 0, TypeError), 
        (Table(table_string=""), Table(table_string=""), None, 0, TypeError), 

        # Test series 3: TypeError if 'prompt' not `str` or `None`
        (Table(table_string=""), None, None, 0, None), 
        (Table(table_string=""), None, bool(), 0, TypeError), 
        (Table(table_string=""), None, bytearray(), 0, TypeError), 
        (Table(table_string=""), None, bytes(), 0, TypeError), 
        (Table(table_string=""), None, classmethod(lambda: None), 0, 
         TypeError), 
        (Table(table_string=""), None, complex(), 0, TypeError), 
        (Table(table_string=""), None, dict(), 0, TypeError), 
        (Table(table_string=""), None, enumerate(str()), 0, TypeError), 
        (Table(table_string=""), None, filter(lambda: None, str()), 0, 
         TypeError), 
        (Table(table_string=""), None, float(), 0, TypeError), 
        (Table(table_string=""), None, frozenset(), 0, TypeError), 
        (Table(table_string=""), None, int(), 0, TypeError), 
        (Table(table_string=""), None, list(), 0, TypeError), 
        (Table(table_string=""), None, map(lambda: None, str()), 0, 
         TypeError), 
        (Table(table_string=""), None, memoryview(bytes()), 0, TypeError), 
        (Table(table_string=""), None, object(), 0, TypeError), 
        (Table(table_string=""), None, property(), 0, TypeError), 
        (Table(table_string=""), None, range(int()), 0, TypeError), 
        (Table(table_string=""), None, reversed(str()), 0, TypeError), 
        (Table(table_string=""), None, set(), 0, TypeError), 
        (Table(table_string=""), None, slice(int()), 0, TypeError), 
        (Table(table_string=""), None, staticmethod(lambda: None), 0, 
         TypeError), 
        (Table(table_string=""), None, str(), 0, None), 
        (Table(table_string=""), None, tuple(), 0, TypeError), 
        (Table(table_string=""), None, type(object()), 0, TypeError), 
        (Table(table_string=""), None, zip(), 0, TypeError), 
        (Table(table_string=""), None, Table(table_string=""), 0, TypeError), 

        # Test case 1: 'options' is a `Table`
        (
            Table(table_data=[{"ITEMS": "Item1"}], title="Test"), 
            None, None, 1, None
        ), 
        # Test case 2: 'options' is a `list`
        (["Item1", "Item2"], None, None, 2, None), 

        # Test case 3: 'options' is a `list` with title provided
        (["Item1", "Item2"], "Mock List", None, 2, None), 

        # Test case 4: 'options' is a `list` with prompt provided
        (["Item1", "Item2"], None, "Mock prompt?", 2, None), 

        # Test case 5: 'options' is an empty `list`
        ([], None, None, 0, ValueError), 
    ]
)
def test_menu_constructor(mocker, options, title, prompt, exp_count, 
                          exception):
    # Execute with exception
    if exception:
        with pytest.raises(exception):
            Menu(options, title, prompt)

    else:
    # Setup mock Table
        if isinstance(options, list):
            mck_T = mocker.Mock(spec=Table)
            T_ptch = mocker.patch("modules.table.Table", return_value=mck_T)
    
    # Setup countRecords and setPrompt mocks
            T_obj = mck_T
        else:
            T_obj = options
        mocker.patch.object(T_obj, "count_records", return_value=exp_count)
        mocker.patch.object(Menu, "set_prompt")
    
    # Execute
        M_inst = Menu(options, title, prompt)

    # Verify options assignment
        if isinstance(options, list):
            T_ptch.assert_called_once_with(title=title, 
                                           table_data=[{"OPTION": option} 
                                                       for option in options])
        else:
            assert M_inst._opts == options
    
    # Verify count assignment
        M_inst._opts.count_records.assert_called_once()
        assert M_inst._ct == exp_count
    
    # Verify setPrompt call
        M_inst.set_prompt.assert_called_once_with(prompt)
