"""Module for handling table formatting and display."""

class Table:
    def __init__(self, 
                 title: str,
                 table_string: str,
                 right_justified_column_labels: str | list[str] | None
                 ) -> None:
        """Initialize the Table instance.

        Args:
            title: The title of the table.
            table_string: A string representation of the table.
            right_justified_column_labels: A string or list of strings
                representing the labels of columns to be right-
                justified.
        """
        self._title = title.upper()
        self._right_justified_columns = []
        self._read_table(table_string)
        if right_justified_column_labels is not None:
            self._add_rjc_label(right_justified_column_labels)
    
    @property
    def records_count(self) -> int:
        """Return the count of records in the table."""
        return self._records_count

    @staticmethod

    def _add_rjc_label(self, label: str | list[str]) -> None:
        """Add labels to the right-justified columns list.

        Args:
            label: A string or list of strings representing the label(s)
                to add.
        """
        self._right_justified_columns.append(label 
                                             if isinstance(label, list) 
                                             else [label])

    def _calculate_columns(self) -> dict[str, int]:
        """Calculate the width of each column based on the dataset."""
        self._column_widths = {key: max(len(key), 
                                        max(len(str(record[key])) 
                                            for record 
                                            in self._dataset)) 
                               for key in self._dataset[0].keys()}
        self._aggregate_column_width = sum(self._column_widths.values())
        self._column_gaps = len(self._column_widths) - 1
        
    def filter_startswith(self, key: str, prefix: str) -> None:
        """Filter records based on whether a key's value starts with a 
            prefix.

        Args:
            key: The key in the records to filter by.
            prefix: The prefix to match against.
        """
        self._dataset = [record for record in self._dataset 
                        if record.get(key, '').startswith(prefix)]
        self._records_count

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
        if line[start].isspace():
            while start < end and line[start].isspace(): start += 1
        else:
            while start > 0 and not line[start - 1].isspace(): start -= 1

        while end > start and not line[end].isspace(): end -= 1
        while end > start and line[end - 1].isspace(): end -= 1

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
    
    def _format_field(self, 
                      field: str, 
                      width: int, 
                      is_right_justified: bool) -> str:
        """Format a field within a table cell.

        Args:
            field: The field value to format.
            width: The width of the field.
            is_right_justified: Whether the field should be right-justified.

        Returns:
            The formatted field as a string.
        """
        return f"{field:{'>' if is_right_justified else '<'}{width}}"

    def _format_record(self, record: dict[str, str]) -> dict[str, str]:
        """Format an entire record for display in the table.

        Args:
            record: A dictionary representing a single record.

        Returns:
            A dictionary with formatted fields.
        """
        return {key: self._format_field(value, 
                                        self._column_widths[key], 
                                        key in self._right_justified_columns) 
                for key, value in record.items()}

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

    def _number_records(self) -> list[dict[str, str]]:
        """Add a numerical index to each record in the table."""
        self._dataset = [{"#": i + 1, **record} 
                         for i, record in enumerate(self._dataset)]
    
    def _make_padding(self, content_width: int, available_width: int) -> str:
        """Create padding for centering content.

        Args:
            content_width: The width of the content to center.
            available_width: The total available width.

        Returns:
            A string of spaces to be used as padding.
        """
        return " " * max(0, (available_width - content_width) // 2)

    def _make_table(self) -> None:
        """Construct the table from the given components."""
        title_row = self._title_padding + self._title
        border_row = self._border
        header_row = (self._table_padding 
                      + self._column_spacing.join(list(
                          self._format_record(self._table_headings).values())))
        data_rows = [(self._table_padding 
                      + self._column_spacing.join(list(
                          self._format_record(record).values()))) 
                     for record in self._dataset]
        self._table = ([title_row, border_row, header_row] 
                       + data_rows 
                       + [border_row])

    def _print_table(self) -> None:
        """Print the constructed table to the console."""
        print()
        print("\n".join(self._table))

    def put_table(self, 
                  border_style: str = "=", 
                  column_gap_size: int = 2, 
                  display_width: int = 36, 
                  is_menu: bool = False) -> None:
        """Format and display a table with the given dataset.

        Args:
            border_style: The character used for the border.
            column_gap_size: The size of the gap between columns.
            display_width: The width of the table display.
            is_menu: Whether the table is being displayed as a menu.
        """
        if is_menu:
            self._number_records()
            self._add_rjc_label("#")
        self._calculate_columns()
        table_width = (self._aggregate_column_width 
                       + self._column_gaps * column_gap_size)
        max_line_length = max(display_width, table_width)
        self._border = border_style * max_line_length
        self._column_spacing = " " * column_gap_size
        self._title_padding = self._make_padding(len(self._title), 
                                                 max_line_length) 
        self._table_padding = self._make_padding(table_width, display_width)
        self._table_headings = {key: key for key in self._dataset[0].keys()}
        self._make_table()
        self._print_table()

    def _read_table(self, input: str) -> None:
        """Parse a table from a string input.

        Args:
            table_string: The string input representing the table.
        """
        lines = input.splitlines()
        keys = lines[0].split()
        positions_list = self._find_column_positions(lines[0], keys)
        self._dataset = [{key: self._get_slice(index, positions_list, line) 
                          for index, key in enumerate(keys)} 
                         for line in lines[1:]]
        self._records_count = len(self._dataset)
