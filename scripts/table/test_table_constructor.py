import pytest
from table import Table


@pytest.fixture
def mock_table(mocker):
    return mocker.Mock(spec=Table)


@pytest.mark.parametrize(
    "table_data, table_string, title, rjust_columns, exception",
    [
        # Test series 1: TypeError if 'table_data' is not 
        #     `list[dict[str, str]]` or `None`
        (None, "", None, None, None), 
        (bool(), None, None, None, TypeError), 
        (bytearray(), None, None, None, TypeError), 
        (bytes(), None, None, None, TypeError), 
        (classmethod(mock_table), None, None, None, TypeError), 
        (complex(), None, None, None, TypeError), 
        (dict(), None, None, None, TypeError), 
        (enumerate(str()), None, None, None, TypeError), 
        (filter(mock_table, str()), None, None, None, TypeError), 
        (float(), None, None, None, TypeError), 
        (frozenset(), None, None, None, TypeError), 
        (int(), None, None, None, TypeError), 
        (map(mock_table, str()), None, None, None, TypeError), 
        (memoryview(bytes()), None, None, None, TypeError), 
        (object(), None, None, None, TypeError), 
        (property(), None, None, None, TypeError), 
        (range(int()), None, None, None, TypeError), 
        (reversed(str()), None, None, None, TypeError), 
        (set(), None, None, None, TypeError), 
        (slice(int()), None, None, None, TypeError), 
        (staticmethod(mock_table), None, None, None, TypeError), 
        (str(), None, None, None, TypeError), 
        (tuple(), None, None, None, TypeError), 
        (type(object()), None, None, None, TypeError), 
        (zip(), None, None, None, TypeError), 

        # Test series 2: TypeError if 'table_string' is not `str` or 
        #     `None`
        (None, bool(), None, None, TypeError), 
        (None, bytearray(), None, None, TypeError), 
        (None, bytes(), None, None, TypeError), 
        (None, classmethod(mock_table), None, None, TypeError), 
        (None, complex(), None, None, TypeError), 
        (None, dict(), None, None, TypeError), 
        (None, enumerate(str()), None, None, TypeError), 
        (None, filter(mock_table, str()), None, None, TypeError), 
        (None, float(), None, None, TypeError), 
        (None, frozenset(), None, None, TypeError), 
        (None, int(), None, None, TypeError), 
        (None, list(), None, None, TypeError), 
        (None, map(mock_table, str()), None, None, TypeError), 
        (None, memoryview(bytes()), None, None, TypeError), 
        (None, object(), None, None, TypeError), 
        (None, property(), None, None, TypeError), 
        (None, range(int()), None, None, TypeError), 
        (None, reversed(str()), None, None, TypeError), 
        (None, set(), None, None, TypeError), 
        (None, slice(int()), None, None, TypeError), 
        (None, staticmethod(mock_table), None, None, TypeError), 
        (None, str(), None, None, None), 
        (None, tuple(), None, None, TypeError), 
        (None, type(object()), None, None, TypeError), 
        (None, zip(), None, None, TypeError), 

        # Test series 3: TypeError if 'title' is not `str` or `None`
        (None, "", None, None, None), 
        (None, "", bool(), None, TypeError), 
        (None, "", bytearray(), None, TypeError), 
        (None, "", bytes(), None, TypeError), 
        (None, "", classmethod(mock_table), None, TypeError), 
        (None, "", complex(), None, TypeError), 
        (None, "", dict(), None, TypeError), 
        (None, "", enumerate(str()), None, TypeError), 
        (None, "", filter(mock_table, str()), None, TypeError), 
        (None, "", float(), None, TypeError), 
        (None, "", frozenset(), None, TypeError), 
        (None, "", int(), None, TypeError), 
        (None, "", list(), None, TypeError), 
        (None, "", map(mock_table, str()), None, TypeError), 
        (None, "", memoryview(bytes()), None, TypeError), 
        (None, "", object(), None, TypeError), 
        (None, "", property(), None, TypeError), 
        (None, "", range(int()), None, TypeError), 
        (None, "", reversed(str()), None, TypeError), 
        (None, "", set(), None, TypeError), 
        (None, "", slice(int()), None, TypeError), 
        (None, "", staticmethod(mock_table), None, TypeError), 
        (None, "", str(), None, None), 
        (None, "", tuple(), None, TypeError), 
        (None, "", type(object()), None, TypeError), 
        (None, "", zip(), None, TypeError), 

        # Test series 4: TypeError if 'rjust_columns' is not `str`, 
        #     `list[str]`, `set[str]`, or `None`
        (None, "", None, None, None), 
        (None, "", None, bool(), TypeError), 
        (None, "", None, bytearray(), TypeError), 
        (None, "", None, bytes(), TypeError), 
        (None, "", None, classmethod(mock_table), TypeError), 
        (None, "", None, complex(), TypeError), 
        (None, "", None, dict(), TypeError), 
        (None, "", None, enumerate(str()), TypeError), 
        (None, "", None, filter(mock_table, str()), TypeError), 
        (None, "", None, float(), TypeError), 
        (None, "", None, frozenset(), TypeError), 
        (None, "", None, int(), TypeError), 
        (None, "", None, list(), None), 
        (None, "", None, map(mock_table, str()), TypeError), 
        (None, "", None, memoryview(bytes()), TypeError), 
        (None, "", None, object(), TypeError), 
        (None, "", None, property(), TypeError), 
        (None, "", None, range(int()), TypeError), 
        (None, "", None, reversed(str()), TypeError), 
        (None, "", None, set(), None), 
        (None, "", None, slice(int()), TypeError), 
        (None, "", None, staticmethod(mock_table), TypeError), 
        (None, "", None, str(), None), 
        (None, "", None, tuple(), TypeError), 
        (None, "", None, type(object()), TypeError), 
        (None, "", None, zip(), TypeError), 

        # Test series 5: ValueError either if both 'table_data' and 
        #     'table_string` are `None`, or if both are not `None`
        (None, None, None, None, ValueError), 
        (list(), "", None, None, ValueError), 
        ([{"k": "v"}], "s", None, None, ValueError)
    ]
)
def test_constructor(mock_table, table_data, table_string, title, 
                     rjust_columns, exception):
    if exception:
        with pytest.raises(exception):
            Table(table_data, table_string, title, rjust_columns)
    else:
        tbl = Table(table_data, table_string, title, rjust_columns)
        assert tbl._records_count == 0
