"""Functions module."""

import subprocess
import sys
from table import Table


def run_command(command: str, 
                capture_output: bool = True,
                use_shell: bool = True) -> str | None:
    """Execute a shell command and return the output or print to stdout.

    Args:
        command: The command to run.
        capture_output: Whether to capture the output or print to 
            stdout.
        use_shell: Whether to use the shell to execute the command.

    Returns:
        The standard output from the command if capture_output is True, 
        otherwise None.

    Raises:
        RuntimeError: If the command fails, an exception is raised with 
        the error message.
    """
    if capture_output:
        result = subprocess.run(command, 
                                capture_output=True, 
                                shell=use_shell, 
                                text=True)
    else:
        result = subprocess.run(command, 
                                stdout=sys.stdout, 
                                stderr=sys.stderr, 
                                shell=use_shell, 
                                text=True)
    if result.returncode != 0:
        error_message = (result.stderr.strip() 
                         if capture_output else "Command failed.")
        raise RuntimeError(error_message)
    return result.stdout.strip() if capture_output else None


def run_badblocks(disk: str, 
                  non_destructive: bool = True, 
                  capture_output: bool = False) -> str | None:
    """Run the `badblocks` command on a specified disk.

    Args:
        disk: The disk identifier (e.g., 'sdb') on which to run 
            `badblocks`.
        non_destructive: If True, run `badblocks` in non-destructive 
            mode; if False, run in destructive write mode.
        capture_output: If True, capture and return the command's output 
            as a string; if False, redirect the output to the standard 
            output.

    Returns:
        The standard output from the command if `capture_output` is True; 
        otherwise, returns None.
    """
    mode = "--non-destructive" if non_destructive else "--write-mode"
    command = f"sudo badblocks {mode} --show-progress --verbose /dev/{disk}"
    if capture_output:
        return run_command(command)
    run_command(command, capture_output=False)
    return None


def unmount_disk(disk: str) -> None:
    """Unmount all mount points associated with a specified disk.

    Args:
        disk: The disk identifier (e.g., 'sda1').
    """
    output = run_command(f"lsblk --output PATH,MOUNTPOINT /dev/{disk}")
    disk_paths = Table(table_string=output)
    disk_paths.filter_nonempty("MOUNTPOINT")
    for i in range(disk_paths.count_records()):
        run_command(f"sudo umount --verbose {disk_paths.get_record(i)['PATH']}", 
                    capture_output=False)
