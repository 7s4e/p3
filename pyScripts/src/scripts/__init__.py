"""
Package Initialization File

This file defines the public API for the package by explicitly exposing
the primary script function.

Modules:
    - find_bonds_script: Contains the `find_bonds` function for selecting bonds
        for investing.
    - get_disk_script: Contains the `get_disk` function for disk-related 
        operations.

__all__:
    Defines symbols to be exported when using `from scripts import *`.
"""
# Importing the `get_disk` function from the module
from .find_bonds_script import find_bonds
from .get_disk_script import get_disk

# Explicitly defining public API
__all__ = ["find_bonds", "get_disk"]
