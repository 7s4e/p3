""""""

from blessed import Terminal


def resize_columns(columns: list[int], box_width: int) -> list[int]:
    pass


def clear_stdscr(term: Terminal) -> None:
    print(term.home + term.clear)


def draw_box(term: Terminal, rows: int, columns: list[int]) -> None:
    box_width = min(term.width, 79)
    table_width = sum(columns) + 2 * (len(columns) - 1)
    if table_width > box_width - 4:
        columns = resize_columns(columns, box_width)
    top_row = f"╔{'═' * (box_width - 2)}╗"
    title_row = heading_row = data_row = blank_row = f"║{' ' * (box_width - 2)}║"
    border_row = f"╟{'─' * (box_width - 2)}╢"
    bottom_row = f"╚{'═' * (box_width - 2)}╝"
    print(term.blue(term.center(top_row)))
    print(term.blue(term.center(title_row)))
    print(term.blue(term.center(border_row)))
    print(term.blue(term.center(heading_row)))
    for _ in range(rows):
        print(term.blue(term.center(data_row)))
    print(term.blue(term.center(bottom_row)))


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