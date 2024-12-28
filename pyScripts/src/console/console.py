# Local import
from .console_base import ConsoleBase


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
        term = ConsoleBase()._trm
        print(term.reverse(f"Running {script_name}...".ljust(term.width)))