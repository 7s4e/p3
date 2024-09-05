#!/usr/bin/env python3

from menu import Menu
import commands as cmd

def delete_disk(disk: str) -> None:
    options = ["dd", "shred", "wipefs", "blkdiscard"]
    pass

def run_badblocks(disk: str) -> None:
    options = ["Non-destructive read-write mode",
               "Destructive write mode"]
    menu = Menu(options, "badblocks test mode")
    menu.run()
    match menu.get_selection():
        case "Non-destructive read-write mode":
            cmd.run_badblocks(disk, non_destructive=True)
        case "Destructive write mode":
            cmd.run_badblocks(disk, non_destructive=False)

def run_fsck(disk: str) -> None:
    options = ["Preview file system check" # --no-action
               ]
    pass # -v
