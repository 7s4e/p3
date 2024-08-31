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
    prompt = f"Are you sure you want to select the disk '{disk}'? (y/n) "
    put_partitions(disk, len(prompt))
    return query_yes_no(prompt)

def get_disks():
    output = run_command("lsblk --nodeps --output NAME,VENDOR,SIZE")
    dataset = read_table(output)
    return [record for record in dataset if record["NAME"].startswith("sd")]

def put_disks(disks, display_width=DEFAULT_TABLE_WIDTH):
    put_table("CONNECTED DEVICES", number_records(disks), display_width)

def put_partitions(disk, display_width=DEFAULT_TABLE_WIDTH):
    output = run_command(
        f"lsblk --output NAME,TYPE,FSTYPE,LABEL,MOUNTPOINTS /dev/{disk}"
    )
    put_table("SELECTED DEVICE", read_table(output), display_width)

def put_table(title, dataset, display_width, border_style=BORDER_STYLE, \
              column_gap_size=COLUMN_GAP_SIZE, \
              right_justified_columns=RIGHT_JUSTIFIED_COLUMNS):

    def make_table(title, dataset, display_width, border_style, \
                   column_gap_size, right_justified_columns):
        
        def calculate_column_widths(dataset):
            return {
                key: max(
                    len(key), max(len(str(record[key])) for record in dataset)
                ) for key in dataset[0].keys()
            }

        def format_record(record, column_widths, right_justified_columns):

            def format_field(field, width, is_right_justified):
                alignment = ">" if is_right_justified else "<"
                return f"{field:{alignment}{width}}"
            
            return {
                key: format_field(
                    value, column_widths[key], key in right_justified_columns
                ) for key, value in record.items()
            }
        
        def make_padding(content_width, available_width):
            return " " * max(0, (available_width - content_width) // 2)

        column_widths = calculate_column_widths(dataset)
        table_width = sum(column_widths.values()) + \
                      column_gap_size * (len(column_widths) - 1)
        table_padding = make_padding(table_width, display_width)
        line_length = max(display_width, table_width)
        title_padding = make_padding(len(title), line_length)
        column_spacing = " " * column_gap_size
        headings = {key: key for key in dataset[0].keys()}

        title_row = title_padding + title
        border_row = border_style * line_length
        header_row = table_padding + \
                     column_spacing.join(list(format_record(
                         headings, column_widths, right_justified_columns
                     ).values()))
        data_rows = [(
            table_padding + \
            column_spacing.join(list(format_record(
                record, column_widths, right_justified_columns
            ).values()))
        ) for record in dataset]

        return [title_row, border_row, header_row] + data_rows + [border_row]
    
    def print_table(table):
        print()
        print("\n".join(table))
    
    table = make_table(title, dataset, display_width, border_style, \
                       column_gap_size, right_justified_columns)
    print_table(table)

def number_records(table):
    return [{"#": i + 1, **record} for i, record in enumerate(table)]

def read_table(input):

    def find_boundaries(column_index, positions_list, line):
        cursor = positions_list[column_index]
        start = cursor if cursor < len(line) else len(line) - 1
        while start < len(line) -1 and line[start].isspace(): start += 1
        while start > 0 and not line[start].isspace(): start -= 1

        next = column_index + 1
        end = positions_list[next] if next < len(positions_list) else len(line)
        if end != len(line):
            while not line[end].isspace(): end -= 1
            while end > start and line[end].isspace(): end -= 1
            end = end + 1 if end != start else end

        return start, end
    
    def find_column_positions(header_line, keys):
        return [header_line.index(key) for key in keys]
    
    def get_slice(column_index, positions_list, line):
        start, end = find_boundaries(column_index, positions_list, line)
        return line[start:end].strip()
    
    lines = input.splitlines()
    keys = lines[0].split()
    positions_list = find_column_positions(lines[0], keys)

    return [{
        key: get_slice(i, positions_list, line) for i, key in enumerate(keys)
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
