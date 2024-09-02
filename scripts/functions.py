"""Functions module."""

import subprocess
from typing import Dict, List


def number_records(table: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Add a numerical index to each record in the table.

    Args:
        table: A list of dictionaries representing the data.

    Returns:
        A list of dictionaries with an added numerical index.
    """
    return [{"#": i + 1, **record} for i, record in enumerate(table)]


def put_table(title: str, 
              dataset: List[Dict[str, str]], 
              display_width: int = 36, 
              border_style: str = "=", 
              column_gap_size: int = 2, 
              right_justified_columns: List[str] = []) -> None:
    """Format and display a table with the given dataset.

    Args:
        title: The title of the table.
        dataset: A list of dictionaries representing the data.
        display_width: The width of the table display.
        border_style: The character used for the border.
        column_gap_size: The size of the gap between columns.
        right_justified_columns: List of columns that should be right-
            justified.
    """
    
    def calculate_column_widths(dataset: List[Dict[str, str]]
                                ) -> Dict[str, int]:
        """Calculate the width of each column based on the dataset.

        Args:
            dataset: A list of dictionaries representing the data.

        Returns:
            A dictionary mapping column names to their respective widths.
        """
        return {key: max(len(key), 
                         max(len(str(record[key])) for record in dataset)) 
                for key in dataset[0].keys()}

    def format_field(field: str, width: int, is_right_justified: bool) -> str:
        """Format a field within a table cell.

        Args:
            field: The field value to format.
            width: The width of the field.
            is_right_justified: Whether the field should be right-
                justified.

        Returns:
            The formatted field as a string.
        """
        return f"{field:{'>' if is_right_justified else '<'}{width}}"

    def format_record(record: Dict[str, str], 
                      column_widths: Dict[str, int], 
                      right_justified_columns: List[str]) -> Dict[str, str]:
        """Format an entire record for display in the table.

        Args:
            record: A dictionary representing a single record.
            column_widths: A dictionary mapping column names to their 
                respective widths.
            right_justified_columns: List of columns that should be 
                right-justified.

        Returns:
            A dictionary with formatted fields.
        """
        return {key: format_field(value, 
                                  column_widths[key], 
                                  key in right_justified_columns) 
                for key, value in record.items()}

    def make_padding(content_width: int, available_width: int) -> str:
        """Create padding for centering content.

        Args:
            content_width: The width of the content to center.
            available_width: The total available width.

        Returns:
            A string of spaces to be used as padding.
        """
        return " " * max(0, (available_width - content_width) // 2)

    def make_table(title: str, 
                   title_padding: str, 
                   table_padding: str, 
                   headings: Dict[str, str], 
                   column_widths: Dict[str, int], 
                   right_justified_columns: List[str], 
                   column_spacing: str, 
                   line_length: int, 
                   border_style: str) -> None:
        """Construct the table from the given components.

        Args:
            title: The title of the table.
            title_padding: Padding for the title.
            table_padding: Padding for the table.
            headings: A dictionary representing the table headings.
            column_widths: A dictionary mapping column names to their 
                respective widths.
            right_justified_columns: List of columns that should be 
                right-justified.
            column_spacing: Spacing between columns.
            line_length: The length of each line in the table.
            border_style: The character used for the border.

        Returns:
            A list of strings representing the rows of the table.
        """
        title_row = title_padding + title
        border_row = border_style * line_length
        header_row = (table_padding
                      + column_spacing.join(list(
                          format_record(headings, 
                                        column_widths, 
                                        right_justified_columns).values())))
        data_rows = [(table_padding 
                      + column_spacing.join(list(
                          format_record(record, 
                                        column_widths, 
                                        right_justified_columns).values()))) 
                     for record in dataset]
        return [title_row, border_row, header_row] + data_rows + [border_row]

    def print_table(table: List[str]) -> None:
        """Print the table to the console.

        Args:
            table: A list of strings representing the rows of the table.
        """
        print()
        print("\n".join(table))

    column_widths = calculate_column_widths(dataset)
    table_width = (sum(column_widths.values()) 
                   + column_gap_size * (len(column_widths) - 1))
    line_length = max(display_width, table_width)
    print_table(make_table(title, 
                           make_padding(len(title), line_length), 
                           make_padding(table_width, display_width), 
                           {key: key for key in dataset[0].keys()}, 
                           column_widths, 
                           right_justified_columns, 
                           " " * column_gap_size, 
                           line_length, 
                           border_style))


def query_integer(min_value: int, max_value: int, prompt: str) -> int:
    """Prompt the user to enter an integer within a specified range.

    Args:
        min_value: The minimum acceptable value.
        max_value: The maximum acceptable value.
        prompt: The prompt message displayed to the user.

    Returns:
        The integer value entered by the user.

    Raises:
        ValueError: If the input is not a valid integer.
    """
    while True:
        try:
            selection = int(input(prompt))
            if min_value <= selection <= max_value:
                return selection
            print(f"Enter a number between {min_value} and {max_value}.")
        except ValueError:
            print("Enter a valid number.")


def query_yes_no(prompt: str) -> bool:
    """Prompt the user to answer with 'y' or 'n'.

    Args:
        prompt: The prompt message displayed to the user.

    Returns:
        True if the user responds with 'y', False if the user responds 
            with 'n'.
    """
    while True:
        response = input(prompt).strip().lower()
        if response in {'y', 'n'}:
            return response == 'y'
        print("Respond with 'y' or 'n'.")


def read_table(input: str) -> List[Dict[str, str]]:
    """Parse a table from a string input.

    Args:
        input: The string input representing the table.

    Returns:
        A list of dictionaries representing the parsed table.
    """

    def find_boundaries(column_index: int, 
                        positions_list: List[int], 
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

        if line[start].isspace():
            while start < end and line[start].isspace(): start += 1
        else:
            while start > 0 and not line[start - 1].isspace(): start -= 1

        while end > start and not line[end].isspace(): end -= 1
        while end > start and line[end - 1].isspace(): end -= 1

        return start, end
    
    def find_column_positions(header_line: str, keys: List[str]) -> List[int]:
        """Find the positions of each column in the header line.

        Args:
            header_line: The header line of the table.
            keys: A list of keys representing the columns.

        Returns:
            A list of positions for each column.
        """
        return [header_line.index(key) for key in keys]
    
    def get_slice(column_index: int, 
                  positions_list: List[int], 
                  line: str) -> str:
        """Extract a slice of text representing a column from a line.

        Args:
            column_index: The index of the column.
            positions_list: A list of positions for each column.
            line: The line of text to slice.

        Returns:
            A string representing the extracted slice for the column.
        """
        start, end = find_boundaries(column_index, positions_list, line)
        return line[start:end].strip()
    
    lines = input.splitlines()
    keys = lines[0].split()
    positions_list = find_column_positions(lines[0], keys)

    return [{key: get_slice(index, positions_list, line) 
             for index, key in enumerate(keys)} 
            for line in lines[1:]]


def run_command(command: str, use_shell: bool =True) -> str:
    """Execute a shell command and return the output.

    Args:
        command: The command to run.
        use_shell: Whether to use the shell to execute the 
            command.

    Returns:
        The standard output from the command.

    Raises:
        RuntimeError: If the command fails, an exception is raised with 
            the error message.
    """
    result = subprocess.run(command, 
                            shell=use_shell, 
                            text=True, 
                            capture_output=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {result.stderr.strip()}")
    return result.stdout.strip()


def unmount_disk(disk: str) -> None:
    """Unmount all mount points associated with a specified disk.

    Args:
        disk: The disk identifier (e.g., 'sda1').
    """
    output = run_command(f"lsblk --output PATH,MOUNTPOINT /dev/{disk}")
    dataset = read_table(output)
    mounted_partitions = [record["PATH"] for record in dataset 
                          if record["MOUNTPOINT"] != ""]
    for partition in mounted_partitions:
        run_command(f"sudo umount {partition}")
