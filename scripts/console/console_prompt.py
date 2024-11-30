"""Console module member"""
# Standard library imports
from typing import Any
import re
import textwrap

# Third-party imports
from blessed import Terminal


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
            raise TypeError("Expected `str` for 'prompt'.")
        if not isinstance(expect_keystroke, bool):
            raise TypeError("Expected `bool` for 'expect_keystroke'.")
        if not isinstance(validate_bool, bool):
            raise TypeError("Expected `bool` for 'validate_bool'.")
        if not isinstance(validate_integer, bool):
            raise TypeError("Expected `bool` for 'validate_integer'.")
        if (integer_validation is not None 
            and not (isinstance(integer_validation, int) 
                     and not isinstance(integer_validation, bool)
                     or isinstance(integer_validation, tuple))):
            raise TypeError("Expected `int`, `tuple[int, int]`, or `None` " +
                            "for 'integer_validation'.")

        # Value validation
        if validate_bool and validate_integer:
            raise ValueError("Both 'validate_bool' and 'validate_integer' " +
                             "cannot be `True`.")
        if integer_validation is not None:
            if not validate_integer:
                raise ValueError("With 'integer_validation', " +
                                 "'validate_integer' must be `True`.")
            if isinstance(integer_validation, int):
                if integer_validation < 0:
                    raise ValueError("Range for 'integer_validation' must " +
                                     "be positive.")
            else:
                if len(integer_validation) != 2:
                    raise ValueError("The 'integer_validation' `tuple` must " +
                                     "have two elements.")
                if integer_validation[0] > integer_validation[1]:
                    raise ValueError("The second value of the " +
                                     "'integer_validation' `tuple` cannot " +
                                     "be less than the first.")

        # Assign validated attributes
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
            self._user_response = self._user_response.lower() == "y"
            return True

        self._put_alert("Respond with 'y' or 'n'.")
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
            self._put_alert("Enter a valid number.")
            return False
        response = int(self._user_response)
        match self._integer_validation:
            case int() as range:
                if response < 0 or response >= range:
                    self._put_alert("Response is out of range.")
                    return False
            case tuple() as limits:
                low, high = limits
                if response < low or response > high:
                    self._put_alert(f"Enter a number between {low} and " +
                                        f"{high}.")
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
        if self._expect_keystroke:
            self._put_prompt(leave_cursor_inline=False)
            self._read_keystroke()
        else:
            self._put_prompt(leave_cursor_inline=True)
            self._read_string()

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
        key = None

        with self._con.cbreak(), self._con.hidden_cursor():
            while key is None or not (32 <= key.code <= 126 or key.code == 10):
                key = self._con.inkey()

        self._user_response = str(key if key.code != 10 else "")

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

        with self._con.cbreak():
            while key is None or key.code != 10:  # Wait New Line/Enter
                key = self._con.inkey()

                if key.code == 8:  # Handle Backspace
                    if response:
                        response.pop()
                        bckspce_sequence = "\b \b" * len(self._con.green("x"))
                        print(bckspce_sequence, end="", flush=True)
                elif 32 <= key.code <= 126:  # Handle printable chars
                    response.append(str(key))
                    formatted_char = self._con.green(str(key))
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
        if self._validate_bool:
            return self._check_bool_validity()
        if self._validate_integer:
            return self._check_integer_validity()
        return True