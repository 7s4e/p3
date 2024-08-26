#!/usr/bin/env python3
import subprocess
# import json
# import os

# Constants
DEFAULT_TABLE_WIDTH = 36
MAX_TABLE_WIDTH = 80
BORDER_STYLE = "="
COLUMN_GAP_SIZE = 2
NAME_IDX = 0
VENDOR_IDX = 1
SIZE_IDX = -1


# Helper functions
def run_command(command, use_shell=True):
    r = subprocess.run(command, shell=use_shell, text=True, capture_output=True)
    if r.returncode != 0:
        raise Exception(f"Command failed: {r.stderr.strip()}")
    return r.stdout.strip()

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
    partitions = run_command(f"lsblk -n -o MOUNTPOINT /dev/{disk}", True)
    for partition in partitions.splitlines():
        if partition:
            run_command(f"sudo umount {partition.strip()}", True)

# Core functions
def confirm_disk(disk):
    put_partitions(disk)
    return query_yes_no(f"Are you sure you want to select the disk '{disk}'? (y/n) ")

def get_disks():
    table = read_table(run_command("lsblk --nodeps --output NAME,VENDOR,SIZE"))
    disks = [entry for entry in table if entry["NAME"].startswith("sd")]
    return disks

def calculate_column_widths(data):
    return [max(len(row[i]) for row in data) for i in range(len(data[0]))]
    
def calculate_padding(content_width, available_width):
    return " " * max(0, (available_width - content_width) // 2)

def format_cells(row, column_widths, right_justify_indexes, is_heading_row):
    formatted_row = []
    for i, cell in enumerate(row):
        cell = cell.upper() if is_heading_row else cell
        if i in right_justify_indexes:
            formatted_row.append(f"{cell:>{column_widths[i]}}")
        else:
            formatted_row.append(f"{cell:<{column_widths[i]}}")
    return formatted_row

def print_table(title, table_data, display_width):
    col_widths = [len(" #")] + calculate_column_widths(table_data)
    gaps_width = COLUMN_GAP_SIZE * (len(col_widths) - 1)
    table_width = sum(col_widths) + gaps_width
    table_padding = calculate_padding(table_width, display_width)
    display_width = max(display_width, table_width)
    title_padding = calculate_padding(len(title), display_width)
    print(f"\n{title_padding}{title}")
    print(f"{BORDER_STYLE * display_width}")
    for i, row in enumerate(table_data):
        is_hdg_row = i == 0
        first_column = " #" if is_hdg_row else str(i)
        row = [first_column] + row
        rgt_jst_col_idxs = [0, len(row) + SIZE_IDX]
        cells = format_cells(row, col_widths, rgt_jst_col_idxs, is_hdg_row)
        print(f"{table_padding}{(' ' * COLUMN_GAP_SIZE).join(cells)}")
    print(f"{BORDER_STYLE * display_width}")

def put_disks(disks, display_width=DEFAULT_TABLE_WIDTH):
    ##BOOKMARK

    table_headers = list(disks[0].keys())
    table_data = [[str(disk[key]) for key in table_headers] for disk in disks]
    disks_table = [table_headers] + table_data
    print_table("CONNECTED DEVICES", disks_table, display_width)

def put_partitions(disk):
    output = run_command(
        f"lsblk --output NAME,TYPE,FSTYPE,LABEL,MOUNTPOINTS /dev/{disk}", True
    )
    print(f"output:\n{output}\n")
    
    lines = output.splitlines()
    print(f"lines:\n{lines}\n")

    table_columns = lines[0].split()
    rows = [line.split() for line in lines[1:]]
    print(f"rows:\n{rows}\n")

    max_width = 80
    table_title = "SELECTED DEVICE"

    col_widths = [max(len(row[i]) for row in [table_columns] + rows) for i in range(len(table_columns))]
    table_width = sum(col_widths) + COLUMN_GAP_SIZE * (len(table_columns) - 1)
    table_width = min(table_width, max_width)

    hdg_padding = (table_width - len(table_title)) // 2
    print(f"\n{' ' * hdg_padding}{table_title}")
    print(BORDER_STYLE * table_width)

    for row in [table_columns] + rows:
        print("  ".join([f"{row[i]:<{col_widths[i]}}" for i in range(len(table_columns))]))
    print(BORDER_STYLE * table_width)

def read_table(input):

    def get_column_positions(header_line, keys):
        return [header_line.index(key) for key in keys]
    
    def find_boundaries(pos_idx, pos_lst, line):
        start = pos_lst[pos_idx]
        while start < len(line) and line[start].isspace(): start += 1
        while start > 0 and not line[start].isspace(): start -= 1

        end = pos_lst[pos_idx + 1] if pos_idx + 1 < len(pos_lst) else len(line)
        if end != len(line):
            while not line[end].isspace(): end -= 1
            while end > start and line[end].isspace(): end -= 1
            end = end + 1 if end != start else end

        return start, end
    
    def get_slice(position_index, positions, line):
        start, end = find_boundaries(position_index, positions, line)
        return line[start:end].strip()
    
    lines = input.splitlines()
    keys = lines[0].split()
    col_pos = get_column_positions(lines[0], keys)

    table = []
    for line in lines[1:]:
        entry = {key: get_slice(i, col_pos, line) for i, key in enumerate(keys)}
        table.append(entry)
    
    return table

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
                disk = disks[0]["NAME"]
            case _:
                prompt = f"Enter a number to select a device (1-{count}): "
                put_disks(disks, len(prompt))
                selection = query_integer(1, count, prompt)
                disk = disks[selection - 1]["NAME"]

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
