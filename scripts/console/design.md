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
* [\_\_init__](#__init_)
* [call](#call)
* [_getResponse](#_getresponse)
* [_validateResponse](#_validateresponse)
* [_readKeystroke](#_readkeystroke)
* [_readString](#_readstring)
* [_checkBoolValidity](#_checkboolvalidity)
* [_checkIntegerValidity](#_checkintegervalidity)
* [_putPrompt](#_putprompt)
* [_putAlert](#_putalert)
* [_printMessage](#_printmessage)
```mermaid
graph TB
    STRT([start])
        STRT -- prompt
                expectKeystroke
                validateBool
                validateInteger
                integerValidation --> INIT
    INIT(*init*)
        INIT --> MAIN
    MAIN([**ConsolePrompt**])
        MAIN -- console  --> CALL
        CALL -- response --> MAIN
    CALL(call)
        CALL          --> GRSP
        CALL          --> VRSP
        VRSP -- valid --> CALL
    GRSP(_getResponse)
        GRSP                      --> RDKY
        RDKY -- key               --> GRSP
        GRSP                      --> RDST
        RDST -- string            --> GRSP
        GRSP -- leaveCursorInline --> PUTP
    RDKY(_readKeystroke)
    RDST(_readString)
        RDST -- leaveCursorInline --> PUTP
    VRSP(_validateResponse)
        VRSP          --> CBOL
        CBOL -- valid --> VRSP
        VRSP          --> CINT
        CINT -- valid --> VRSP
    CBOL(_checkBoolValidation)
        CBOL -- alert --> PUTA
    CINT(_checkIntegerValitation)
        CINT -- alert --> PUTA
    PUTP(_putPrompt)
        PUTP -- formattedPrompt
                leaveCursorInline --> PRNT
    PUTA(_putAlert)
        PUTA -- formattedAlert
                leaveCursorInline --> PRNT
    PRNT(_printMessage)
```
[️⬆️](#console-module)
---
### `__init__`
```mermaid
flowchart LR
    STR([start])
        STR --> GET
    GET[\prompt
         expectKeystroke
         validateBool
         validateInt
         intValidation\]
        GET --> SET
    SET[/prompt
         expectKeystroke
         validateBool
         validateInt
         intValidation/]
        SET --> END
    END([**ConsolePrompt**])
```
```
init(prompt, expectKeystroke, validateBool, validateInt, intValidation)
    SET self.prompt <- prompt
    SET self.expectKeystroke <- expectKeystroke
    SET self.validateBool <- validateBool
    SET self.validateInt <- validateInt
    SET self.intValidation <- intValidation
END
```
 [️⬆️](#consoleprompt)
---
### `call`
```mermaid
flowchart LR
    CONP([**ConsolePrompt**])
        CONP --> RCON
    RCON[\console\]
        RCON --> WCON
    WCON[/console/]
        WCON --> VALD
    VALD{valid}
        VALD -- True  --> GETR
        VALD -- False --> GRES
        VRES          --> VALD
    GRES[[getResponse]]
        GRES --> VRES
    VRES[[validateResponse]]
    GETR[\validatedResponse\]
        GETR --> RTRN
    RTRN([validatedResponse])
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
 [️⬆️](#consoleprompt)
---
### `_getResponse`
```mermaid
flowchart LR
    CALL([call])
        CALL --> GETK
    GETK[\expectKeystroke\]
        GETK --> EXPK
    EXPK{expectKeystroke}
        EXPK -- True  --> PPFA
        EXPK -- False --> PPTR
    PPFA[[putPrompt-False]]
        PPFA --> RKEY
    PPTR[[putPrompt-True]]
        PPTR --> RSTR
    RKEY[[readKeystroke]]
        RKEY --> TEND
    RSTR[[readString]]
        RSTR --> TEND
    TEND([end])
```
```
getResponse()
    GET self.expectKeystroke
    IF expectKeystroke
        putPrompt(inlineCursor=False)
        userResponse <- readKeystroke()
    ELSE
        putPrompt(inlineCursor=True)
        userResponse <- readString()
END
```
[️⬆️](#consoleprompt)
---
### `_validateResponse`
```mermaid
flowchart TB
    CALL([call])
        CALL --> RDBI
    RDBI[\validateBool
          validateInt\]
        RDBI --> VBOL
    VBOL{validateBool}
        VBOL -- True  --> CBOL
        VBOL -- False --> VINT
    VINT{validateInteger}
        VINT -- True  --> CINT
        VINT -- False --> RTRN
    CBOL[[checkBoolValidity]]
        CBOL --> RTRN
    CINT[[checkIntValidity]]
        CINT --> RTRN
    RTRN([valid])
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
[️⬆️](#consoleprompt)
---
### `_readKeystroke`
```mermaid
flowchart LR
    GRES([getResponse])
        GRES --> GKEY
    GKEY[\keystroke\]
        GKEY          --> PRNT
        PRNT -- False --> GKEY
    PRNT{printable}
        PRNT -- True --> WRES
    WRES[/userResponse/]
        WRES --> TEND
    TEND([end])
```
```
_readKeystroke()
    GET keystroke
    SET userResponse <- keystroke
END
```
[️⬆️](#consoleprompt)
---
### `_readString`
```mermaid
flowchart TB
    GRES([getResponse])
        GRES --> GKEY
    GKEY[\keystroke\]
        GKEY          --> ENTR
        PRNT -- False --> GKEY
        RPOP          --> GKEY
        RADD          --> GKEY
    ENTR{*Enter*}
        ENTR -- True  --> WRES
        ENTR -- False --> BKSP
    BKSP{*Backspace*}
        BKSP -- True  --> RPOP
        BKSP -- False --> PRNT
    PRNT{printable}
        PRNT -- True --> RADD
    RPOP[response.pop]
    RADD[response.append]
    WRES[/userResponse/]
        WRES --> TEND
    TEND([end])
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
[️⬆️](#consoleprompt)
---
### `_checkBoolValidity`
```mermaid
flowchart LR
    VRES([validateResponse])
        VRES --> RRES
    RRES[\userResponse\]
        RRES --> YSNO
    YSNO{*y* or *n*}
        YSNO -- True  --> WRES
        YSNO -- False --> PUTA
    WRES[/validatedResponse/]
        WRES --> RTNT
    PUTA[[putAlert]]
        PUTA --> RTNF
    RTNF([False])
    RTNT([True])
```
```
checkBoolValidation()
    IF self.userResponse.lower IN {'y', 'n'}
        SET self.validatedResponse <- userResponse == 'y'
        RETURN True
    putAlert()
    RETURN False
```
[️⬆️](#consoleprompt)
---
### `_checkIntegerValidity`
```mermaid
flowchart TB
    VRES([validateResponse])
        VRES --> URIV
    URIV[\userResponse
          intValidation\]
        URIV --> RNAN
    RNAN{userResponse NAN}
        RNAN -- True  --> PUTA
        RNAN -- False --> TYPE
    TYPE{integerValidation.type}
        TYPE -- int   --> OOFR
        TYPE -- tuple --> BYND
        TYPE -- None -->  WRES
    OOFR{out of range}
        OOFR -- True  --> PUTA
        OOFR -- False --> WRES
    BYND{beyond limits}
        BYND -- True  --> PUTA
        BYND -- False --> WRES
    WRES[/validatedResponse/]
        WRES --> RTNT
    PUTA[[putAlert]]
        PUTA --> RTNF
    RTNF([False])
    RTNT([True])
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
[️⬆️](#consoleprompt)
---
### `_putPrompt`
```mermaid
flowchart LR
    GRRS([getResponse
          readString])
        GRRS --> LCIP
    LCIP[\prompt
          leaveCursorInline\]
        LCIP --> PRNT
    PRNT[[printMessage]]
        PRNT --> TEND
    TEND([end])
```
```
putPrompt(leaveCursorInline)
    printMessage(console.brightYellow + prompt, leaveCursorInline)
END
```
[️⬆️](#consoleprompt)
---
### `_putAlert`
```mermaid
flowchart LR
    CBCI([checkBoolValidity
          checkIntValidity])
        CBCI --> ALRT
    ALRT[\alert\]
        ALRT --> PRNT
    PRNT[[printMessage]]
        PRNT --> TEND
    TEND([end])
```
```
putAlert(alert, leaveCursorInline)
    printMessage(console.red + alert, leaveCursorInline)
END
```
[️⬆️](#consoleprompt)
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
[️⬆️](#consoleprompt)
---
---
## `ConsoleTable`
