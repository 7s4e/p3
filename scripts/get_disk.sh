#!/bin/bash
#
# Select a connected disk.

# Source of query_integer, query_yes_no, unmount_disk
source functions.sh

# Globals
BORDER_STYLE="="
COLUMN_GAP=2

################################################################################
# Prompt user to confirm selected disk.
# Arguments:
#   $1 - Selected disk (e.g., "sda").
# Outputs:
#   0 - If user confirms.
#   1 - If user declines.
################################################################################
confirm_disk() {
  local disk="$1"
  local prompt="Are you sure you want select the disk '$disk'? (y/n) "

  put_partitions "$disk"
  query_yes_no "$prompt"
}

################################################################################
# Get list of block devices, filtered for SCSI disks.
# Arguments:
#   None.
# Outputs:
#   A JSON array of objects representing disks with the keys:
#     - "name"   : The name of the disk (e.g., "sda").
#     - "vendor" : The vendor of the disk.
#     - "size"   : The size of the disk.
################################################################################
get_disks() {
  # Use 'lsblk' to list block devices.
  lsblk -d --noheadings --output NAME,VENDOR,SIZE | \
    
  # Use 'gawk' to filter devices with names starting "sd".
  gawk '$1 ~ /^sd/' | \
    
  # Use 'jq' to process the filtered output into a JSON array of objects.
  jq --null-input --raw-input '
    [inputs | split(" ") | {name: .[0], vendor: .[1], size: .[2]}] | flatten
  '
}

################################################################################
# Display a formatted table of connected disks.
# Arguments:
#   $1 - JSON array containing disk information (name, vendor, size).
#   $2 - Optional: Table width. Default is 36.
# Outputs:
#   Writes a formatted table to stdout.
################################################################################
put_disks() {
  local disks="$1"
  local table_width="${2:-36}"
  local heading_text="CONNECTED DEVICES"
  local heading_padding=$(( ($table_width - ${#heading_text}) / 2 ))

  echo
  printf "%*s%s\n" "$heading_padding" "" "$heading_text"
  printf '%*s\n' "$table_width" | tr ' ' "${BORDER_STYLE:-=}"

  echo "$disks" | \
  jq --raw-output '

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
        col_width[i] = length($i) > col_width[i] ? length($i) : col_width[i]
      }
    }
    END {
      content_witdh = 0

      # Calculate the total content width of the table.
      for (i = 1; i <= length(col_width); i++) content_width += col_width[i]

      # Calculate the padding needed to center the table within the table width.
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

  printf '%*s\n' "$table_width" | tr ' ' "${BORDER_STYLE:-=}"
}

################################################################################
# Display partition informtation for a specific disk in a formated table.
# Arguments:
#   $1 - Selected disk (e.g., "sda").
# Outputs:
#   Writes a formatted table to stdout.
################################################################################
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
      # Store the data in an array and calculate the column widths.
      for (i = 1; i <= NF; i++) {
        data[NR, i] = $i
        col_width[i] = length($i) > col_width[i] ? length($i) : col_width[i]
      }
    }
    END {
      content_width = 0

      # Calculate the total content width of the table.
      for (i = 1; i <= length(col_width); i++) content_width += col_width[i]
      content_width += col_gap * (NF -1)
      content_width = content_width > max ? max : content_width

      # Calculate the padding and print header.
      hdg_padding = int((content_width - length(heading)) / 2)
      printf "%*s%s\n", hdg_padding, "", heading
      border_line = sprintf("%*s", content_width, "")
      gsub(/ /, border, border_line)
      print border_line

      # Print the table content with proper spacing and alignment.
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

################################################################################
# Select a connected disk.
# Arguments:
#   None.
# Outputs:
#   Selected disk.
################################################################################
main() {
  local disk disks selection menu_prompt unmount_prompt

  while true; do

    # Get information on connected disks.
    disks="$(get_disks)" || { echo "Failed to get disks."; return 1; }
    count="$(echo "$disks" | jq 'length')" || {
      echo "Failed to get count of disks."; return 1;
    }

    # Handle by number of devices connected.
    case $count in
      0)
        # Allow user to connect missing device.
        echo "Connect a device and press any key to continue..."
        read -sn 1
        continue
        ;;
      1)
        # Nominate only connected disk.
        disk="$(echo "$disks" | jq --raw-output '.[0].name')" || {
          echo "Failed to parse only disk name."; return 1;
        }
        ;;
      *)
        # Put menu of connected disks and get user selection.
        menu_prompt="Enter a number to select a device (1-$count): "
        put_disks "$disks" "${#menu_prompt}"
        selection="$(query_integer 1 "$count" "$menu_prompt")"
        disk="$(
          echo "$disks" | jq --raw-output ".[$((selection - 1))].name"
        )" || {
          echo "Failed to parse selected disk name."; return 1;
        }
        ;;
    esac

    # Confirm selected disk, allowing unmounting of unwanted disks.
    if confirm_disk "$disk"; then
      break
    else
      unmount_prompt="Do you want to unmount '$disk'? (y/n) "
      if query_yes_no "$unmount_prompt"; then
        unmount_disk "$disk"
      fi
      echo "Check device and press any key to continue..."
      read -sn 1
      continue
    fi
  done

  echo "$disk"
}

main