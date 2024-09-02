"""Functions module."""

import subprocess
from table import Table


def query_integer(min_value: int, max_value: int, prompt: str) -> int:
    """Prompt the user to enter an integer within a specified range.

    Args:
        min_value: The minimum acceptable value.
        max_value: The maximum acceptable value.
        prompt: The prompt message displayed to the user.

    Returns:
        The integer value entered by the user.

    Raises:
        ValueError: If the input is not a valid integer.
    """
    while True:
        try:
            selection = int(input(prompt))
            if min_value <= selection <= max_value:
                return selection
            print(f"Enter a number between {min_value} and {max_value}.")
        except ValueError:
            print("Enter a valid number.")


def query_yes_no(prompt: str) -> bool:
    """Prompt the user to answer with 'y' or 'n'.

    Args:
        prompt: The prompt message displayed to the user.

    Returns:
        True if the user responds with 'y', False if the user responds 
            with 'n'.
    """
    while True:
        response = input(prompt).strip().lower()
        if response in {'y', 'n'}:
            return response == 'y'
        print("Respond with 'y' or 'n'.")


def run_command(command: str, use_shell: bool = True) -> str:
    """Execute a shell command and return the output.

    Args:
        command: The command to run.
        use_shell: Whether to use the shell to execute the 
            command.

    Returns:
        The standard output from the command.

    Raises:
        RuntimeError: If the command fails, an exception is raised with 
            the error message.
    """
    result = subprocess.run(command, 
                            shell=use_shell, 
                            text=True, 
                            capture_output=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {result.stderr.strip()}")
    return result.stdout.strip()


def run_script(command: str) -> None:
    # Run the script with user interaction
    process = subprocess.Popen(['./get_disk.py'])
    try:
        # Wait for the process to complete, allowing user interaction
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        process.kill()
    # Since the user interacted directly, no need to capture stdout/stderr


def unmount_disk(disk: str) -> None:
    """Unmount all mount points associated with a specified disk.

    Args:
        disk: The disk identifier (e.g., 'sda1').
    """
    output = run_command(f"lsblk --output PATH,MOUNTPOINT /dev/{disk}")
    disk_paths = Table(table_string=output)
    disk_paths.filter_nonempty("MOUNTPOINT")
    for i in range(disk_paths.count_records()):
        run_command(f"sudo umount {disk_paths.get_record(i)['PATH']}")
