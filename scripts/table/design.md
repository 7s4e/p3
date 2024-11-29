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
graph
    STRT([start])
        STRT -- tableData
                tableString
                title
                rjustColumns --> INIT
    subgraph i [Initialize Table Methods]
        style i fill:#4682b4,stroke:#b97d4b,stroke-width:2px,color:#0ff
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
    TABL([**Table**])
        INIT --> TABL
        TABL --> PTBL
    subgraph d [Display Table Methods]
        style d fill:#4682b4,stroke:#b97d4b,stroke-width:2px
        PTBL(putTable)
            PTBL --> NUMR
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
flowchart
    classDef shape fill:#4682b4,stroke:#b97d4b,stroke-width:2px
    STR([start]):::shape
        STR --> SRC
    SRC[\"<span style='color:cyan;'>tableSource</span>
          <span style='color:magenta;'>title</span>
          <span style='color:yellow;'>rjustLabel</span>"\]:::shape
        SRC --> DOS
    DOS{"<span style='color:cyan;'>data | string</span>"}:::shape
        DOS -- data  --> CAP
        DOS -- string --> RDT
    CAP[[capitalizeKeys]]:::shape
        CAP --> SET
    RDT[[readTable]]:::shape
        RDT --> SET
    SET[/"<span style='color:magenta;'>title</span>, rjustCols"/]:::shape
        SET --> HCL
    HCL{"<span style='color:yellow;'>has</span>"}:::shape
        HCL -- True  --> ACL
        HCL -- False --> END
    ACL[[addRjustColLabel]]:::shape
        ACL --> END
    END([Table]):::shape
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
    classDef shape fill:#4682b4,stroke:#b97d4b,stroke-width:2px
    STR([init]):::shape
        STR --> DTA
    DTA[\data\]:::shape
        DTA --> DTM
    DTM{datum}:::shape
        DTM -- True  --> CAP
        CAP          --> DTM
        DTM -- False --> SET
    CAP[set KEY:value]:::shape
    SET[/dataset, length/]:::shape
        SET --> END
    END([end]):::shape
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
flowchart
    classDef shape fill:#4682b4,stroke:#b97d4b,stroke-width:2px
    STR([init]):::shape
        STR --> TBS
    TBS[\string\]:::shape
        TBS --> SPT
    SPT["split <span style='color:cyan;'>lines</span>
         set <span style='color:magenta;'>headers</span>"]:::shape
        SPT --> FCP
    FCP[[findColumnPositions]]:::shape
        FCP --> LNS
    LNS{"<span style='color:cyan;'>line</span>"}:::shape
        LNS -- True  --> HDR
        SDS          --> LNS
        LNS -- False --> SLN
    HDR{"<span style='color:magenta;'>header</span>"}:::shape
        HDR -- True  --> GSL
        SHV          --> HDR
        HDR -- False --> SDS
    GSL[[getSlice]]:::shape
        GSL --> SHV
    SDS[/dataset/]:::shape
    SLN[/length/]:::shape
        SLN --> END
    SHV[set HEADER:value]:::shape
    END([end]):::shape
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
    classDef shape fill:#4682b4,stroke:#b97d4b,stroke-width:2px
    STR([readTable]):::shape
        STR --> INP
    INP[\"<span style='color:cyan;'>headerLine</span>
         <span style='color:magenta;'>keys</span>"\]:::shape
        INP --> KEY
    KEY{<span style='color:magenta;'>key</span>}:::shape
        KEY -- True  --> POS
        POS          --> KEY
        KEY -- False --> END
    POS["get <span style='color:cyan;'>position</span>
         append to positions"]:::shape
    END([return positions]):::shape
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
    classDef shape fill:#4682b4,stroke:#b97d4b,stroke-width:2px
    STR([readTable]):::shape
        STR --> FBD
    FBD[[findBoundaries]]:::shape
        FBD --> SET
    SET[set start, end]:::shape
        SET --> END
    END([return line.slice]):::shape
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
flowchart
    classDef shape fill:#4682b4,stroke:#b97d4b,stroke-width:2px
    STR([getSlice]):::shape
        STR --> ARG
    ARG[\"<span style='color:cyan;'>columnIndex</span>
          <span style='color:magenta;'>positionsList</span>
          <span style='color:yellow;'>line</span>"\]:::shape
        ARG --> INT
    INT[[initialize start, end]]:::shape
        INT --> AJS
    AJS[[adjust start]]:::shape
        AJS --> AJE
    AJE[[adjust end]]:::shape
        AJE --> END
    END(["return <span style='color:green;'>start</span>, <span style=
              'color:red;'>end</span>"]):::shape
```
###### Initialize Subgraph
```mermaid
flowchart
    classDef shape fill:#4682b4,stroke:#b97d4b,stroke-width:2px
    INP[\input\]:::shape
        INP --> SST
    subgraph init [Initialize start, end]
        SST["<span style='color:green;'>start</span> = <span style=
                 'color:magenta;'>positions</span>.<span style='color:cyan;'
                 >index</span>"]:::shape
            SST --> LST
        LST{"<span style='color:cyan;'>index</span> + 1 < <span style=
                 'color:magenta;'>positions</span>.length"}:::shape
            LST -- False --> SE1
            LST -- True  --> SE2
        SE1["<span style='color:red;'>end</span> = <span style=
                 'color:magenta;'>positions</span>.<span style='color:cyan;'
                 >index</span>+1"]:::shape
        SE2["<span style='color:red;'>end</span> = <span style=
                 'color:magenta;'>positions</span>.length"]:::shape
    end
    AJS[[adjust start]]:::shape
        SE1 --> AJS
        SE2 --> AJS
```
###### Start Subgraph
```mermaid
flowchart
    classDef shape fill:#4682b4,stroke:#b97d4b,stroke-width:2px
    INT[[initialize start, end]]:::shape
        INT --> SIL
    subgraph start [Adjust start]
        SIL{"<span style='color:green;'>start</span> < <span style=
                 'color:yellow;'>line</span>.length"}:::shape
            SIL -- True --> SIS
            SIL -- False --> SLL
        SIS{"<span style='color:yellow;'>line</span>.<span style=
                 'color:green;'>start</span> == space"}:::shape
            SIS -- True --> WIS
            SIS -- False --> WNS
        WIS{"<span style='color:green;'>start</span> < <span style=
                 'color:red;'>end</span> &&
             <span style='color:yellow;'>line</span>.<span style=
                 'color:green;'>start</span> == space"}:::shape
            WIS -- True --> MSR
            MSR         --> WIS
        WNS{"<span style='color:yellow;'>line</span>.<span style=
                 'color:green;'>start</span>-1 != space"}:::shape
            WNS -- True --> MSL
            MSL         --> WNS
        MSR["<span style='color:green;'>start</span> += 1"]:::shape
        MSL["<span style='color:green;'>start</span> -= 1"]:::shape
        SLL["<span style='color:green;'>start</span> = <span style=
                 'color:yellow;'>line</span>.length"]:::shape
    end
    AJE[[adjust end]]:::shape
            WIS -- False --> AJE
            WNS -- False --> AJE
            SLL          --> AJE
```
###### End Subgraph
```mermaid
flowchart
    classDef shape fill:#4682b4,stroke:#b97d4b,stroke-width:2px
    AJS[[adjust start]]:::shape
        AJS --> EIL
    subgraph end [Adjust end]
        EIL{"<span style='color:red;'>end</span> < <span style='color:yellow;'
                 >line</span>.length"}:::shape
            EIL -- True  --> WNS
            EIL -- False --> ELL
        WNS{"<span style='color:yellow;'>line</span>.<span style=
                 'color:red;'>end</span> != space"}:::shape
            WNS -- True  --> ML1
            ML1          --> WNS
            WNS -- False --> WLS
        WLS{"<span style='color:yellow;'>line</span>.<span style=
                 'color:red;'>end</span>-1 == space"}:::shape
            WLS -- True --> ML2
            ML2         --> WLS
        ML1["<span style='color:red;'>end</span> -= 1"]:::shape
        ML2["<span style='color:red;'>end</span> -= 1"]:::shape
        ELL["<span style='color:red;'>end</span> = <span style=
                 'color:yellow;'>line</span>.length"]:::shape
    end
    RTN([return]):::shape
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
    classDef shape fill:#4682b4,stroke:#b97d4b,stroke-width:2px
    STR([start]):::shape -->
    PRC[update, add labels]:::shape -->
    END([end]):::shape
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
graph
    TABL([**Table**])
        TABL --> FTNE
        TABL --> FTSW
        TABL --> PTBL
    subgraph m [Modify Table Methods]
        style m fill:#4682b4,stroke:#b97d4b,stroke-width:2px,color:#0ff
        FTNE(filterNonempty)
        FTSW(filterStartswith)
        RSZC(resizeColumns)
    end
    subgraph d [Display Table Methods]
        style d fill:#4682b4,stroke:#b97d4b,stroke-width:2px
        PTBL(puttable)
    end
    subgraph C [**ConsoleTable**]
        style C fill:#b97d4b,stroke:#4682b4,stroke-width:2px
        DPLY(display)
            PTBL -- Table --> DPLY
            DPLY --> SDMN
        SDMN(setDemensions)
            SDMN -- widthLimit --> RSZC
    end
```
[️⬆️](#method-groups)
---
##### `filterNonempty`
```mermaid
flowchart
    classDef shape fill:#4682b4,stroke:#b97d4b,stroke-width:2px
    STR([Table]):::shape
        STR --> INP
    INP[\"<span style='color:cyan;'>dataset</span>
          <span style='color:magenta;'>key</span>"\]:::shape
        INP --> RCD
    RCD{"<span style='color:cyan;'>record</span>"}:::shape
        RCD -- True  --> KEY
        KEY -- False --> RCD
        ADD          --> RCD
        RCD -- False --> SET
    KEY{"<span style='color:magenta;'>key</span> in <span style=
             'color:cyan;'>record</span>"}:::shape
        KEY -- True --> ADD
    ADD["add <span style='color:cyan;'>record</span> to <span style=
             'color:yellow;'>newDataset</span>"]:::shape
    SET[/"<span style='color:yellow;'>newDataset</span>"/]:::shape
        SET --> END
    END([end]):::shape
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
flowchart
    classDef shape fill:#4682b4,stroke:#b97d4b,stroke-width:2px
    STR([Table]):::shape
        STR --> INP
    INP[\"<span style='color:cyan;'>dataset</span>
          <span style='color:magenta;'>key</span>
          <span style='color:yellow;'>prefix</span>"\]:::shape
        INP --> RCD
    RCD{"<span style='color:cyan;'>record</span>"}:::shape
        RCD -- True  --> KEY
        KEY -- False --> RCD
        ADD          --> RCD
        RCD -- False --> SET
    KEY{"<span style='color:magenta;'>key</span> starts with <span style=
             'color:yellow;'>prefix</span>"}:::shape
        KEY -- True --> ADD
    ADD["add <span style='color:cyan;'>record</span> to <span style=
             'color:yellow;'>newDataset</span>"]:::shape
    SET[/"<span style='color:yellow;'>newDataset</span>"/]:::shape
        SET --> END
    END([end]):::shape
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
flowchart
    classDef shape fill:#4682b4,stroke:#b97d4b,stroke-width:2px
    STR([Table]):::shape
        STR --> INP
    INP[\"<span style='color:cyan;'>tableWidth</span>
          <span style='color:magenta;'>widthLimit</span>
          <span style='color:yellow;'>columnWidths</span>"\]:::shape
        INP --> TRM
    TRM["trimLength = <span style='color:cyan;'>tableWidth</span> - <span 
             style='color:magenta;'>widthLimit</span>"]:::shape
        TRM --> WHL
    WHL{trimLength > 0}:::shape
        WHL -- True  --> WTH
        DEC          --> WHL
        WHL -- False --> END
    WTH["get key of <span style='color:yellow;'>columnWidths</span>.values.max"]:::shape
        WTH --> SET
    SET[/"<span style='color:yellow;'>columnWidths</span>.key -= 1
         <span style='color:cyan;'>tableWidth</span> -= 1"/]:::shape
        SET --> DEC
    DEC[trimLength -= 1]:::shape
    END([end]):::shape
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
        style i fill:#4682b4,stroke:#b97d4b,stroke-width:2px
        INIT(*init*)
    end
    subgraph d [Display Table Methods]
        style d fill:#4682b4,stroke:#b97d4b,stroke-width:2px,color:#0ff
        PTBL(putTable)
            PTBL --> NUMR
            PTBL --> CALW
        NUMR(_numberRecords)
        CALW(_calculateWidths)
    end
    subgraph C [**ConsoleTable**]
        style C fill:#b97d4b,stroke:#4682b4,stroke-width:2px
        DPLY(display)
            PTBL -- Table --> DPLY
            DPLY --> SDMN
        SDMN(setDemensions)
    end
    subgraph m [Modify Table Methods]
        style m fill:#4682b4,stroke:#b97d4b,stroke-width:2px
        RSZC(resizeColumns)
            SDMN -- widthLimit --> RSZC
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
flowchart
    classDef shape fill:#4682b4,stroke:#b97d4b,stroke-width:2px
    STR([Table]):::shape
        STR --> INP
    INP[\"<span style='color:cyan;'>isMenu</span>
          <span style='color:magenta;'>console</span>"\]:::shape
        INP --> IIM
    IIM{"<span style='color:cyan;'>isMenu</span>"}:::shape
        IIM -- True  --> NBR
        IIM -- False --> CWD
    NBR[[_numberRecords]]:::shape
        NBR --> CWD
    CWD[[_calculateWidths]]:::shape
        CWD --> CST
    CST[[ConsoleTable.init]]:::shape
        CST --> DIS
    DIS[["ConsoleTable.<span style='color:magenta;'>display</span>"]]:::shape
        DIS --> END
    END([end]):::shape
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
flowchart
    classDef shape fill:#4682b4,stroke:#b97d4b,stroke-width:2px
    STR([putTable]):::shape
        STR --> INP
    INP[\"<span style='color:cyan;'>dataset</span>"\]:::shape
        INP --> FOR
    FOR{"<span style='color:cyan;'>record</span>"}:::shape
        FOR -- True  --> SKV
        SKV          --> FOR
        FOR -- False --> URC
    SKV["set No.:<span style='color:cyan;'>index</span>+1"]:::shape
    URC["set <span style='color:magenta;'>updatedRecord</span>"]:::shape
        URC --> UDS
    UDS[/"<span style='color:magenta;'>updatedDataset</span>"/]:::shape
        UDS --> RJC
    RJC[[_addRjustColLabel]]:::shape
        RJC --> END
    END([end]):::shape
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
flowchart
    classDef shape fill:#4682b4,stroke:#b97d4b,stroke-width:2px
    STR([putTable]):::shape
        STR --> INP
    INP[\"<span style='color:cyan;'>dataset</span>"\]:::shape
        INP --> KEY
    KEY{"<span style='color:cyan;'>key</span>"}:::shape
        KEY -- True  --> RCD
        KMX          --> KEY
        KEY -- False --> SCW
    RCD{"<span style='color:cyan;'>record</span>"}:::shape
        RCD -- True  --> RMX
        RMX          --> RCD
        RCD -- False --> KMX
    RMX["max >= <span style='color:cyan;'>record.key</span>.length"]:::shape
    KMX["max >= <span style='color:cyan;'>key</span>.length"]:::shape
    SCW["columnWidth = <span style='color:cyan;'>key</span>:max"]:::shape
        SCW --> ACW
    ACW[/columnWidths <br> tableWidth/]:::shape
        ACW --> END
    END([end]):::shape
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
