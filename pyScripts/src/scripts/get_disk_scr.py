#!/usr/bin/env python3
# Local module imports
from modules import commands as cmd
from modules import utilities as utl
from modules import Console, ConsolePrompt, Menu, Table


def confirm_disk(disk: str) -> bool:
    """Prompt the user to confirm the selection of a disk.

    Args:
        disk: The name of the disk to confirm.

    Returns:
        True if the user confirms, False otherwise.
    """
    # print(f"TRACE: GD > main > getDisk > confirmDisk called with {disk}")#####
    prompt = f"Are you sure you want to select the disk '{disk}'? (y/n) "
    # print(f"TRACE: GD > main > getDisk > confirmDisk.prompt assigned")#####
    output = cmd.list_block_devices(disk, 
                                    columns=["NAME", "TYPE", "FSTYPE", "LABEL", 
                                             "MOUNTPOINTS"])
    # print(f"TRACE: GD > main > getDisk > confirmDisk.output: {output}")#####
    partitions = Table(title="selected device", table_string=output)
    # print(f"TRACE: GD > main > getDisk > confirmDisk.partitions: {partitions}")#####
    print()
    # print(f"TRACE: GD > main > getDisk > confirmDisk new line printed")#####
    partitions.put_table()
    # print(f"TRACE: GD > main > getDisk > confirmDisk.partitions put")#####
    disk_confirmation = ConsolePrompt(prompt, 
                                      expect_keystroke=True, 
                                      validate_bool=True)
    # print(f"TRACE: GD > main > getDisk > confirmDisk.disk_confirmation: {disk_confirmation}")#####
    return disk_confirmation.call()


def get_disks() -> Table:
    """Retrieve a list of connected disks.

    Returns:
        A list of dictionaries containing disk information.
    """
    # print(f"TRACE: GD > main > getDisk > getDisks called >>>>>>>>>>>>>>>>>>>>>")#####
    output = cmd.list_block_devices(columns=["NAME", "VENDOR", "SIZE"], 
                                    show_dependents=False)
    # print(f"TRACE: GD > main > getDisk > getDisks.output: {output}")#####
    disks = Table(title="connected devices", table_string=output, 
                  rjust_columns="SIZE")
    # print(f"TRACE: GD > main > getDisk > getDisks.disks: {disks}")#####
    disks.filter_startswith("NAME", "sd")
    # print(f"TRACE: GD > main > getDisk > getDisks.disks: {disks}")#####
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
    print()
    disk_selection.run()
    return disk_selection.get_selection("NAME")


def get_disk() -> str:
    """Main function to select and confirm a disk.

    Continuously prompts the user to connect and select a disk until
    a disk is confirmed. Offers to unmount the disk if not confirmed.

    Returns:
        The name of the confirmed disk.
    """
    print(f"TRACE: GD > main > getDisk called >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")#####
    caller_info = utl.get_caller_info()
    Console.put_script_banner(caller_info["function"])
    print(f"TRACE: GD > main > getDisk Console.putScriptBanner executed")#####

    while True:
        print(f"TRACE: GD > main > getDisk loop started")#####
        disks = get_disks()
        print(f"TRACE: GD > main > getDisk.disks: {disks}")#####
        count = disks.count_records()
        print(f"TRACE: GD > main > getDisk.count: {count}")#####

        if count == 0:
            print(f"TRACE: GD > main > getDisk.count == 0 ....................")#####
            no_disk_msg = ("Press 'q' to quit, or connect a device and " +
                           "press any key to continue...")
            print(f"TRACE: GD > main > getDisk.no_disk_msg assigned")#####
            no_disk_alert = ConsolePrompt(no_disk_msg, expect_keystroke=True)
            print(f"TRACE: GD > main > getDisk.no_disk_alert: {no_disk_alert}")#####
            response = no_disk_alert.call()
            print(f"TRACE: GD > main > getDisk.response: {response}")#####
            utl.abort(response in {"q", "Q"}, caller_info["file"])
            continue

        disk = (disks.get_record(0)["NAME"] 
                if count == 1 else select_disk(disks))
        print(f"TRACE: GD > main > getDisk.disk: {disk}")#####

        if confirm_disk(disk):
            break
        else:
            unmount_prompt = f"Do you want to unmount '{disk}'? (y/n)"
            unmount_confirmation = ConsolePrompt(unmount_prompt, 
                                                 expect_keystroke=True, 
                                                 validate_bool=True)
            if unmount_confirmation.call():
                cmd.unmount_disk(disk)
            check_disk_msg = "Check device and press any key..."
            check_disk_alert = ConsolePrompt(check_disk_msg, 
                                             expect_keystroke=True)
            check_disk_alert.call()

    return disk


def main() -> str:
    Console.clear_stdscr()
    print(f"TRACE: GD > main called >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")#####
    return get_disk()


if __name__ == "__main__":
    disk = main()
    print(disk)
