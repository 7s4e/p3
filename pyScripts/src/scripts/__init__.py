"""
Package Initialization File

This file defines the public API for the package by explicitly exposing
the `get_disk` function.

Modules:
    - get_disk_script: Contains the `get_disk` function for disk-related 
        operations.

__all__:
    Defines symbols to be exported when using `from scripts import *`.
"""
# Importing the `get_disk` function from the module
from .get_disk_script import get_disk

# Explicitly defining public API
__all__ = ["get_disk"]
