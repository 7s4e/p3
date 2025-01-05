import pytest
from blessed import Terminal
from modules import ConsoleTable, Table


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
    # Execute
    if exception:
        with pytest.raises(exception):
            ConsoleTable(data)
    else:
        CT_inst = ConsoleTable(data)
    
    # Verify
        assert isinstance(CT_inst._trm, Terminal)
        assert CT_inst._data == data
