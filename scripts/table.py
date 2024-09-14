"""Module for handling table formatting and display."""

from blessed import Terminal
from console import Console_Table

class Table:
    def __init__(self, 
                 table_data: list[dict[str, str]] | None = None,
                 table_string: str | None = None,
                 title: str | None = None,
                 rjust_columns: str | list[str] | None = None) -> None:
        """Initialize the Table instance.

        Args:
            table_data: A list of dictionaries representing the table 
                data. Each dictionary corresponds to a row, with keys as 
                column labels and values as the corresponding cell data.
            table_string: A string representation of the table.
            title: The title of the table, which will be converted to 
                uppercase.
            rjust_columns: A string or set of strings representing the 
                columns to be right-justified.

        Raises:
            ValueError: If neither or both of 'table_data' and 
                'table_string' are provided.
        """
        if (table_data is None) == (table_string is None):
            raise ValueError(
                "Provide exactly one of 'table_data' or 'table_string'."
                )
        if table_data is not None:
            self._capitalize_keys(table_data)
        else:
            self._read_table(table_string)
        if title is not None:
            self._title = title.upper()
        self._right_justified_columns = set()
        if rjust_columns is not None:
            self._add_rjust_col_label(rjust_columns)

    def _add_rjust_col_label(self, label: str | list[str]) -> None:
        """Add labels to the right-justified columns list.

        Args:
            label: A string or list of strings representing the label(s)
                to add.
        """
        if isinstance(label, list):
            for each in label:
                self._right_justified_columns.add(each)
        else:
            self._right_justified_columns.add(label)

    def _calculate_widths(self) -> None:
        """Calculate the width of each column and of a table made up of
            the dataset.
        """
        self._column_widths = {key: max(len(key), 
                                        max(len(str(record[key])) 
                                            for record 
                                            in self._dataset)) 
                               for key in self._dataset[0].keys()}
        self._table_width = (sum(self._column_widths.values()) 
                             + 2 * (len(self._column_widths) - 1))

    def _capitalize_keys(self, data: list[dict[str, str]]) -> None:
        self._dataset = [{key.upper(): value for key, value in datum.items()}  
                         for datum in data]
        self._records_count = len(self._dataset)

    def count_records(self) -> int:
        """Return the count of records in the table."""
        return self._records_count

    def filter_nonempty(self, key: str) -> None:
        """Filter records based on whether a key's value exists.

        Args:
            key: The key in the records by which to filter.
        """
        self._dataset = [record for record in self._dataset 
                        if record.get(key.upper(), '') != ""]
        self._records_count = len(self._dataset)

    def filter_startswith(self, key: str, prefix: str) -> None:
        """Filter records based on whether a key's value starts with a 
            prefix.

        Args:
            key: The key in the records by which to filter.
            prefix: The prefix to match against.
        """
        self._dataset = [record for record in self._dataset 
                        if record.get(key.upper(), '').startswith(prefix)]
        self._records_count = len(self._dataset)

    def _find_boundaries(self, 
                         column_index: int, 
                         positions_list: list[int], 
                         line: str) -> tuple[int, int]:
        """Find the start and end positions of a column in a line.

        Args:
            column_index: The index of the column.
            positions_list: A list of positions for each column.
            line: The line of text to analyze.

        Returns:
            A tuple containing the start and end positions.
        """
        start = min(positions_list[column_index], len(line) - 1)
        end = min((positions_list[column_index + 1] 
                   if column_index + 1 < len(positions_list) 
                   else len(line) - 1), 
                  len(line) - 1)

        # Adjust the start and end positions to align with non-
        #   whitespace content.
        if start != len(line) - 1:
            if line[start].isspace():
                while start < end and line[start].isspace(): start += 1
            else:
                while start > 0 and not line[start - 1].isspace(): start -= 1
        else:
            start = len(line)
        
        if end != len(line) - 1:
            while end > start and not line[end].isspace(): end -= 1
            while end > start and line[end - 1].isspace(): end -= 1
        else:
            end = len(line)

        return start, end

    def _find_column_positions(self, 
                               header_line: str, 
                               keys: list[str]) -> list[int]:
        """Find the positions of each column in the header line.

        Args:
            header_line: The header line of the table.
            keys: A list of keys representing the columns.

        Returns:
            A list of positions for each column.
        """
        return [header_line.index(key) for key in keys]

    def get_headings(self) -> dict[str, str]:
        return {key: key for key in self._dataset[0].keys()}

    def get_column_widths(self) -> dict[str, int]:
        return self._column_widths

    def get_record(self, index: int) -> dict[str, str]:
        return self._dataset[index]

    def get_rjust_columns(self) -> set[str]:
        return self._right_justified_columns

    def _get_slice(self, 
                   column_index: int, 
                   positions_list: list[int], 
                   line: str) -> str:
        """Extract a slice of text representing a column from a line.

        Args:
            column_index: The index of the column.
            positions_list: A list of positions for each column.
            line: The line of text to slice.

        Returns:
            A string representing the extracted slice for the column.
        """
        start, end = self._find_boundaries(column_index, positions_list, line)
        return line[start:end].strip()

    def get_table_width(self) -> int:
        return self._table_width

    def get_title(self) -> str:
        return self._title

    def _number_records(self) -> list[dict[str, str]]:
        """Add a numerical index to each record in the table."""
        self._dataset = [{"#": i + 1, **record} 
                         for i, record in enumerate(self._dataset)]
        self._add_rjust_col_label("#")

    def put_table(self, 
                  terminal: Terminal,
                  is_menu: bool = False) -> None:
        """Format and display a table with the given dataset.

        Args:
            terminal: 
            is_menu: Whether the table is being displayed as a menu.
        """
        if is_menu:
            self._number_records()
        self._calculate_widths()
        table = Console_Table(self)
        table.display(terminal)

    def _read_table(self, input: str) -> None:
        """Parse a table from a string input.

        Args:
            table_string: The string input representing the table.
        """
        lines = input.splitlines()
        keys = lines[0].split()
        positions_list = self._find_column_positions(lines[0], keys)
        self._dataset = [{key.upper(): self._get_slice(index, 
                                                       positions_list, 
                                                       line) 
                          for index, key in enumerate(keys)} 
                         for line in lines[1:]]
        self._records_count = len(self._dataset)

    def resize_columns(self, width_limit: int) -> None:
        trim_length = width_limit - self._table_width
        while trim_length > 0:
            max_length = 0
            for key, value in self._column_widths.items():
                if value >= max_length:
                    widest_column = key
            self._column_widths[widest_column] -= 1
            trim_length -= 1
