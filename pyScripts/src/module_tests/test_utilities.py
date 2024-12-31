import pytest
from modules import utilties as utl

@pytest.mark.parametrize(
    "str_in, exp_out", 
    [("get_disk", "getDisk")]
)
def test_snake_to_camel(str_in, exp_out):
    # Execute
    result = utl.snake_to_camel(str_in)

    # Veriry
    assert result == exp_out