"""Menu module"""
# Standard library imports
from typing import Any

# Local module import
from .console import ConsolePrompt
from .table import Table

class Menu:
    def __init__(self, 
                 options: list | Table, 
                 title: str | None = None,
                 prompt: str | None = None) -> None:
        # print(f"TRACE: Menu.init called >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")#####
        # Parameter validation
        from modules.table import Table  # matchs test_menu_constuctory.py
        if not isinstance(options, (list, Table)):
            raise TypeError("Expected `Table` or `list` for 'options'")
        if isinstance(options, list) and options == []:
            raise ValueError("'options' cannot be an empty list")
        if not (title is None or isinstance(title, str)):
            raise TypeError("Expected `str` or `None` for 'title'")
        if not (prompt is None or isinstance(prompt, str)):
            raise TypeError("Expected `str` or `None` for 'prompt'")

        # Assign validated attributes
        self._options = (Table(title=title, 
                               table_data=[{"OPTION": option} 
                                           for option in options]) 
                         if isinstance(options, list) else options)
        # print(f"TRACE: Menu.init _options set as {self._options}")#####
        self._count = self._options.count_records()
        # print(f"TRACE: Menu.init _count set as {self._count}")#####
        self.set_prompt(prompt)
    
    def get_selection(self, key: str = "OPTION") -> Any:
        return self._selection[key.upper()]

    def run(self) -> None:
        # print(f"TRACE: Menu.run called >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")#####
        self._options.put_table(is_menu=True)
        # print(f"TRACE: Menu.run Table.putTable executed")#####
        index = int(self._prompt.call()) - 1
        self._selection = self._options.get_record(index)

    def set_prompt(self, prompt: str | None = None) -> None:
        # print(f"TRACE: Menu.setPrompt called >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")#####
        count = self._count
        # print(f"TRACE: Menu.setPrompt.count: {count}")#####
        prompt = (f"Enter number (1-{count}) for selection:" 
                  if prompt is None else prompt)
        # print(f"TRACE: Menu.setPrompt.prompt: {prompt}")#####
        self._prompt = ConsolePrompt(prompt, 
                                     expect_keystroke=count < 10, 
                                     validate_integer=True, 
                                     integer_validation=(1, count))
        # print(f"TRACE: Menu.setPrompt _prompt set as {self._prompt}")#####
