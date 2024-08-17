#!/bin/bash

# Function Name: elevate_privileges
# Description: re-run script, if necessary, as superuser.
# Parameters: none
elevate_privileges() {
    if [[ $EUID -ne 0 ]]; then
        export CURRENT_USER=$(whoami)
        exec sudo --preserve-env "$0" "$@"
    fi
}

query_menu_selection() {
    local prompt="${1:-"Enter your selection: "}"
    local range="$2"
    local response

    while true; do
        read -p "$prompt" response
        echo
        if [[ ! "$response" =~ ^[0-9]+$ ]] || {
            [ -v range ] && (( response < 1 || response > range ));
        }; then
            echo "Error: '$response' is an invalid response." >&2
        else
            break
        fi
    done
    echo "$response"
}

# Function Name: query_yes_no
# Description: prompt user to respond yes or no
# Parameters: $1 - prompt put to user
# Returns:
#   0 - true
#   1 - false
# Issue: can't use -n 1 without the prompt on same line as invalid input
query_yes_no() {
    local prompt="$1"
    local response

    while true; do
        read -p "$prompt" response
        echo
        if [[ "$response" =~ ^[ynYN]$ ]]; then
            if [[ "$response" == "y" ||  "$response" == "Y" ]]; then
                return 0
            else
                return 1
            fi
        else
            echo "Error: '$response' is an invalid response." >&2
            continue
        fi
    done
}

# Function Name: set_vars_from_obj
# Description: sets key/value pairs from JSON object as environment variables
# Parameters: $1 - JSON data
set_vars_from_obj() {
    local object="$1"
    eval "$(
        echo "$object" | 
        jq --raw-output '
            to_entries | 
            .[] | 
            "\(.key | ascii_upcase)=\"" + (.value | tostring) + "\""
        ' | 
        sed 's/^/export /'
    )"
}
