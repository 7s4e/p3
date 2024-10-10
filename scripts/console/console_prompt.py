"""Console module member"""
# Standard library imports
from typing import Any
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
            raise TypeError(
                "Expected `int`, `tuple[int, int]`, or `None` for 'integer_validation'.")

        # Value validation
        if validate_bool and validate_integer:
            raise ValueError(
                "Both 'validate_bool' and 'validate_integer' cannot be `True`.")
        if integer_validation is not None:
            if not validate_integer:
                raise ValueError(
                    "With 'integer_validation', 'validate_integer' must be `True`.")
            if isinstance(integer_validation, int):
                if integer_validation < 0:
                    raise ValueError(
                        "Range for 'integer_validation' must be positive.")
            else:
                if len(integer_validation) != 2:
                    raise ValueError(
                        "The 'integer_validation' `tuple` must have two elements.")
                if integer_validation[0] > integer_validation[1]:
                    raise ValueError(
                        "The second value of the 'integer_validation' `tuple` cannot be less than the first.")

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
        return str(key)

    # def _read_string(self) -> str:
    #     """Capture a string input from the user, handling enter and 
    #         backspace keys.

    #     This method reads characters from the user input in a terminal 
    #     session, with special handling for 'Enter' (which ends the 
    #     input) and 'Backspace' (which removes the last entered 
    #     character). The input is captured one character at a time until 
    #     'Enter' is pressed.

    #     Returns:
    #         str: The string input provided by the user.
    #     """
    #     user_input = []
    #     with self._con.cbreak():
    #         while True:
    #             key = self._con.inkey()
    #             if key.is_sequence and key.name == 'KEY_ENTER':
    #                 break
    #             if key.is_sequence and key.name == 'KEY_BACKSPACE':
    #                 if user_input:
    #                     user_input.pop()
    #                     self._put_prompt(leave_cursor_inline=True)
    #                     print(self._con.move_left(), end='', flush=True)
    #             else:
    #                 user_input.append(str(key))
    #                 # print(self._con.green(key), end='', flush=True)
    #                 print(key, end='', flush=True)
    #     print()
    #     return ''.join(user_input)

    def _read_string(self) -> str:
        """Capture a string input from the user, handling Enter and Backspace."""
        user_input = []
        with self._con.cbreak():
            while True:
                print(f"\nLoop start")  # Debugging statement

                key = self._con.inkey()
                print(f"Key attributes: is_sequence={key.is_sequence}, name={key.name}")
            
                # Handle Enter key
                if key.is_sequence and key.name == 'KEY_ENTER':
                    print(f"User input upon ENTER: {user_input}")  # Debugging statement
                    break
            
                # Handle Backspace key
                print(f"Backspace test: {key.is_sequence} and {key.name}")
                if key.is_sequence and key.name == 'KEY_BACKSPACE':
                    print(f"User input upon BACKSPACE: {user_input}")  # Debugging statement
                    if user_input:
                        user_input.pop()
                        self._put_prompt(leave_cursor_inline=True)
                        print(self._con.move_left(), end='', flush=True)
                else:
                    # Ensure that only string characters are appended and printed
                    char = str(key)  # Convert key to string
                    if len(char) == 1:  # Only print and append regular characters
                        user_input.append(char)
                        print(char, end='', flush=True)
                print(f"\nLoop end: {user_input}")  # Debugging statement


        print()  # End with a newline after input
        return ''.join(user_input)


# def _read_string(self) -> str:
#     """Capture a string input from the user, handling Enter and Backspace."""
#     user_input = []
#     with self._con.cbreak():
#         while True:
#             key = self._con.inkey()
            
#             # Handle Enter key
#             if key.is_sequence and 'ENTER' in key.name:
#                 break
            
#             # Handle Backspace key
#             if key.is_sequence and 'BACKSPACE' in key.name:
#                 if user_input:
#                     user_input.pop()
#                     self._put_prompt(leave_cursor_inline=True)
#                     print(self._con.move_left(), end='', flush=True)
#             else:
#                 # Ensure that only string characters are appended and printed
#                 char = str(key)  # Convert key to string
#                 if len(char) == 1:  # Only print and append regular characters
#                     user_input.append(char)
#                     print(char, end='', flush=True)

#     print()  # End with a newline after input
#     return ''.join(user_input)




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