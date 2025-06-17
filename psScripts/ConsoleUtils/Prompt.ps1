class Prompt {
    hidden [string]$_Cue
    hidden [Terminal]$_Terminal
    hidden [bool]$_ExpectKeystroke
    hidden [bool]$_ValidateBool
    hidden [bool]$_ValidateInt
    hidden [object]$_IntValidation # int or [int,int]
    hidden [hashtable]$_ErrorCount
    hidden [string]$_UserResponse
    hidden [object]$_ValidatedResponse

    Prompt(
        [string]$cue,
        [bool]$expectKeystroke = $false,
        [bool]$validateBool = $false,
        [bool]$validateInteger = $false,
        [object]$integerValidation = $null
    ) {
        if ($validateBool -and $validateInteger) {
            throw "Cannot validate both boolean and integer input."
        }
        if ($integerValidation -ne $null -and -not $validateInteger) {
            throw "Integer validation provided without validation enabled."
        }
        if ($integerValidation -is [int] -and $integerValidation -lt 0) {
            throw "Integer range must be positive."
        }
        if ($integerValidation -is [array]) {
            if ($integerValidation.Count -ne 2) {
                throw "Tuple for integer validation must have 2 elements."
            }
            if ($integerValidation[0] -gt $integerValidation[1]) {
                throw "Integer validation lower bound exceeds upper bound."
            }
        }

        $this._Terminal = [Terminal]::new()
        $this._Cue = $cue
        $this._ExpectKeystroke = $expectKeystroke
        $this._ValidateBool = $validateBool
        $this._ValidateInt = $validateInt
        $this._IntValidation = $intValidation
        $this._ErrorCount = @{ "yes/no" = 0; "NaN" = 0; "OOR" = 0; "OOL" = 0 }
    }

    [object]Call() {
        $valid = $false
        while (-not $valid) {
            $this._GetResponse()
            $valid = $this._ValidateResponse()
        }

        foreach ($key in $this._ErrorCount.Keys) {
            $this._ErrorCount[$key] = 0
        }

        return $this._ValidatedResponse
    }

    [void]_GetResponse() {
        $this._Terminal.SetForegroundColor('Yellow')
        $this._Terminal.Write("$($this._cue) ")
        $this._Terminal.ResetColor()

        $this._UserResponse = if ($this._ExpectKeystroke) {
            $key = $null
            while ($null -eq $key) {
                $key = $this._Terminal.ReadKey()
            }
            $key
        } else {
            $this._Terminal.ReadLine()
        }
    }

    [bool]_ValidateResponse() {
        if ($this._ValidateBool) {
            return $this._CheckBool()
        }
        elseif ($this._ValidateInt) {
            return $this._CheckInt()
        }
        else {
            $this._ValidatedResponse = $this._UserResponse
            return $true
        }
    }

    [bool]_CheckBool() {
        $resp = $this._UserResponse.Trim().ToLower()
        if ($resp -eq 'y' -or $resp -eq 'n') {
            $this._ValidatedResponse = ($resp -eq 'y')
            return $true
        }
        $this._ErrorCount["yes/no"]++
        $this._ShowAlert(
            "Please enter 'y' or 'n'", 
            $this._ErrorCount["yes/no"]
        )
        return $false
    }

    [bool]_CheckInt() {
        if (-not ($this._UserResponse -match '^-?\d+$')) {
            $this._ErrorCount["NaN"]++
            $this._ShowAlert("Enter a valid number", $this._ErrorCount["NaN"])
            return $false
        }

        $resp = [int]$this._UserResponse

        if ($this._IntValidation -is [int]) {
            if ($resp -lt 0 -or $resp -ge $this._IntValidation) {
                $this._ErrorCount["OOR"]++
                $this._ShowAlert(
                    "Value must be between 0 and $($this._IntValidation - 1)", 
                    $this._ErrorCount["OOR"]
                )
                return $false
            }
        } elseif ($this._IntValidation -is [array]) {
            $low, $high = $this._IntValidation
            if ($resp -lt $low -or $resp -gt $high) {
                $this._ErrorCount["OOL"]++
                $this._ShowAlert(
                    "Enter a number between $low and $high", 
                    $this._ErrorCount["OOL"]
                )
                return $false
            }
        }

        $this._ValidatedResponse = $resp
        return $true
    }

    [void]_ShowAlert([string]$msg, [int]$count) {
        $this._Terminal.SetForegroundColor('Red')
        $this._Terminal.WriteLine("[$count] $msg")
        $this._Terminal.ResetColor()
    }
}