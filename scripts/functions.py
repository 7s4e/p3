"""Functions module."""

import subprocess
from table import Table


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
