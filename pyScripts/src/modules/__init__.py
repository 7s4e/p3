"""
Package Initialization File

This file defines the public API for the `modules` package by explicitly 
listing the modules and classes to be exposed when using 
`from modules import *`.

Modules:
    commands: Provides various commands for the package.
    utilities: Contains utility functions and helpers.

Classes:
    Console: Handles console-related operations.
    ConsoleAnyKeyPrompt: Prompts for any key from user.
    ConsoleBooleanPrompt: Prompts for yes/no response from user.
    ConsoleFreeFormPrompt: Prompts for any response from user.
    ConsoleIntegerPrompt: Prompts for validated integer from user.
    ConsoleTable: Manages console-based table rendering.
    Menu: Supports interactive menu creation and management.
    Table: Implements table-related functionalities.

__all__:
    Defines symbols to be exported when using `from modules import *`.
"""
# Importing modules
from . import commands, utilities

# Importing classes
from .console import Console, ConsoleAnyKeyPrompt, ConsoleBooleanPrompt
from .console import ConsoleFreeFormPrompt, ConsoleIntegerPrompt, ConsoleTable
from .menu import Menu
from .table import Table

# Explicitly defining public API
__all__ = ["commands", "utilities", 
           "Console", "ConsoleAnyKeyPrompt", "ConsoleBooleanPrompt", 
           "ConsoleFreeFormPrompt", "ConsoleIntegerPrompt", "ConsoleTable", 
           "Menu", 
           "Table"]
