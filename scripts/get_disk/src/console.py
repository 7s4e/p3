"""Console module."""
# Standard library imports
from __future__ import annotations
from typing import Any, TYPE_CHECKING
import textwrap

# Third-party imports
from blessed import Terminal

# Local module import
if TYPE_CHECKING:
    from get_disk.src.table import Table


def clear_stdscr(con: Terminal) -> None:
    """Clear terminal screen and reset cursor to the home position.

    Args:
        con: The terminal object used to control screen operations.
    """
    print(con.home + con.clear)


def put_script_banner(con: Terminal, script_name: str) -> None:
    """Display reverse-video banner in terminal with the script name.

    Args:
        con: The terminal object used for formatting and display.
        script_name: The name of the script to be displayed in the 
            banner.
    """
    print(con.reverse(f"Running {script_name}...".ljust(con.width)))


class ConsolePrompt:
    """A class to manage console prompts and user input validation.

    This class facilitates prompting the user for input via the console, 
    with options for validating boolean and integer responses. It can 
    expect either a single keystroke or a full string input, and handle 
    input validation accordingly.

    Args:
        prompt: The message to display to the user.
        expect_keystroke: If True, expect a single keystroke input.
        validate_bool: If True, validate the input as a boolean 
            ('y' or 'n').
        validate_integer: If True, validate the input as an integer.
        integer_validation: Defines integer validation criteria. Can be 
            an upper limit (int) or a range (tuple of two ints).

    Attributes:
        _prompt: The prompt message to display to the user.
        _expect_keystroke: Flag indicating if a keystroke is expected.
        _validate_bool: Flag indicating if boolean validation is 
            enabled.
        _validate_integer: Flag indicating if integer validation is 
            enabled.
        _integer_validation: Validation criteria for integers.

    Methods:
        call(console): Prompt the user and return the validated 
            response.
        _get_response(): Get the user's response based on expected input 
            type.
        _validate_response(): Validate the user's input based on the 
            specified criteria.
        _read_string(): Capture a string input from the user.
        _read_keystroke(): Capture a single keystroke from the user.
        _check_integer_validation(): Validate the user's integer 
            response.
        _check_bool_validation(): Validate the user's boolean response.
        _put_prompt(leave_cursor_inline): Display the prompt message.
        _put_alert(alert): Display an alert message.
        _align_message(message): Align the message to the left for 
            display.
    """

    def __init__(self, 
                 prompt: str, 
                 expect_keystroke: bool = False, 
                 validate_bool: bool = False,
                 validate_integer: bool = False, 
                 integer_validation: int | tuple[int, int] | None = None
                 ) -> None:
        """Initialize the console prompt with specified parameters."""
        self._prompt = prompt
        self._expect_keystroke = expect_keystroke
        self._validate_bool = validate_bool
        self._validate_integer = validate_integer
        self._integer_validation = integer_validation

    # Public Method
    def call(self, console: Terminal) -> Any:
        """Prompt the user, validate the response, and return the valid 
            input.

        This method sets the console for user interaction and repeatedly 
        prompts the user for input until a valid response is received. 
        The validation is handled by the `_validate_response` method. 
        Once the input is valid, it returns the validated response.

        Args:
            console: The console or terminal instance for user 
                interaction.

        Returns:
            Any: The validated response from the user, which could be a 
                string, integer, or boolean, depending on the validation 
                type.
        """
        self._con = console
        valid = False
        while not valid:
            self._get_response()
            valid = self._validate_response()
        return self._response

    # Private Methods
    def _check_bool_validation(self) -> bool:
        """Validate the user's boolean response based on 'y' or 'n' 
            input.

        This method checks whether the user's response is a valid 'y' or 
        'n'. If the input is valid, it converts 'y' to `True` and 'n' to 
        `False`, storing the result in `_response`. If the input is 
        invalid, an alert is displayed prompting the user to respond 
        with 'y' or 'n'.

        Returns:
            bool: True if the response is valid ('y' or 'n'), False 
                otherwise.
        """
        if self._response.lower() in {"y", "n"}:
            self._response = self._response.lower() == "y"
            return True

        self._put_alert("Respond with 'y' or 'n'.")
        return False

    def _check_integer_validation(self) -> bool:
        """Validate the user's integer response based on the expected 
            criteria.

        This method validates the user's response, ensuring it is a 
        valid integer and meets the conditions specified by 
        `_integer_validation`. The validation can either check for any 
        integer, a maximum bound, or a range of values.

        If the validation fails, an alert is displayed with the 
        appropriate message.

        Returns:
            bool: True if the response is valid, False otherwise.
        """
        if self._integer_validation is None:
            try:
                if isinstance(int(self._response), int):
                    return True
            except ValueError:
                pass
            self._put_alert("Enter a valid number.")
            return False

        if isinstance(self._integer_validation, int):
            if 0 <= int(self._response) < self._integer_validation:
                return True
            self._put_alert("Response is out of range.")
            return False

        lo, hi = self._integer_validation
        if lo <= int(self._response) <= hi:
            return True

        self._put_alert(f"Enter a number between {lo} and {hi}.")
        return False

    def _get_response(self) -> None:
        """Prompt the user and capture their response.

        This method displays a prompt to the user and captures either a 
        single keystroke or a full string input, depending on the 
        `_expect_keystroke` flag. The response is stored in the 
        `_response` attribute.

        If `_expect_keystroke` is True, a keystroke is read and stored; 
        otherwise, a string input is captured.
        """
        if self._expect_keystroke:
            self._put_prompt(leave_cursor_inline=False)
            self._response = self._read_keystroke()
        else:
            self._put_prompt(leave_cursor_inline=True)
            self._response = self._read_string()

    def _print_message(self, message: str, leave_cursor_inline: bool) -> None:
        """Print a centered, wrapped message to the console.

        This method displays a message centered within the console 
        width. If the message is longer than the display width, it is 
        wrapped. The cursor can either remain inline with the message or 
        move to the next line based on the `leave_cursor_inline` 
        argument.

        Args:
            message: The message to be printed.
            leave_cursor_inline: If True, the cursor remains inline with 
                a trailing space after the message. If False, the cursor 
                moves to the next line after printing.
        """
        display_width = min(self._con.width, 79)
        padding = " " * ((self._con.width - display_width) // 2)
        print(textwrap.fill(message, 
                            width=display_width, 
                            initial_indent=padding, 
                            subsequent_indent=padding), 
              end=" " if leave_cursor_inline else "\n", 
              flush=True)

    def _put_alert(self, alert: str) -> None:
        """Display an alert message to the user in red.

        This method prints the provided alert message to the console in 
        red. The cursor moves to the next line after being displayed.

        Args:
            alert: The alert message to be displayed.
        """
        self._print_message(self._con.red(alert), leave_cursor_inline=False)

    def _put_prompt(self, leave_cursor_inline: bool) -> None:
        """Display the prompt message to the user.

        This method prints the prompt message to the console in bright 
        yellow. The cursor's position after displaying the prompt is 
        determined by the `leave_cursor_inline` argument.

        Args:
            leave_cursor_inline: If True, the cursor remains inline with 
                a trailing space; if False, it moves to the next line 
                after the prompt.
        """
        self._print_message(self._con.bright_yellow(self._prompt), 
                            leave_cursor_inline=leave_cursor_inline)
        
    def _read_keystroke(self) -> str:
        """Read and return a single keystroke from the user.

        This method captures a single keypress from the user, operating in 
        'cbreak' mode, where input is read one character at a time without 
        waiting for a newline. The cursor is hidden during the input.

        Returns:
            str: A string representation of the key pressed.
        """
        with self._con.cbreak(), self._con.hidden_cursor():
            key = self._con.inkey()
        return repr(key)

    def _read_string(self) -> str:
        """Capture a string input from the user, handling enter and 
            backspace keys.

        This method reads characters from the user input in a terminal 
        session, with special handling for 'Enter' (which ends the 
        input) and 'Backspace' (which removes the last entered 
        character). The input is captured one character at a time until 
        'Enter' is pressed.

        Returns:
            str: The string input provided by the user.
        """
        user_input = []
        with self._con.cbreak():
            while True:
                key = self._con.inkey()
                if key.is_sequence and key.name == 'KEY_ENTER':
                    break
                if key.is_sequence and key.name == 'KEY_BACKSPACE':
                    if user_input:
                        user_input.pop()
                        self._put_prompt(leave_cursor_inline=True)
                        print(self._con.move_left(), end='', flush=True)
                else:
                    user_input.append(key)
                    print(self._con.green(key), end='', flush=True)
        print()
        return ''.join(user_input)

    def _validate_response(self) -> bool:
        """Validate the response based on the defined validation type.

        This method checks the response using either a boolean or 
        integer validation, depending on the internal flags 
        `_validate_bool` or `_validate_integer`. If neither flag is set, 
        it defaults to returning `True`.

        Returns:
            bool: The result of the validation check, or True if no 
            validation is required.
        """
        if self._validate_bool:
            return self._check_bool_validation()
        if self._validate_integer:
            return self._check_integer_validation()
        return True


class ConsoleTable:
    """A class to represent a terminal-based table.

    Args:
        data: An instance of the `Table` class containing the data to be 
            displayed in the terminal.

    Attributes:
        _data: The table data provided at initialization.
        _borders: A dictionary defining the table's border characters.

    Methods:
        display(console): Display the table on the terminal.
        _draw_row(row_type, index): Draw a specific row in the table.
        _draw_table(record_count): Draw the full table structure.
        _get_row_ends(row_type, is_line_type): Get row ends and padding.
        _get_text_content(row_type, index): Retrieve text content for a 
            row.
        _process_text_content(row_type, content, rjust_col): Process row 
            content into formatted text cells.
        _set_dimensions(): Set display and table dimensions based on 
            terminal width.
    """

    def __init__(self, data: Table) -> None:
        """Initialize the TerminalTable with data and default borders."""
        self._data = data
        self._borders = {"top": {"left": "╔", "fill": "═", "right": "╗"}, 
                         "inner": {"left": "╟", "fill": "─", "right": "╢"}, 
                         "bottom": {"left": "╚", "fill": "═", "right": "╝"},
                         "side": "║"}

    # Public Method
    def display(self, console: Terminal) -> None:
        """Display the table on the terminal.

        This method initializes the terminal settings, adjusts the table 
        dimensions, and draws the table on the screen by rendering its 
        borders, title, headings, and records.

        Args:
            con: An instance of the `Terminal` class, used to handle 
                terminal display settings and styling.
        """
        self._con = console
        self._set_dimensions()
        self._draw_table(self._data.count_records())

    # Private Methods
    def _draw_row(self, row_type: str, index: int | None = None) -> None:
        """Draw a specific row in the table based on the row type.

        This method draws different types of rows such as borders (top, 
        inner, bottom), and text rows (title, headings, or a record). 
        The row content is dynamically generated based on the 
        `row_type`. For "record" rows, the content can be right-
        justified based on column definitions.

        Args:
            row_type: A string indicating the type of row to draw. Valid 
                types include "top", "inner", "bottom" (for line types) 
                and "title", "headings", "record" (for text types).
            index: An integer index is required when drawing a "record" 
                row to specify which record to draw. Defaults to None.
        """
        line_types = ["top", "inner", "bottom"]
        text_types = ["title", "headings", "record"]
    
        rjust_col = (self._data.get_rjust_columns() 
                     if row_type == "record" else {})

        margin = " " * self._margin_size

        left, right, gap = self._get_row_ends(row_type, 
                                              row_type in line_types)

        content = (self._get_text_content(row_type, index)
                   if row_type in text_types
                   else self._borders[row_type]["fill"])

        cells = (self._process_text_content(row_type, content, rjust_col)
                 if row_type in text_types
                 else [
                     f"{self._con.blue(content * (self._table_width + 2))}"])

        print(f"{margin}{left}{gap}{'  '.join(cells)}{gap}{right}")

    def _draw_table(self, record_count: int) -> None:
        """Draw full table with borders, title, headings, and records.

        This method draws the table structure by sequentially rendering 
        the top border, title row, inner border, headings, and a 
        specified number of records. It finishes by rendering the bottom 
        border of the table.

        Args:
            record_count: The number of record rows to draw.
        """
        self._draw_row("top")
        self._draw_row("title")
        self._draw_row("inner")
        self._draw_row("headings")
        for i in range(record_count):
            self._draw_row("record", i)
        self._draw_row("bottom")

    def _get_row_ends(self, 
                      row_type: str, 
                      is_line_type: bool) -> tuple[str, str, str]:
        """Generate a row's left and right ends  and the inner padding.

        This function returns the left and right end characters for a 
        row based on whether the `row_type` is a line type or not. If 
        the row is a line type, the left and right ends are styled as 
        borders from the `self._borders` dictionary, otherwise, both 
        left and right are a default 'side' border. Non-line, text-type 
        rows have a single space as padding.

        Args:
            row_type: The type of the row, used to determine the border style.
            is_line_type: A boolean flag indicating if the row is a line type
                (used for borders) or a content row.

        Returns:
            A tuple of three strings:
                - The left border (styled).
                - The right border (styled).
                - The padding between cells (either a space or an empty 
                    string).
        """
        if is_line_type:
            left_end = f"{self._con.blue(self._borders[row_type]['left'])}"
            right_end = f"{self._con.blue(self._borders[row_type]['right'])}"
            padding = ""
        else:
            left_end = right_end = f"{self._con.blue(self._borders['side'])}"
            padding = " "

        return left_end, right_end, padding

    def _get_text_content(self, 
                          row_type: str, 
                          index: int | None = None) -> str | dict[str, str]:
        """Retrieve the text content for a specific type of table row.

        This method returns the text content for the specified 
        `row_type`, which can be the table's title, headings, or a 
        specific data record. For "record" rows, an `index` must be 
        provided to retrieve the appropriate row data.

        Args:
            row_type: The type of row to retrieve. Can be "title", 
                "headings", or "record".
            index: The index of the record to retrieve, required if 
                `row_type` is "record".
        
        Returns:
            The content of the row, either as:
                - A string for "title" row.
                - A dictionary of column headers for "headings" row.
                - A dictionary representing a specific data record for 
                    "record" row.
        
        Raises:
            ValueError: If `row_type` is "record" and no `index` is 
                provided.
        """
        match row_type:
            case "title":
                return self._data.get_title()
            case "headings":
                return self._data.get_headings()
            case "record":
                if index is None:
                    raise ValueError(
                        "Index must be provided for 'record' row_type")
                return self._data.get_record(index)

    def _process_text_content(self, 
                              row_type: str, 
                              content: str | dict[str, str], 
                              rjust_col: set) -> list[str]:
        """Process the content of a table row into formatted text cells.

        Depending on the `row_type`, this method processes and formats 
        text content for each cell of the row. For the title row, it 
        centers the text and applies a terminal reverse effect. For 
        headings, it centers the text and underlines it. For other rows 
        [records], it adjusts the text alignment based on the column 
        width, right-justifying the columns in `rjust_col`.

        Args:
            row_type: The type of row being processed. Can be "title", 
                "headings", or other string representing a regular data 
                row ["records"].
            content: Either a string (for title row) or a dictionary 
                where keys are column names and values are the cell 
                content.
            rjust_col: A set of keys representing columns that should be 
                right-justified.

        Returns:
            A list of formatted strings, each representing a cell in the 
            row.
        """
        cells = []

        if row_type == "title":
            # Format the title row by centering the content and applying 
            # reverse style.
            cell = f"{self._con.reverse(content.center(self._table_width))}"
            cells.append(cell)
        else:
            # Iterate over content dictionary and format each cell.
            for key, value in content.items():
                width = self._column_widths[key]
                if row_type == "headings":
                    # Center and underline heading text.
                    cell = f"{self._con.underline(value.center(width))}"
                else:
                    # Right-justify or left-justify based on column key.
                    cell = (f"{value.rjust(width)}" if key in rjust_col 
                            else f"{value.ljust(width)}")
                cells.append(cell)
        
        return cells

    def _set_dimensions(self) -> None:
        """Set display and table dimensions based on the terminal width.

        This method determines the display width and table width 
        relative to the terminal's current width. If the table width 
        exceeds the available display space, it resizes the columns to 
        fit within the display. The column widths are then updated for 
        rendering the table.

        Side effects:
            - Updates `self._display_width` to the terminal width, 
                capped at 79.
            - Updates `self._margin_size` to center the content if 
                necessary.
            - Updates `self._table_width` based on the current table 
                data.
            - Resizes table columns if the table width exceeds available 
                space.
            - Updates `self._column_widths` to reflect the resized table 
                layout.
        """
        self._display_width = min(self._con.width, 79)
        self._margin_size = (self._con.width - self._display_width) // 2
        self._table_width = self._data.get_table_width()

        table_space = self._display_width - 4  # For borders and padding
        if self._table_width > table_space:
            self._data.resize_columns(table_space)
            self._table_width = self._data.get_table_width()

        self._column_widths = self._data.get_column_widths()
