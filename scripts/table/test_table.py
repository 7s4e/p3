import pytest
from unittest.mock import MagicMock
from table import Table


# @pytest.fixture
# def mock_instance():
#     class Table:
#         def __init__(self):
#             self._dataset = []
#             self._records_count = 0
#         def _capitalize_keys(self, data):
#             self._dataset = [{key.upper(): value 
#                               for key, value in datum.items()} 
#                              for datum in data]
#             self._records_count = len(self._dataset)
#     return Table()

# @pytest.mark.parametrize("input_data, expected_dataset, expected_count",
#     [
#         # Test case 1: Simple case with one dictionary
#         (
#             [{"key1": "value1", "key2": "value2"}],
#             [{"KEY1": "value1", "KEY2": "value2"}],
#             1,
#         ),
#         # Test case 2: Multiple dictionaries with mixed keys
#         (
#             [{"key1": "value1"}, {"Key2": "value2"}],
#             [{"KEY1": "value1"}, {"KEY2": "value2"}],
#             2,
#         ),
#         # Test case 3: Empty list
#         (
#             [],
#             [],
#             0,
#         ),
#         # Test case 4: Empty dictionaries
#         (
#             [{}],
#             [{}],
#             1,
#         ),
#         # Test case 5: Special characters and numbers in keys
#         (
#             [{"k3y!": "v@lue", "123": "456"}],
#             [{"K3Y!": "v@lue", "123": "456"}],
#             1,
#         ),
#     ],
# )

# def test_capitalize_keys(table_instance, input_data, expected_dataset, expected_count):
#     """Test the _capitalize_keys method."""
#     table_instance._capitalize_keys(input_data)

#     # Assert dataset is updated correctly
#     assert table_instance._dataset == expected_dataset

#     # Assert records count is updated correctly
#     assert table_instance._records_count == expected_count


# Test _capitalize 

# # Test Table
# @pytest.mark.parametrize(
#     " data,                                                                 title_arg,    exp_title", 
#     [([{"col1": "val1", "col2": "val2"}, {"col1": "val3", "col2": "val4"}], "Data Table", "DATA TABLE")])

# def test_instance(data, title_arg, exp_title):
#     # Setup
#     # Execute
#     table = Table(table_data=data, title=title_arg)

#     # Verify
#     assert table._title == exp_title




# @pytest.fixture
# def mock_data_table():
#     title = "Data Table"
#     rjust_columns = {"column2"}
#     return Table(table_data=table_data, title=title, 
#                  rjust_columns=rjust_columns)

# @pytest.fixture
# def mock_string_table():
#     table_string = """
#     column1 column2
#     value1   value2
#     value3   value4
#     """
#     title = "String Table"
#     rjust_columns = {"column2"}
#     return Table(table_string=table_string, title=title, 
#                  rjust_columns=rjust_columns)


# # Test Table Initialization
# # @pytest.mark.parametrize(
# #     " fixture,           title", 
# #     [("mock_data_table",   "DATA TABLE"), 
# #      ("mock_string_table", "STRING TABLE")])

# # def test_fixture(fixture, title, request):
# #     # Setup, Execute
# #     instance = request.getfixturevalue(fixture)

# #     # Verify
# #     assert len(instance._dataset) == 2
# #     assert instance._title == title
# #     assert "COLUMN2" in instance._right_justified_columns
