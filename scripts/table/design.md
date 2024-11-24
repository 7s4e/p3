# Table Module
## `Table`
### Method Groups
* [Initialize Table Methods](#initialize-table-methods)
* [Modify Table Methods](#modify-table-methods)
* [Display Table Methods](#display-table-methods)
* [Getters](#getters)
#### Initialize Table Methods
* [\_\_init__](#__init__)
* [_capitalizeKeys](#_capitalizekeys)
* [_readTable](#_readtable)
* [_findColumnPositions](#_findcolumnpositions)
* [_getSlice](#_getslice)
* [_findBoundaries](#_findboundaries)
* [_addRjustColLabel](#_addrjustcollabel)
```mermaid
graph TB
    TABL([**Table**])
        TABL -- tableData
                tableString
                title
                rjustColumns --> INIT
    subgraph i [Initialize Table Methods]
        INIT(*init*)
            INIT -- tableData   --> CAPK
            INIT -- tableString --> READ
        CAPK(_capitalizeKeys)
        READ(_readTable)
            READ -- headerLine
                    keys            --> FNDC
            FNDC -- columnPositions --> READ
            READ -- columnIndex
                    positionsList
                    line            --> GETS
            GETS -- slice           --> READ
        FNDC(_findColumnPositions)
        GETS(_getSlice)
            GETS -- columnIndex
                    positionsList
                    line          --> FNDB
            FNDB -- boundaries    --> GETS
        FNDB(_findBoundaries)
    end
    subgraph d [Display Table Methods]
        NUMR(_numberRecords)
    end
    ARJC(_addRjustColLabel)
        INIT -- rjustColumns --> ARJC
        NUMR                 --> ARJC
```
[️⬆️](#method-groups)
---
##### `__init__`
```mermaid
flowchart TB
    STR([start])
        STR --> SRC
    SRC[\"<span style='color:cyan;'>tableSource</span>
          <span style='color:magenta;'>title</span>
          <span style='color:yellow;'>rjustLabel</span>"\]
        SRC --> DOS
    DOS{"<span style='color:cyan;'>data | string</span>"}
        DOS -- data  --> CAP
        DOS -- string --> RDT
    CAP[[capitalizeKeys]]
        CAP --> SET
    RDT[[readTable]]
        RDT --> SET
    SET[/"<span style='color:magenta;'>title</span>, rjustCols"/]
        SET --> HCL
    HCL{"<span style='color:yellow;'>has</span>"}
        HCL -- True  --> ACL
        HCL -- False --> END
    ACL[[addRjustColLabel]]
        ACL --> END
    END([Table])
```
```
init(tableData, tableString, title, rjustColLabel)
    IF (tableData IS None) == (tableString IS None)
        RAISE ValueError
    IF tableData
        CALL capitalizeKeys
    ELSE
        CALL readTable
    SET title
    SET rjustColumns
    IF rjustColLabel
        CALL addRjustColLabel
END
```
[️⬆️](#initialize-table-methods)
---
##### `_capitalizeKeys`
```mermaid
flowchart LR
    STR([init])
        STR --> DTA
    DTA[\data\]
        DTA --> DTM
    DTM{datum}
        DTM -- True  --> CAP
        CAP          --> DTM
        DTM -- False --> SET
    CAP[set KEY:value]
    SET[/dataset, length/]
        SET --> END
    END([end])
```
```
capitalize_keys(data)
    SET self.dataset <- []
    FOR datum IN data
        FOR key, value IN datum
            SET datum[key.upper] <- value
        APPEND datum TO self.dataset
    SET self.recordsCount <- self.dataset.length
```
[️⬆️](#initialize-table-methods)
---
##### `_readTable`
```mermaid
flowchart TB
    STR([init])
        STR --> TBS
    TBS[\string\]
        TBS --> SPT
    SPT["split <span style='color:cyan;'>lines</span>
         set <span style='color:magenta;'>headers</span>"]
        SPT --> FCP
    FCP[[findColumnPositions]]
        FCP --> LNS
    LNS{"<span style='color:cyan;'>line</span>"}
        LNS -- True  --> HDR
        SDS          --> LNS
        LNS -- False --> SLN
    HDR{"<span style='color:magenta;'>header</span>"}
        HDR -- True  --> GSL
        SHV          --> HDR
        HDR -- False --> SDS
    GSL[[getSlice]]
        GSL --> SHV
    SDS[/dataset/]
    SLN[/length/]
        SLN --> END
    SHV[set HEADER:value]
    END([end])
```
```
readTable(string)
    SET lines <- string.splitlines
    SET headers <- lines[0].split
    SET columnPositions <- findColumnPositions()
    FOR line IN lines
        FOR header, index in headers
            SET value <- getSlice()
            SET datum[header.upper] <- value
        APPEND datum TO self.dataset
    SET self.recordsCount <- self.dataset.length
```
[️⬆️](#initialize-table-methods)
---
##### `_findColumnPositions`
```mermaid
flowchart LR
    STR([readTable])
        STR --> INP
    INP[\"<span style='color:cyan;'>headerLine</span>
         <span style='color:magenta;'>keys</span>"\]
        INP --> KEY
    KEY{<span style='color:magenta;'>key</span>}
        KEY -- True  --> POS
        POS          --> KEY
        KEY -- False --> END
    POS["get <span style='color:cyan;'>position</span>
         append to positions"]
    END([return positions])
```
```
findColumnPositions(headerLine, keys)
    SET positions <- []
    FOR key IN keys
        SET position <- headerLine.index OF key
        APPEND position TO positions
    RETURN positions
```
[️⬆️](#initialize-table-methods)
---
##### `_getSlice`
```mermaid
flowchart LR
    STR([readTable])
        STR --> FBD
    FBD[[findBoundaries]]
        FBD --> SET
    SET[set start, end]
        SET --> END
    END([return line.slice])
```
```
getSlice(columnIndex, positionsList, line)
    SET start, end <- findBoundaries(columnIndex, positionsList, line)
    RETURN line[start:end]
```
[️⬆️](#initialize-table-methods)
---
##### `_findBoundaries`
###### Overview
```mermaid
flowchart LR
    STR([getSlice])
        STR --> ARG
    ARG[\"<span style='color:cyan;'>columnIndex</span>
          <span style='color:magenta;'>positionsList</span>
          <span style='color:yellow;'>line</span>"\]
        ARG --> INT
    INT[[initialize start, end]]
        INT --> AJS
    AJS[[adjust start]]
        AJS --> AJE
    AJE[[adjust end]]
        AJE --> END
    END(["return <span style='color:green;'>start</span>, <span style=
              'color:red;'>end</span>"])
```
###### Initialize Subgraph
```mermaid
flowchart LR
    INP[\input\]
        INP --> SST
    subgraph init [Initialize start, end]
        SST["<span style='color:green;'>start</span> = <span style=
                 'color:magenta;'>positions</span>.<span style='color:cyan;'
                 >index</span>"]
            SST --> LST
        LST{"<span style='color:cyan;'>index</span> + 1 < <span style=
                 'color:magenta;'>positions</span>.length"}
            LST -- False --> SE1
            LST -- True  --> SE2
        SE1["<span style='color:red;'>end</span> = <span style=
                 'color:magenta;'>positions</span>.<span style='color:cyan;'
                 >index</span>+1"]
        SE2["<span style='color:red;'>end</span> = <span style=
                 'color:magenta;'>positions</span>.length"]
    end
    AJS[[adjust start]]
        SE1 --> AJS
        SE2 --> AJS
```
###### Start Subgraph
```mermaid
flowchart LR
    INT[[initialize start, end]]
        INT --> SIL
    subgraph start [Adjust start]
        SIL{"<span style='color:green;'>start</span> < <span style=
                 'color:yellow;'>line</span>.length"}
            SIL -- True --> SIS
            SIL -- False --> SLL
        SIS{"<span style='color:yellow;'>line</span>.<span style=
                 'color:green;'>start</span> == space"}
            SIS -- True --> WIS
            SIS -- False --> WNS
        WIS{"<span style='color:green;'>start</span> < <span style=
                 'color:red;'>end</span> &&
             <span style='color:yellow;'>line</span>.<span style=
                 'color:green;'>start</span> == space"}
            WIS -- True --> MSR
            MSR         --> WIS
        WNS{"<span style='color:yellow;'>line</span>.<span style=
                 'color:green;'>start</span>-1 != space"}
            WNS -- True --> MSL
            MSL         --> WNS
        MSR["<span style='color:green;'>start</span> += 1"]
        MSL["<span style='color:green;'>start</span> -= 1"]
        SLL["<span style='color:green;'>start</span> = <span style=
                 'color:yellow;'>line</span>.length"]
    end
    AJE[[adjust end]]
            WIS -- False --> AJE
            WNS -- False --> AJE
            SLL          --> AJE
```
###### End Subgraph
```mermaid
flowchart LR
    AJS[[adjust start]]
        AJS --> EIL
    subgraph end [Adjust end]
        EIL{"<span style='color:red;'>end</span> < <span style='color:yellow;'
                 >line</span>.length"}
            EIL -- True  --> WNS
            EIL -- False --> ELL
        WNS{"<span style='color:yellow;'>line</span>.<span style=
                 'color:red;'>end</span> != space"}
            WNS -- True  --> ML1
            ML1          --> WNS
            WNS -- False --> WLS
        WLS{"<span style='color:yellow;'>line</span>.<span style=
                 'color:red;'>end</span>-1 == space"}
            WLS -- True --> ML2
            ML2         --> WLS
        ML1["<span style='color:red;'>end</span> -= 1"]
        ML2["<span style='color:red;'>end</span> -= 1"]
        ELL["<span style='color:red;'>end</span> = <span style=
                 'color:yellow;'>line</span>.length"]
    end
    RTN([return])
            WLS -- False --> RTN
            ELL --> RTN
```
```
findBoundaries(columnIndex, positionsList, line)
    # Initial start and end positions
    SET start <- positionsList[columnIndex]
    IF columnIndex + 1 < positionsList.length
        SET end <- positionsList[columnIndex + 1]
    ELSE
        SET end <- line.length
    # Adjust start position
    IF start < line.length
        IF line[start] == " "
            WHILE start < end && line[start] == " "
                start += 1
        ELSE
            WHILE start > 0 && line[start - 1] != " "
                start -= 1
    ELSE
        start = line.length
    # Adjust end position
    IF end < line.length
        WHILE end > start && line[end] != " "
            end -= 1
        WHILE end > start && line[end - 1] == " "
            end -= 1
    ELSE:
        end = line.length
    RETURN start, end
```
[️⬆️](#initialize-table-methods)
---
##### `_addRjustColLabel`
```mermaid
flowchart LR
    STR([start]) -->
    PRC[update, add labels] -->
    END([end])
```
```
addRjustColLabel(label)
    IF label IS TYPE list, set
        UPDATE self.rightJustifiedColumns WITH label
    ELSE
        ADD label TO self.rightJustifiedColumns
```
[️⬆️](#initialize-table-methods)
---
#### Modify Table Methods
* [filterNonempty](#filternonempty)
* [filterStartswith](#filterstartswith)
* [resizeColumns](#resizecolumns)
```mermaid
graph TB
    TABL([**Table**])
        TABL --> FTNE
        TABL --> FTSW
        TABL -- widthLimit --> RSZC
    subgraph m [Modify Table Methods]
        FTNE(filterNonempty)
        FTSW(filterStartswith)
        RSZC(resizeColumns)
    end
```
[️⬆️](#method-groups)
---
##### `filterNonempty`
```mermaid
flowchart LR
    STR([Table])
        STR --> INP
    INP[\"<span style='color:cyan;'>dataset</span>
          <span style='color:magenta;'>key</span>"\]
        INP --> RCD
    RCD{"<span style='color:cyan;'>record</span>"}
        RCD -- True  --> KEY
        KEY -- False --> RCD
        ADD          --> RCD
        RCD -- False --> SET
    KEY{"<span style='color:magenta;'>key</span> in <span style=
             'color:cyan;'>record</span>"}
        KEY -- True --> ADD
    ADD["add <span style='color:cyan;'>record</span> to <span style=
             'color:yellow;'>newDataset</span>"]
    SET[/"<span style='color:yellow;'>newDataset</span>"/]
        SET --> END
    END([end])
```
```
filterNonempty(key)
    SET newDataset <- []
    FOR record IN self.dataset
        IF key NOT IN record
            APPEND record TO newDataset
    SET self.dataset <- newDataset
    SET self.recordsCount <- self.dataset.length
```
[️⬆️](#modify-table-methods)
---
##### `filterStartswith`
```mermaid
flowchart LR
    STR([Table])
        STR --> INP
    INP[\"<span style='color:cyan;'>dataset</span>
          <span style='color:magenta;'>key</span>
          <span style='color:yellow;'>prefix</span>"\]
        INP --> RCD
    RCD{"<span style='color:cyan;'>record</span>"}
        RCD -- True  --> KEY
        KEY -- False --> RCD
        ADD          --> RCD
        RCD -- False --> SET
    KEY{"<span style='color:magenta;'>key</span> starts with <span style=
             'color:yellow;'>prefix</span>"}
        KEY -- True --> ADD
    ADD["add <span style='color:cyan;'>record</span> to <span style=
             'color:yellow;'>newDataset</span>"]
    SET[/"<span style='color:yellow;'>newDataset</span>"/]
        SET --> END
    END([end])
```
```
filterStartswith(key, prefix)
    SET newDataset <- []
    FOR record IN self.dataset
        IF key STARTSWITH prefix
            APPEND record TO newDataset
    SET self.dataset <- newDataset
    SET self.recordsCount <- self.dataset.length
```
[️⬆️](#modify-table-methods)
---
##### `resizeColumns`
```mermaid
flowchart TB
    STR([Table])
        STR --> INP
    INP[\"<span style='color:cyan;'>tableWidth</span>
          <span style='color:magenta;'>widthLimit</span>
          <span style='color:yellow;'>columnWidths</span>"\]
        INP --> TRM
    TRM["trimLength = <span style='color:cyan;'>tableWidth</span> - <span 
             style='color:magenta;'>widthLimit</span>"]
        TRM --> WHL
    WHL{trimLength > 0}
        WHL -- True  --> WTH
        DEC          --> WHL
        WHL -- False --> END
    WTH["get key of <span style='color:yellow;'>columnWidths</span>.values.max"]
        WTH --> SET
    SET[/"<span style='color:yellow;'>columnWidths</span>.key -= 1
         <span style='color:cyan;'>tableWidth</span> -= 1"/]
        SET --> DEC
    DEC[trimLength -= 1]
    END([end])
```
```
resizeColumns(widthLimit)
    SET trimLength <- self.tableWidth - widthLimit
    WHILE trimLength > 0
        SET maxWidth <- 0
        FOR key, value IN self.columnWidths
            IF value > maxWidth
                SET widestColumn <- key
        self.columnWidth[widestColumn] -= 1
        self.tablewidth -= 1
        trimLength -= 1
```
[️⬆️](#modify-table-methods)
---
#### Display Table Methods
* [putTable](#puttable)
* [_numberRecords](#_numberrecords)
* [_calculateWidths](#_calculatewidths)
* [_addRjustColLabel](#_addrjustcollabel) (see Initialize Table Methods)
```mermaid
graph LR
    TABL([**Table**])
        TABL -- console
                isMenu  --> PTBL
    subgraph i [Initialize Table Methods]
        INIT(*init*)
    end
    subgraph d [Display Table Methods]
        PTBL(putTable)
            PTBL --> NUMR
            PTBL --> CALW
        NUMR(_numberRecords)
        CALW(_calculateWidths)
    end
    ARJC(_addRjustColLabel)
        INIT        --> ARJC
        NUMR -- No. --> ARJC
```
[️⬆️](#method-groups)
---
##### `putTable`
* [ConsoleTable](../console/console_table.py)
```mermaid
flowchart TB
    STR([Table])
        STR --> INP
    INP[\"<span style='color:cyan;'>isMenu</span>
          <span style='color:magenta;'>console</span>"\]
        INP --> IIM
    IIM{"<span style='color:cyan;'>isMenu</span>"}
        IIM -- True  --> NBR
        IIM -- False --> CWD
    NBR[[_numberRecords]]
        NBR --> CWD
    CWD[[_calculateWidths]]
        CWD --> CST
    CST[[ConsoleTable.init]]
        CST --> DIS
    DIS[["ConsoleTable.<span style='color:magenta;'>display</span>"]]
        DIS --> END
    END([end])
```
```
putTable(console, isMenu)
    IF isMenu
        CALL self.numberRecords
    CALL self.calculateWidths
    SET table <- ConsoleTable
    CALL table.display(console)
```
[️⬆️](#display-table-methods)
---
##### `_numberRecords`
```mermaid
flowchart TB
    STR([putTable])
        STR --> INP
    INP[\"<span style='color:cyan;'>dataset</span>"\]
        INP --> FOR
    FOR{"<span style='color:cyan;'>record</span>"}
        FOR -- True  --> SKV
        SKV          --> FOR
        FOR -- False --> URC
    SKV["set No.:<span style='color:cyan;'>index</span>+1"]
    URC["set <span style='color:magenta;'>updatedRecord</span>"]
        URC --> UDS
    UDS[/"<span style='color:magenta;'>updatedDataset</span>"/]
        UDS --> RJC
    RJC[[_addRjustColLabel]]
        RJC --> END
    END([end])
```
```
numberRecords()
    FOR index, record IN dataset
        SET key, value <- "#", index + 1
        SET updatedRecord <- key:value + record
        ADD updatedRecord <- newDataset
    CALL self.addRjustColLabel("#")
END
```
[️⬆️](#display-table-methods)
---
##### `_calculateWidths`
```mermaid
flowchart TB
    STR([putTable])
        STR --> INP
    INP[\"<span style='color:cyan;'>dataset</span>"\]
        INP --> KEY
    KEY{"<span style='color:cyan;'>key</span>"}
        KEY -- True  --> RCD
        KMX          --> KEY
        KEY -- False --> SCW
    RCD{"<span style='color:cyan;'>record</span>"}
        RCD -- True  --> RMX
        RMX          --> RCD
        RCD -- False --> KMX
    RMX["max >= <span style='color:cyan;'>record.key</span>.length"]
    KMX["max >= <span style='color:cyan;'>key</span>.length"]
    SCW["columnWidth = <span style='color:cyan;'>key</span>:max"]
        SCW --> ACW
    ACW[/columnWidths <br> tableWidth/]
        ACW --> END
    END([end])
```
```
calculateWidths()
    FOR key IN dataset.keys
        SET max <- 0
        FOR record IN dataset
            IF record[key].length > max
                max <- record[key].length
        IF key.length > max
            max <- key.length
    SET columnWidth <- key:value
    ADD columnWidth TO columnWidths
    SET tableWidth <- columnWidths.values.sum + 2 * (columnWidths.length - 1)
END
```
[️⬆️](#display-table-methods)
---
#### Getters
* [countRecors](#countrecords)
* [getColumnWidts](#getcolumnwidths)
* [getHeadings](#getheadings)
* [getRecord](#getrecord)
* [getRjustColumns](#getrjustcolumns)
* [getTableWidth](#gettablewidth)
* [getTitle](#gettitle)
```mermaid
graph LR
    TABL([**Table**])
        TABL --> g
        g    --> TABL
    subgraph g [Getters]
        CRCD(countRecords)
        GHDG(getHeadings)
        GCLW(getColumnWidths)
        GRCD(getRecord)
        GRJC(getRjustColumns)
        GTBW(getTableWidth)
        GTTL(getTitle)
    end
```
[️⬆️](#method-groups)
---
##### `countRecords`
```
countRecords()
    RETURN self.recordsCount
```
[️⬆️](#getters)
---
##### `getColumnWidths`
```
getColumnWidths()
    RETURN self.columnWidths
```
[️⬆️](#getters)
---
##### `getHeadings`
```
getHeadings()
    FOR key IN dataset.keys
        heading <- key:key
    ADD heading TO headings
    RETURN headings
```
[️⬆️](#getters)
---
##### `getRecord`
```
getRecord(index)
    IF index < 0 OR index >= self.dataset.length
        RAISE IndexError
    RETURN self.dataset[index]
```
[️⬆️](#getters)
---
##### `getRjustColumns`
```
getRjustColumns()
    RETURN self.rightJustifiedColumns
```
[️⬆️](#getters)
---
##### `getTableWidth`
```
getTableWidth()
    RETURN self.tableWidth
```
[️⬆️](#getters)
---
##### `getTitle`
```
getTitle()
    RETURN self.Title
```
[️⬆️](#getters)
---