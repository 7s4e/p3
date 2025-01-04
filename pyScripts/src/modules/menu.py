"""
Menu Module

This module defines a `Menu` class that allows for the creation and 
interaction with a menu system.

Imports:
    Standard library:
        from typing import Any: Represents any valid Python object type 
            in type annotations.

    Local modules:
        from console import ConsolePrompt: A class for handling user 
            prompts with validation for user responses.
        from table import Table: A helper class managing table data.

Class:
    Menu: A class representing a menu with options and user input 
        handling.

"""
# Standard library imports
from typing import Any

# Local module import
from .console import ConsolePrompt
from .table import Table

class Menu:
    """
    Represents a menu with options and user input handling.

    The `Menu` class allows creating a menu with options either from a 
    list or a `Table` object. The user can select an option by entering 
    the corresponding number.

    Args:
        options: A list of options or a `Table` object representing the 
            menu items.
        title: The title of the menu.
        prompt: A custom prompt message.

    Attributes:
        _ct: The number of menu options.
        _opts: Menu options as a `Table` object.
        _prmt: A `ConsolePrompt` object to manage user interaction.
        _sel: User-selected option.

    Methods:
        get_selection: Get user-selected option from the menu.
        run: Display menun and get user input.
        set_prompt: Set a `ConsolePrompt` object to manage user 
            interaction.
    """
    def __init__(self, options: list | Table, title: str | None = None, 
                 prompt: str | None = None) -> None:
        # Parameter validation
        from modules.table import Table
        if not isinstance(options, (list, Table)):
            raise TypeError("Expected `Table` or `list` for 'options'")
        if isinstance(options, list) and options == []:
            raise ValueError("'options' cannot be an empty list")
        if not (title is None or isinstance(title, str)):
            raise TypeError("Expected `str` or `None` for 'title'")
        if not (prompt is None or isinstance(prompt, str)):
            raise TypeError("Expected `str` or `None` for 'prompt'")

        # Assign validated attributes
        self._opts = (Table(title=title, 
                            table_data=[{"OPTION": option} for option in options]) 
                      if isinstance(options, list) else options)
        self._ct = self._opts.count_records()
        self.set_prompt(prompt)
    
    # Public methods
    def get_selection(self, key: str = "OPTION") -> Any:
        """
        Return the selected option from the menu.

        Args:
            key: The key used to retrieve the selection. 

        Returns:
            The selected option as any type.
        """
        return self._selection[key.upper()]

    def run(self) -> None:
        """
        Display the menu and wait for user input.

        Side effect:
            _sel: Set user selection.
        """
        self._opts.put_table(is_menu=True)
        index = int(self._prmt.call()) - 1
        self._sel = self._opts.get_record(index)

    def set_prompt(self, prompt: str | None = None) -> None:
        """
        Sets the `ConsolePrompt` object for the menu.

        Args:
            prompt: A custom prompt message.
        
        Side effect:
            _prmt: Set the prompt to manage the menu.
        """
        count = self._ct
        prompt = (f"Enter number (1-{count}) for selection:" 
                  if prompt is None else prompt)
        self._prmt = ConsolePrompt(prompt, expect_keystroke=count < 10, 
                                   validate_integer=True, 
                                   integer_validation=(1, count))
