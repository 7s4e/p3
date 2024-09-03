#!/usr/bin/env python3


from get_disk import get_disk

MAIN_MENU = [
    "Check disk health"
]

CHECK_MENU = [
    
]

def make_boot_disk(disk: str | None = None) -> None:
    if disk is None:
        disk = get_disk()
    print(f"MBD>mbd-disk: {disk}")


def main() -> None:
    make_boot_disk()


if __name__ == "__main__":
    main()

# print(f"MBD>mbd-disk: {disk}")

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