#!/usr/bin/env python3


from get_disk import get_disk
import scripts.commands as cmd
import interface as itf


def make_boot_disk(disk: str | None = None) -> None:
    if disk is None:
        disk = get_disk()
    cmd.unmount_disk(disk)
    itf.run_badblocks(disk)
    itf.run_parted(disk)


def main() -> None:
    make_boot_disk()


if __name__ == "__main__":
    main()

# print(f"MBD>mbd-disk: {disk}")

# ## Generic Preparation
# * `# parted /dev/sdX`
#     * `mklabel gpt` to create partition table
#     * `mkpart primary 0% 100%` to create partition
#     * `set 1 msftdata on` for Windows data
# * `# mkfs.exfat -n "My Label" /dev/sdXn`