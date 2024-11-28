"""Commands module: Contains functions to run system commands."""

# Standard library imports
from subprocess import run
from sys import stdout, stderr

# Local module imports
from table import Table


def list_block_devices(disk: str | None = None, 
                       columns: list[str] = list(),
                       show_dependents: bool = True) -> str:
    """Generate and run the 'lsblk' command to list block devices with 
        optional filters.

    Args:
        disk (str | None, optional): The specific disk to query (e.g., 
            'sda'). If None, all disks are listed. Defaults to None.
        columns (list[str], optional): A list of columns to include in 
            the output. Defaults to an empty list.
        show_dependents (bool, optional): If True, include dependent 
            devices (e.g., partitions). If False, append '--nodeps' to 
            exclude them. Defaults to True.

    Returns:
        str: The output of the 'lsblk' command.
    """
    # Construct the command based on the parameters
    deps = "" if show_dependents else " --nodeps"
    output = "" if not columns else f" --output {','.join(columns)}"
    path = "" if disk is None else f" /dev/{disk}"
    
    # Run the constructed 'lsblk' command and return its output.
    return run_command("lsblk" + deps + output + path)


def run_badblocks(disk: str, 
                  non_destructive: bool = True, 
                  capture_output: bool = False) -> str | None:
    """Run the `badblocks` command on a specified disk to check for bad 
        sectors.

    Args:
        disk (str): The disk identifier (e.g., 'sdb') on which to run 
            `badblocks`.
        non_destructive (bool, optional): If True, run `badblocks` in 
            non-destructive mode; if False, run in destructive write 
            mode. Defaults to True.
        capture_output (bool, optional): If True, capture and return the 
            command's output as a string; if False, redirect the output 
            to the standard output. Defaults to False.

    Returns:
        str | None: The standard output from the command if 
            `capture_output` is True; otherwise, returns None.
    """
    # Select mode based on the non_destructive flag
    mode = "--non-destructive" if non_destructive else "--write-mode"
    
    # Construct the `badblocks` command
    command = f"sudo badblocks {mode} --show-progress --verbose /dev/{disk}"
    
    # Run the command and capture or display the output based on the 
    # capture_output flag
    if capture_output:
        return run_command(command, capture_output=True)
    run_command(command, capture_output=False)
    return None


def run_command(command: str, 
                capture_output: bool = True,
                use_shell: bool = True) -> str | None:
    """Execute a shell command and return the output or print to stdout.

    Args:
        command (str): The command to run.
        capture_output (bool, optional): Whether to capture the output 
            or print to stdout. Defaults to True.
        use_shell (bool, optional): Whether to use the shell to execute 
            the command. Defaults to True

    Returns:
        str | None: The standard output from the command if 
            capture_output is True; otherwise None.

    Raises:
        RuntimeError: If the command fails, an exception is raised with 
            the error message.
    """
    if capture_output:
        result = run(command, capture_output=True, stdout=None, stderr=None, 
                     shell=use_shell, text=True)
    else:
        result = run(command, capture_output=False, stdout=stdout, 
                     stderr=stderr, shell=use_shell, text=True)

    # Check for command failure and raise an error with the appropriate message.
    if result.returncode != 0:
        error_message = (result.stderr.strip() 
                         if capture_output else "Command failed.")
        raise RuntimeError(error_message)

    # Return the output or None, depending on the capture_output flag.
    return result.stdout.strip() if capture_output else None


def unmount_disk(disk: str) -> None:
    """Unmount all mount points associated with a specified disk.

    Args:
        disk (str): The disk identifier (e.g., 'sda1').
    """
    # Get the list of mount points for the given disk using 'lsblk'
    output = run_command(f"lsblk --output PATH,MOUNTPOINT /dev/{disk}")
    
    # Create a table from the output and filter to keep only non-empty 
    # mount points
    disk_paths = Table(table_string=output)
    disk_paths.filter_nonempty("MOUNTPOINT")
    
    # Unmount each disk path in the table
    for i in range(disk_paths.count_records()):
        cmd_str = f"sudo umount --verbose {disk_paths.get_record(i)['PATH']}"
        run_command(cmd_str, capture_output=False)
