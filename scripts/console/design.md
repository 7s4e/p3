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
* [\_\_init__](#__init__)
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
graph
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
flowchart
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
flowchart
    CALL([call])
        CALL --> GETK
    GETK[\expectKeystroke\]
        GETK --> EXPK
    EXPK{expectKeystroke}
        EXPK -- True  --> PPFA
        EXPK -- False --> PPTR
    PPFA[[putPrompt *False*]]
        PPFA --> RKEY
    PPTR[[putPrompt *True*]]
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
flowchart
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
flowchart
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
flowchart
    PPPA([putPrompt
          putAlert])
        PPPA --> CMLC
    CMLC[\console
          message
          leaveCursorInline\]
        CMLC --> SDPE
    SDPE[displayWidth
         padding
         lineEnd]
        SDPE --> PRNT
    PRNT[/padding + message + end/]
        PRNT --> TEND
    TEND([end])
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
* [\_\_init__](#__init__-1)
* [display](#display)
* [_setDimensions](#_setdimensions)
* [_drawTable](#_drawtable)
* [_drawRow](#_drawrow)
* [_getRowEnds](#_getrowends)
* [_getRowContent](#_getrowcontent)
* [_processRowContent](#_processrowcontent)
* [Table](../table/design.md)
```mermaid
graph
    style MAIN fill:#4682b4,stroke:#b97d4b,stroke-width:2px,color:#0ff
    style T fill:#b97d4b,stroke:#4682b4,stroke-width:2px
    style C fill:#b97d4b,stroke:#4682b4,stroke-width:2px
    classDef method fill:#4682b4,stroke:#b97d4b,stroke-width:2px
    STRT([start])
        STRT -- data --> INIT
    INIT(*init*):::method
        INIT --> MAIN
    MAIN([**ConsoleTable**])
        MAIN -- console  --> DSPL
    DSPL(display):::method
        DSPL                 --> SDMN
        TGET -- recordCount --> DSPL
        DSPL -- recordCount --> DTBL
    SDMN(_setDimensions):::method
        TGET -- tableWidth   --> SDMN
        SDMN -- tableSpace   --> RSZC
        TGET -- columnWidths --> SDMN
    DTBL(_drawTable):::method
        DTBL -- row --> DROW
    DROW(_drawRow):::method
        TGET -- rjustCols --> DROW
        DROW -- row       --> GRWE
        GRWE -- spacing   --> DROW
        DROW -- row       --> GTXT
        GTXT -- content   --> DROW
        DROW -- row       --> PTXT
        PTXT -- cells     --> DROW
    GRWE(_getRowEnds):::method
    GTXT(_getRowContent):::method
        TGET -- title    --> GTXT
        TGET -- headings --> GTXT
        TGET -- record   --> GTXT
    PTXT(_processRowContent):::method
        PTXT --> RVRS
        PTXT --> UDLN
    subgraph T [**Table**]
        TGET(Table getters)
        RSZC(resizeColumns)
    end
    subgraph C [**blessed.Terminal**]
        RVRS(reverse)
        UDLN(underline)
    end
```
[️⬆️](#console-module)
---
### `__init__`
```mermaid
flowchart LR
    classDef this fill:#4682b4,stroke:#b97d4b,stroke-width:2px
    STRT([start])
        STRT --> GDTA
    GDTA[\data\]
        GDTA --> SDTA
    SDTA[/data
         borders/]
        SDTA --> CTBL
    CTBL([**ConsoleTable**]):::this
```
```
init(data)
    SET self.data <- data
    SET self.borders <- {"top": {"left": "╔", "fill": "═", "right": "╗"}, 
                         "inner": {"left": "╟", "fill": "─", "right": "╢"}, 
                         "bottom": {"left": "╚", "fill": "═", "right": "╝"}, 
                         "side": "║"}
END
```
 [️⬆️](#consoletable)
---
### `display`
```mermaid
flowchart
    classDef this fill:#4682b4,stroke:#b97d4b,stroke-width:2px
    classDef that fill:#b97d4b,stroke:#4682b4,stroke-width:2px
    CTBL([**ConsoleTable**]):::this
        CTBL --> GCNS
    GCNS[\console\]
        GCNS --> SCNS
    SCNS[/console/]
        SCNS --> SDMN
    SDMN[[setDimensions]]:::this
        SDMN --> CREC
    CREC[[countRecords]]:::that
        CREC --> DTBL
    DTBL[[drawTable]]:::this
        DTBL --> THEE
    THEE([end])
```
```
display(console)
    SET self.con <- console
    self.setDimensions()
    self.drawTable(self.data.countRecords())
END
```
 [️⬆️](#consoletable)
---
### `_setDimensions`
```mermaid
flowchart
    classDef this fill:#4682b4,stroke:#b97d4b,stroke-width:2px
    classDef that fill:#b97d4b,stroke:#4682b4,stroke-width:2px
    DSPL([display]):::this
        DSPL --> GCNS
    GCNS[\console\]
        GCNS --> SDMT
    SDMT[/displayWidth
          marginSize/]
        SDMT --> GTW1
    GTW1[[getTableWidth]]:::that
        GTW1 --> STW1
    STW1[/tableWidth/]
        STW1 --> TBSP
    TBSP[tableSpace]
        TBSP --> WVSS
    WVSS{tableWidth > tableSpace}
        WVSS -- True  --> RSZC
        WVSS -- False --> GCLW
    RSZC[[resizeColumns]]:::that
        RSZC --> GTW2
    GTW2[[getTableWidth]]:::that
        GTW2 --> STW2
    STW2[/tableWidth/]
        STW2 --> GCLW
    GCLW[[getColumnWidths]]:::that
        GCLW --> SCLW
    SCLW[/columnWidths/]
        SCLW --> THEE
    THEE([end])
```
```
setDimensions()
    SET self.displayWidth <- MIN(self.con.width, 79)
    SET self.marginSize <- (con.width - displayWidth) // 2
    SET self.tableWidth <- self.data.getTableWidth()
    SET tableSpace = displayWidth - 4
    IF tableWidth > tableSpace
        data.resizeColumns(tableSpace)
        tableWidth <- data.getTableWidth()
    SET self.columnWidths <- data.getColumnWidths()
END
```
 [️⬆️](#consoletable)
---
### `_drawTable`
```mermaid
flowchart
    classDef this fill:#4682b4,stroke:#b97d4b,stroke-width:2px
    DSPL([display]):::this
        DSPL --> RCNT
    RCNT[\recordCount\]
        RCNT --> DRTP
    DRTP[[drawRow *top*]]:::this
        DRTP --> DRTL
    DRTL[[drawRow *title*]]:::this
        DRTL --> DRIN
    DRIN[[drawRow *inner*]]:::this
        DRIN --> DRHD
    DRHD[[drawRow *headings*]]:::this
        DRHD --> FIRC
    FIRC{i < recordCount}
        FIRC -- True  --> DRRC
        DRRC          --> FIRC
        FIRC -- False --> DRBT
    DRRC[[drawRow *record*]]:::this
    DRBT[[drawRow *bottom*]]:::this
        DRBT --> THEE
    THEE([end])
```
```
drawTable(recordCount)
    self.drawRow("top")
    self.drawRow("title")
    self.drawRow("inner")
    self.drawRow("headings")
    FOR i IN recordCount
        self.drawRow("record", i)
    self.drawRow("bottom")
END
```
 [️⬆️](#consoletable)
---
### `_drawRow`
```mermaid
flowchart
    classDef this fill:#4682b4,stroke:#b97d4b,stroke-width:2px
    classDef that fill:#b97d4b,stroke:#4682b4,stroke-width:2px
    DTBL([drawTable]):::this
        DTBL --> RTRI
    RTRI[\rowType
          recordIndex\]
        RTRI --> SLTT
    SLTT[lineTypes
         textTypes]
        SLTT --> RTYP
    RTYP{rowType}
        RTYP -- record --> GRJC
        RTYP -- NOT record --> SMRG
    GRJC[[getRjustColumns]]:::that
        GRJC --> SRJC
    SRJC[rjustCol]
        SRJC --> SMRG
    SMRG[margin]
        SMRG --> GRWE
    GRWE[[getRowEnds]]:::this
        GRWE --> SLRG
    SLRG[left
         right
         gap]
        SLRG --> RTT1
    RTT1{rowType in textTypes}
        RTT1 -- True  --> GTXC
        RTT1 -- False --> SCNT
    GTXC[[getTextContent]]:::this
        GTXC --> SCNT
    SCNT[content]
        SCNT --> RTT2
    RTT2{rowType in textTypes}
        RTT2 -- True  --> PTXC
        RTT2 -- False --> SCLL
    PTXC[[processRowContent]]:::this
        PTXC --> SCLL
    SCLL[cells]
        SCLL --> PRNT
    PRNT[/margin + left + gap + cells + gap + right/]
        PRNT --> THEE
    THEE([end])
```
```
drawRow(rowType, recordIndex)
    SET lineTypes <- ["top", "inner", "bottom"]
    SET textTypes <- ["title", "headings", "record"]
    IF rowType == "record"
        SET rjustCol <- self.data.getRjustColumns()
    ELSE
        SET rjustCol <- {}
    SET margin <- " " * self.marginSize
    SET left, right, gap <- self.getRowEnds(rowType, rowType IN lineTypes)
    IF rowType IN textTypes
        SET content <- self.getTextContent(rowType, recordIndex)
    ELSE
        SET content <- self.borders[rowType]["fill"]
    IF rowType IN textTypes
        SET cells <- self.processRowContent(rowType, content, rjustCol)
    ELSE
        SET cells <- content * (self.tableWidth + 2)
    PUT margin + left + gap + cells.join("  ") + gap + right
END
```
 [️⬆️](#consoletable)
---
### `_getRowContent`
```mermaid
flowchart LR
    classDef this fill:#4682b4,stroke:#b97d4b,stroke-width:2px
    classDef that fill:#b97d4b,stroke:#4682b4,stroke-width:2px
    DWRW([drawRow]):::this
        DWRW --> RTIX
    RTIX[\rowType
          index\]
        RTIX --> RTYP
    RTYP{rowType}
        RTYP -- title   --> GTTL
        RTYP -- heading --> GHDG
        RTYP -- record  --> GREC
    GTTL[[getTitle]]:::that
        GTTL --> RTNT
    GHDG[[getHeadings]]:::that
        GHDG --> RTNH
    GREC[[getRecord]]:::that
        GREC --> RTNR
    RTNT([title])
    RTNH([headings])
    RTNR([record])
```
```
getTextContent(rowType, index)
    SWITCH rowType
        CASE "title"
            RETURN self.data.getTitle()
        CASE "headings"
            RETURN self.data.getHeadings()
        CASE "record"
            RETURN self.data.getRecord(index)
END
```
 [️⬆️](#consoletable)
---
### `_getRowEnds`
```mermaid
flowchart
    classDef this fill:#4682b4,stroke:#b97d4b,stroke-width:2px
    DWRW([drawRow]):::this
        DWRW --> RTLT
    RTLT[\rowType
          isLineType\]
        RTLT --> ISLT
    ISLT{isLineType}
        ISLT -- True  --> GBRT
        ISLT -- False --> GBSD
    GBRT[\borders.rowType\]
        GBRT --> SLRP
    GBSD[\borders.side\]
        GBSD --> SLRP
    SLRP[leftEnd
         rightEnd
         padding]
        SLRP --> RTRN
    RTRN([left
          right
          gap])
```
```
getRowEnds(rowType, isLineType)
    IF isLineType
        SET leftEnd <- self.borders[rowType]["left"]
        SET rightEnd <- self.borders[rowType]["right"]
        SET padding <- ""
    ELSE
        SET leftEnd, rightEnd <- self.borders["side"]
        SET padding <- " "
    RETURN leftEnd, rightEnd, padding
END
```
 [️⬆️](#consoletable)
---
### `_processRowContent`
```mermaid
flowchart
    classDef this fill:#4682b4,stroke:#b97d4b,stroke-width:2px
    classDef that fill:#b97d4b,stroke:#4682b4,stroke-width:2px
    DWRW([drawRow]):::this
        DWRW --> TCRJ
    TCRJ[\rowType
          content
          rjustCol\]
        TCRJ --> RTTL
    RTTL{rowType == title}
        RTTL -- True  --> SCTL
        RTTL -- False --> IINC
    SCTL[cell]
        SCTL --> APC1
    APC1[cells]
        APC1 --> RTRN
    IINC{item in content}
        IINC -- True  --> GCLW
        APC2          --> IINC
        IINC -- False --> RTRN
    GCLW[\columnWidth\]
        GCLW --> RTHD
    RTHD{rowType == headings}
        RTHD -- True  --> SCHD
        RTHD -- False --> KRJC
    SCHD[cell]
        SCHD --> APC2
    KRJC{key in rjustCol}
        KRJC -- True  --> SCRJ
        KRJC -- False --> SCLJ
    SCRJ[cell]
        SCRJ --> APC2
    SCLJ[cell]
        SCLJ --> APC2
    APC2[cells]
    RTRN([cells])
```
```
processRowContent(rowType, content, rjusCol)
    SET cells <- []
    IF rowType == "title"
        SET cell <- centered content in reverse
        APPEND cell TO cells
    ELSE
        FOR key, value IN content
            GET self.columnWidths[key]
            IF rowType == "headings"
                SET cell <- centered value in underline
            ELSE
                IF key IN rjustCol
                    SET cell <- right-justified value
                ELSE
                    SET cell <- left-justified value
            APPEND cell TO cells
    RETURN cells
END
```
 [️⬆️](#consoletable)
---
