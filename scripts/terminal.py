""""""

from blessed import Terminal


PROMPT_COLOR = "bright_yellow"

def clear_stdscr(term: Terminal) -> None:
    print(term.home + term.clear)


def get_padding(term: Terminal) -> str:
    return " " * (max(0, term.width - 79) // 2)


def prompt_key(term: Terminal, prompt: str) -> str:
    padding = get_padding(term)
    print(term.bright_yellow(f"{padding}{prompt}"))
    with term.cbreak(), term.hidden_cursor():
        key = term.inkey()
    return repr(key)


def prompt_str(term: Terminal, prompt: str) -> str:
    padding = get_padding(term)
    print(term.bright_yellow(f"{padding}{prompt}"))


def put_script_banner(term: Terminal, script_name: str) -> None:
    print(term.reverse(f"Running {script_name}...".ljust(term.width)))