#!/usr/bin/env python3


from menu import Menu
from table import Table
import commands as cmd


RIGHT_JUSTIFIED_COLUMNS = ["#", "SIZE"]


def confirm_disk(disk: str) -> bool:
    """Prompt the user to confirm the selection of a disk.

    Args:
        disk: The name of the disk to confirm.

    Returns:
        True if the user confirms, False otherwise.
    """
    prompt = f"Are you sure you want to select the disk '{disk}'? (y/n) "
    output = cmd.run_command(
        f"lsblk --output NAME,TYPE,FSTYPE,LABEL,MOUNTPOINTS /dev/{disk}")
    partitions = Table(title="selected device", table_string=output)
    partitions.put_table(display_width=len(prompt))
    return Menu.query_yes_no(prompt)


def get_disks() -> Table:
    """Retrieve a list of connected disks.

    Returns:
        A list of dictionaries containing disk information.
    """
    output = cmd.run_command("lsblk --nodeps --output NAME,VENDOR,SIZE")
    disks = Table(title="connected devices", 
                  table_string=output, 
                  right_justified_column_labels="SIZE")
    disks.filter_startswith("NAME", "sd")
    return disks


def select_disk(disks: Table) -> str:
    """Prompt the user to select a disk from a list of disks.

    Args:
        disks: A list of dictionaries containing disk information.
        count: The number of disks available for selection.

    Returns:
        The name of the selected disk.
    """
    disk_selection = Menu(disks)
    disk_selection.run()
    return disk_selection.get_selection("NAME")


def get_disk() -> str:
    """Main function to select and confirm a disk.

    Continuously prompts the user to connect and select a disk until
    a disk is confirmed. Offers to unmount the disk if not confirmed.

    Returns:
        The name of the confirmed disk.
    """
    while True:
        disks = get_disks()
        count = disks.count_records()

        if count == 0:
            print("Connect a device and press any key to continue...")
            input()
            continue

        disk = (disks.get_record(0)["NAME"] 
                if count == 1 else select_disk(disks))

        if confirm_disk(disk):
            break
        else:
            if Menu.query_yes_no(f"Do you want to unmount '{disk}'? (y/n) "):
                cmd.unmount_disk(disk)
            print("Check device and press Enter...")
            input()

    return disk


def main() -> str:
    disk = get_disk()
    return disk


if __name__ == "__main__":
    disk = main()
    print(disk)
