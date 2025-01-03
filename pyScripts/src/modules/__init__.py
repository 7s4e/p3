"""
Package Initialization File

This file defines the public API for the `modules` package by explicitly 
listing the modules and classes to be exposed when using 
`from modules import *`.

Modules:
    - commands: Provides various commands for the package.
    - utilities: Contains utility functions and helpers.

Classes:
    - Console: Handles console-related operations.
    - ConsolePrompt: Facilitates console-based user prompts.
    - ConsoleTable: Manages console-based table rendering.
    - Menu: Supports interactive menu creation and management.
    - Table: Implements table-related functionalities.

__all__:
    Defines symbols to be exported when using `from modules import *`.
"""
# Importing modules
from . import commands, utilities

# Importing classes
from .console import Console, ConsolePrompt, ConsoleTable
from .menu import Menu
from .table import Table

# Explicitly defining public API
__all__ = ["commands", "utilities", 
           "Console", "ConsolePrompt", "ConsoleTable", 
           "Menu", 
           "Table"]
