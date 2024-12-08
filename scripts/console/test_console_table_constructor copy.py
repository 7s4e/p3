import pytest
import sys
from console_table import ConsoleTable
from table import Table


@pytest.mark.parametrize(
    "data, exception",
    [
        # Test series: TypeError if 'data' not `Table`
        (None, TypeError), 
        (bool(), TypeError), 
        (bytearray(), TypeError), 
        (bytes(), TypeError), 
        (classmethod(lambda: None), TypeError), 
        (complex(), TypeError), 
        (dict(), TypeError), 
        (enumerate(str()), TypeError), 
        (filter(lambda: None, str()), TypeError), 
        (float(), TypeError), 
        (frozenset(), TypeError), 
        (int(), TypeError), 
        (list(), TypeError), 
        (map(lambda: None, str()), TypeError), 
        (memoryview(bytes()), TypeError), 
        (object(), TypeError), 
        (property(), TypeError), 
        (range(int()), TypeError), 
        (reversed(str()), TypeError), 
        (set(), TypeError), 
        (slice(int()), TypeError), 
        (staticmethod(lambda: None), TypeError), 
        (str(), TypeError), 
        (tuple(), TypeError), 
        (type(object()), TypeError), 
        (zip(), TypeError), 
        (Table(table_string=""), None)
    ]
)
def test_console_table_constructor(data, exception):
    if exception:
        with pytest.raises(exception):
            ConsoleTable(data)
    else:
        instance = ConsoleTable(data)
        assert instance._data == data
        assert instance._borders["top"]["left"] == "╔"
        assert instance._borders["top"]["fill"] == "═"
        assert instance._borders["top"]["right"] == "╗"
        assert instance._borders["inner"]["left"] == "╟"
        assert instance._borders["inner"]["fill"] == "─"
        assert instance._borders["inner"]["right"] == "╢"
        assert instance._borders["bottom"]["left"] == "╚"
        assert instance._borders["bottom"]["fill"] == "═"
        assert instance._borders["bottom"]["right"] == "╝"
        assert instance._borders["side"] == "║"
