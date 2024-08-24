#!/usr/bin/env python3
import subprocess
# import json
# import os

# Constants
BORDER_STYLE = "="
COLUMN_GAP = 2

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
    disks = []
    output = run_command("lsblk -d --noheadings --output NAME,VENDOR,SIZE")
    for line in output.splitlines():
        columns = line.split()
        name = columns[0]
        vendor = columns[1] if len(columns) > 2 else ""
        size = columns[-1]
        if name.startswith("sd"):
            disks.append({"name": name, "vendor": vendor, "size": size})
    return disks

def put_disks(disks, display_width=36):
    right_justify_index = 2

    def calculate_column_widths(data):
        return [max(len(row[i]) for row in data) for i in range(len(data[0]))]
    
    # bookmark
    def format_row(row, column_widths, right_justify_index):
        formatted_row = []
        for j, cell in enumerate(row):
            if j == right_justify_index:
                formatted_row.append(f"{cell:>{column_widths[j]}}")
            else:
                formatted_row.append(f"{cell:<{column_widths[j]}}")
        return formatted_row


    right_justify_index = 2
    table_title = "CONNECTED DEVICES"
    title_padding = (display_width - len(table_title)) // 2
    table_columns = list(disks[0].keys())
    table_data = [table_columns] + \
        [[str(disk[key]) for key in table_columns] for disk in disks]
    column_widths = [max(
        len(row[i]) for row in table_data) for i in range(len(table_columns)
    )]
    table_width = len("#") + sum(column_widths) + COLUMN_GAP * len(table_columns)
    table_padding = max(0, (display_width - table_width) // 2)
    display_width = max(display_width, table_width)
    print(f"\n{' ' * title_padding}{table_title}")
    print(f"{BORDER_STYLE * display_width}")
    for i, row in enumerate(table_data):
        first_column = "#" if i == 0 else str(i)
        row_content = " " * table_padding + first_column
        for j in range(len(table_columns)):
            column_content = row[j] if i != 0 else row[j].upper()
            if j != right_justify_index:
                column_content = f"{column_content:<{column_widths[j]}}"
            else:
                column_content = f"{column_content:>{column_widths[j]}}"
            row_content += f"{' ' * COLUMN_GAP}{column_content}"
        print(row_content)
    print(f"{BORDER_STYLE * display_width}")



#     def print_table(data, column_widths, title, display_width, right_justify_index):
#         """Print the table with title, border, and formatted rows."""
#         title_padding = (display_width - len(title)) // 2
#         table_width = len("#") + sum(column_widths) + COLUMN_GAP * (len(data[0]) - 1)
#         table_padding = max(0, (display_width - table_width) // 2)

#         print(f"\n{' ' * title_padding}{title}")
#         print(f"{BORDER_STYLE * display_width}")
        
#         for i, row in enumerate(data):
#             first_column = "#" if i == 0 else str(i)
#             row_content = " " * table_padding + first_column
#             row_content += f"{' ' * COLUMN_GAP}".join(format_row(row, column_widths, right_justify_index))
#             print(row_content)
        
#         print(f"{BORDER_STYLE * display_width}")

#     # Main function logic
#     table_columns = list(disks[0].keys())
#     table_data = [table_columns] + [[str(disk[key]) for key in table_columns] for disk in disks]
#     column_widths = calculate_column_widths(table_data)
    
#     print_table(table_data, column_widths, "CONNECTED DEVICES", display_width, right_justify_index)

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
