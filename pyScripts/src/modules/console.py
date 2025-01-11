"""
Console Module

This module defines classes for handling console-based user interactions 
and displaying formatted tables in a terminal.

Imports:
    Standard library:
        from __future__ import annotations: Postpone the evaluation of 
            type annotations, allowing forward references without string 
            literals.
        from abc import ABC, abstractmethod: Define abstract base 
            classes and enforce implementation of required methods in 
            subclasses. 
        from re import fullmatch: Provide support for regular 
            expressions, enabling pattern matching and text 
            manipulation.
        from sys import stdout: Provide access to the standard output 
            stream, used for printing to the terminal.
        from textwrap import fill: Provide text wrapping functionality 
            for formatting text, especially for console output.
        from typing import Any, TYPE_CHECKING:
            Any: Represent any valid Python object type in type 
                annotations.
            TYPE_CHECKING: Use for conditional imports to prevent 
                circular dependencies during runtime, primarily for type 
                checking.

    Third-party:
        from blessed import Terminal: Manage terminal output, including 
            color handling, cursor movement, and screen clearing.
    
    Local modules:
        from utilities import snake_to_camel, truncate_string
            snake_to_camel: Convert snake_case strings to camelCase.
            truncate_string: Truncate strings to a specified length.
        if TYPE_CHECKING:
            from table import Table: Conditionally import for static 
                type checking to avoid circular imports at runtime.

Classes:
    ConsoleBase: The base class that initiates an instance of the 
        Terminal class.
    Console: A subclass of ConsoleBase, providing static methods for 
        console-related operations.
    ConsolePrompt: An abstract subclass of ConsoleBase, responsible for 
        handling user prompts with validation for user responses.
    ConsoleAnyKeyPrompt: A subclass or ConsolePrompt, prompting the user 
        to respond with any key.
    ConsoleBooleanPrompt: A subclass or ConsolePrompt, prompting the user 
        for a boolean response.
    ConsoleFreeFormPrompt: A subclass or ConsolePrompt, prompting the 
        user for a response without validation requirements.
    ConsoleIntegerPrompt: A subclass or ConsolePrompt, prompting the 
        user for an integer with an option validation constraint.
    ConsoleTable: A subclass of ConsoleBase, responsible for displaying 
        tables in the terminal.

Constants:
    BORDERS (dict): Defines the border characters for table layout.
    FORMATTING_ALLOCATION (dict): Defines the length of formatting
        sequences for different styles.
"""
# Standard library imports
from __future__ import annotations
from abc import ABC, abstractmethod
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
        back_n_lines: Clears the terminal n rows up from the cursor
        clear_screen: Clears the terminal screen and resets the cursor 
            to the home position.
        put_script_banner: Displays a reverse-video banner with the 
            script name.
    """
    @staticmethod
    def back_n_lines(n: int) -> None:
        """
        Move cursor back `n` lines and clear each line.

        This method uses ANSI escape codes to move the cursor up 
        (`\033[F`) and to clear the contents of each line (`\033[K`). 
        The changes are flushed to the terminal to ensure immediate 
        application.
        
        Args:
            n: The number of lines to move back and clear.
        """
        if not isinstance(n, int): raise TypeError("Expected `int` for 'n'")
        if n < 0: raise ValueError("The value 'n' must be positive")

        for _ in range(min(n, ConsoleBase()._trm.height)):
            stdout.write("\033[F")
            stdout.write("\033[K")
        stdout.flush()

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
        script_name = snake_to_camel(str(script_name))
        print(term.reverse(f"Running {script_name}...".ljust(term.width)))
    

class ConsolePrompt(ConsoleBase, ABC):
    """
    An abstract class to manage console prompts and possible validation.

    This class facilitates prompting the user for input via the console, 
    with subclasses providing options for validating boolean and integer 
    responses. Subclasses may expect either a single keystroke or a full 
    string input.

    Args:
        cue: The message to display to the user.

    Attributes:
        _expect_keystroke: Abstract attribute for flag indicating only a 
            keystroke is expected.
        _reset_value: Virtual attribute for the default error count.
        _cue: The message displayed to the user.
        _error_count: The number of errors since last validation.
        _user_response: The user's raw response.
        _validated_response: The user's validated response.

    Methods:
        _validate_response: Abstract method to validate the user's 
            input.
        call: Prompt the user and return the validated response.
        _back_n_lines: Delete and move cursor up 'n' lines.
        _get_response: Get the user's response based on expected input type.
        _print_message: Print formatted message to stdout.
        _put_alert: Display an alert message.
        _put_prompt: Display the cue message.
        _read_keystroke: Capture a single keystroke from the user.
        _read_string: Capture a string input from the user.
        _reset_error_count: Reset the error count to the default.
    """
    def __init__(self, cue: str = "> ") -> None:

        # Type validation
        if not isinstance(cue, str): 
            raise TypeError("Expected `str` for 'cue'")

        # Initialize base and assign validated attributes
        super().__init__()
        self._cue = cue
        self._reset_value = 0
        self._error_count = self._reset_value
        self._user_response = ""
        self._validated_response = None
    
    # Abstract methods    
    @property
    @abstractmethod
    def _expect_keystroke(self) -> bool:
        """Define whether only a keystroke is expected from the user."""
        pass

    @abstractmethod
    def _validate_response(self) -> bool:
        """
        Set user's response as validated per subclass definition.
        
        Side effect:
            _validated_response: Set user response as validated.
        
        Return:
            True if subclass definition does not return as False.
        """
        self._validated_response = self._user_response
        return True

    # Public Method
    def call(self) -> Any:
        """
        Get, validate, and return user input.

        Returns:
            Any validated response from the user, which could be a 
            string, integer, or boolean, depending on the validation 
            type.
        """
        while True:
            self._get_response()
            if self._validate_response():
                self._reset_error_count()
                return self._validated_response

    # Private Methods
    # def _back_n_lines(self, n: int) -> None:
    #     """
    #     Move cursor back `n` lines and clear each line.

    #     This method uses ANSI escape codes to move the cursor up 
    #     (`\033[F`) and to clear the contents of each line (`\033[K`). 
    #     The changes are flushed to the terminal to ensure immediate 
    #     application.
        
    #     Args:
    #         n: The number of lines to move back and clear.
    #     """
    #     for _ in range(n):
    #         stdout.write("\033[F")
    #         stdout.write("\033[K")
    #     stdout.flush()

    def _get_response(self) -> None:
        """Prompt the user and capture input."""
        # If keystroke expected, read it after prompting
        if self._expect_keystroke:
            self._put_prompt(kp_cur_inline=False)
            self._read_keystroke()
        
        # If string expected, show it inline with cue.
        else:
            self._put_prompt(kp_cur_inline=True)
            self._read_string()

    def _print_message(self, msg: str, fmt_alloc: int, kp_cur_inline: bool
                       ) -> None:
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

    def _put_alert(self, alert: str, error_count: int) -> None:
        """
        Display alert message with escalating formatting.

        Args:
            alert: The alert message to be displayed.
            error_count: The number of times alert is triggered without 
                validation.
        """
        # Delete cue or both cue and last alert message
        Console.back_n_lines(min(error_count, 2))
        # self._back_n_lines(min(error_count, 2))

        # Apply formatting based on error count
        formatting_steps = [(1, lambda msg: self._trm.red(msg), 
                             FORMATTING_ALLOCATION["red"]), 
                            (2, lambda msg: self._trm.reverse(msg), 
                             FORMATTING_ALLOCATION["reverse"]),
                            (3, lambda msg: self._trm.blink(msg), 
                             FORMATTING_ALLOCATION["blink"])]
        fmt_alloc = 0
        for step, formatter, allocation in formatting_steps:
            if error_count >= step:
                alert = formatter(alert)
                fmt_alloc += allocation

        # Subsequent alerts show invalid input
        if error_count >= 4:
            alert = (self._trm.red(f"'{self._user_response}' is invalid. ") + 
                     alert)
        
        # Alert printed
        if error_count > 0:
            self._print_message(alert, fmt_alloc, kp_cur_inline=False)

    def _put_prompt(self, kp_cur_inline: bool) -> None:
        """
        Display the prompt cue to the user.

        Args:
            kp_cur_inline: If True, the cursor remains inline with 
                a trailing space; if False, it moves to the next line 
                after the prompt.
        """
        self._print_message(self._trm.yellow(self._cue), 
                            FORMATTING_ALLOCATION["yellow"], 
                            kp_cur_inline=kp_cur_inline)

    def _read_keystroke(self) -> None:
        """
        Read a single keystroke, filtering for printable characters.

        This method captures input in raw mode using the `cbreak` and 
        `hidden_cursor` contexts to disable line buffering and hide the 
        cursor. It ensures that only printable ASCII characters (codes 
        32 to 126) or the Enter key (code 10) are accepted. If the Enter 
        key is pressed, the response is stored as an empty string.

        Side effect:
            _user_response: Set user response.
        """
        # Initialize values
        key = None
        miskey_ct = -1
        self._user_response = ""

        # While loop within contexts filtering for printable characters
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
        self._user_response = str(key if code != 10 else "")

    def _read_string(self) -> None:
        """
        Capture string, handling printable chars, backspaces, and Enter.

        This method operates in raw mode using the terminal's `cbreak` 
        context, allowing it to process input character by character. 
        Printable characters are displayed in green as they are typed, 
        backspaces remove the last character from the response, and 
        pressing Enter finalizes the input.

        Side effect:
            _user_response: Set user response.
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
        self._user_response = "".join(response)
    
    def _reset_error_count(self) -> None:
        """
        Reset error count to default value.
        
        Side effect:
            _error_count: Value reset.
        """
        self._error_count = self._reset_value


class ConsoleAnyKeyPrompt(ConsolePrompt):
    """
    An implementation of ConsolePrompt for a single keystroke.

    Args:
        cue: The message to display to the user.

    Attributes:
        _expect_keystroke: Implementation of abstract attribute.

    Methods:
        _validate_response: Implementation of abstract method.
    """
    def __init__(self, cue: None | str = "Press any key to continue..."
                 ) -> None:
        super().__init__(cue)
    
    @property
    def _expect_keystroke(self) -> bool:
        """Flag indicating only a keystroke is expected."""
        return True
    
    def _validate_response(self) -> bool:
        """Run base definition without further validation."""
        return super()._validate_response()


class ConsoleBooleanPrompt(ConsolePrompt):
    """
    An implementation of ConsolePrompt for a boolean value.

    Args:
        cue: The message to display to the user.

    Attributes:
        _expect_keystroke: Implementation of abstract attribute.

    Methods:
        _validate_response: Implementation of abstract method.
        _check_bool: Validate user response as boolean value.
    """
    def __init__(self, cue: None | str = "(y/n)?") -> None:
        super().__init__(cue)
    
    @property
    def _expect_keystroke(self) -> bool:
        """Flag indicating only a keystroke is expected."""
        return True
    
    def _validate_response(self) -> bool:
        """Validate user response with the check_bool() method."""
        return super()._validate_response() if self._check_bool() else False
    
    def _check_bool(self) -> bool:
        """
        Validate user's response as 'yes' or 'no'.

        Side effect:
            _validated_response: Set boolean as validated response.

        Returns:
            A boolean, True if the response is valid, False otherwise.
        """
        # Valid response sets _validated_responseonse attribute
        if self._user_response.lower() in {"y", "n"}:
            self._user_response = self._user_response.lower() == "y"
            return True
        
        # Invalid response alerts user
        self._error_count += 1
        self._put_alert("Respond with 'y' or 'n'", self._error_count)
        return False


class ConsoleFreeFormPrompt(ConsolePrompt):
    """
    An implementation of ConsolePrompt without validation.

    Args:
        cue: The message to display to the user.

    Attributes:
        _expect_keystroke: Implementation of abstract attribute.

    Methods:
        _validate_response: Implementation of abstract method.
    """
    def __init__(self, cue: str | None = None) -> None:
        super().__init__() if cue is None else super().__init__(cue)
    
    @property
    def _expect_keystroke(self) -> bool:
        """Flag indicating a string is expected."""
        return False
    
    def _validate_response(self) -> bool:
        """Run base definition without further validation."""
        return super()._validate_response()


class ConsoleIntegerPrompt(ConsolePrompt):
    """
    An implemenation of ConsolePrompt for an interger value.

    Args:
        cue: The message to display to the user.
        constraint: Integer validation parameter.

    Attributes:
        _expect_keystroke: Implementation of abstract attribute.
        _reset_value: Overridden virtual attribute.
    
    Methods:
        _validate_response: Implementation of abstract method.
        _check_int: Validate user response as integer value.
    """
    def __init__(self, cue: str | None = None, 
                 constraint: int | tuple[int, int] | None = None) -> None:
        # Type validation
        if (constraint is not None 
            and not (isinstance(constraint, int) 
                     and not isinstance(constraint, bool) 
                     or isinstance(constraint, tuple))):
            raise TypeError("Expected `int`, `tuple[int, int]`, or " + 
                            "`None` for 'constraint'")
        
        # Value validation
        if constraint is not None:
            if isinstance(constraint, int):
                if constraint < 0:
                    raise ValueError("Range for 'constraint' must be " + 
                                     "positive")
            else:
                if len(constraint) != 2:
                    raise ValueError("There must be two elements for " + 
                                     "'constraint', a lower and upper " +
                                     "limit")
                if constraint[0] > constraint[1]:
                    raise ValueError("The second element of " + 
                                     "'constraint' cannot be less " + 
                                     "than the first")
                
        super().__init__() if cue is None else super().__init__(cue)
        self._constraint = constraint
        self._reset_value = {"NaN": 0, "OOR": 0, "OOL": 0}
        self._reset_error_count()
    
    @property
    def _expect_keystroke(self) -> bool:
        """Flag if single digit integer is is expected."""
        if self._constraint is None: return False
        if isinstance(self._constraint, int): return self._constraint <= 10
        return self._constraint[0] >= 0 and self._constraint[1] <= 9
    
    def _validate_response(self) -> bool:
        """Validate user response with the check_int() method."""
        return super()._validate_response() if self._check_int() else False
    
    def _check_int(self) -> bool:
        """
        Validate user's response against available criterion.

        The method uses regular expression for matching:
            r'...': denotes raw literal string
            -?: indicates optional negative sign
            [0-9]+: matches one or more repetitions of any single digit

        Side effect:
            _validated_response: Set integer as validated response.

        Returns:
            A boolean, True if the response is valid, False otherwise.
        """
        # Invalid alert if not a number
        if not bool(fullmatch(r'-?[0-9]+', self._user_response)):
            self._error_count["NaN"] += 1
            self._put_alert("Enter a valid number", self._error_count["NaN"])
            return False
        
        # Integer validated against integer validation attribute
        response = int(self._user_response)
        match self._constraint:

            # Criterion is single integer defining range
            case int() as range:
                if response < 0 or response >= range:
                    self._error_count["OOR"] += 1
                    self._put_alert("Response is out of range", 
                                    self._error_count["OOR"])
                    return False
            
            # Crierion is tuple of lower and upper limits
            case tuple() as limits:
                low, high = limits
                if response < low or response > high:
                    self._error_count["OOL"] += 1
                    self._put_alert(f"Enter a number between {low} and " +
                                    f"{high}", self._error_count["OOL"])
                    return False
            
            # No integer validation criteria
            case None: return True


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
        _draw_row: Render a specific type of table row.
        _drw_tb: Render the table by sequentially drawing each row.
        _get_row_content: Retrieve content for a specific row type.
        _get_row_ends: Retrieve the left and right borders, and the 
            padding for a row, depending on its type.
        _process_row_content: Style the row content based on its type 
            and justify based on column.
        _set_dimensions: Calculate table dimensions and adjust column 
            widths to fit within the terminal display.
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
        self._set_dimensions()
        self._draw_table(self._data.count_records())

    # Private Methods
    def _draw_row(self, rw_tp: str, idx: int | None = None) -> None:
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
        left, right, gap = self._get_row_ends(rw_tp, is_line_type)

        # Retrieve row content based on type
        content = (self._get_row_content(rw_tp, idx) 
                   if is_text_type else BORDERS[rw_tp]["fill"])
        
        # Process content into styled cells or line fillers
        cells = (self._process_row_content(rw_tp, content, rjust_cols) 
                 if is_text_type 
                 else [self._trm.blue(content * (self._tbl_wd + 2))])
        
        # Construct and print the row
        print(f"{margin}{left}{gap}{'  '.join(cells)}{gap}{right}")
    
    def _draw_table(self, rec_ct: int) -> None:
        """
        Render the entire table by sequentially drawing each row type.

        Args:
            rec_ct: Number of record rows to draw.
        """
        # Header rows
        header_sequence = ["top", "title", "inner", "headings"]
        for row_type in header_sequence: self._draw_row(row_type)
        
        # Record rows
        for i in range(rec_ct): self._draw_row("record", i)
        
        # Bottom row
        self._draw_row("bottom")
    
    def _get_row_content(self, rw_tp: str, idx: int | None = None
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

    def _get_row_ends(self, rw_tp: str, is_ln_tp: bool
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

    def _process_row_content(self, rw_tp: str, 
                             cont: str | dict[str, str], 
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

    def _set_dimensions(self) -> None:
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
