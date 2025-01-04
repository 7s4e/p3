"""
Table Module

This module defines a `Table` class that allows for the creation and 
manipulation of data in a table.

Imports:
    Local module:
        from console import ConsoleTable: A class for handling display 
            of the table.

Class:
    Table: A class representing a table of data, with methods to create 
        and report on the table.

"""
# Local module import
from .console import ConsoleTable


class Table:
    """
    A class to represent and manipulate a table of data.

    The `Table` class allows for the creation of tables either from a 
    list of dictionaries (where each dictionary represents a table 
    record) or from a string representation of a table. The class 
    provides various methods for filtering, formatting, and retrieving 
    table data.

    Args:
        table_data: A list of dictionaries representing the table data. 
            Each dictionary corresponds to a row, with keys as column 
            labels and values as the corresponding cell data.
        table_string: A string representation of the table.
        title: The title of the table, which will be converted to 
            uppercase.
        rjust_columns: A string, list, or set of strings representing 
            the columns to be right-justified.
    
    Attributes:
        _ds: The table dataset as a list of dictionaries.
        _rec_ct: The number of records (rows) in the table.
        _rj_cols: A set of right-justified columns.
        _ttl: The title of the table, stored in uppercase.

    
        _column_widths (dict[str, int]): The width of each column in the 
            table.
        _table_width (int): The total width of the table including 
            column separators.

    Methods:
        count_records: Return the number of records in the dataset.
        filter_nonempty: Filter records for non-empty values of 
            specified key.
        filter_startswith: Filter records for values with a specified 
            key and prefix.
        get_column_widths: Return the widths of each column.
        get_headings: Return a dictionary of column headings.
        get_record: Retrieve a specific record by its index.
        get_rjust_columns: Return the set of right-justified columns.
        get_table_width: Return the total width of the table.
        get_title: Return the title of the table.
        put_table: Format and display the table using a terminal.
        resize_columns: Resize column widths to fit within a specified 
            width limit.
        _add_rj_col_lbl: Add one or more labels to the set of right-
            justified columns.
        _cap_keys: Capitalize dataset keys.
        _fnd_bnds: Find the start and end positions of record columns.
        _fnd_col_pos: Find the starting positions headings.
        _get_slc: Extract a slice of column from a line.
        _num_recs: Assign number to each record.
        _rd_tbl: Parse a table from a string input and set as dataset.    
        _set_wds: Set column and table widths.
"""
    def __init__(self, table_data: list[dict[str, str]] | None = None, 
                 table_string: str | None = None, title: str | None = None, 
                 rjust_columns: str | list[str] | set[str] | None = None
                 ) -> None:
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
        
        # Get table     
        if table_data: self._cap_keys(table_data)
        else: self._rd_tbl(table_string)
        
        # Set attributes
        self._ttl = title.upper() if title else None
        self._rj_cols = set()
        if rjust_columns: self._add_rj_col_lbl(rjust_columns)

    # Public Methods
    def count_records(self) -> int:
        """Return the number of records in the dataset."""
        return self._rec_ct

    def filter_nonempty(self, key: str) -> None:
        """
        Filter records for non-empty values of the specified key.

        Args:
            key: The key for the filtered values.
        
        Side effects:
            _ds: Replace with filtered dataset.
            _rec_ct: Update records count.
        """
        self._ds = [record for record in self._ds 
                    if (key.upper() not in record 
                        or record.get(key.upper(), '').strip())]
        self._rec_ct = len(self._ds)

    def filter_startswith(self, key: str, pfx: str) -> None:
        """
        Filter records for values of specified key having the specified 
            prefix.
        
        Args:
            key: The key for the filtered values.
            pfx: The prefix to match values.
        
        Side effects:
            _ds: Replace with filtered dataset.
            _rec_ct: Update records count.
        """
        self._ds = [record for record in self._ds 
                    if (key.upper() in record and 
                        record.get(key.upper(), '').startswith(pfx))]
        self._rec_ct = len(self._ds)

    def get_column_widths(self) -> dict[str, int]:
        """Return a dictionary of the column widths."""
        return self._col_wds

    def get_headings(self) -> dict[str, str]:
        """Return a dictionary of the column headings"""
        return {key: key for key in self._ds[0].keys()}

    def get_record(self, idx: int) -> dict[str, str]:
        """
        Retrieve a specific record from the dataset.

        Args:
            idx: The index of the record to retrieve.
        
        Returns:
            The record at the specified index as a dictionary.
    
        Raises:
            IndexError: If the index is out of range of the dataset.
        """
        if idx < 0 or idx >= len(self._ds):
            raise IndexError("Index out of range.")
        return self._ds[idx]

    def get_rjust_columns(self) -> set[str]:
        """Return a set of right-justified columns."""
        return self._rj_cols

    def get_table_width(self) -> int:
        """Return the width of the table."""
        return self._tbl_wd

    def get_title(self) -> str:
        """Return the title of the table."""
        return self._ttl

    def put_table(self, is_mnu: bool = False) -> None:
        """
        Pass table to `ConsoleTable` object for display.

        Args:
            is_mnu: Whether the table to display is for a menu.
        """
        # Prepare table
        if is_mnu: self._num_recs()
        self._set_wds()

        # Pass table to `ConsoleTable` object for display.
        table = ConsoleTable(self)
        table.display()

    def resize_columns(self, wd_lim: int) -> None:
        """
        Resize column widths to fit within the specified width limit.

        Args:
            wd_lim: The maximum allowable width for the table.
        
        Side effects:
            _col_wds: Update widths as trimmed.
            _tbl_wd: Update width as trimmed.
        """
        # Calculate the total width to trim
        trim_length = self._tbl_wd - wd_lim

        # Trim columns in loop to satisfy width limit
        while trim_length > 0:

            # Find the column with the maximum width
            widest_column = max(self._col_wds, key=self._col_wds.get)

            # Reduce and update widths
            self._col_wds[widest_column] -= 1
            trim_length -= 1
            self._tbl_wd -= 1

    # Private Methods
    def _add_rj_col_lbl(self, lbl: str | list[str] | set[str]) -> None:
        """
        Add one or more labels to the set of right-justified columns.

        Args:
            lbl: A string, list, or set of labels to add.
        
        Side effect:
            _rj_cols: Update set
        """
        if isinstance(lbl, (list, set)):
            self._rj_cols.update(l.upper() for l in lbl)
        else:
            self._rj_cols.add(lbl.upper())

    def _cap_keys(self, tbl: list[dict[str, str]]) -> None:
        """
        Capitalize table keys, set as dataset, count records.

        Args:
            tbl: The list of dictionaries to process.
        
        Side effects:
            _ds: Set table as dataset.
            _rec_ct: Set record count.
        """
        self._ds = [{key.upper(): value for key, value in datum.items()} 
                    for datum in tbl]
        self._rec_ct = len(self._ds)

    def _fnd_bnds(self, col_idx: int, pos_lst: list[int], ln: str
                  ) -> tuple[int, int]:
        """
        Find the start and end positions of a column in a line.

        Args:
            col_idx: The index of the column in the positions list.
            pos_lst: A list of starting positions for each column.
            ln: The line of text to analyze.
        
        Returns:
            A tuple a column's start and end positions of the column.
        """
        # Determine the initial start and end positions
        start = pos_lst[col_idx]
        end = pos_lst[col_idx + 1] if col_idx + 1 < len(pos_lst) else len(ln)

        # Adjust the start position to align with non-whitespace content
        if start < len(ln):
            if ln[start].isspace():
                while start < end and ln[start].isspace(): start += 1
            else:
                while start > 0 and not ln[start - 1].isspace(): start -= 1
        else:
            start = len(ln)

        # Adjust the end position to align with non-whitespace content
        if end < len(ln):
            while end > start and not ln[end].isspace(): end -= 1
            while end > start and ln[end - 1].isspace(): end -= 1
        else:
            end = len(ln)

        return start, end

    def _fnd_col_pos(self, hdr_ln: str, keys: list[str]) -> list[int]:
        """
        Find the start of each column in the header line.

        Args:
            hdr_ln: The header line with column names.
            keys: The list of column names in the header line.
        
        Returns:
            A list of starting positions for each column in the header 
                line.
        """
        positions = []
        for key in keys:
            positions.append(hdr_ln.index(key))
        return positions

    def _get_slc(self, col_idx: int, pos_lst: list[int], ln: str) -> str:
        """
        Extract the text of a column from a line.

        Args:
            col_idx: The index of the column to extract.
            pos_lst: A list of column positions in the line.
            ln: The line from which to extract the column slice.
        
        Returns:
            The substring for the specified column.
        """
        start, end = self._fnd_bnds(col_idx, pos_lst, ln)
        return ln[start:end].strip()

    def _num_recs(self) -> None:
        """
        Add a new column numbering the records.

        Side-effects:
            _ds: update dataset with new numbered, right-justified 
                column.
        """
        # Number each record, beginning at 1
        self._ds = [{"#": i + 1, **record} 
                    for i, record in enumerate(self._ds)]

        # Include in set of right-justified columns
        self._add_rj_col_lbl("#")

    def _rd_tbl(self, tbl_str: str) -> None:
        """
        Parse a table from a string input and set is as a dataset.

        Args:
            tbl_str (str): String input representing the table.

        Side effects:
            _ds: Set table as dataset.
            _rec_ct: Set record count.
        """
        # Split the input string into lines
        lines = tbl_str.splitlines()

        if len(lines) > 0:
            
            # Get header information
            headers = lines[0].split()
            col_pos = self._fnd_col_pos(lines[0], headers)

            # Parse each subsequent line into a dictionary with header keys
            self._ds = [{header.upper(): self._get_slc(index, col_pos, line) 
                         for index, header in enumerate(headers)} 
                        for line in lines[1:]]
        
        # Empty string
        else: self._ds = []
    
        # Update the count of records in the dataset
        self._rec_ct = len(self._ds)

    def _set_wds(self) -> None:
        """
        Calculate the column and tables.

        Side effects:
            _col_wds: Set widths mapped to their columns.
            _tbl_wd: Set width of the table including column padding.
        """
        self._col_wds = {key: max(len(key), max(len(str(record[key])) 
                                                for record in self._ds)) 
                         for key in self._ds[0].keys()}
        self._tbl_wd = (sum(self._col_wds.values()) + 
                        2 * (len(self._col_wds) - 1))
