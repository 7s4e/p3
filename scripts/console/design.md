# Console Module
* [clearStdscr](#clearstdscr)
* [putScriptBanner](#putscriptbanner)
* [ConsolePrompt](#consoleprompt)
* [ConsoleTable](#consoletable)
---
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
---
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
---
---
## `ConsolePrompt`
```mermaid
graph TB
    MAIN([**ConsolePrompt**])
        MAIN -- prompt
                expectKeystroke
                validateBool
                validateInteger
                integerValidation 
             --> INIT
        MAIN -- console --> CALL
    CALL("<b><u>call</u></b>
          <div style='text-align:left;'>SET console
                                        GET validatedResponse</div>")
        CALL --> GR
        CALL --> VR
        CALL -- response --> MAIN
    CBV("<b><u>_checkBoolValidation</u></b>
         <div style='text-align:left;'>GET userResponse
                                       SET validatedResponse</div>")
        CBV -- alert --> PA
        CBV -- valid --> VR
    CIV("<b><u>_checkIntegerValitation</u></b>
         <div style='text-align:left;'>GET userResponse
                                       SET validatedResponse</div>")
        CIV -- alert --> PA
        CIV -- valid --> VR
    GR("<b><u>_getResponse</u></b>
        <div style='text-align:left;'>GET expectKeystroke
                                      SET userResponse</div>")
        GR -- leaveCursorInline --> PP
        GR --> RK
        GR --> RS
    INIT("<b><u>init</u></b>
          <div style='text-align:left;'>SET prompt
                                        SET expectKeystroke
                                        SET validateBool
                                        SET validateInteger
                                        SET integerValidation</div>")
    PA("<b><u>_putAlert</u></b>
        <div style='text-align:left;'>GET console</div>")
        PA -- formattedAlert
              leaveCursorInline
           --> PM
    PM(**_printMessage**)
    PP("<b><u>_putPrompt</u>
        </b><div style='text-align:left;'>GET_console
                                          GET_prompt</div>")
        PP -- formattedPrompt
              leaveCursorInline
           --> PM
    RK("<b><u>_readKeystroke</u></b>
        <div style='text-align:left;'>GET console</div>")
        RK -- key --> GR
    RS("<b><u>_readString</u></b>
        <div style='text-align:left;'>GET console</div>")
        RS -- leaveCursorInline --> PP
        RS -- string --> GR
    VR("<b><u>_validateResponse</u></b>
        <div style='text-align:left;'>GET_validateBool
                                      GET_validateInteger</div>")
        VR --> CBV
        VR --> CIV
        VR -- valid --> CALL
```
* [call](#call)
* [_getResponse](#_getresponse)
* [_readKeystroke](#_readkeystroke)
* [_readString](#_readstring)
* [_putPrompt](#_putprompt)
* [_putAlert](#_putalert)
* [_printMessage](#_printmessage)
---
### `call`
```mermaid
flowchart LR
    STR([start])
        STR --> SET
    SET[/set console/]
        SET --> GR
    GR[call getResponse]
        GR --> VR
    RTN{valid}
        RTN -- True --> END
        RTN -- False --> GR
    VR[call validateResponse]
        VR --> RTN
    END([end])
```
```
call(console)
    SET self.console <- console
    SET valid <- False
    WHILE NOT valid
        getResponse()
        valid <- validateResponse()
    RETURN self.validatedResponse
END
```
---
### `_getResponse`
```mermaid
flowchart LR
    STR([start])
        STR --> KEY
    KEY{expectKeystroke}
        KEY -- True --> CALLF
        KEY -- False --> CALLT
    CALLF[call putPrompt <br> cursor left on new line]
        CALLF --> READK
    CALLT[call putPrompt <br> cursor left inline]
        CALLT --> READS
    READK[call readKeystroke]
        READK --> SET
    READS[call readString]
        READS --> SET
    SET[/set userResponse/]
        SET --> END
    END([end])
```
```
getResponse()
    GET self.expectKeystroke
    IF expectKeystroke
        putPrompt(inlineCursor=False)
        SET userResponse <- readKeystroke()
    ELSE
        putPrompt(inlineCursor=True)
        SET userResponse <- readString()
END
```
---
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
---
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
readString()
    SET userInput <- []
    WHILE True
        SET key = input()
        IF key == Enter
            BREAK
        IF key == Backspace
            POP userInput
            PUT prompt + userInput
        ELSE
            APPEND userInput + key
            PUT key
    RETURN userInput
END
```
---
### `_putPrompt`
```mermaid
flowchart LR
    STR([start]) --> CALL
    CALL[call printMessage] --> END
    END([end])
```
```
putPrompt(leaveCursorInline)
    printMessage(console.brightYellow + prompt, leaveCursorInline)
END
```
---
### `_validateResponse`
```mermaid
flowchart TB
    STR([start])
        STR --> VB
    CBV[call checkBoolValidation]
        CBV --> RTN
    CIV[call checkIntegerValidation]
        CIV --> RTN
    RTN[/return validation status/]
        RTN --> END
    VB{validateBool}
        VB -- True --> CBV
        VB -- False --> VI
    VI{validateInteger}
        VI -- True --> CIV
        VI -- False --> RTN
    END([end])
```
```
validateResponse()
    IF self.validateBool
        RETURN checkBoolValidation()
    IF self.validateInteger
        RETURN checkIntegerValidation()
    RETURN True
END
```
---
### `_checkBoolValidation`
```mermaid
flowchart LR
    STR([start])
        STR --> UR
    PUT[/put alert/]
        PUT --> RTN
    RTN[return validation status]
        RTN --> END
    SET[set validatedResponse]
        SET --> RTN
    UR{userResponse}
        UR -- y | n --> SET
        UR -- invalid --> PUT
    END([end])
```
```
checkBoolValidation()
    IF self.userResponse.lower IN {'y', 'n'}
        SET self.validatedResponse <- userResponse == 'y'
        RETURN True
    putAlert()
    RETURN False
```
---
### `_checkIntegerValidation`
```mermaid
flowchart TB
    STR([start])
        STR --> UR
    INT{0 <= userResponse < integerValitation}
        INT -- True --> SET
        INT -- False --> PUT
    IVT{integerValidation Type}
        IVT -- None --> SET
        IVT -- int --> INT
        IVT -- tuple --> TPL
    PUT[/put alert/]
        PUT --> RTN
    RTN[return validation status]
        RTN --> END
    SET[set validatedResponse]
        SET --> RTN
    TPL{integerValidation.0 <= userResponse <= integerValidation.1}
        TPL -- True --> SET
        TPL -- False --> PUT
    UR{userReponse Type int}
        UR -- True --> IVT
        UR -- False --> PUT
    END([end])
```
```
checkIntegerValidation()
    IF self.userResponse IS NOT TYPE int
        putAlert(TypeError message)
        RETURN False
    SWITCH self.integerValidation TYPE
        CASE int
            IF userResponse < 0 OR userResponse >= integervalidation
                putAlert(ValueError: exceeds range)
                RETURN False
        CASE tuple
            SET lo, hi <- integervalidation
            IF userResponse < lo OR userResponse > hi
                putAlert(ValueError: exceeds limits)
                RETURN False
        CASE None
            BREAK
    SET self.validatedResponse <- userResponse
```
---
### `_putAlert`
```mermaid
flowchart LR
    STR([start]) --> CALL
    CALL[call printMessage] --> END
    END([end])
```
```
putAlert(alert, leaveCursorInline)
    printMessage(console.red + alert, leaveCursorInline)
END
```
---
### `_printMessage`
```mermaid
flowchart LR
    STR([start]) --> SET
    SET[compute displayWidth, padding, lineEnd] --> PUT
    PUT[/print/] --> END
    END([end])
```
```
printMessage(message, leaveCursorInline)
    SET displayWidth
    SET padding
    WITH leaveCursorInline SET lineEnd
    PUT message
END
```
---
---
## `ConsoleTable`
