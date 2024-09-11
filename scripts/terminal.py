"""terminal.py"""

from blessed import Terminal
# from table import Table


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


class Box:
    # def __init__(self, data: Table) -> None:
    def __init__(self, data) -> None:
        self._data = data
        self._borders = {"top": {"left": "╔", "fill": "═", "right": "╗"}, 
                         "inner": {"left": "╟", "fill": "─", "right": "╢"}, 
                         "bottom": {"left": "╚", "fill": "═", "right": "╝"},
                         "side": "║"}

    def display(self, term: Terminal) -> None:
        self._term = term
        self._display_width = max(term.width, 79)
        self._table_width = self._data.get_table_width()
        table_space = self._display_width - 4
        if self._table_width > table_space:
            self._data.resize_columns(table_space)
            self._table_width = self._data.get_table_width()
        self._column_widths = self._data.get_column_widths()
        self._draw_row("top")
        self._draw_row("title")
        self._draw_row("inner")
        self._draw_row("heading")
        for i in range(self._data.count_records()):
            self._draw_row("record", i)
        self._draw_row("bottom")
    
    def _draw_row(self, row_type: str, index: int | None = None) -> None:
        line_types = ["top", "inner", "bottom"]
        text_types = ["title", "heading", "record"]
        row_cells = rjust_columns = []
        if row_type in line_types:
            l_end = self._borders[row_type]["left"]
            r_end = self._borders[row_type]["right"]
        else:
            l_end = r_end = f"{self._term.blue(self._borders['side'])}"
        if row_type in text_types:
            match row_type:
                case "title":
                    content_source = self._data.get_title()
                case "heading":
                    content_source = self._data.get_headings()
                case "record":
                    content_source = self._data.get_record(index)
                    rjust_columns = self._data.get_rjust_columns()
        else:
            content_source = self._borders[row_type]["fill"]
        if row_type in line_types:
            cell = f"{content_source * (self._table_width + 2)}"
            row_cells.append(cell)
            gap = ""
        else:
            if row_type == "title":
                cell = f"{content_source.center(self._table_width)}"
                cell = f"{self._term.reverse(cell)}"
                row_cells.append(cell)
            else:
                for key, cell_value in content_source.items():
                    cell_width = self._column_widths[key]
                    if row_type == "heading":
                        cell = f"{cell_value.center(cell_width)}"
                        cell = f"{self._term.underline(cell)}"
                    else:
                        if key in rjust_columns:
                            cell = f"{cell_value.rjust(cell_width)}"
                        else:
                            cell = f"{cell_value.ljust(cell_width)}"
                    row_cells.append(cell)
            gap = " "
        row_content = f"{l_end}{gap}{'  '.join(row_cells)}{gap}{r_end}"
        if row_type in line_types:
            row_content = f"{self._term.blue(row_content)}"
        print(self._term.center(row_content))
