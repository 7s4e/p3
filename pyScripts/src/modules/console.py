"""
Console Module

This module defines classes for handling console-based user interactions 
and displaying formatted tables in a terminal.

Imports:
    - Standard library:
        - subprocess: For running shell commands.
        - sys: For redirecting command output to the standard output.
    - Local modules:
        - Table: A helper class for parsing and managing table-like 
          command output.


Imports:
    - Standard library:
        - from __future__ import annotations: Postpones the evaluation 
          of type annotations, allowing forward references without 
          string literals.
        - from re import fullmatch: Provides support for regular expressions, 
          enabling pattern matching and text manipulation.
        - from sys import stdout: Provides access to the standard output 
          stream, used for printing to the terminal.
        - from textwrap import fill: Provides text wrapping functionality 
          for formatting text, especially for console output.
        - from typing import Any, TYPE_CHECKING:
            - Any: Represents any valid Python object type in type 
              annotations.
            - TYPE_CHECKING: Used for conditional imports to prevent 
              circular dependencies during runtime, primarily for type 
              checking.

    - Third-party:
        - from blessed import Terminal: Manages terminal output, 
          including color handling, cursor movement, and screen 
          clearing.

    - Local modules:
        - snake_to_camel: A utility function for converting snake_case 
          strings to camelCase.
        - truncate_string: A utility function for truncating strings to 
          a specified length.
        - if TYPE_CHECKING:
            - Table: Conditionally imported for static type checking to 
              avoid circular imports at runtime.

Classes:
    ConsoleBase: The base class that initiates an instance of the 
        Terminal class.
    Console: A subclass of ConsoleBase, providing static methods for 
        console-related operations.
    ConsolePrompt: A subclass of ConsoleBase, responsible for handling 
        user prompts with validation for user responses.
    ConsoleTable: A subclass of ConsoleBase, responsible for displaying 
        tables in the terminal.

Constants:
    BORDERS (dict): Defines the border characters for table layout.
    FORMATTING_ALLOCATION (dict): Defines the length of formatting
        sequences for different styles.
"""
# Standard library imports
from __future__ import annotations
from re import fullmatch
from sys import stdout
from textwrap import fill
from typing import Any, TYPE_CHECKING

# Third-party import
from blessed import Terminal

# Local imports
from .utilities import snake_to_camel, truncate_string
if TYPE_CHECKING:
    from .table import Table


# Constants
BORDERS = {"top": {"left": "╔", "fill": "═", "right": "╗"}, 
           "inner": {"left": "╟", "fill": "─", "right": "╢"}, 
           "bottom": {"left": "╚", "fill": "═", "right": "╝"}, 
           "side": "║"}

FORMATTING_ALLOCATION = {"blink": len("[blink][/blink]"), 
                        "blue": len("[blue][/blue]"), 
                        "red": len("[red][/red]"), 
                        "reverse": len("[reverse][/reverse]"), 
                        "yellow": len("[yellow][/yellow]")}


class ConsoleBase:
    """
    A base class for managing terminal-based user interfaces.

    This class initializes a `Terminal` object to interact with the 
    terminal for input/output operations. It can be extended to provide 
    functionality for handling prompts, user input, and output 
    formatting.

    Attributes:
        _trm: The Terminal object used for interacting with the console.
    """
    def __init__(self):
        self._trm = Terminal()


class Console(ConsoleBase):
    """
    A class for handling terminal operations.

    This class inherits from `ConsoleBase` and provides static methods 
    manipulating the terminal screen.

    Methods:
        clear_screen: Clears the terminal screen and resets the cursor 
            to the home position.
        put_script_banner: Displays a reverse-video banner with the 
            script name.
    """
    @staticmethod
    def clear_screen() -> None:
        """Clear terminal screen and reset cursor to the home position.
        """
        term = ConsoleBase()._trm
        print(term.home + term.clear)
    
    @staticmethod
    def put_script_banner(script_name: str) -> None:
        """Display reverse-video banner with the script name.

        Args:
            script_name: The name of the script to be displayed in the 
                banner.
        """
        term = ConsoleBase()._trm
        script_name = snake_to_camel(script_name)
        print(term.reverse(f"Running {script_name}...".ljust(term.width)))


class ConsolePrompt(ConsoleBase):
    """
    A class to manage console prompts and user input validation.

    This class facilitates prompting the user for input via the console, 
    with options for validating boolean and integer responses. It can 
    expect either a single keystroke or a full string input, and handle 
    input validation accordingly.

    Args:
        cue: The message to display to the user.
        expect_keystroke: If True, expect a single keystroke input.
        validate_bool: If True, validate the input as a boolean ('y' or 
            'n').
        validate_integer: If True, validate the input as an integer.
        integer_validation: Defines integer validation criteria. Can be 
            an upper limit (int) or a range (tuple of two ints).

    Attributes:
        _cue: The message to display to the user.
        _e_ct: A tally of various errors until validation.
        _exp_kst: Flag indicating if a keystroke is expected.
        _int_vld: Validation criteria for integers.
        _trm: blessed.Terminal inherited from ConsoleBase
        _val_bool: Flag indicating if boolean validation is 
            enabled.
        _val_int: Flag indicating if integer validation is 
            enabled.
        _vld_resp: The user's validated response.

    Methods:
        call: Prompt the user and return the validated response.
        _back_n_lines: Delete and move cursor up 'n' lines.
        _chk_bool_vld: Validate the user's boolean response.
        _chk_int_vld: Validate the user's integer response.
        _get_resp: Get the user's response based on expected input type.
        _print_msg: Print formatted message to stdout.
        _put_alert: Display an alert message.
        _put_prompt: Display the cue message.
        _read_kst: Capture a single keystroke from the user.
        _read_str: Capture a string input from the user.
        _val_resp: Validate the user's input based on the specified 
            criteria.
    """

    def __init__(self, cue: str, expect_keystroke: bool = False, 
                 validate_bool: bool = False, validate_integer: bool = False, 
                 integer_validation: int | tuple[int, int] | None = None
                 ) -> None:

        # Type validation
        if not isinstance(cue, str):
            raise TypeError("Expected `str` for 'cue'")
        if not isinstance(expect_keystroke, bool):
            raise TypeError("Expected `bool` for 'expect_keystroke'")
        if not isinstance(validate_bool, bool):
            raise TypeError("Expected `bool` for 'validate_bool'")
        if not isinstance(validate_integer, bool):
            raise TypeError("Expected `bool` for 'validate_integer'")
        if (integer_validation is not None 
            and not (isinstance(integer_validation, int) 
                     and not isinstance(integer_validation, bool)
                     or isinstance(integer_validation, tuple))):
            raise TypeError("Expected `int`, `tuple[int, int]`, or `None` " +
                            "for 'integer_validation'")

        # Value validation
        if validate_bool and validate_integer:
            raise ValueError("Both 'validate_bool' and 'validate_integer' " + 
                             "cannot be `True`")
        if integer_validation is not None:
            if not validate_integer:
                raise ValueError("With 'integer_validation', " + 
                                 "'validate_integer' must be `True`")
            if isinstance(integer_validation, int):
                if integer_validation < 0:
                    raise ValueError("Range for 'integer_validation' must "
                                     "be positive")
            else:
                if len(integer_validation) != 2:
                    raise ValueError("The 'integer_validation' `tuple` " + 
                                     "must have two elements")
                if integer_validation[0] > integer_validation[1]:
                    raise ValueError("The second value of the " + 
                                     "'integer_validation' `tuple` cannot " + 
                                     "be less than the first")

        # Initialize base and assign validated attributes
        super().__init__()
        self._cue = cue
        self._exp_kst = expect_keystroke
        self._val_bool = validate_bool
        self._val_int = validate_integer
        self._int_vld = integer_validation
        self._e_ct = {"yes/no": 0, "NaN": 0, "OOR": 0, "OOL": 0}

    # Public Method
    def call(self) -> Any:
        """
        Get, validate, and return user input.

        Returns:
            Any: The validated response from the user, which could be a 
                string, integer, or boolean, depending on the validation 
                type.
        """
        # Execute validation loop
        valid = False
        while not valid:
            self._get_resp()
            valid = self._val_resp()
        
        # Reset error count and return validated response
        self._e_ct = {error: 0 for error in self._e_ct}
        return self._vld_resp

    # Private Methods
    def _back_n_lines(self, n: int) -> None:
        """
        Move cursor back `n` lines and clear each line.

        This method uses ANSI escape codes to move the cursor up 
        (`\033[F`) and to clear the contents of each line (`\033[K`). 
        The changes are flushed to the terminal to ensure immediate 
        application.
        
        Args:
            n: The number of lines to move back and clear.
        
        Raises:
            ValueError: If `n` is negative, as moving backwards a 
                negative number of lines is invalid.
        """
        if n < 0:
            raise ValueError("Number of lines cannot be negative.")
        for i in range(n):
            stdout.write("\033[F")
            stdout.write("\033[K")
        stdout.flush()

    def _chk_bool_vld(self) -> bool:
        """
        Validate user's response as 'yes' or 'no'.

        Side effect:
            _vld_resp: sets boolean as validated response.

        Returns:
            bool: True if the response is valid, False otherwise.
        """
        # Valid response sets _vld_response attribute
        if self._user_resp.lower() in {"y", "n"}:
            self._vld_resp = self._user_resp.lower() == "y"
            return True
        
        # Invalid response alerts user        
        self._e_ct["yes/no"] += 1
        self._put_alert("Respond with 'y' or 'n'", self._e_ct["yes/no"])
        return False

    def _chk_int_vld(self) -> bool:
        """
        Validate user's response against available criterion.

        The method uses regular expression for matching:
            r'...': denotes raw literal string
            -?: indicates optional negative sign
            [0-9]+: matches one or more repetitions of any single digit

        Side effect:
            _vld_resp: sets integer as validated response.

        Returns:
            bool: True if the response is valid, False otherwise.
        """
        # Invalid alert if not a number
        if not bool(fullmatch(r'-?[0-9]+', self._user_resp)):
            self._e_ct["NaN"] += 1
            self._put_alert("Enter a valid number", self._e_ct["NaN"])
            return False
        
        # Integer validated against integer validation attribute
        response = int(self._user_resp)
        match self._int_vld:

            # Criterion is single integer defining range
            case int() as range:
                if response < 0 or response >= range:
                    self._e_ct["OOR"] += 1
                    self._put_alert("Response is out of range", 
                                    self._e_ct["OOR"])
                    return False
            
            # Crierion is tuple of lower and upper limits
            case tuple() as limits:
                low, high = limits
                if response < low or response > high:
                    self._e_ct["OOL"] += 1
                    self._put_alert(f"Enter a number between {low} and " +
                                    f"{high}", self._e_ct["OOL"])
                    return False
            
            # No integer validation criteria
            case None: pass
        
        # Valid response sets _vld_response attribute
        self._vld_resp = str(response)
        return True

    def _get_resp(self) -> None:
        """Prompt the user and capture input."""
        # If keystroke expected, read it after prompting
        if self._exp_kst:
            self._put_prompt(keep_cur_inline=False)
            self._read_kst()
        
        # If string expected, show it inline with cue.
        else:
            self._put_prompt(keep_cur_inline=True)
            self._read_str()

    def _print_message(self, msg: str, fmt_alloc: int, keep_cur_inline: bool
                       ) -> None:
        """
        Print left-justfied, wrapped message in center of console.

        Args:
            msg: The message to be printed.
            fmt_alloc: Allocation required for formatting text styles
            keep_cur_inline: If True, the cursor remains inline with 
                a trailing space after the message. If False, the cursor 
                moves to the next line after printing.
        """
        # Set width to display message and padding to center width
        display_width = min(self._trm.width, 79)
        padding = " " * ((self._trm.width - display_width) // 2)

        # Print textwrapped, padded message and deposit cursor
        print(fill(msg, width=(display_width + fmt_alloc + len(padding)), 
                   initial_indent=padding, subsequent_indent=padding), 
              end=" " if keep_cur_inline else "\n",
              flush=True)

    def _put_alert(self, alert: str, err_ct: int) -> None:
        """
        Display alert message with escalating formatting.

        Args:
            alert: The alert message to be displayed.
            err_ct: The number of times alert is triggered without 
                validation.
        """
        # Delete cue or both cue and last alert message
        self._back_n_lines(min(err_ct, 2))

        # First alert in red
        if err_ct >= 1:
            alert = self._trm.red(alert)
            fmt_alloc = FORMATTING_ALLOCATION["red"]
        
        # Second alert adds reverse-video effect
        if err_ct >= 2:
            alert = self._trm.reverse(alert)
            fmt_alloc += FORMATTING_ALLOCATION["reverse"]
        
        # Third alert adds blinking effect
        if err_ct >= 3:
            alert = self._trm.blink(alert)
            fmt_alloc += FORMATTING_ALLOCATION["blink"]
        
        # Subsequent alerts show invalid input
        if err_ct >= 4:
            alert = (self._trm.red(f"'{self._user_resp}' is invalid. ") + 
                     alert)
        
        # Alert printed
        if err_ct > 0:
            self._print_message(alert, fmt_alloc, keep_cur_inline=False)

    def _put_prompt(self, keep_cur_inline: bool) -> None:
        """
        Display the prompt cue to the user.

        Args:
            keep_cur_inline: If True, the cursor remains inline with 
                a trailing space; if False, it moves to the next line 
                after the prompt.
        """
        self._print_message(self._trm.yellow(self._cue), 
                            FORMATTING_ALLOCATION["yellow"], 
                            keep_cur_inline=keep_cur_inline)

    def _read_kst(self) -> None:
        """
        Read a single keystroke, filtering for printable characters.

        This method captures input in raw mode using the `cbreak` and 
        `hidden_cursor` contexts to disable line buffering and hide the 
        cursor. It ensures that only printable ASCII characters (codes 
        32 to 126) or the Enter key (code 10) are accepted. If the Enter 
        key is pressed, the response is stored as an empty string.

        Side effect:
            _user_resp: sets user response.
        """
        # Initialize values
        key = None
        miskey_ct = -1
        self._user_resp = ""

        # While loop with contexts filtering for printable characters
        with self._trm.cbreak(), self._trm.hidden_cursor():
            while key is None or not (32 <= code <= 126 or code == 10):
                key = self._trm.inkey()
                try:
                    code = ord(key)
                except:
                    key = None
                    miskey_ct += 1
                    self._put_alert("Input not printable", miskey_ct)
        
        # Set user response
        self._user_resp = str(key if code != 10 else "")

    def _read_str(self) -> None:
        """Read a user input string character by character, handling 
            backspace and printable characters, and store the final 
            input in `_user_response`.

        This method operates in raw mode using the `cbreak()` context of 
        the terminal, allowing it to capture each keystroke as the user 
        types. Backspace characters remove the last typed character from 
        the display and the internal response, while printable 
        characters (ASCII codes 32-126) are appended to the response and 
        printed in green. The input ends when the Enter key (ASCII code 
        10) is pressed.

        Attributes:
            _user_response (str): The final user input string captured.
        """
        key = None
        response = []

        with self._trm.cbreak():
            while key is None or key_code != 10:  # Wait New Line/Enter
                key = self._trm.inkey()
                try:
                    key_code = ord(key)
                except:
                    key = None
                else:
                    if key_code == 8 or key_code == 127:  # Backspace
                        if response:
                            response.pop()
                            bckspce_sequence = ("\b \b" * 
                                                len(self._trm.green("x")))
                            print(bckspce_sequence, end="", flush=True)
                    elif 32 <= key.code <= 126:  # Printable chars
                        response.append(str(key))
                        formatted_char = self._trm.green(str(key))
                        print(formatted_char, end="", flush=True)
            print()  # Move to next line after Enter

        self._user_resp = "".join(response)


    def _val_resp(self) -> bool:
        """Validate the response based on the defined validation type.

        This method checks the response using either a boolean or 
        integer validation, depending on the internal flags 
        `_val_bool` or `_val_int`. If neither flag is set, 
        it defaults to returning `True`.

        Returns:
            bool: The result of the validation check, or True if no 
            validation is required.
        """
        if self._val_bool:
            return self._chk_bool_vld()
        if self._val_int:
            return self._chk_int_vld()
        self._vld_resp = self._user_resp
        return True


class ConsoleTable(ConsoleBase):
    """A class to represent a terminal-based table.

    Args:
        data: An instance of the `Table` class containing the data to be 
            displayed in the terminal.

    Attributes:
        _trm: blessed.Terminal inherited from ConsoleBase
        _data: The table data provided at initialization.
        _borders: A dictionary defining the table's border characters.

    Methods:
        display(): Display the table on the terminal.
        _draw_row(row_type, index): Draw a specific row in the table.
        _draw_table(record_count): Draw the full table structure.
        _get_row_ends(row_type, is_line_type): Get row ends and padding.
        _get_row_content(row_type, index): Retrieve text content for a 
            row.
        _process_row_content(row_type, content, rjust_col): Process row 
            content into formatted text cells.
        _set_dimensions(): Set display and table dimensions based on 
            terminal width.
    """

    def __init__(self, data: Table) -> None:
        # Lazy import avoids circular import and enables runtime type 
        # validation
        from modules.table import Table  # for test_console_table_constructor.py
        if not isinstance(data, Table):
            raise TypeError("Expected `Table` for 'data'")
        
        # Base initialization and attribute assignment
        super().__init__()
        self._data = data


    # Public Method
    def display(self) -> None:
        """Display the table on the terminal.

        This method initializes the terminal settings, adjusts the table 
        dimensions, and draws the table on the screen by rendering its 
        borders, title, headings, and records.

        Args:
            con: An instance of the `Terminal` class, used to handle 
                terminal display settings and styling.
        """
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

        content = (self._get_row_content(row_type, index)
                   if row_type in text_types
                   else BORDERS[row_type]["fill"])

        cells = (self._process_row_content(row_type, content, rjust_col)
                 if row_type in text_types
                 else [
                     f"{self._trm.blue(content * (self._table_width + 2))}"])

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

    def _get_row_content(self, 
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
                return self._data.get_record(index)

    def _get_row_ends(self, 
                      row_type: str, 
                      is_line_type: bool) -> tuple[str, str, str]:
        """Generate a row's left and right ends  and the inner padding.

        This function returns the left and right end characters for a 
        row based on whether the `row_type` is a line type or not. If 
        the row is a line type, the left and right ends are styled as 
        borders from the `BORDERS` dictionary, otherwise, both 
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
            left_end = f"{self._trm.blue(BORDERS[row_type]['left'])}"
            right_end = f"{self._trm.blue(BORDERS[row_type]['right'])}"
            padding = ""
        else:
            left_end = right_end = f"{self._trm.blue(BORDERS['side'])}"
            padding = " "
        return left_end, right_end, padding

    def _process_row_content(self, 
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
            cntnt = truncate_string(content, self._table_width)
            cell = f"{self._trm.reverse(cntnt.center(self._table_width))}"
            cells.append(cell)
        else:
            # Iterate over content dictionary and format each cell.
            for key, value in content.items():
                width = self._column_widths[key]
                vlu = truncate_string(value, width)
                if row_type == "headings":
                    # Center and underline heading text.
                    cell = f"{self._trm.underline(str(vlu).center(width))}"
                else:
                    # Right-justify or left-justify based on column key.
                    cell = (f"{str(vlu).rjust(width)}" if key in rjust_col 
                            else f"{str(vlu).ljust(width)}")
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
        self._display_width = min(self._trm.width, 79)
        self._margin_size = (self._trm.width - self._display_width) // 2
        self._table_width = self._data.get_table_width()

        table_space = self._display_width - 4  # For borders and padding
        if self._table_width > table_space:
            self._data.resize_columns(table_space)
            self._table_width = self._data.get_table_width()

        self._column_widths = self._data.get_column_widths()
