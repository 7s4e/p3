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
        """Retrieve the text content for a specific type of table row.

        This method returns the text content for the specified 
        `row_type`, which can be the table's title, headings, or a 
        specific data record. For "record" rows, an `index` must be 
        provided to retrieve the appropriate row data.

        Args:
            row_type: The type of row to retrieve. Can be "title", 
                "headings", or "record".
            index: The index of the record to retrieve, required if 
                `row_type` is "record".
        
        Returns:
            The content of the row, either as:
                - A string for "title" row.
                - A dictionary of column headers for "headings" row.
                - A dictionary representing a specific data record for 
                    "record" row.
        
        Raises:
            ValueError: If `row_type` is "record" and no `index` is 
                provided.
        """
        match row_type:
            case "title":
                return self._data.get_title()
            case "headings":
                return self._data.get_headings()
            case "record":
                if index is None:
                    raise ValueError(
                        "Index must be provided for 'record' row_type")
                return self._data.get_record(index)

    def _process_text_content(self, 
                              row_type: str, 
                              content: str | dict[str, str], 
                              rjust_col: set) -> list[str]:
        """Process the content of a table row into formatted text cells.

        Depending on the `row_type`, this method processes and formats 
        text content for each cell of the row. For the title row, it 
        centers the text and applies a terminal reverse effect. For 
        headings, it centers the text and underlines it. For other rows 
        [records], it adjusts the text alignment based on the column 
        width, right-justifying the columns in `rjust_col`.

        Args:
            row_type: The type of row being processed. Can be "title", 
                "headings", or other string representing a regular data 
                row ["records"].
            content: Either a string (for title row) or a dictionary 
                where keys are column names and values are the cell 
                content.
            rjust_col: A set of keys representing columns that should be 
                right-justified.

        Returns:
            A list of formatted strings, each representing a cell in the 
            row.
        """
        cells = []

        if row_type == "title":
            # Format the title row by centering the content and applying 
            # reverse style.
            cell = f"{self._term.reverse(content.center(self._table_width))}"
            cells.append(cell)
        else:
            # Iterate over content dictionary and format each cell.
            for key, value in content.items():
                width = self._column_widths[key]
                if row_type == "headings":
                    # Center and underline heading text.
                    cell = f"{self._term.underline(value.center(width))}"
                else:
                    # Right-justify or left-justify based on column key.
                    cell = (f"{value.rjust(width)}" if key in rjust_col 
                            else f"{value.ljust(width)}")
                    cells.append(cell)
        
        return cells


    def _set_dimensions(self) -> None:
        """Set display and table dimensions based on terminal width.

        This method calculates the display width and table width by 
        considering the terminal width and the total width of the table. 
        If the table width exceeds the available display space, it 
        resizes the columns to fit. Finally, it updates the column 
        widths for rendering the table.

        Side effects:
            - Updates self._display_width with the terminal width 
                (capped at 79).
            - Updates self._table_width based on the table data.
            - Resizes table columns if the table exceeds the available 
                space.
            - Updates self._column_widths to reflect the current table 
                layout.
        """
        self._display_width = min(self._term.width, 79)
        self._table_width = self._data.get_table_width()

        table_space = self._display_width - 4  # For borders and padding
        if self._table_width > table_space:
            self._data.resize_columns(table_space)
            self._table_width = self._data.get_table_width()

        self._column_widths = self._data.get_column_widths()
