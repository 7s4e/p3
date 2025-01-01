import inspect
import sys


def abort(signal: bool, scr_name: str) -> None:
    """
    Quits running script gracefully with exit code 10.
    
    Args:
        scr_name (str): The name of the script.
    """
    if signal:
        print(f"Aborted {scr_name}")
        sys.exit(10)


def get_caller_info() -> dict[str, str]:
    """
    Retrieves information about the calling frame, including the 
    function name, file name, and line number.

    Returns:
        A dictionary with keys 'function', 'file', and 'line', 
        containing the respective information about the caller.
    """
    frame = inspect.currentframe()
    if frame is None or frame.f_back is None:
        return {"function": "", "file": "", "line": ""}
    caller_frame = frame.f_back
    return {"function": caller_frame.f_code.co_name,
            "file": caller_frame.f_code.co_filename, 
            "line": str(caller_frame.f_lineno)}


def snake_to_camel(snake_str: str) -> str:
    """
    Converts a snake_case string to camelCase.
    
    Args:
        snake_str (str): The input string in snake_case.
        
    Returns:
        str: The converted string in camelCase.
    """
    segments = snake_str.split('_')
    return segments[0] + ''.join(segment.capitalize() for segment in segments[1:])
    