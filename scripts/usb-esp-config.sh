#!/bin/bash

source functions.sh

BORDER_STYLE="="
COLUMN_GAP=2

confirm_disk() {
    local disk="$1"
    local prompt="Are you sure you want the ESP on the disk '$disk'? (y/n) "

    put_partitions "$disk"
    query_yes_no "$prompt"
}

get_disks() {
    lsblk -d --noheadings --output NAME,VENDOR,SIZE | \
    gawk '$1 ~ /^sd/' | \
    jq --null-input --raw-input '
        [inputs | split(" ") | {name: .[0], vendor: .[1], size: .[2]}] | flatten
    '
}

put_disks() {
    local disks="$1"
    local table_width="${2:-36}"
    local heading_text="CONNECTED DEVICES"
    local heading_padding=$(( ($table_width - ${#heading_text}) / 2 ))

    echo
    printf "%*s%s\n" "$heading_padding" "" "$heading_text"
    printf '%*s\n' "$table_width" | tr ' ' "${BORDER_STYLE:-=}"

    echo "$disks" | \
    jq -r '
        (.[0] | keys_unsorted) as $keys |
        ($keys | join("\t")) as $header |
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
            for (i = 1; i <= NF; i++) {
                data[NR, i] = NR == 1 ? toupper($i) : $i
                col_width[i] = length($i) > col_width[i] ? length($i) : \
                    col_width[i]
            }
        }
        END {
            content_witdh = 0
            for (i = 1; i <= length(col_width); i++) {
                content_width += col_width[i]
            }
            tbl_padding = (tbl_width - content_width - col_gap * (NF - 1)) / 2
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