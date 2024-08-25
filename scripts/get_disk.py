#!/usr/bin/env python3
import subprocess
# import json
# import os

# Constants
BORDER_STYLE = "="
COLUMN_GAP = "  "

# Helper functions
def run_command(command):
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        raise Exception(f"Command failed: {result.stderr.strip()}")
    return result.stdout.strip()

def query_yes_no(prompt):
    while True:
        response = input(prompt).lower()
        if response in ('y', 'n'):
            return response == 'y'
        print("Please respond with 'y' or 'n'.")

def query_integer(min_value, max_value, prompt):
    while True:
        try:
            selection = int(input(prompt))
            if min_value <= selection <= max_value:
                return selection
            print(f"Please enter a number between {min_value} and {max_value}.")
        except ValueError:
            print("Please enter a valid number.")

def unmount_disk(disk):
    partitions = run_command(f"lsblk -n -o MOUNTPOINT /dev/{disk}")
    for partition in partitions.splitlines():
        if partition:
            run_command(f"sudo umount {partition.strip()}")

# Core functions
def confirm_disk(disk):
    put_partitions(disk)
    return query_yes_no(f"Are you sure you want to select the disk '{disk}'? (y/n) ")

def get_disks():
    NAME_IDX = 0
    VENDOR_IDX = 1
    SIZE_IDX = -1
    disks = []
    output = run_command("lsblk -d --noheadings --output NAME,VENDOR,SIZE")
    for line in output.splitlines():
        columns = line.split()
        name = columns[NAME_IDX]
        vendor = columns[VENDOR_IDX] if len(columns) > 2 else ""
        size = columns[SIZE_IDX]
        if name.startswith("sd"):
            disks.append({"name": name, "vendor": vendor, "size": size})
    return disks

def put_disks(disks, display_width=36):

    def calculate_column_widths(data):
        return [max(len(row[i]) for row in data) for i in range(len(data[0]))]
    
    def format_row(row, column_widths, right_justify_indexes):
        formatted_row = []
        for i, cell in enumerate(row):
            if i in right_justify_indexes:
                formatted_row.append(f"{cell:>{column_widths[i]}}")
            else:
                formatted_row.append(f"{cell:<{column_widths[i]}}")
        return formatted_row

    def print_table(title, table_data, display_width):
        title_padding = (display_width - len(title)) // 2
        column_widths = calculate_column_widths(table_data)
        column_widths = [len("#")] + column_widths
        table_width = sum(column_widths) + len("  ") * (len(table_data[0]) - 1)
        table_padding = max(0, (display_width - table_width) // 2)
        display_width = max(display_width, table_width)
####
        print(f"\n{' ' * title_padding}{title}")
        print(f"{BORDER_STYLE * display_width}")
        for i, row in enumerate(table_data):
            first_column = "#" if i == 0 else str(i)
            row_content = " " * table_padding + first_column + " " * COLUMN_GAP
            row_content += f"{' ' * COLUMN_GAP}".join(
                format_row(row, column_widths, [])
            )
            print(row_content)
        print(f"{BORDER_STYLE * display_width}")

    table_headers = list(disks[0].keys())
    table_data = [[str(disk[key]) for key in table_headers] for disk in disks]
    disks_table = [table_headers] + table_data
    print_table("CONNECTED DEVICES", disks_table, display_width)

    # print(f"\n{' ' * title_padding}{table_title}")
    # print(f"{BORDER_STYLE * display_width}")
    # for i, row in enumerate(table_data):
    #     first_column = "#" if i == 0 else str(i)
    #     row_content = " " * table_padding + first_column
    #     for j in range(len(table_columns)):
    #         column_content = row[j] if i != 0 else row[j].upper()
    #         if j != right_justify_index:
    #             column_content = f"{column_content:<{column_widths[j]}}"
    #         else:
    #             column_content = f"{column_content:>{column_widths[j]}}"
    #         row_content += f"{' ' * COLUMN_GAP}{column_content}"
    #     print(row_content)
    # print(f"{BORDER_STYLE * display_width}")



def put_partitions(disk):
    output = run_command(f"lsblk --output NAME,TYPE,FSTYPE,LABEL,MOUNTPOINTS /dev/{disk}")
    lines = output.splitlines()

    table_columns = lines[0].split()
    rows = [line.split() for line in lines[1:]]

    max_width = 80
    table_title = "SELECTED DEVICE"

    col_widths = [max(len(row[i]) for row in [table_columns] + rows) for i in range(len(table_columns))]
    table_width = sum(col_widths) + COLUMN_GAP * (len(table_columns) - 1)
    table_width = min(table_width, max_width)

    hdg_padding = (table_width - len(table_title)) // 2
    print(f"\n{' ' * hdg_padding}{table_title}")
    print(BORDER_STYLE * table_width)

    for row in [table_columns] + rows:
        print("  ".join([f"{row[i]:<{col_widths[i]}}" for i in range(len(table_columns))]))
    print(BORDER_STYLE * table_width)

def main():
    while True:
        disks = get_disks()
        count = len(disks)

        match count:
            case 0:
                print("Connect a device and press any key to continue...")
                input()
                continue
            case 1:
                disk = disks[0]['name']
            case _:
                prompt = f"Enter a number to select a device (1-{count}): "
                put_disks(disks, len(prompt))
                selection = query_integer(1, count, prompt)
                disk = disks[selection - 1]['name']

        if confirm_disk(disk):
            break
        else:
            if query_yes_no(f"Do you want to unmount '{disk}'? (y/n) "):
                unmount_disk(disk)
            print("Check device and press any key to continue...")
            input()

    print(f"Selected disk: {disk}")

if __name__ == "__main__":
    main()
