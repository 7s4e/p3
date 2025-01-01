# Local module import
from .console import ConsoleTable


class Table:
    """
    A class to represent and manipulate a table of data.
    The `Table` class allows for the creation of tables either from a 
    list of dictionaries (where each dictionary represents a row of 
    data) or from a string representation of a table. The class provides 
    various methods for filtering, formatting, and retrieving table 
    data. It also handles right-justification of specified columns and 
    can display the table in a console-friendly format.
    Attributes:
        _dataset (list[dict[str, str]]): The table data as a list of 
            dictionaries.
        _column_widths (dict[str, int]): The width of each column in the 
            table.
        _table_width (int): The total width of the table including 
            column separators.
        _right_justified_columns (set[str]): A set of columns that 
            should be right-justified when displayed.
        _title (str | None): The title of the table, stored in 
            uppercase.
        _records_count (int): The number of records (rows) in the table.
    Methods:
        count_records: Return the number of records in the dataset.
        filter_nonempty: Filter records based on non-empty values for a 
            specified key.
        filter_startswith: Filter records based on values that start with a 
            specified prefix for a key.
        get_column_widths: Return the width of each column.
        get_headings: Return a dictionary of column headings.
        get_record: Retrieve a specific record by its index.
        get_rjust_columns: Return the set of right-justified columns.
        get_table_width: Return the total width of the table.
        get_title: Return the title of the table.
        put_table: Format and display the table using a terminal.
        resize_columns: Resize column widths to fit within a specified 
            width limit.
"""
    def __init__(self, 
                 table_data: list[dict[str, str]] | None = None, 
                 table_string: str | None = None, 
                 title: str | None = None, 
                 rjust_columns: str | list[str] | set[str] | None = None
                 ) -> None:
        """Initialize the Table instance.
        Args:
            table_data: A list of dictionaries representing the table 
                data. Each dictionary corresponds to a row, with keys as 
                column labels and values as the corresponding cell data.
            table_string: A string representation of the table.
            title: The title of the table, which will be converted to 
                uppercase.
            rjust_columns: A string, list, or set of strings representing
                the columns to be right-justified.
        Raises:
            ValueError: If neither or both 'table_data' and 
                'table_string' are provided.
        """
        print(f"TRACE: Table.init called with {table_data}, {table_string}, {title}, {rjust_columns}")#####
        # Type validation
        if not (table_data is None or 
                (isinstance(table_data, list) and 
                 all(isinstance(d, dict) and 
                     all(isinstance(k, str) and isinstance(v, str) 
                         for k, v in d.items()) 
                     for d in table_data))):
            raise TypeError("expected 'list[dict[str, str]]' or 'None' for " + 
                            f"`table_data`, not {type(table_data).__name__}")
        if not (table_string is None or isinstance(table_string, str)):
            raise TypeError("expected 'str' or 'None' for `table_string`")
        if not (title is None or isinstance(title, str)):
            raise TypeError("expected 'str' or 'None' for `title`")
        if not (rjust_columns is None or isinstance(rjust_columns, str) or 
                ((isinstance(rjust_columns, list) or 
                  isinstance(rjust_columns, set)) 
                 and all(isinstance(i, str) for i in rjust_columns))):
            raise TypeError("expected 'str', 'list[str]', 'set[str]', or " + 
                            "'None' for `rjust_columns`")

        # Value validation
        if (table_data is None) == (table_string is None):
            raise ValueError("Provide exactly one of 'table_data' or " +
                             "'table_string'.")
        
        # Assign validated attributes        
        if table_data:
            print(f"TRACE: Table.init.table_data == True")#####
            self._capitalize_keys(table_data)
        else:
            print(f"TRACE: Table.init.table_data == False")#####
            self._read_table(table_string)
        
        self._title = title.upper() if title else None
        # print(f"TRACE: Table.init > self._title set as {self._title}")#####
        self._right_justified_columns = set()
        # print(f"TRACE: Table.init > self._right_justified_columns set as {self._right_justified_columns}")#####
        
        if rjust_columns:
            # print(f"TRACE: Table.init.rjust_columns == True")#####
            self._add_rjust_col_label(rjust_columns)

    # Public Methods
    def count_records(self) -> int:
        """Return the number of records in the dataset.

        Returns:
            int: The count of records.
        """
        return self._records_count

    def filter_nonempty(self, key: str) -> None:
        """Filter records to include only those where the value for the 
            specified key is non-empty.
        Args:
            key (str): The key in the records to check for non-empty 
                values.
        Updates:
            Filters self._dataset in place to include only records where 
            the value for the specified key is non-empty. Updates 
            self._records_count to reflect the new number of records.
        """
        self._dataset = [record for record in self._dataset 
                         if (key.upper() not in record or 
                             record.get(key.upper(), '').strip())]
        self._records_count = len(self._dataset)

    def filter_startswith(self, key: str, prefix: str) -> None:
        """Filter records to include only those where the value for the 
            specified key starts with the given prefix.
        Args:
            key (str): The key in the records to check.
            prefix (str): The prefix to match against.
        Updates:
            Filters self._dataset in place to include only records where 
            the value for the specified key starts with the given 
            prefix. Updates self._records_count to reflect the new 
            number of records.
        """
        self._dataset = [record for record in self._dataset 
                         if (key.upper() in record and 
                             record.get(key.upper(), '').startswith(prefix))]
        self._records_count = len(self._dataset)

    def get_column_widths(self) -> dict[str, int]:
        """Return a dictionary of column widths.
        Returns:
            dict[str, int]: A dictionary with column names as keys and 
                their widths as values.
        """
        return self._column_widths

    def get_headings(self) -> dict[str, str]:
        """Return a dictionary of column headings where each key is 
            mapped to itself.
        Returns:
            dict[str, str]: A dictionary with column names as both keys 
                and values.
        """
        return {key: key for key in self._dataset[0].keys()}

    def get_record(self, index: int) -> dict[str, str]:
        """Retrieve a specific record from the dataset.
        Args:
            index (int): The index of the record to retrieve.
        Returns:
            dict[str, str]: The record at the specified index.
    
        Raises:
            IndexError: If the index is out of range of the dataset.
        """
        if index < 0 or index >= len(self._dataset):
            raise IndexError("Index out of range.")
        return self._dataset[index]

    def get_rjust_columns(self) -> set[str]:
        """Return a set of column names that are right-justified.
        Returns:
            set[str]: A set of column names that are right-justified.
        """
        return self._right_justified_columns

    def get_table_width(self) -> int:
        """Return the width of the table.
        Returns:
            int: The width of the table.
        """
        return self._table_width

    def get_title(self) -> str:
        """Return the title of the table.
        Returns:
            str: The title of the table.
        """
        return self._title

    def put_table(self, is_menu: bool = False) -> None:
        """Format and display a table with the given dataset.
        Args:
            console (Terminal): The Terminal object used for displaying 
                the table.
            is_menu (bool, optional): Whether the table is being 
                displayed as a menu. Defaults to False.
        """
        if is_menu:
            self._number_records()
        self._calculate_widths()
        # Create an instance of Console_Table with the current 
        # instance's data
        table = ConsoleTable(self)

        # Display the table using the provided Terminal object
        table.display()

    def resize_columns(self, width_limit: int) -> None:
        """Resize column widths to fit within the specified width limit.
        Args:
            width_limit (int): The maximum allowable width for the 
                table.
        """
        # Calculate the total width to trim
        trim_length = self._table_width - width_limit
        # Continue trimming column widths until the trim length is 
        # satisfied
        while trim_length > 0:
            # Find the column with the maximum width
            widest_column = max(self._column_widths, 
                                key=self._column_widths.get)
            # Reduce the width of the widest column
            self._column_widths[widest_column] -= 1
        
            # Update the total width to be trimmed
            trim_length -= 1
            # Update the current table width
            self._table_width -= 1

    # Private Methods
    def _add_rjust_col_label(self, label: str | list[str] | set[str]) -> None:
        """Add one or more labels to the set of right-justified columns.
        Args:
            label: A string, list, or set of labels to add.
        """
        if isinstance(label, (list, set)):
            self._right_justified_columns.update(l.upper() for l in label)
        else:
            self._right_justified_columns.add(label.upper())

    def _calculate_widths(self) -> None:
        """Calculate the width of each column and the total table width 
            based on the dataset.
        Updates:
            Updates self._column_widths with the width of each column.
            Updates self._table_width with the total width of the table 
                including column separators.
        """
        self._column_widths = {
            key: max(len(key), 
                     max(len(str(record[key])) for record in self._dataset))
            for key in self._dataset[0].keys()
        }
        self._table_width = (sum(self._column_widths.values()) 
                             + 2 * (len(self._column_widths) - 1))

    def _capitalize_keys(self, data: list[dict[str, str]]) -> None:
        """Convert all dictionary keys in the dataset to uppercase.
        Args:
            data (list[dict[str, str]]): The list of dictionaries to process.
        Updates:
            Updates self._dataset with keys converted to uppercase and updates
            self._records_count with the new count of records.
        """
        # print(f"TRACE: Table. > init > capitalize_keys called with {data}")#####
        self._dataset = [{key.upper(): value for key, value in datum.items()} 
                         for datum in data]
        # print(f"TRACE: Table. > init > capitalize_keys self._dataset set as {self._dataset}")#####
        self._records_count = len(self._dataset)
        # print(f"TRACE: Table. > init > capitalize_keys self._records_count set as {self._records_count}")#####

    def _find_boundaries(self, 
                         column_index: int, 
                         positions_list: list[int], 
                         line: str) -> tuple[int, int]:
        """Find the start and end positions of a column in a line, 
            adjusting for whitespace.
        Args:
            column_index (int): The index of the column in the positions 
                list.
            positions_list (list[int]): A list of starting positions for 
                each column.
            line (str): The line of text to analyze.
        Returns:
            tuple[int, int]: A tuple containing the start and end 
                positions of the column.
        """
        # Determine the initial start and end positions
        start = positions_list[column_index]
        end = (positions_list[column_index + 1] 
               if column_index + 1 < len(positions_list) else len(line))

        # Adjust the start position to align with non-whitespace content
        if start < len(line):
            if line[start].isspace():
                while start < end and line[start].isspace():
                    start += 1
            else:
                while start > 0 and not line[start - 1].isspace():
                    start -= 1
        else:
            start = len(line)

        # Adjust the end position to align with non-whitespace content
        if end < len(line):
            while end > start and not line[end].isspace():
                end -= 1
            while end > start and line[end - 1].isspace():
                end -= 1
        else:
            end = len(line)

        return start, end

    def _find_column_positions(self, 
                               header_line: str, 
                               keys: list[str]) -> list[int]:
        """Find the starting positions of each column in the header 
            line.
        Args:
            header_line (str): The header line of the table containing 
                column names.
            keys (list[str]): A list of column names to locate in the 
                header line.
        Returns:
            list[int]: A list of starting positions for each column in 
                the header line.

        Raises:
            ValueError: If any key is not found in the header line.
        """
        positions = []
        for key in keys:
            try:
                positions.append(header_line.index(key))
            except ValueError as e:
                raise ValueError(
                    f"Column '{key}' not found in header line."
                ) from e
        return positions

    def _get_slice(self, 
                   column_index: int, 
                   positions_list: list[int], 
                   line: str) -> str:
        """Extract a slice of text representing a column from a line.
        Args:
            column_index (int): The index of the column to extract.
            positions_list (list[int]): A list of column positions in 
                the line.
            line (str): The line of text from which to extract the 
                column slice.
        Returns:
            str: The extracted slice of text for the specified column, 
                with leading and trailing whitespace removed.
        """
        start, end = self._find_boundaries(column_index, positions_list, line)
        return line[start:end].strip()

    def _number_records(self) -> None:
        """Add a numerical index to each record in the dataset and 
            update column labels.
        This method adds a numerical index to each record in the 
        dataset, with the index starting at 1. It also updates the 
        column labels to ensure proper right-justification for the index 
        column.
        """
        # Add a numerical index to each record, starting from 1
        self._dataset = [{"#": i + 1, **record} 
                         for i, record in enumerate(self._dataset)]
        # Update the column label for the index to ensure right-
        # justification
        self._add_rjust_col_label("#")

    def _read_table(self, table_string: str) -> None:
        """Parse a table from a string input and store it as a dataset.
        Args:
            table_string (str): The string input representing the table.
        """
        # print(f"TRACE: Table.init > readTable called with {table_string} >>>>>")#####
        # Split the input string into lines
        lines = table_string.splitlines()
        # print(f"TRACE: Table.init > readTable.lines: {lines}")#####

        # Non-empty string
        if len(lines) > 0:
            # print(f"TRACE: Table.init > readTable len(lines) > 0")#####
            
            # Extract column headers from the first line
            headers = lines[0].split()
            # print(f"TRACE: Table.init > readTable.headers: {headers}")#####
            
            # Find the positions of each column in the header line
            col_positions = self._find_column_positions(lines[0], headers)
            # print(f"TRACE: Table.init > readTable.col_positions: {col_positions}")#####

            # Parse each subsequent line into a dictionary with header keys
            self._dataset = [{header.upper(): self._get_slice(index, 
                                                              col_positions, 
                                                              line) 
                              for index, header in enumerate(headers)} 
                             for line in lines[1:]]
            # print(f"TRACE: Table.init > readTable _dataset set as {self._dataset}")#####
        
        # Empty string
        else:
            # print(f"TRACE: Table.init > readTable len(lines) !> 0")#####
            self._dataset = []
            # print(f"TRACE: Table.init > readTable _dataset set as {self._dataset}")#####
    
        # Update the count of records in the dataset
        self._records_count = len(self._dataset)
        # print(f"TRACE: Table.init > readTable _records_count set as {self._records_count}")#####
