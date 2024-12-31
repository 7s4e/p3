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
    