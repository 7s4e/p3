#!/usr/bin/env python3
# Standard library imports
import inspect

# Third-party imports
from blessed import Terminal

# Local module imports
from menu import Menu
from table import Table
import commands as cmd
import terminal as trm


def confirm_disk(terminal: Terminal, disk: str) -> bool:
    """Prompt the user to confirm the selection of a disk.

    Args:
        disk: The name of the disk to confirm.

    Returns:
        True if the user confirms, False otherwise.
    """
    prompt = f"Are you sure you want to select the disk '{disk}'? (y/n) "
    output = cmd.list_block_devices(disk, 
                                    columns=["NAME", "TYPE", "FSTYPE", "LABEL", 
                                             "MOUNTPOINTS"])
    partitions = Table(title="selected device", table_string=output)
    partitions.put_table(terminal)
    return Menu.query_yes_no(prompt)


def get_disks() -> Table:
    """Retrieve a list of connected disks.

    Returns:
        A list of dictionaries containing disk information.
    """
    output = cmd.list_block_devices(columns=["NAME", "VENDOR", "SIZE"], 
                                    show_dependendents=False)
    disks = Table(title="connected devices", 
                  table_string=output, 
                  right_justified_column_labels="SIZE")
    disks.filter_startswith("NAME", "sd")
    return disks


def select_disk(term: Terminal, disks: Table) -> str:
    """Prompt the user to select a disk from a list of disks.

    Args:
        disks: A list of dictionaries containing disk information.
        count: The number of disks available for selection.

    Returns:
        The name of the selected disk.
    """
    disk_selection = Menu(disks)
    disk_selection.run(term)
    return disk_selection.get_selection("NAME")


def get_disk(terminal: Terminal) -> str:
    """Main function to select and confirm a disk.

    Continuously prompts the user to connect and select a disk until
    a disk is confirmed. Offers to unmount the disk if not confirmed.

    Returns:
        The name of the confirmed disk.
    """
    trm.put_script_banner(terminal, inspect.currentframe().f_code.co_name)

    while True:
        disks = get_disks()
        count = disks.count_records()

        if count == 0:
            trm.prompt_key(terminal, 
                           "Connect a device and press any key to continue...")
            continue

        disk = (disks.get_record(0)["NAME"] 
                if count == 1 else select_disk(terminal, disks))

        if confirm_disk(terminal, disk):
            break
        else:
            if Menu.query_yes_no(f"Do you want to unmount '{disk}'? (y/n) "):
                cmd.unmount_disk(disk)
            print("Check device and press Enter...")
            input()

    return disk


def main(terminal: Terminal) -> str:
    trm.clear_stdscr(terminal)
    disk = get_disk(terminal)
    return disk


if __name__ == "__main__":
    terminal = Terminal()
    disk = main(terminal)
    print(disk)
