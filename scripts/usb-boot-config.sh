#!/bin/bash
# This script installs GRUB with the EFI and boot directories on separate 
# partitions, or it updates the GRUB configuration file with the latest version 
# at c3/usb/grub.cfg. See c3/usb/README.md for details.


# SETUP #
# Source of elevate_privileges(), query_boolean(), and set_vars_from_obj()
source functions.sh

# Capture CURRENT_USER and elevate to superuser
elevate_privileges


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

# MAIN SCRIPT EXECUTION #
confirm_mounting

if [[ -d "$BOOT_MNT_PT/$REPO" ]]; then
    cd "$BOOT_MNT_PT/$REPO" || exit
    update_repo
else
    if [[ -f "$DATA_FILE" ]]; then
        read_data
    else
        get_data
    fi

    cd "$BOOT_MNT_PT" || exit
    clone_repo
    install_grub
    configure_grub
fi