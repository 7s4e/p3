#!/usr/bin/env python3

import functions as fm
from typing import Dict, List

# Constants
RIGHT_JUSTIFIED_COLUMNS = ["#", "SIZE"]

# Functions
def confirm_disk(disk: str) -> bool:
    """Prompt the user to confirm the selection of a disk.

    Args:
        disk: The name of the disk to confirm.

    Returns:
        True if the user confirms, False otherwise.
    """
    prompt = f"Are you sure you want to select the disk '{disk}'? (y/n) "
    put_partitions(disk, len(prompt))
    return fm.query_yes_no(prompt)

def get_disks() -> List[Dict[str, str]]:
    """Retrieve a list of connected disks.

    Returns:
        A list of dictionaries containing disk information.
    """
    output = fm.run_command("lsblk --nodeps --output NAME,VENDOR,SIZE")
    dataset = fm.read_table(output)
    return [record for record in dataset if record["NAME"].startswith("sd")]

def put_disks(disks: List[Dict[str, str]], display_width: int) -> None:
    """Display a table of connected disks.

    Args:
        disks: A list of dictionaries containing disk information.
        display_width: The width of the table display.
    """
    fm.put_table("CONNECTED DEVICES", fm.number_records(disks), display_width, 
                 right_justified_columns=RIGHT_JUSTIFIED_COLUMNS)

def put_partitions(disk: str, display_width: int) -> None:
    """Display a table of partitions for a selected disk.

    Args:
        disk: The name of the disk.
        display_width: The width of the table display.
    """
    output = fm.run_command(
        f"lsblk --output NAME,TYPE,FSTYPE,LABEL,MOUNTPOINTS /dev/{disk}"
        )
    fm.put_table("SELECTED DEVICE", fm.read_table(output), display_width)

def select_disk(disks: List[Dict[str, str]], count: int) -> str:
    """Prompt the user to select a disk from a list of disks.

    Args:
        disks: A list of dictionaries containing disk information.
        count: The number of disks available for selection.

    Returns:
        The name of the selected disk.
    """
    prompt = f"Enter a number to select a device (1-{count}): "
    put_disks(disks, len(prompt))
    selection = fm.query_integer(1, count, prompt)
    return disks[selection - 1]["NAME"]

def main() -> str:
    """Main function to select and confirm a disk.

    Continuously prompts the user to connect and select a disk until
    a disk is confirmed. Offers to unmount the disk if not confirmed.

    Returns:
        The name of the confirmed disk.
    """
    while True:
        disks = get_disks()
        count = len(disks)

        if count == 0:
            print("Connect a device and press any key to continue...")
            input()
            continue

        disk = disks[0]["NAME"] if count == 1 else select_disk(disks, count)

        if confirm_disk(disk):
            break
        else:
            if fm.query_yes_no(f"Do you want to unmount '{disk}'? (y/n) "):
                fm.unmount_disk(disk)
            print("Check device and press any key to continue...")
            input()

    return disk

if __name__ == "__main__":
    main()
