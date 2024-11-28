#!/usr/bin/env python3
# Standard library imports
from inspect import currentframe

# Third-party imports
from blessed import Terminal

# Local module imports
# from menu import Menu
from commands import list_block_devices, unmount_disk
from console import clear_stdscr, put_script_banner, ConsolePrompt
from table import Table


def confirm_disk(console: Terminal, disk: str) -> bool:
    """Prompt the user to confirm the selection of a disk.

    Args:
        disk: The name of the disk to confirm.

    Returns:
        True if the user confirms, False otherwise.
    """
    prompt = f"Are you sure you want to select the disk '{disk}'? (y/n) "
    output = list_block_devices(disk, 
                                columns=["NAME", "TYPE", "FSTYPE", "LABEL", 
                                         "MOUNTPOINTS"])
    partitions = Table(title="selected device", table_string=output)
    partitions.put_table(console)
    disk_confirmation = ConsolePrompt(prompt,
                                          expect_keystroke=True, 
                                          validate_bool=True)
    return disk_confirmation.call(console)


def get_disks() -> Table:
    """Retrieve a list of connected disks.

    Returns:
        A list of dictionaries containing disk information.
    """
    output = list_block_devices(columns=["NAME", "VENDOR", "SIZE"], 
                                show_dependents=False)
    disks = Table(title="connected devices", table_string=output, 
                  rjust_columns="SIZE")
    disks.filter_startswith("NAME", "sd")
    return disks


# def select_disk(console: Terminal, disks: Table) -> str:
#     """Prompt the user to select a disk from a list of disks.

#     Args:
#         disks: A list of dictionaries containing disk information.
#         count: The number of disks available for selection.

#     Returns:
#         The name of the selected disk.
#     """
#     disk_selection = Menu(disks)
#     disk_selection.run(console)
#     return disk_selection.get_selection("NAME")


def get_disk(console: Terminal) -> str:
    """Main function to select and confirm a disk.

    Continuously prompts the user to connect and select a disk until
    a disk is confirmed. Offers to unmount the disk if not confirmed.

    Returns:
        The name of the confirmed disk.
    """
    put_script_banner(console, currentframe().f_code.co_name)

    while True:
        disks = get_disks()
        count = disks.count_records()

        if count == 0:
            no_disk_msg = "Connect a device and press any key to continue..."
            no_disk_alert = ConsolePrompt(no_disk_msg, expect_keystroke=True)
            no_disk_alert.call(console)
            continue

    #     disk = (disks.get_record(0)["NAME"] 
    #             if count == 1 else select_disk(console, disks))

    #     if confirm_disk(console, disk):
    #         break
    #     else:
    #         if Menu.query_yes_no(f"Do you want to unmount '{disk}'? (y/n) "):
    #             unmount_disk(disk)
    #         print("Check device and press Enter...")
    #         input()

    # return disk


def main(console: Terminal) -> str:
    clear_stdscr(console)
    disk = get_disk(console)
    return disk


if __name__ == "__main__":
    console = Terminal()
    disk = main(console)
    print(disk)
