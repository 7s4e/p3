"""Menu module"""
# Standard library imports
from typing import Any

# Third-party imports
from blessed import Terminal

# Local module import
from console_prompt import ConsolePrompt
from table import Table

class Menu:
    def __init__(self, 
                 options: Table | list, 
                 title: str | None = None,
                 prompt: str | None = None) -> None:
        self._options = (options
                         if isinstance(options, Table) 
                         else Table(title=title, 
                                    table_data=[{"OPTION": option} 
                                                 for option in options]))
        self._count = self._options.count_records()
        self.set_prompt(prompt)
    
    def get_selection(self, key: str = "OPTION") -> Any:
        return self._selection[key.upper()]

    def run(self, console: Terminal) -> None:
        self._options.put_table(console, is_menu=True)
        index = self._prompt.call(console) - 1
        self._selection = self._options.get_record(index)

    def set_prompt(self, prompt: str | None = None) -> None:
        count = self._count
        prompt = (f"Enter number (1-{self._count}) for selection:" 
                  if prompt is None else prompt)
        self._prompt = ConsolePrompt(prompt, 
                                     expect_keystroke=count < 10, 
                                     validate_integer=True, 
                                     integer_validation=(1, count))
