#!/bin/bash
# Introduction


# SETUP #
# Source of elevate_privileges(), query_boolean(), and set_vars_from_obj()
source functions.sh

# Capture CURRENT_USER and elevate to superuser
# elevate_privileges


# CONSTANTS #
# Confidential Configuration Cache (C3)
CURRENT_HOME="/home/$CURRENT_USER"
LOCAL_DIR="Repositories"
REPO="c3"
DATA_DIR="data"
DATA_SRC="data.json"

# Script Values
DATA_FILE="$CURRENT_HOME/$LOCAL_DIR/$REPO/$DATA_DIR/$DATA_SRC"
BOOT_MNT_PT="/mnt/boot"
ESP_MNT_PT="/mnt/esp"
GIT_HOST="github.com"
CHKOUT_DIR="usb"

# NAME, EMAIL, TOKEN are also set either as environment variables with 
#   read_data() or as global variables with get_data().


# SCRIPT FUNCTIONS #

# Function Name: check_mountpoint
# Description: checks if a USB partition is mounted
# Parameters: $1: mount point path
check_mountpoint() {
    local mnt_pt="$1"
    if mountpoint --quiet "$mnt_pt"; then
        findmnt --noheadings --output SOURCE "$mnt_pt"
    else
        echo "There is no USB partition mounted at $mnt_pt."
        return 1
    fi
}

# Function Name: clone_repo
# Description: clone, configure and commit repository with sparse checkout
# Parameters: none
clone_repo() {
    git clone --no-checkout "https://$TOKEN@$GIT_HOST/$NAME/$REPO.git"
    cd "$BOOT_MNT_PT/$REPO" || exit
    git config core.sparseCheckout true
    echo "/$CHKOUT_DIR/" > .git/info/sparse-checkout
    git checkout
    configure_git
    echo ".gitignore" >> .git/info/sparse-checkout
    git read-tree -mu HEAD
    git add .gitignore
    git commit --message "Ignore credentials"
}

# Function Name: configure_git
# Description: configure git user and store credentials
# Parameters: none
configure_git() {
    git config credential.helper store
    echo "https://$TOKEN@$GIT_HOST" > .git-credentials
    echo ".git-credentials" >> .gitignore
    git config user.email "$EMAIL"
    git config user.name "$NAME"
}

# Function Name: configure_grub
# Description: Link GRUB configuration to updated copy in the C3 repository
# Parameters: none
configure_grub() {
    cd "$BOOT_MNT_PT/boot/grub" || exit
    ln --symbolic --verbose "../../$REPO/$CHKOUT_DIR/grub.cfg" grub.cfg
}

# Function Name: confirm_mounting
# Description: Confirm USB partitions are correctly mounted
# Parameters: none
confirm_mounting() {
    local esp_device boot_device
    esp_device=$(check_mountpoint "$ESP_MNT_PT") || exit
    boot_device=$(check_mountpoint "$BOOT_MNT_PT") || exit

    local prompt
    prompt="Is $esp_device at $ESP_MNT_PT and $boot_device at $BOOT_MNT_PT correct? (y/n) "
    if ! query_boolean "$prompt" false; then
        echo "Correct the USB partition mounts before re-running this script."
        exit
    fi
}

# Function Name: get_data
# Description: Get Github configuration data from user, if necessary
# Parameters: none
get_data() {
    read -p "Github username: " NAME
    read -p "Github email: " EMAIL
    read -sp "Github personal access token: " TOKEN
    echo
}

# Function Name: install_grub
# Description: Install GRUB on USB drive
# Parameters: none
install_grub() {
    local device
    device=$(df "$BOOT_MNT_PT/$REPO" | awk "NR==2 {print $1}")
    mkdir --verbose "$BOOT_MNT_PT/boot"
    grub-install --target=x86_64-efi --efi-directory="$ESP_MNT_PT" \
        --boot-directory="$BOOT_MNT_PT/boot" --removable --recheck --no-floppy \
        "$device"
}

# Function Name: read_data
# Description: Read Github configuration data from file, if able
# Parameters: none
read_data() {
    local data
    data=$(jq --raw-output ".git" $DATA_FILE)
    set_vars_from_obj "$data"
}

# Function Name: update_repo
# Description: Update checked out respository
# Parameters: none
update_repo() {
    git fetch origin
    git read-tree -mu HEAD
    git rebase origin/main
}




    # echo "*     CONNECTED USB diskS     *"
    # echo "================================="
    # echo "NAME     SIZE  VENDOR     MODEL     "
    # lsblk --noheadings --output NAME,SIZE,VENDOR,MODEL | \
    #     awk '$1 ~ /^sdb/ {
    #         printf "%-6s %6s  %-10s %-20s\n", $1, $2, $3, $4
    #     }'
    # lsblk -o KNAME,NAME,TYPE,LABEL,FSTYPE,MOUNTPOINTS | awk '$1 ~ /^sdb/' 
    # capture cols: KNAME,PATH,MOUNTPOINT,UUID,MODEL,MOUNTPOINTS,TRAN,PKNAME,VENDOR

BORDER_STYLE="="
COLUMN_GAP=2

confirm_disk() {
    local disk="$1"
    local prompt="Are you sure you want the ESP on the disk "$disk"? (y/n) "

    put_partitions "$disk"
    echo "$(query_yes_no "$prompt")"
}

get_disks() {
    local disks='[]'

    while IFS=' ' read -r name vendor size; do
        local disk
        disk=$(
            jq -n --arg name "$name" --arg vendor "$vendor" --arg size "$size" \
                '{name: $name, vendor: $vendor, size: $size}'
        )
        disks=$(jq -c --argjson disk "$disk" '. += [$disk]' <<< "$disks")
    done < <(
        lsblk -d --noheadings --output NAME,VENDOR,SIZE | \
        gawk '$1 ~ /^sd/'
    )

    echo "$disks"
}

put_disks() {
    local disks="$1"
    local table_width="${2:-36}"
    local heading_text="CONNECTED DEVICES"
    local heading_padding=$(( ($table_width - ${#heading_text}) / 2 ))

    echo
    printf "%*s%s\n" "$heading_padding" "" "$heading_text"
    printf '%*s\n' "$table_width" | tr ' ' "${BORDER_STYLE:-=}"

    echo "$disks" | jq -r '
        (.[0] | keys_unsorted) as $keys |
        ($keys | join("\t")) as $header |
        "#\t\($header)\n" + (
            to_entries |
            map([.key + 1, .value[$keys[]]]) |
            map(join("\t")) |
            join("\n")
        )
    ' | gawk --assign OFS='\t' --assign col_gap=$COLUMN_GAP \
        --assign tbl_width="$table_width" '
        {
            for (i = 1; i <= NF; i++) {
                if (NR == 1) data[NR, i] = toupper($i)
                else data[NR, i] = $i
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
                printf "\n"
            }
        }
    '
    printf '%*s\n' "$table_width" | tr ' ' "${BORDER_STYLE:-=}"
}


put_partitions() {
    local disk=$(echo "$1" | tr -d '"')
    local max_width=80
    local heading_text="SELECTED DEVICE"
    local output=$(lsblk --output NAME,TYPE,FSTYPE,LABEL,MOUNTPOINTS | \
        gawk --assign disk="$disk" 'NR==1 || $1 ~ disk')

    echo
    echo "$output" | gawk --assign col_gap="$COLUMN_GAP" \
        --assign border="${BORDER_STYLE:-=}" --assign max="$max_width" \
        --assign heading="$heading_text" '
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
            if (content_width > max) content_width = max

            hdg_padding = int((content_width - length(heading)) / 2)
            printf "%*s%s\n", hdg_padding, "", heading

            border_line = sprintf("%*s", content_width, "")
            gsub(/ /, border, border_line)
            print border_line

            for (i = 1; i <= NR; i++) {
                for (j = 1; j <= NF; j++) {
                    printf "%-*s", col_width[j] + col_gap, data[i, j]
                }
                printf "\n"
            }
            print border_line
        }
    '
}

select_disk() {
    local disk disks
    local -i count selection
    
    disks="$(get_disks)" || { echo "Failed to get disks."; return 1; }
    count="$(echo "$disks" | jq 'length')" || { 
        echo "Failed to get count of disks."; return 1;
    }

    case $count in
        0)
            echo "Connect a device and press any key to continue..."
            read -sn 1
            select_disk
            ;;
        1)
            disk="$(echo "$disks" | jq -r '.[0].name')" || { 
                echo "Failed to parse only disk name."; return 1;
            }
            ;;
        *)
            local prompt="The ESP is for which device? (1-$count) "
            put_disks "$disks" "${#prompt}"
            selection="$(query_menu_selection "$prompt" "$count")"
            disk="$(echo "$disks" | jq -r ".[$((selection - 1))].name")" || {
                echo "Failed to parse selected disk name."; return 1;
            }
            ;;
    esac

    confirm_disk "$disk"


    echo "done"
    echo "$?"
    if [ $? -eq 1 ]; then
        echo "Connect the correct device, then press any key to continue..."
        read -sn 1
        select_disk
    fi
}

# MAIN SCRIPT EXECUTION #
select_disk

# confirm_mounting

# if [[ -d "$BOOT_MNT_PT/$REPO" ]]; then
#     cd "$BOOT_MNT_PT/$REPO" || exit
#     update_repo
# else
#     if [[ -f "$DATA_FILE" ]]; then
#         read_data
#     else
#         get_data
#     fi

#     cd "$BOOT_MNT_PT" || exit
#     clone_repo
#     install_grub
#     configure_grub
# fi