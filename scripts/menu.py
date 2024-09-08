""""""

from typing import Any
from blessed import Terminal
from table import Table

class Menu:
    def __init__(self, 
                 options: Table | list, 
                 title: str | None = None) -> None:
        self._options = (options
                         if isinstance(options, Table) 
                         else Table(title=title, 
                                    table_data=[{"OPTION": option} 
                                                 for option in options]))
        self._count = self._options.count_records()
        self._prompt = f"Enter number (1-{self._count}) for selection: "
    
    def _prompt_selection(self) -> int:
        while True:
            try:
                selection = int(input(self._prompt))
                if 1 <= selection <= self._count:
                    return selection
                print(f"Enter a number between 1 and {self._count}.")
            except ValueError:
                print("Enter a valid number.")

    def get_selection(self, key: str = "OPTION") -> Any:
        return self._selection[key.upper()]

    def run(self, terminal: Terminal) -> None:
        # self._options.put_table(display_width=len(self._prompt), is_menu=True)
        self._options.put_table(terminal=terminal, is_menu=True)
        index = self._prompt_selection() - 1
        self._selection = self._options.get_record(index)

    @staticmethod
    def query_yes_no(prompt: str) -> bool:
        while True:
            response = input(prompt).strip().lower()
            if response in {'y', 'n'}:
                return response == 'y'
            print("Respond with 'y' or 'n'.")
