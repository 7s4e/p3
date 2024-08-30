#!/usr/bin/env python3
import subprocess
# import json
# import os

# Constants
DEFAULT_TABLE_WIDTH = 36
MAX_TABLE_WIDTH = 80
BORDER_STYLE = "="
COL_GAP_SIZE = 2
NAME_IDX = 0
VENDOR_IDX = 1
SIZE_IDX = -1
RIGHT_JUSTIFIED_COLUMNS = ["#", "SIZE"]


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
    dataset = read_table(run_command("lsblk --nodeps --output NAME,VENDOR,SIZE"))
    return [record for record in dataset if record["NAME"].startswith("sd")]

def put_disks(disks, display_width=DEFAULT_TABLE_WIDTH):
    put_table("CONNECTED DEVICES", number_records(disks), display_width)

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

    col_wths = [max(len(row[i]) for row in [table_columns] + rows) for i in range(len(table_columns))]
    table_width = sum(col_wths) + COL_GAP_SIZE * (len(table_columns) - 1)
    table_width = min(table_width, max_width)

    hdg_padding = (table_width - len(table_title)) // 2
    print(f"\n{' ' * hdg_padding}{table_title}")
    print(BORDER_STYLE * table_width)

    for row in [table_columns] + rows:
        print("  ".join([f"{row[i]:<{col_wths[i]}}" for i in range(len(table_columns))]))
    print(BORDER_STYLE * table_width)

def put_table(title, dataset, display_width):

    def make_table(title, dataset, display_width):
        
        def calculate_column_widths(dataset):
            return {
                key: max(
                    len(key), max(len(str(record[key])) for record in dataset)
                ) for key in dataset[0].keys()
            }

        def make_padding(content_width, available_width):
            return " " * max(0, (available_width - content_width) // 2)

        def format_record(record, col_widths):

            def format_field(field, width, is_right_justified):
                alignment = ">" if is_right_justified else "<"
                return f"{field:{alignment}{width}}"
            
            return {
                key: format_field(
                    value, col_widths[key], key in RIGHT_JUSTIFIED_COLUMNS
                ) for key, value in record.items()
            }
        
        col_wths = calculate_column_widths(dataset)
        table_wth = sum(col_wths.values()) + COL_GAP_SIZE * (len(col_wths) - 1)
        table_pdg = make_padding(table_wth, display_width)
        line_length = max(display_width, table_wth)
        title_pdg = make_padding(len(title), line_length)
        gap = " " * COL_GAP_SIZE
        headings = {key: key for key in dataset[0].keys()}

        title_row = title_pdg + title
        border_row = BORDER_STYLE * line_length
        header_row = table_pdg + \
                     gap.join(list(format_record(headings, col_wths).values()))
        data_rows = [(
            table_pdg + \
            gap.join(list(format_record(record, col_wths).values()))
        ) for record in dataset]

        return [title_row, border_row, header_row] + data_rows + [border_row]
    
    def print_table(table):
        print()
        print("\n".join(table))
    
    table = make_table(title, dataset, display_width)
    print_table(table)

def number_records(table):
    return [{"#": i + 1, **record} for i, record in enumerate(table)]

def read_table(input):

    def find_column_positions(header_line, keys):
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
    col_pos = find_column_positions(lines[0], keys)

    return [{
        key: get_slice(i, col_pos, line) for i, key in enumerate(keys)
        } for line in lines[1:]
    ]

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
