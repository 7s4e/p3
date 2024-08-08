#!/bin/bash

# Function Name: elevate_privileges
# Description: re-run script, if necessary, as superuser.
# Parameters: none
elevate_privileges() {
    if [[ $EUID -ne 0 ]]; then
        exec sudo "$0" "$@"
    fi
}

# Function Name: query_boolean
# Description: prompt user to respond yes or no
# Parameters:
#   $1 - prompt put to user
#   $2 - (default true) affirmative bias toward the response:
#           true - requires an explicit negative response and accepts all other 
#               responses as affirmative
#           false - requires an explicit positive response and accepts all 
#               other responses as negative
# Returns:
#   0 - true
#   1 - false
query_boolean() {
    local prompt="$1"
    local has_affirmative_bias="${2:-true}"
    local response=""
    read -p "$prompt" response
    response=$(echo "${response:0:1}" | tr "[:upper:]" "[:lower:]")
    if [[ $has_affirmative_bias == true ]]; then
        if [[ "$response" == "n"  ]]; then
            return 1
        else
            return 0
        fi
    else
        if [[ "$response" == "y"  ]]; then
            return 0
        else
            return 1
        fi
    fi
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
