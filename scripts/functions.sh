#!/bin/bash

# Function Name: elevate_privileges
# Description: Re-run script as superuser if not already running with elevated 
#   privileges.
elevate_privileges() {
    if [[ $EUID -ne 0 ]]; then
        export CURRENT_USER=$(whoami)
        exec sudo --preserve-env "$0" "$@"
    fi
}

# Function Name: query_integer
# Description: Propmt user for an integer from a given range.
# Parameters:
#   $1 - The lower limit of the valid range (optional, default: 1).
#   $2 - The upper limit of the valid range (optional, default: 100).
#   $3 - The prompt text (optional, default: "Enter your selection: ").
# Returns: The user-selected number.
query_integer() {
    local lower_limit="${1:-1}"
    local upper_limit="${2:-100}"
    local prompt="${1:-"Enter a number: "}"
    local response

    while true; do
        read -p "$prompt" response
        echo
        if [[ ! "$response" =~ ^[0-9]+$ ]] || 
            (( response < lower_limit || response > upper_limit )); then
            echo "Error: '$response' is an invalid response." >&2
        else
            break
        fi
    done
    echo "$response"
}

# Function Name: query_yes_no
# Description: Prompt user to answer yes or no.
# Parameters:
#   $1 - The prompt text.
# Returns:
#   0 - Yes (y/Y)
#   1 - No (n/N)
# Issue: can't use -n 1 without the prompt on same line as invalid input
query_yes_no() {
    local prompt="${1:-"Yes or no? "}"
    local response

    while true; do
        read -n 1 -p "$prompt" response
        echo
        if [[ "$response" =~ ^[ynYN]$ ]]; then
            [[ "$response" =~ ^[yY]$ ]] && return 0 || return 1
        else
            echo "Error: '$response' is an invalid response." >&2
        fi
    done
}

# Function Name: set_vars_from_obj
# Description: Set environmental variables from a JSON object.
# Parameters:
#   $1 - JSON object as string.
set_vars_from_obj() {
    local object="$1"
    eval "$(
        echo "$object" | \
        jq --raw-output '
            to_entries | .[] | "export \(.key | ascii_upcase)=\"(.value)\""
        '
    )"
}