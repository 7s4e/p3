""""""

from blessed import Terminal


def clear_stdscr(term: Terminal) -> None:
    print(term.home + term.clear)


def get_padding(term: Terminal) -> str:
    return " " * max(0, term.width - 79) // 2


def prompt(term: Terminal, prompt: str) -> None:
    padding = get_padding(term)
    print(term.yellow(f"{padding}{prompt}"))


def put_script_banner(term: Terminal, script_name: str) -> None:
    print(term.reverse(f"Running {script_name}...".ljust(term.width)))