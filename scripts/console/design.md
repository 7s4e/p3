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
graph TD
    %% Class Initialization
    CLS([ConsolePrompt]) 
        -- prompt <br> expectKeystroke <br> validateBool <br> validateInteger <br> integerValidation 
        --> INIT(init)
    INIT 
        -. _prompt <br> _expectKeystroke <br> _validateBool <br> _validateInteger <br> _integerValidation 
        .-> INST[instance]
    
    %% Public method call()
    CLS -- console --> CALL(call)
    CALL -. _console .-> INST
    INST -. _response .-> CALL
    CALL -- response --> CLS

        %% Calls getResonse() and validateResponse()
        CALL --> GR(_getResponse)

            %% Private method getResponse()
            INST -. _expectKeystroke .-> GR
            GR -. _response .-> INST
            
                %% Calls putPrompt(), readKeystroke(), and readString()
                GR -- leaveCursorInline --> PP(_putPrompt)

                    %% Private method putPrompt()


                GR --> RK(_readKeystroke)
                GR --> RS(_readString)
                
        CALL --> VR(_validateResponse)
        VR -- valid --> CALL


    INST -. _console <br> _prompt .-> PP
    PP -- formattedPrompt <br> leaveCursorInline--> PM(_printMessage)

    INST -. _console .-> RK
    RK -- key --> GR

    INST -. _console .-> RS
    RS -- string --> GR
```
## `ConsoleTable`
