# Console Module
* [clearStdscr](#clearstdscr)
* [putScriptBanner](#putscriptbanner)
* [ConsolePrompt](#consoleprompt)
* [ConsoleTable](#consoletable)
### `clearStdscr`
```mermaid
flowchart LR
    A([start]) --> B[/print/]
    B --> C([end])
```
```
void clearStdscr(Terminal console)
    PUT console.home + console.clear
END
```
### `putScriptBanner`
```mermaid
flowchart LR
    A([start]) --> B[/print/]
    B --> C([end])
```
```
void putScriptBanner(Terminal console, string scriptName)
    PUT "Running {scriptName}..."
        + left-justified(console.width)
        + console.reverse
END
```
## `ConsolePrompt`
```mermaid
graph TB
    MAIN([ConsolePrompt]) 
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
## `ConsoleTable`
