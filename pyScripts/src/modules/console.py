"""
Console Module

This module defines classes for handling console-based user interactions 
and displaying formatted tables in a terminal.

Imports:
    Standard library:
        from __future__ import annotations: Postpones the evaluation of 
            type annotations, allowing forward references without string 
            literals.
        from re import fullmatch: Provides support for regular 
            expressions, enabling pattern matching and text 
            manipulation.
        from sys import stdout: Provides access to the standard output 
            stream, used for printing to the terminal.
        from textwrap import fill: Provides text wrapping functionality 
            for formatting text, especially for console output.
        from typing import Any, TYPE_CHECKING:
            Any: Represents any valid Python object type in type 
                annotations.
            TYPE_CHECKING: Used for conditional imports to prevent 
                circular dependencies during runtime, primarily for type 
                checking.

    Third-party:
        from blessed import Terminal: Manages terminal output, including 
            color handling, cursor movement, and screen clearing.
    
    Local modules:
        from utilities import snake_to_camel, truncate_string
            snake_to_camel: A utility function for converting snake_case 
                strings to camelCase.
            truncate_string: A utility function for truncating strings 
                to a specified length.
        if TYPE_CHECKING:
            from table import Table: Conditionally imported for static 
                type checking to avoid circular imports at runtime.

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
if TYPE_CHECKING: from .table import Table


# Constants
BORDERS = {"top": {"left": "╔", "fill": "═", "right": "╗"}, 
           "inner": {"left": "╟", "fill": "─", "right": "╢"}, 
           "bottom": {"left": "╚", "fill": "═", "right": "╝"}, 
           "side": "║"}

FORMATTING_ALLOCATION = {"blink": len("[blink][/blink]"), 
                        "blue": len("[blue][/blue]"), 
                        "green": len("[green][/green]"), 
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
        _trm: blessed.Terminal inherited from ConsoleBase.
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
        _put_alrt: Display an alert message.
        _put_prmt: Display the cue message.
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
            Any validated response from the user, which could be a 
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
        """
        for _ in range(n):
            stdout.write("\033[F")
            stdout.write("\033[K")
        stdout.flush()

    def _chk_bool_vld(self) -> bool:
        """
        Validate user's response as 'yes' or 'no'.

        Side effect:
            _vld_resp: Set boolean as validated response.

        Returns:
            A boolean, True if the response is valid, False otherwise.
        """
        # Valid response sets _vld_response attribute
        if self._user_resp.lower() in {"y", "n"}:
            self._vld_resp = self._user_resp.lower() == "y"
            return True
        
        # Invalid response alerts user        
        self._e_ct["yes/no"] += 1
        self._put_alrt("Respond with 'y' or 'n'", self._e_ct["yes/no"])
        return False

    def _chk_int_vld(self) -> bool:
        """
        Validate user's response against available criterion.

        The method uses regular expression for matching:
            r'...': denotes raw literal string
            -?: indicates optional negative sign
            [0-9]+: matches one or more repetitions of any single digit

        Side effect:
            _vld_resp: Set integer as validated response.

        Returns:
            A boolean, True if the response is valid, False otherwise.
        """
        # Invalid alert if not a number
        if not bool(fullmatch(r'-?[0-9]+', self._user_resp)):
            self._e_ct["NaN"] += 1
            self._put_alrt("Enter a valid number", self._e_ct["NaN"])
            return False
        
        # Integer validated against integer validation attribute
        response = int(self._user_resp)
        match self._int_vld:

            # Criterion is single integer defining range
            case int() as range:
                if response < 0 or response >= range:
                    self._e_ct["OOR"] += 1
                    self._put_alrt("Response is out of range", 
                                    self._e_ct["OOR"])
                    return False
            
            # Crierion is tuple of lower and upper limits
            case tuple() as limits:
                low, high = limits
                if response < low or response > high:
                    self._e_ct["OOL"] += 1
                    self._put_alrt(f"Enter a number between {low} and " +
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
            self._put_prmt(kp_cur_inline=False)
            self._read_kst()
        
        # If string expected, show it inline with cue.
        else:
            self._put_prmt(kp_cur_inline=True)
            self._read_str()

    def _pnt_msg(self, msg: str, fmt_alloc: int, kp_cur_inline: bool) -> None:
        """
        Print left-justfied, wrapped message in center of console.

        Args:
            msg: The message to be printed.
            fmt_alloc: Allocation required for formatting text styles
            kp_cur_inline: If True, the cursor remains inline with 
                a trailing space after the message. If False, the cursor 
                moves to the next line after printing.
        """
        # Set width to display message and padding to center width
        display_width = min(self._trm.width, 79)
        padding = " " * ((self._trm.width - display_width) // 2)

        # Print textwrapped, padded message and deposit cursor
        print(fill(msg, width=(display_width + fmt_alloc + len(padding)), 
                   initial_indent=padding, subsequent_indent=padding), 
              end=" " if kp_cur_inline else "\n",
              flush=True)

    def _put_alrt(self, alert: str, err_ct: int) -> None:
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
            self._pnt_msg(alert, fmt_alloc, kp_cur_inline=False)

    def _put_prmt(self, kp_cur_inline: bool) -> None:
        """
        Display the prompt cue to the user.

        Args:
            kp_cur_inline: If True, the cursor remains inline with 
                a trailing space; if False, it moves to the next line 
                after the prompt.
        """
        self._pnt_msg(self._trm.yellow(self._cue), 
                      FORMATTING_ALLOCATION["yellow"], 
                      kp_cur_inline=kp_cur_inline)

    def _read_kst(self) -> None:
        """
        Read a single keystroke, filtering for printable characters.

        This method captures input in raw mode using the `cbreak` and 
        `hidden_cursor` contexts to disable line buffering and hide the 
        cursor. It ensures that only printable ASCII characters (codes 
        32 to 126) or the Enter key (code 10) are accepted. If the Enter 
        key is pressed, the response is stored as an empty string.

        Side effect:
            _user_resp: Set user response.
        """
        # Initialize values
        key = None
        miskey_ct = -1
        self._user_resp = ""

        # While loop within contexts filtering for printable characters
        with self._trm.cbreak(), self._trm.hidden_cursor():
            while key is None or not (32 <= code <= 126 or code == 10):
                key = self._trm.inkey()
                try:
                    code = ord(key)
                except:
                    key = None
                    miskey_ct += 1
                    self._put_alrt("Input not printable", miskey_ct)
        
        # Set user response
        self._user_resp = str(key if code != 10 else "")

    def _read_str(self) -> None:
        """
        Capture string, handling printable chars, backspaces, and Enter.

        This method operates in raw mode using the terminal's `cbreak` 
        context, allowing it to process input character by character. 
        Printable characters are displayed in green as they are typed, 
        backspaces remove the last character from the response, and 
        pressing Enter finalizes the input.

        Side effect:
            _user_resp: Set user response.
        """
        # Initialize values
        key = None
        response = []

        with self._trm.cbreak():
            # Wait Enter key
            while key is None or code != 10:
                key = self._trm.inkey()

                # Get ASCII decimal code
                try:
                    code = ord(key)
                
                # Reset key if code unavailable
                except:
                    key = None
                
                else:
                    # Simulate backspace on existing string
                    if response and (code == 8 or code == 127):
                        response.pop()
                        backspace_ct = 1 + FORMATTING_ALLOCATION["green"]
                        sequence = "\b \b" * backspace_ct
                        print(sequence, end="", flush=True)
                    
                    # Put printable character in green
                    elif 32 <= key.code <= 126:
                        response.append(str(key))
                        formatted_char = self._trm.green(str(key))
                        print(formatted_char, end="", flush=True)
            
            # Print new line upon Enter
            print()
        
        # Set user response
        self._user_resp = "".join(response)

    def _val_resp(self) -> bool:
        """
        Validate user response according to validation parameters.

        Side effect:
            _vld_resp: Validate user response if no parameters given.
        
        Returns:
            The boolean result of the validation check, or True if no 
            validation is required.
        """
        if self._val_bool: return self._chk_bool_vld()
        if self._val_int: return self._chk_int_vld()
        self._vld_resp = self._user_resp
        return True


class ConsoleTable(ConsoleBase):
    """
    A class for rendering tables in the console with styled formatting.

    This class extends `ConsoleBase` to provide functionality for 
    displaying data tables in a structured, visually appealing format. 
    It handles dynamic resizing based on terminal dimensions, formatting 
    of rows and columns, and supports styled output such as underlined 
    headings and color-coded borders.

    Args:
        table: An instance of Table to be rendered.
    
    Attributes:
        _col_wds: A map of columns to their widths.
        _data: The table data as a Table object.
        _disp_wd: The width for display in console.
        _mrg_sz: The size of margin required to center the table in 
            console.
        _tbl_wd: The width required for table columns and padding.
        _trm: blessed.Terminal inherited from ConsoleBase.

    Methods:
        display: Public method to render the table to the console.
        _drw_rw: Render a specific type of table row.
        _drw_tb: Render the table by sequentially drawing each row.
        _get_rw_cntnt: Retrieve content for a specific row type.
        _get_rw_ends: Retrieve the left and right borders, and the 
            padding for a row, depending on its type.
        _proc_rw_cntnt: Style the row content based on its type and 
            justify base on column.
        _set_dims: Calculate table dimensions and adjust column widths 
            to fit within the terminal display.
    """
    def __init__(self, table: Table) -> None:
        # Lazy import avoids circular import at runtime type validation
        from modules.table import Table
        if not isinstance(table, Table):
            raise TypeError("Expected `Table` for 'table'")
        
        # Base initialization and attribute assignment
        super().__init__()
        self._data = table

    # Public Method
    def display(self) -> None:
        """Display the table on the console."""
        self._set_dims()
        self._drw_tbl(self._data.count_records())

    # Private Methods
    def _drw_rw(self, rw_tp: str, idx: int | None = None) -> None:
        """
        Render a specific row type with styling.

        Args:
            rw_tp: The type of row to draw.
            idx: The index of the record row if applicable.
        """
        # Define row type categories
        is_line_type = rw_tp in {"top", "inner", "bottom"}
        is_text_type = rw_tp in {"title", "headings", "record"}

        # Determine justification for record rows
        rjust_cols = (self._data.get_rjust_columns() 
                     if rw_tp == "record" else {})
        
        # Get components for rendering the row
        margin = " " * self._mrg_sz
        left, right, gap = self._get_rw_ends(rw_tp, is_line_type)

        # Retrieve row content based on type
        content = (self._get_rw_cntnt(rw_tp, idx) 
                   if is_text_type else BORDERS[rw_tp]["fill"])
        
        # Process content into styled cells or line fillers
        cells = (self._proc_rw_cntnt(rw_tp, content, rjust_cols) 
                 if is_text_type 
                 else [self._trm.blue(content * (self._tbl_wd + 2))])
        
        # Construct and print the row
        print(f"{margin}{left}{gap}{'  '.join(cells)}{gap}{right}")
    
    def _drw_tbl(self, rec_ct: int) -> None:
        """
        Render the entire table by sequentially drawing each row type.

        Args:
            rec_ct: Number of record rows to draw.
        """
        # Header rows
        header_sequence = ["top", "title", "inner", "headings"]
        for row_type in header_sequence: self._drw_rw(row_type)
        
        # Record rows
        for i in range(rec_ct): self._drw_rw("record", i)
        
        # Bottom row
        self._drw_rw("bottom")
    
    def _get_rw_cntnt(self, rw_tp: str, idx: int | None = None
                      ) -> str | dict[str, str]:
        """
        Retrieve the text content for a specific type of table row.

        Args:
            rw_tp: The type of row to retrieve, either "title", 
                "headings", or "record".
            idx: The index of the record to retrieve, if "record" type.
        
        Returns:
            Row content, either a string for the "title" row, or a 
            dictionary for "headings" and "record".
        """
        match rw_tp:
            case "title": return self._data.get_title()
            case "headings": return self._data.get_headings()
            case "record": return self._data.get_record(idx)

    def _get_rw_ends(self, rw_tp: str, is_ln_tp: bool
                     ) -> tuple[str, str, str]:
        """
        Retrieve the left and right borders and padding for a row.

        Args:
            rw_tp: The type of the row to determine border style.
            is_ln_tp: A boolean flag indicating whether the row is a 
                line type (used for borders) or a content row.

        Returns:
            A tuple of three strings: the left border (styled), the 
            right border (styled), and the inner padding within the 
            outside border.
        """
        # Table borders
        if is_ln_tp:
            left_end = f"{self._trm.blue(BORDERS[rw_tp]['left'])}"
            right_end = f"{self._trm.blue(BORDERS[rw_tp]['right'])}"
            padding = ""
        
        # Text borders
        else:
            left_end = right_end = f"{self._trm.blue(BORDERS['side'])}"
            padding = " "
        
        return left_end, right_end, padding

    def _proc_rw_cntnt(self, rw_tp: str, cont: str | dict[str, str], 
                       rjust_cols: set) -> list[str]:
        """Process the content of a table row into formatted text cells.

        Args:
            rw_tp: The type of row to process, either "title", 
                "headings", "record".
            cont: Either a string (for title row) or a dictionary with 
                content mapped to column names.
            rjust_cols: A set of keys representing columns to be right-
                justified.

        Returns:
            A list of formatted strings, each representing a cell in the 
            row.
        """
        # Initialize list
        cells = []

        # Title content
        if rw_tp == "title":
            cont = truncate_string(cont, self._tbl_wd)
            cell = f"{self._trm.reverse(cont.center(self._tbl_wd))}"
            cells.append(cell)
        
        else:
            # Iterate headings and record content
            for key, value in cont.items():
                width = self._col_wds[key]
                value = truncate_string(value, width)

                # Cell content for headings
                cell = (f"{self._trm.underline(str(value).center(width))}" 
                        if rw_tp == "headings" 

                        # Right-justified cell content for records
                        else (f"{str(value).rjust(width)}" 
                              if key in rjust_cols 
                              
                              # Left-justified cell content for records
                              else f"{str(value).ljust(width)}"))
                
                # Build headings and record content
                cells.append(cell)
        
        return cells

    def _set_dims(self) -> None:
        """
        Set display and table dimensions based on the terminal width.

        Side effects:
            _disp_wd: Sets the display width, constrained by terminal 
                size or a maximum of 79 characters.
            _mrg_sz: Sets margin required to center the table.
            _tbl_wd: Sets width required for table columns and inner 
                padding.
            _col_wds: Sets width of each column.
        """
        # Set display and table dimensions
        self._disp_wd = min(self._trm.width, 79)
        self._mrg_sz = (self._trm.width - self._disp_wd) // 2
        self._tbl_wd = self._data.get_table_width()

        # Adjust table dimensions
        table_space = self._disp_wd - 4  # For borders and padding
        if self._tbl_wd > table_space:
            self._data.resize_columns(table_space)
            self._tbl_wd = self._data.get_table_width()
        
        # Set column dimensions
        self._col_wds = self._data.get_column_widths()
