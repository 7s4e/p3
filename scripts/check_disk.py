#!/usr/bin/env python3

from menu import Menu
import commands as cmd
from get_disk import get_disk

def run_badblocks(disk: str) -> None:
    options = ["Non-destructive read-write mode",
               "Destructive write mode"]
    menu = Menu(options, "badblocks test mode")
    menu.run()
    match menu.get_selection():
        case "Non-destructive read-write mode":
            cmd.run_command(f"sudo badblocks -nsv /dev/{disk}")
            # -sv no show
        case "Destructive write mode":
            cmd.run_command(f"sudo badblocks -wsv /dev/{disk}")

def run_fsck(disk: str) -> None:
    pass

def check_disk(disk: str | None = None) -> None:
    if disk is None:
        disk = get_disk()
    cmd.unmount_disk(disk)
    options = ["Scan for bad sectors", 
               "Check file system", 
               "Do both"]
    menu = Menu(options, "check disk")
    menu.run()
    match menu.get_selection():
        case "Scan for bad sectors":
            run_badblocks(disk)
        case "Check file system":
            run_fsck(disk)
        case "Do both":
            run_badblocks(disk)
            run_fsck(disk)


def main() -> None:
    check_disk()


if __name__ == "__main__":
    main()

# print(f"MBD>mbd-disk: {disk}")
# sudo badblocks -v /dev/sdX > badsectors.txt
# sudo fsck -l badsectors.txt /dev/sdX
# ## Generic Preparation
# * `$ lsblk` to identify storage devices
# * `# umount /dev/sdXn` to unmount
# * `# badblocks -sv /dev/sdX` to check health status
#     * `-sv` read-only test
#     * `-nsv` non-destructive read-write test
#     * `-wsv` destructive read-write test
# * `# parted /dev/sdX`
#     * `mklabel gpt` to create partition table
#     * `mkpart primary 0% 100%` to create partition
#     * `set 1 msftdata on` for Windows data
# * `# mkfs.exfat -n "My Label" /dev/sdXn`