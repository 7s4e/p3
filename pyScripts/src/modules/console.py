# Standard library imports
from __future__ import annotations  # Postpone evaluation of annotations
from typing import Any, TYPE_CHECKING
import re
import textwrap

# Third-party import
from blessed import Terminal

# Local imports
from .utilities import snake_to_camel
if TYPE_CHECKING:
    from .table import Table  # For static type checking only


BORDERS = {"top": {"left": "╔", "fill": "═", "right": "╗"}, 
           "inner": {"left": "╟", "fill": "─", "right": "╢"}, 
           "bottom": {"left": "╚", "fill": "═", "right": "╝"}, 
           "side": "║"}

FORMATTING_ALLOWANCE = {"blue": len("[blue][/blue]"), 
                        "red": len("[red][/red]"), 
                        "yellow": len("[yellow][/yellow]")}


class ConsoleBase:
    def __init__(self):
        # print(f"TRACE: ConsoleBase.init called >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")#####
        self._trm = Terminal()
        # print(f"TRACE: ConsoleBase.init trm.width: {self._trm.width}")#####
        # print(f"TRACE: ConsoleBase.init <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")#####


class Console(ConsoleBase):
    @staticmethod
    def clear_stdscr() -> None:
        """Clear terminal screen and reset cursor to the home position.
        """
        term = ConsoleBase()._trm
        print(term.home + term.clear)
    
    @staticmethod
    def put_script_banner(script_name: str) -> None:
        """Display reverse-video banner in terminal with the script 
            name.

        Args:
            script_name: The name of the script to be displayed in the 
                banner.
        """
        # print(f"TRACE: Console.put_script_banner called with {script_name} >>>")#####
        term = ConsoleBase()._trm
        # print(f"TRACE: Console.put_script_banner.term: {term}")#####
        scr_str = snake_to_camel(script_name)
        # print(f"TRACE: Console.put_script_banner.scr_str: {scr_str}")#####
        print(term.reverse(f"Running {scr_str}...".ljust(term.width)))
        # print(f"TRACE: Console.put_script_banner <<<<<<<<<<<<<<<<<<<<<<<<<<<<<")#####


class ConsolePrompt(ConsoleBase):
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
        _trm: blessed.Terminal inherited from ConsoleBase
        _prompt: The prompt message to display to the user.
        _expect_keystroke: Flag indicating if a keystroke is expected.
        _validate_bool: Flag indicating if boolean validation is 
            enabled.
        _validate_integer: Flag indicating if integer validation is 
            enabled.
        _integer_validation: Validation criteria for integers.

    Methods:
        call(): Prompt the user and return the validated response.
        _get_response(): Get the user's response based on expected input 
            type.
        _validate_response(): Validate the user's input based on the 
            specified criteria.
        _read_string(): Capture a string input from the user.
        _read_keystroke(): Capture a single keystroke from the user.
        _check_integer_validity(): Validate the user's integer 
            response.
        _check_bool_validity(): Validate the user's boolean response.
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

        # Type validation
        if not isinstance(prompt, str):
            raise TypeError("Expected `str` for 'prompt'")
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
                    raise ValueError("Range for 'integer_validation' must " +
                                     "be positive")
            else:
                if len(integer_validation) != 2:
                    raise ValueError("The 'integer_validation' `tuple` must " +
                                     "have two elements")
                if integer_validation[0] > integer_validation[1]:
                    raise ValueError("The second value of the " +
                                     "'integer_validation' `tuple` cannot " +
                                     "be less than the first")

        # Initialize base and assign validated attributes
        # print(f"TRACE: ConsolePrompt.init called >>>>>>>>>>>>>>>>>>>>>>>>>>>>>")#####
        super().__init__()
        # print(f"TRACE: ConsolePrompt.init ConsoleBase called")#####
        # print(f"TRACE: ConsolePrompt.init trm.width {self._trm.width}")#####
        self._prompt = prompt
        # print(f"TRACE: ConsolePrompt.init _prompt set as {self._prompt}")#####
        self._expect_keystroke = expect_keystroke
        # print(f"TRACE: ConsolePrompt.init _expect_keystroke set as {self._expect_keystroke}")#####
        self._validate_bool = validate_bool
        # print(f"TRACE: ConsolePrompt.init _validate_bool set as {self._validate_bool}")#####
        self._validate_integer = validate_integer
        # print(f"TRACE: ConsolePrompt.init _validate_integer set as {self._validate_integer}")#####
        self._integer_validation = integer_validation
        # print(f"TRACE: ConsolePrompt.init _integer_validation set as {self._integer_validation}")#####
        # print(f"TRACE: ConsolePrompt.init <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")#####

    # Public Method
    def call(self) -> Any:
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
        # print(f"TRACE: ConsolePrompt.call called >>>>>>>>>>>>>>>>>>>>>>>>>>>>>")#####
        valid = False
        # print(f"TRACE: ConsolePrompt.call.valid == {valid}")#####
        while not valid:
            # print(f"TRACE: ConsolePrompt.call.valid == {valid} .......>>>>>>>>")#####
            self._get_response()
            # print(f"TRACE: ConsolePrompt.call getResponse executed")#####
            valid = self._validate_response()
            # print(f"TRACE: ConsolePrompt.call validateResponse executed")#####
            # print(f"TRACE: ConsolePrompt.call.valid == {valid}")#####
        # print(f"TRACE: ConsolePrompt.call validated_response == {self._validated_response}")#####
        return self._validated_response

    # Private Methods
    def _check_bool_validity(self) -> bool:
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
        if self._user_response.lower() in {"y", "n"}:
            self._validated_response = self._user_response.lower() == "y"
            return True

        self._put_alert("Respond with 'y' or 'n'")
        return False

    def _check_integer_validity(self) -> bool:
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
        if not bool(re.fullmatch(r'-?[0-9]+', self._user_response)):
            self._put_alert("Enter a valid number")
            return False
        response = int(self._user_response)
        match self._integer_validation:
            case int() as range:
                if response < 0 or response >= range:
                    self._put_alert("Response is out of range")
                    return False
            case tuple() as limits:
                low, high = limits
                if response < low or response > high:
                    self._put_alert(f"Enter a number between {low} and " +
                                        f"{high}")
                    return False
            case None: pass
        self._validated_response = str(response)
        return True            

    def _get_response(self) -> None:
        """Prompt the user and capture their response.

        This method displays a prompt to the user and captures either a 
        single keystroke or a full string input, depending on the 
        `_expect_keystroke` flag. The response is stored in the 
        `_response` attribute.

        If `_expect_keystroke` is True, a keystroke is read and stored; 
        otherwise, a string input is captured.
        """
        # print(f"TRACE: ConsolePrompt.call > getResponse called >>>>>>>>")#####
        if self._expect_keystroke:
            # print(f"TRACE: ConsolePrompt.call > getResponse expectKeystroke == {self._expect_keystroke} ...")#####
            self._put_prompt(leave_cursor_inline=False)
            # print(f"TRACE: ConsolePrompt.call > putPrompt executed")#####
            self._read_keystroke()
            # print(f"TRACE: ConsolePrompt.call > readKeystroke executed")#####
        else:
            # print(f"TRACE: ConsolePrompt.call > getResponse expectKeystroke == {self._expect_keystroke} ...")#####
            self._put_prompt(leave_cursor_inline=True)
            # print(f"TRACE: ConsolePrompt.call > putPrompt executed")#####
            self._read_string()
            # print(f"TRACE: ConsolePrompt.call > readString executed")#####
        # print(f"TRACE: ConsolePrompt.call > getResponse <<<<<<<<<<<<<<<")#####

    def _print_message(self, message: str, formatting_allowance: int, 
                       leave_cursor_inline: bool) -> None:
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
        # print(f"TRACE: ConsolePrompt.call > getResponse > putPrompt > printMessage called with {message}, {formatting_allowance}, {leave_cursor_inline}>>>")#####
        # print(f"TRACE: ConsolePrompt.call > getResponse > putPrompt > printMessage _trm.width: {self._trm.width}")#####
        display_width = min(self._trm.width, 79)
        # print(f"TRACE: ConsolePrompt.call > getResponse > putPrompt > printMessage.display_width: {display_width}")#####
        padding = " " * ((self._trm.width - display_width) // 2)
        # print(f"TRACE: ConsolePrompt.call > getResponse > putPrompt > printMessage.padding.length: {len(padding)}")#####
        print(textwrap.fill(message, width=(display_width + 
                                            formatting_allowance + 
                                            len(padding)), 
                            initial_indent=padding, subsequent_indent=padding), 
              end=" " if leave_cursor_inline else "\n", flush=True)
        # print(f"TRACE: ConsolePrompt.call > getResponse > putPrompt > printMessage <<<")#####

    def _put_alert(self, alert: str) -> None:
        """Display an alert message to the user in red.

        This method prints the provided alert message to the console in 
        red. The cursor moves to the next line after being displayed.

        Args:
            alert: The alert message to be displayed.
        """
        self._print_message(self._trm.red(alert), FORMATTING_ALLOWANCE["red"], 
                            leave_cursor_inline=False)

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
        # print(f"TRACE: ConsolePrompt.call > getResponse > putPrompt called >>>")#####
        self._print_message(self._trm.yellow(self._prompt), 
                            FORMATTING_ALLOWANCE["yellow"], 
                            leave_cursor_inline=leave_cursor_inline)
        # print(f"TRACE: ConsolePrompt.call > getResponse > putPrompt <<<")#####


    def _read_keystroke(self) -> None:
        """Captures a single keystroke from the user, waiting for a 
            printable character or the Enter key, and stores the result 
            in `_user_response`.
        
        This method operates in raw mode using the `cbreak()` and 
        `hidden_cursor()` contexts of the terminal, allowing it to read 
        user input without displaying the cursor. It continues to 
        capture keystrokes until a valid character (ASCII codes 32-126) 
        or the Enter key (ASCII code 10) is detected. If the Enter key 
        is pressed, an empty string is stored in `_user_response`.

        Attributes:
            _user_response (str): The captured keystroke, or an empty 
                string if the Enter key is pressed.
        """
        # print(f"TRACE: ConsolePrompt.call > getResponse > readKeystroke called >>>")#####
        key = None
        # print(f"TRACE: ConsolePrompt.call > getResponse > readKeystroke.key: {key}")#####

        with self._trm.cbreak(), self._trm.hidden_cursor():
            while key is None or not (32 <= key_code <= 126 or key_code == 10):
                # print(f"TRACE: ConsolePrompt.call > getResponse > readKeystroke loop started ...")#####
                key = self._trm.inkey()
                # print(f"TRACE: ConsolePrompt.call > getResponse > readKeystroke.key: {key}")#####
                try:
                    # print(f"TRACE: ConsolePrompt.call > getResponse > readKeystroke try started ...")#####
                    key_code = ord(key)
                    # print(f"TRACE: ConsolePrompt.call > getResponse > readKeystroke loop ended with {key}, {key_code}")#####
                except:
                    # print(f"TRACE: ConsolePrompt.call > getResponse > readKeystroke try failed ...")#####
                    key = None
                    # print(f"TRACE: ConsolePrompt.call > getResponse > readKeystroke loop ended with {key}")#####

        self._user_response = str(key if key_code != 10 else "")
        # print(f"TRACE: ConsolePrompt.call > getResponse > readKeystroke _user_response set as {self._user_response}")#####
        # print(f"TRACE: ConsolePrompt.call > getResponse > readKeystroke <<<")#####

    def _read_string(self) -> None:
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

        self._user_response = "".join(response)


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
        # print(f"TRACE: ConsolePrompt.call > validateResponse called >>>>>>>>>>>>>>>>>>>>>>")#####
        if self._validate_bool:
            # print(f"TRACE: ConsolePrompt.call > validateResponse validateBool == True ...")#####
            return self._check_bool_validity()
        if self._validate_integer:
            # print(f"TRACE: ConsolePrompt.call > validateResponse validateInteger == True ...")#####
            return self._check_integer_validity()
        # print(f"TRACE: ConsolePrompt.call > validateResponse validateBool == False && validateInteger == False ...")#####
        self._validated_response = self._user_response
        # print(f"TRACE: ConsolePrompt.call > validateResponse user_response: {self._user_response}")#####
        # print(f"TRACE: ConsolePrompt.call > validateResponse validated_response: {self._validated_response}")#####
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
            cell = f"{self._trm.reverse(content.center(self._table_width))}"
            cells.append(cell)
        else:
            # Iterate over content dictionary and format each cell.
            for key, value in content.items():
                width = self._column_widths[key]
                if row_type == "headings":
                    # Center and underline heading text.
                    cell = f"{self._trm.underline(value.center(width))}"
                else:
                    # Right-justify or left-justify based on column key.
                    cell = (f"{str(value).rjust(width)}" if key in rjust_col 
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
        self._display_width = min(self._trm.width, 79)
        self._margin_size = (self._trm.width - self._display_width) // 2
        self._table_width = self._data.get_table_width()

        table_space = self._display_width - 4  # For borders and padding
        if self._table_width > table_space:
            self._data.resize_columns(table_space)
            self._table_width = self._data.get_table_width()

        self._column_widths = self._data.get_column_widths()
