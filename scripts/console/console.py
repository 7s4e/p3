"""Console module."""
# Third-party imports
from blessed import Terminal

# Local module import
from console_prompt import ConsolePrompt
from console_table import ConsoleTable

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
