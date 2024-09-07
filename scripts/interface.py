#!/usr/bin/env python3

from menu import Menu
import commands as cmd

def delete_disk(disk: str) -> None:
    options = ["dd", "shred", "wipefs", "blkdiscard"]
    pass

def run_badblocks(disk: str) -> None:
    """Prompt the user to select a `badblocks` test mode and execute the 
        corresponding command.

    Args:
        disk: The disk identifier (e.g., 'sdb') on which to run 
            `badblocks`.

    Returns:
        None

    This function presents a menu with three options:
        1. Non-destructive read-write mode
        2. Destructive write mode
        3. Skip

    Based on the user's selection, it calls `cmd.run_badblocks` with the 
    appropriate mode or skips execution if the user selects "Skip".
    """
    options = ["Non-destructive read-write mode",
               "Destructive write mode",
               "Skip `badblocks`"]
    menu = Menu(options, "badblocks")
    menu.run()
    
    match menu.get_selection():
        case "Non-destructive read-write mode":
            cmd.run_badblocks(disk, non_destructive=True)
        case "Destructive write mode":
            cmd.run_badblocks(disk, non_destructive=False)
        case "Skip `badblocks`":
            pass


def run_fsck(disk: str) -> None:
    options = ["Preview file system check" # --no-action
               ]
    pass # -v


def run_parted(disk: str) -> None:
    print("parting")
