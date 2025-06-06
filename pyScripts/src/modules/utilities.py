"""
Utilities Module

Functions:
    abort(signal, scr_name): Exit the script if the signal is True.
    get_calendar_difference(start, end): Calculate calendar-based date 
        difference.
    get_caller_info(): Retrieve function name, file, and line number of 
        the caller.
    snake_to_camel(snake_str): Convert a snake_case string to camelCase.
    truncate_string(strng, max_lngth): Truncate a string and append 
        ellipses.
"""
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from inspect import currentframe
from pandas import Timestamp
from typing import Union
from sys import exit


def abort(signal: bool, scr_name: str) -> None:
    """
    Quits running script gracefully with exit code 10.
    
    Args:
        scr_name (str): The name of the script.
    """
    if signal:
        print(f"Aborted {scr_name}")
        exit(10)


def get_calendar_difference(start: Union[date, datetime, Timestamp], 
                            end: Union[date, datetime, Timestamp]
                            ) -> relativedelta:
    """
    Calculate the calendar-based difference between two dates.

    Args:
        start (Union[date, datetime, Timestamp]): The starting date.
        end (Union[date, datetime, Timestamp]): The ending date.

    Returns:
        relativedelta: The calendar-based difference between `end` and 
            `start` as a `relativedelta` object with attributes for 
            `years`, `months`, `days`, and other calendar components.
    """
    return relativedelta(end, start)


def get_caller_info() -> dict[str, str]:
    """
    Retrieves information about the calling frame, including the 
    function name, file name, and line number.

    Returns:
        A dictionary with keys 'function', 'file', and 'line', 
        containing the respective information about the caller.
    """
    frame = currentframe()
    if frame is None or frame.f_back is None:
        return {"function": "", "file": "", "line": ""}
    caller_frame = frame.f_back
    return {"function": caller_frame.f_code.co_name,
            "file": caller_frame.f_code.co_filename, 
            "line": str(caller_frame.f_lineno)}


def snake_to_allcaps(snake_str: str) -> str:
    words = snake_str.split('_')
    return ' '.join(word.upper() for word in words)


def snake_to_camel(snake_str: str) -> str:
    """
    Converts a snake_case string to camelCase.
    
    Args:
        snake_str (str): The input string in snake_case.
        
    Returns:
        str: The converted string in camelCase.
    """
    parts = snake_str.split('_')
    return parts[0] + ''.join(part.capitalize() for part in parts[1:])


def snake_to_title(snake_str: str) -> str:
    words = snake_str.split('_')
    return ' '.join(word.capitalize() for word in words)


def truncate_string(strng: str, max_lngth: int) -> str:
    """
    Truncate a string to a specified maximum length, adding ellipses
    if the string is truncated.

    Args:
        strng (str): The string to truncate.
        max_lngth (int): The maximum allowed length, including ellipses.

    Returns:
        str: The truncated string with ellipses if necessary.
    """
    lgth = len(str(strng))
    return (strng if lgth <= max_lngth 
            else "." * max_lngth if max_lngth < 3 
            else strng[:max_lngth - 3] + "...")
