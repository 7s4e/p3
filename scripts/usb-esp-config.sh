#!/bin/bash

source functions.sh

BORDER_STYLE="="
COLUMN_GAP=2

# Function Name: confirm_disk
# Description:
#   Prompts the user to confirm whether they want to place the EFI System 
#   Partition (ESP) on the specified disk. The function first displays the 
#   partitions of the disk and then asks for user confirmation with a yes/no 
#   prompt.
# Parameters:
#   $1 - The name of the disk (e.g., "sda") for which the confirmation is 
#   required.
# Returns:
#   0 - If the user confirms with 'y' or 'Y'.
#   1 - If the user declines with 'n' or 'N'.
confirm_disk() {
    # The disk name provided as the first argument.
    local disk="$1"

    # Construct the confirmation prompt message.
    local prompt="Are you sure you want the ESP on the disk '$disk'? (y/n) "

    # Display the partitions on the specified disk.
    put_partitions "$disk"

    # Prompt the user for confirmation and return the result.
    query_yes_no "$prompt"
}

# Function Name: get_disks
# Description:
#   Retrieves a list of connected SCSI disks to identify USB block devices, 
#   along with their vendor names and sizes. The information is formatted as a 
#   JSON array of objects, with each object containing the disk's name, vendor, 
#   and size.
# Parameters:
#   None.
# Returns:
#   A JSON array where each element is an object representing a disk, with the 
#   keys:
#       - "name"   : The name of the disk (e.g., "sda").
#       - "vendor" : The vendor of the disk.
#       - "size"   : The size of the disk.
get_disks() {
    # Use 'lsblk' to list block devices, excluding headers and only showing 
    # NAME, VENDOR, and SIZE columns.
    lsblk -d --noheadings --output NAME,VENDOR,SIZE | \
    
    # Use 'gawk' to filter the output to include only devices with names 
    # starting with "sd".
    gawk '$1 ~ /^sd/' | \
    
    # Use 'jq' to process the filtered output into a JSON array of objects.
    jq --null-input --raw-input '

        # Start a new jq program, treating input as raw strings
        [
            # Begin array construction, processing each line of input
            inputs | 
            
            # Split each input line by spaces into an array of words
            split(" ") | 
            
            # Create a JSON object with keys 'name', 'vendor', and 'size'
            {name: .[0], vendor: .[1], size: .[2]}
        
        ] | 
        
        # Flatten the resulting array into a single-level array of objects
        flatten
    '
}

# Function Name: put_disks
# Description: Display a formatted table of connected disks.
# Parameters:
#   $1 - JSON array containing disk information (name, vendor, size).
#   $2 - Optional: Table width. Default is 36.
put_disks() {
    local disks="$1"
    local table_width="${2:-36}"
    local heading_text="CONNECTED DEVICES"
    local heading_padding=$(( ($table_width - ${#heading_text}) / 2 ))

    echo

    # Print the table heading, centered within the specified table width.
    printf "%*s%s\n" "$heading_padding" "" "$heading_text"

    # Print a border line below the heading.
    printf '%*s\n' "$table_width" | tr ' ' "${BORDER_STYLE:-=}"

    # Process the JSON data to create a table of disks.
    echo "$disks" | \
    jq -r '

        # Extract keys (column names) from the first object in the array.
        (.[0] | keys_unsorted) as $keys |
        
        # Generate the table header from the keys, joined by tabs.
        ($keys | join("\t")) as $header |

        # Create the table body: prepend a row number, then join values by tabs.
        "#\t\($header)\n" + (
            to_entries |
            map([.key + 1, .value[$keys[]]]) |
            map(join("\t")) |
            join("\n")
        )
    ' | \
    gawk --assign OFS='\t' --assign col_gap=$COLUMN_GAP \
        --assign tbl_width="$table_width" '
        {
            # Store the data in an array and calculate the column widths.
            for (i = 1; i <= NF; i++) {
                data[NR, i] = NR == 1 ? toupper($i) : $i
                col_width[i] = length($i) > col_width[i] ? length($i) : \
                    col_width[i]
            }
        }
        END {
            content_witdh = 0

            # Calculate the total content width of the table.
            for (i = 1; i <= length(col_width); i++) {
                content_width += col_width[i]
            }

            # Calculate the padding needed to center the table within the table 
            # width.
            tbl_padding = (tbl_width - content_width - col_gap * (NF - 1)) / 2

            # Print the table content with proper spacing and alignment.
            for (i = 1; i <= NR; i++) {
                printf "%*s", tbl_padding, ""
                for (j = 1; j <= NF; j++) {
                    if (j == 4) printf "%*s", col_width[j], data[i, j]
                    else printf "%-*s", col_width[j] + col_gap, data[i, j]
                }
                print ""
            }
        }
    '

    # Print a border line below the table.
    printf '%*s\n' "$table_width" | tr ' ' "${BORDER_STYLE:-=}"
}


put_partitions() {
    local disk="${1//\"/}"
    local max_width=80
    local heading_text="SELECTED DEVICE"

    echo
    lsblk --output NAME,TYPE,FSTYPE,LABEL,MOUNTPOINTS | \
    gawk --assign disk="$disk" 'NR==1 || $1 ~ disk' | \
    gawk --assign col_gap="$COLUMN_GAP" --assign border="${BORDER_STYLE:-=}" \
        --assign max="$max_width" --assign heading="$heading_text" '
        {
            for (i = 1; i <= NF; i++) {
                data[NR, i] = $i
                col_width[i] = length($i) > col_width[i] ? length($i) : \
                    col_width[i]
            }
        }
        END {
            content_width = 0
            for (i = 1; i <= length(col_width); i++) {
                content_width += col_width[i]
            }
            content_width += col_gap * (NF -1)
            content_width = content_width > max ? max : content_width

            hdg_padding = int((content_width - length(heading)) / 2)
            printf "%*s%s\n", hdg_padding, "", heading

            border_line = sprintf("%*s", content_width, "")
            gsub(/ /, border, border_line)
            print border_line

            for (i = 1; i <= NR; i++) {
                for (j = 1; j <= NF; j++) {
                    printf "%-*s", col_width[j] + col_gap, data[i, j]
                }
                print ""
            }
            print border_line
        }
    '
}

select_disk() {
    local disks selection

    while true; do
        disks="$(get_disks)" || { echo "Failed to get disks."; return 1; }
        count="$(echo "$disks" | jq 'length')" || {
            echo "Failed to get count of disks."; return 1;
        }
        
        case $count in
            0)
                echo "Connect a device and press any key to continue..."
                read -sn 1
                continue
                ;;
            1)
                disk="$(echo "$disks" | jq -r '.[0].name')" || {
                    echo "Failed to parse only disk name."; return 1;
                }
                ;;
            *)
                local menu_prompt="The ESP is for which device? (1-$count) "
                put_disks "$disks" "${#menu_prompt}"
                selection="$(query_integer 1 "$count" "$menu_prompt")"
                disk="$(
                    echo "$disks" | jq -r ".[$((selection - 1))].name"
                )" || {
                    echo "Failed to parse selected disk name."; return 1;
                }
                ;;
        esac

        if confirm_disk "$disk"; then
            break
        else
            local unmount_prompt="Do you want to unmount '$disk'? (y/n) "
            if query_yes_no "$unmount_prompt"; then
                unmount_disk "$disk"
            fi
            echo "Check device and press any key to continue..."
            read -sn 1
            continue
        fi
    done
}

unmount_disk() {
    local disk="$1"

    lsblk --noheadings --output PATH,MOUNTPOINTS | \
    gawk --assign disk="$disk" '$1 ~ disk && $2 != "" {print $1}' | \
    xargs -I {} umount --verbose "{}"
}

select_disk
echo "selected: $disk"