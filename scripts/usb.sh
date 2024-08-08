#!/bin/bash

# Source of elevate_privileges(), query_boolean(), and set_vars_from_obj()
source functions.sh

# CONSTANTS
BOOT_MNT_PT="/mnt/boot"
DATA_FILE="/home/bryant/Repositories/c3/data/data.json"
ESP_MNT_PT="/mnt/esp"
GIT_HOST="github.com"
REPO="c3"
CHKOUT_DIR="usb"

# NAME, EMAIL, TOKEN are also set either as environment variables with 
# read_data() or as global variables with get_data().

# Function Name: clone_repo
# Description: clone, configure and commit repository with sparse checkout
# Parameters: none
clone_repo() {

    # Clone the repository and configure sparse checkout
    git clone --no-checkout "https://$TOKEN@$GIT_HOST/$NAME/$REPO.git"
    cd "$BOOT_MNT_PT/$REPO" || exit
    git config core.sparseCheckout true
    echo "/$CHKOUT_DIR/" > .git/info/sparse-checkout
    git checkout

    # Store credentials and configure git
    git config credential.helper store
    echo "https://$TOKEN@$GIT_HOST" > .git-credentials
    echo ".git-credentials" >> .gitignore
    echo ".gitignore" >> .git/info/sparse-checkout

    # Update the repository and commit changes
    git read-tree --merge --update HEAD
    git add .gitignore

    # Configure git user and commit
    git config user.email "$EMAIL"
    git config user.name "$NAME"
    git commit --message "Ignore credentials"
}

# Function Name: configure_grub
# Description: Link GRUB configuration to updated copy in the C3 repository
# Parameters: none
configure_grub() {
    cd "$BOOT_MNT_PT/grub"
    ln --symbolic "../$REPO/$CHKOUT_DIR/grub.cfg" grub.cfg
    echo "Setting GRUB configuration..."
}

# Function Name: confirm_mounting
# Description: Confirm USB partitions are correctly mounted
# Parameters: none
confirm_mounting() {

    # Variables for mounting status, mounted devices, and confirmation prompt
    local has_esp has_boot
    local esp_device boot_device
    local prompt

    # Check for USB partition mounted to /mnt/esp
    if mountpoint --quiet "$ESP_MNT_PT"; then
        has_esp=true
        esp_device=$(findmnt --noheadings --output SOURCE "$ESP_MNT_PT")
    else
        has_esp=false
        echo "There is no USB partition mounted at $ESP_MNT_PT."
    fi

    # Check for USB partition mounted to /boot/esp
    if mountpoint --quiet "$BOOT_MNT_PT"; then
        has_boot=true
        boot_device=$(findmnt --noheadings --output SOURCE "$BOOT_MNT_PT")
    else
        has_boot=false
        echo "There is no USB partition mounted at $BOOT_MNT_PT."
    fi

    # Prompt user for confirmation, and put instructions as appropriate
    if [[ $has_esp == false || $has_boot == false ]]; then
        echo "Mount the USB before re-running this script."
        exit
    else
        prompt="Is $esp_device at $ESP_MNT_PT and $boot_device at $BOOT_MNT_PT correct? (y/n) "
        if !(query_boolean "$prompt" false); then
            echo "Correct the USB partition mounts before re-running this script."
            exit
        fi
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
    local device=$(df "$BOOT_MNT_PT/$REPO" | awk "NR==2 {print $1}")
    grub-install --target=x86_64-efi --efi-directory="$ESP_MNT_PT" \
        --boot-directory="$BOOT_MNT_PT" --removable --recheck --no-floppy \
        "$device"
}

# Function Name: read data
# Description: Read Github configuration data from file, if able
# Parameters: none
read_data() {
    local data=$(jq --raw-output ".git" $DATA_FILE)
    set_vars_from_obj $data
    echo "Reading Github configuration data..."
}

# Function Name: update_repo
# Description: Update checked out respository
# Parameters: none
update_repo() {
    git fetch origin
    git read-tree --merge --update HEAD
    git rebase origin/main
}

# MAIN
elevate_privileges
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
    clone_repo
    install_grub
    configure_grub
fi
