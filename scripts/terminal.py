"""terminal.py"""

from blessed import Terminal
# from table import Table


def clear_stdscr(term: Terminal) -> None:
    print(term.home + term.clear)


def get_padding(term: Terminal) -> str:
    return " " * (max(0, term.width - 79) // 2)


def prompt_key(term: Terminal, prompt: str) -> str:
#    padding = get_padding(term)
#    print(term.bright_yellow(f"{padding}{prompt}"))
    put_prompt(term, prompt)
    with term.cbreak(), term.hidden_cursor():
        key = term.inkey()
    return repr(key)


def prompt_str(term: Terminal, prompt: str) -> str:
    padding = get_padding(term)
    print(term.bright_yellow(f"{padding}{prompt}"))


def put_prompt(term: Terminal, prompt: str) -> None:
    print(term.center(term.bright_yellow(prompt.ljust(min(term.width, 79)))))


def put_script_banner(term: Terminal, script_name: str) -> None:
    print(term.reverse(f"Running {script_name}...".ljust(term.width)))


class Terminal_Table:
    # def __init__(self, data: Table) -> None:
    def __init__(self, data) -> None:
        self._data = data
        self._borders = {"top": {"left": "╔", "fill": "═", "right": "╗"}, 
                         "inner": {"left": "╟", "fill": "─", "right": "╢"}, 
                         "bottom": {"left": "╚", "fill": "═", "right": "╝"},
                         "side": "║"}

    def display(self, term: Terminal) -> None:
        self._term = term
        self._set_dimensions()
        self._draw_table(self._data.count_records())

    def _draw_row(self, row_type: str, index: int | None = None) -> None:
        line_types = ["top", "inner", "bottom"]
        text_types = ["title", "headings", "record"]
        rjust_col = self._data.get_rjust_columns() if row_type == "record" else {}
        l_end, r_end, gap = self._get_row_ends(row_type, row_type in line_types)
        content = (self._get_text_content(row_type, index)
                   if row_type in text_types
                   else self._borders[row_type]["fill"])
        cells = (self._process_text_content(row_type, content, rjust_col)
                 if row_type in text_types
                 else [f"{self._term.blue(content * (self._table_width + 2))}"])
        print(self._term.center(f"{l_end}{gap}{'  '.join(cells)}{gap}{r_end}"))

    def _draw_table(self, record_count: int) -> None:
        self._draw_row("top")
        self._draw_row("title")
        self._draw_row("inner")
        self._draw_row("headings")
        for i in range(record_count):
            self._draw_row("record", i)
        self._draw_row("bottom")

    def _get_row_ends(self, 
                      row_type: str, 
                      is_line_type: bool) -> tuple[str, str, str]:
        if is_line_type:
            l_end = f"{self._term.blue(self._borders[row_type]['left'])}"
            r_end = f"{self._term.blue(self._borders[row_type]['right'])}"
            gap = ""
        else:
            l_end = r_end = f"{self._term.blue(self._borders['side'])}"
            gap = " "
        return l_end, r_end, gap

    def _get_text_content(self, 
                          row_type: str, 
                          index: int | None = None) -> str | dict[str, str]:
        match row_type:
            case "title":
                return self._data.get_title()
            case "headings":
                return self._data.get_headings()
            case "record":
                return self._data.get_record(index)

    def _process_text_content(self, 
                              row_type: str, 
                              content: str | dict[str, str], 
                              rjust_col: set) -> list[str]:
        cells = []
        if row_type == "title":
            cell = f"{self._term.reverse(content.center(self._table_width))}"
            cells.append(cell)
        else:
            for key, value in content.items():
                width = self._column_widths[key]
                cell = (f"{self._term.underline(value.center(width))}" 
                        if row_type == "headings" 
                        else (f"{value.rjust(width)}" 
                              if key in rjust_col 
                              else f"{value.ljust(width)}"))
                cells.append(cell)
        return cells

    def _set_dimensions(self) -> None:
        self._display_width = min(self._term.width, 79)
        self._table_width = self._data.get_table_width()
        table_space = self._display_width - 4
        if self._table_width > table_space:
            self._data.resize_columns(table_space)
            self._table_width = self._data.get_table_width()
        self._column_widths = self._data.get_column_widths()
