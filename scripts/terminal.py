""""""

from blessed import Terminal
from table import Table as Data


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


class Table:
    def __init__(self, data: Data) -> None:
        self._data = data
    
    def display(self, term: Terminal) -> None:
        display_width = max(term.width, 79)
        table_width = self._data.get_table_width()
        if table_width > display_width - 4:
            self._data.resize_columns(display_width - 4)
            table_width = self._data.get_table_width()
        self._draw_line_row(term, "top", display_width)
        self._draw_text_row(term, "title", table_width)
        self._draw_line_row(term, "inner", display_width)
        self._draw_text_row(term, "headings", table_width)
        for _ in range(self._data.count_records()):
            self._draw_text_row(term, "data", table_width)
        self._draw_line_row(term, "bottom", display_width)
    
    def _draw_line_row(self, 
                       term: Terminal, 
                       row: str, 
                       display_width: int) -> None:
        BORDERS = {"top": {"left_end": "╔", "fill": "═", "right_end": "╗"},
                   "inner": {"left_end": "╟", "fill": "─", "right_end": "╢"},
                   "bottom": {"left_end": "╚", 
                              "fill": "═", 
                              "right_end": "╝"}}
        left_end = BORDERS[row]["left_end"]
        line_fill = BORDERS[row]["fill"] * (display_width - 2)
        right_end = BORDERS[row]["right_end"]
        line_row = left_end + line_fill + right_end
        print(term.blue(term.center(line_row)))

    def _draw_text_row(self, 
                       term: Terminal, 
                       type: str, 
                       table_width: int) -> None:
        BORDER = "║"
