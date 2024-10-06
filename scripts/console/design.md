# Console Module
* [clearStdscr](#clearstdscr)
* [putScriptBanner](#putscriptbanner)
* [ConsolePrompt](#consoleprompt)
* [ConsoleTable](#consoletable)
### `clearStdscr`
```mermaid
flowchart LR
    STR([start])
        STR --> PUT
    PUT[/print/]
        PUT --> END
    END([end])
```
```
clearStdscr(console)
    PUT console.home + console.clear
END
```
### `putScriptBanner`
```mermaid
flowchart LR
    STR([start])
        STR --> PUT
    PUT[/print/]
        PUT --> END
    END([end])
```
```
putScriptBanner(console, scriptName)
    PUT "Running {scriptName}..."
        + left-justified(console.width)
        + console.reverse
END
```
## `ConsolePrompt`
```mermaid
graph TB
    MAIN([ConsolePrompt])
        MAIN 
            -- prompt <br> expectKeystroke <br> validateBool <br> validateInteger <br> integerValidation 
            --> INIT
        MAIN -- console --> CALL
    CALL(call <br> SET_console <br> GET_response)
        CALL --> GR
        CALL --> VR
        CALL -- response --> MAIN
    CBV(_checkBoolValitation <br> GET_response)
        CBV -- alert --> PA
        CBV -- valid --> VR
    CIV(_checkIntegerValitation <br> GET_response)
        CIV -- alert --> PA
        CIV -- valid --> VR
    GR(_getResponse <br> GET_expectKeystroke <br> SET_response)
        GR -- leaveCursorInline --> PP
        GR --> RK
        GR --> RS
    INIT(init <br> SET_prompt <br> SET_expectKeystroke <br> SET_validateBool <br> SET_validateInteger <br> SET_integerValidation)
    PA(_putAlert <br> GET_console)
        PA -- formattedAlert <br> leaveCursorInline--> PM
    PM(_printMessage)
    PP(_putPrompt <br> GET_console<br> GET_prompt)
        PP -- formattedPrompt <br> leaveCursorInline--> PM
    RK(_readKeystroke <br> GET_console)
        RK -- key --> GR
    RS(_readString <br> GET_console)
        RS -- leaveCursorInline --> PP
        RS -- string --> GR
    VR(_validateResponse <br> GET_validateBool <br> GET_validateInteger)
        VR --> CBV
        VR --> CIV
        VR -- valid --> CALL
```
* [_readKeystroke](#_readkeystroke)
* [_readString](#_readstring)
* [_putPrompt](#_putprompt)
* [_putAlert](#_putalert)
* [_printMessage](#_printmessage)
### `_readKeystroke`
```mermaid
flowchart LR
    STR([start])
        STR --> GET
    GET[/get keystroke/]
        GET --> RTN
    RTN[return keystroke]
        RTN --> END
    END([end])
```
```
_readKeystroke()
    GET keystroke
    RETURN keystroke
END
```
### `_readString`
```mermaid
flowchart TB
    STR([start])
        STR --> GET
    ADD[append key to string]
        ADD --> PUTK
    BCK[pop from string]
        BCK --> PUTP
    EBO{Enter <br> Backspace <br> or other key}
        EBO -- Enter --> RTN
        EBO -- Backspace --> BCK
        EBO -- other --> ADD
    GET[/get keystroke/]
        GET --> EBO
    PUTK[/print key/]
        PUTK --> GET
    PUTP[/put prompt, string/]
        PUTP --> GET
    RTN[return string]
        RTN --> END
    END([end])
```
```
_readString()
    ...
END
```
### `_putPrompt`
```mermaid
flowchart LR
    STR([start]) --> CALL
    CALL[call _printMessage] --> END
    END([end])
```
```
_putPrompt(leaveCursorInline)
    CALL _printMessage(_console.brightYellow + _prompt, leaveCursorInline)
END
```
### `_putAlert`
```mermaid
flowchart LR
    STR([start]) --> CALL
    CALL[call _printMessage] --> END
    END([end])
```
```
_putAlert(alert, leaveCursorInline)
    CALL _printMessage(_console.red + alert, leaveCursorInline)
END
```
### `_printMessage`
```mermaid
flowchart LR
    STR([start]) --> SET
    SET[compute displayWidth, padding, lineEnd] --> PUT
    PUT[/print/] --> END
    END([end])
```
```
_printMessage(message, leaveCursorInline)
    SET displayWidth
    SET padding
    WITH leaveCursorInline SET lineEnd
    PUT message
END
```
## `ConsoleTable`
