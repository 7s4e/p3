#!/usr/bin/env python3
"""
Bond Selection Script

This script evaluates a CSV file of bonds on the market and identifies those
with the best yields.

Functions:
    main(): Clears the screen and initiates the bond selection process.

Usage:
    Run this script directly to initiate the bond selection process. The script 
    can be integrated into other tools by importing the `get_bond` function.
"""
# Local module imports
# from modules import commands as cmd
from modules import utilities as utl
from modules import Console#, ConsolePrompt, Menu, Table


# def check_disk(caller):
#     """
#     Prompt user to check device connections and present option to quit.

#     Args:
#         caller: The calling file name.

#     Exit:
#         The script terminates at user's discretion.
#     """
#     msg = "Press 'q' to quit, or check disks and press any key to continue..."
#     prmpt = ConsolePrompt(msg, expect_keystroke=True)
#     rspns = prmpt.call()
#     utl.abort(rspns in {"q", "Q"}, caller)
    

# def confirm_disk(disk: str) -> bool:
#     """
#     Prompt the user to confirm the selection of a disk.

#     Args:
#         disk: The name of the disk to confirm.

#     Returns:
#         True if the user confirms, False otherwise.
#     """
#     prompt = f"Are you sure you want to select the disk '{disk}'? (y/n) "
#     output = cmd.list_block_devices(disk, 
#                                     columns=["NAME", "TYPE", "FSTYPE", "LABEL", 
#                                              "MOUNTPOINTS"])
#     partitions = Table(title="selected device", table_string=output)
#     print()
#     partitions.put_table()
#     disk_confirmation = ConsolePrompt(prompt, expect_keystroke=True, 
#                                       validate_bool=True)
#     return disk_confirmation.call()


# def get_disks() -> Table:
#     """
#     Retrieve a list of connected disks.

#     Returns:
#         A list of dictionaries containing disk information.
#     """
#     output = cmd.list_block_devices(columns=["NAME", "VENDOR", "SIZE"], 
#                                     show_dependents=False)
#     disks = Table(title="connected devices", table_string=output, 
#                   rjust_columns="SIZE")
#     disks.filter_startswith("NAME", "sd")
#     return disks


# def select_disk(disks: Table) -> str:
#     """
#     Prompt the user to select a disk from a list of disks.

#     Args:
#         disks: A list of dictionaries containing disk information.
#         count: The number of disks available for selection.

#     Returns:
#         The name of the selected disk.
#     """
#     disk_selection = Menu(disks)
#     print()
#     disk_selection.run()
#     return disk_selection.get_selection("NAME")


# def get_disk() -> str:
#     """
#     Main function to select and confirm a disk.

#     Continuously prompts the user to connect and select a disk until
#     a disk is confirmed. Offers to unmount the disk if not confirmed.

#     Returns:
#         The name of the confirmed disk.
#     """
#     caller_info = utl.get_caller_info()
#     Console.put_script_banner(caller_info["function"])

#     while True:
#         disks = get_disks()
#         count = disks.count_records()

#         if count == 0:
#             check_disk(caller_info["file"])
#             continue

#         disk = (disks.get_record(0)["NAME"] 
#                 if count == 1 else select_disk(disks))

#         if confirm_disk(disk):
#             break
#         else:
#             unmount_prompt = f"Do you want to unmount '{disk}'? (y/n)"
#             unmount_confirmation = ConsolePrompt(unmount_prompt, 
#                                                  expect_keystroke=True, 
#                                                  validate_bool=True)
#             if unmount_confirmation.call():
#                 cmd.unmount_disk(disk)
#             check_disk(caller_info["file"])

#     return disk

def find_bonds() -> str:
    """
    Placeholder function for bond selection.

    Returns:
        A string indicating the function is not yet implemented.
    """
    df = utl.read_csv("../../../in/bond.csv")
    print(df.head())
    return "Bond selection functionality is not yet implemented."


def main() -> str:
    Console.clear_screen()
    print(find_bonds())


if __name__ == "__main__":
    main()
