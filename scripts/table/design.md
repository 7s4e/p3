# Table Module
## `Table`
* [\_\_init__](#__init__)
* [_capitalizeKeys](#_capitalizekeys)
* [_readTable](#_readtable)
* [_findColumnPositions](#_findcolumnpositions)
* [_getSlice](#_getslice)
```mermaid
graph TB
    MAIN([**Table**])
        MAIN -- tableData
                tableString
                title
                rjustColumns
             --> INIT
        MAIN --> FNE
        MAIN --> FSW
        MAIN -- index --> GRCD
        MAIN -- console
                isMenu
             --> PT
        MAIN -- widthLimit --> RC
    INIT(*init*)
        INIT -- tableData --> CK
        INIT -- tableString --> RT
        INIT -- rjustColumns --> ARJCL
    ARJCL(_addRjustColLabel)
    CK(_capitalizeKeys)
    CR(countRecords)
        CR -- recordsCount --> MAIN
    CW(_calculateWidths)
    FB(_findBoundaries)
        FB -- boundaries --> GS
    FCP(_findColumnPositions)
        FCP -- columnPositions --> RT
    FNE(filterNonempty)
    FSW(filterStartswith)
    GH(getHeadings)
        GH -- headings --> MAIN
    GCW(getColumnWidths)
        GCW -- columnWidths --> MAIN
    GRCD(getRecord)
        GRCD -- record --> MAIN
    GRJC(getRjustColumns)
        GRJC -- rightJustifiedColumns --> MAIN
    GS(_getSlice)
        GS -- columnIndex
              positionsList
              line
           --> FB
        GS -- slice --> RT
    GTW(getTableWidth)
        GTW -- tableWidth --> MAIN
    GTTL(getTitle)
        GTTL -- title --> MAIN
    NR(_numberRecords)
        NR --> ARJCL
    PT(putTable)
        PT --> NR
        PT --> CW
    RC(resizeColumns)
    RT(_readTable)
        RT -- headerLine
              keys
           --> FCP
        RT -- columnIndex
              positionsList
              line
           --> GS
```
[️⬆️](#table-module)
---
### `__init__`
```mermaid
flowchart LR
    STR([start])
        STR --> TS
    TS{tableSource}
        TS -- data --> CK
        TS -- string --> RT
    CK[call capitalizeKeys]
        CK --> SET
    RT[call readTable]
        RT --> SET
    SET[set title, rjustCols]
        SET --> END
    END([end])
```
```
init(tableData, tableString, title, rjustColumns)
    IF (tableData IS None) == (tableString IS None)
        RAISE ValueError
    IF tableData
        CALL capitalizeKeys
    ELSE
        CALL readTable
    SET title
    SET rjustColumns
END
```
[️⬆️](#table)
---
### `_capitalizeKeys`
```mermaid
flowchart LR
    STR([start])
        STR --> DATA
    DATA{datum in data}
        DATA -- True --> CAP
        DATA -- False --> SET
    CAP[set KEY:value]
        CAP --> DATA
    SET[set dataset, length]
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
[️⬆️](#table)
---
### `_readTable`
```mermaid
flowchart LR
    STR([start])
        STR --> SPLTSET
    SPLTSET[split lines <br> set headers]
        SPLTSET --> FCP
    FCP[call findColumnPositions]
        FCP --> LNS
    LNS{line in lines}
        LNS -- True --> HDR
        LNS --> SETLN
    HDR{header in headers}
        HDR -- True --> GS
        HDR -- False --> SETDS
    GS[call getSlice]
        GS --> SETKV
    SETKV[set HEADER:value]
        SETKV --> HDR
    SETDS[set dataset]
        SETDS --> LNS
    SETLN[set length]
        SETLN --> END
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
[️⬆️](#table)
---
### `_findColumnPositions`
```mermaid
flowchart LR
    STR([start])
        STR --> KEY
    KEY{key in keys}
        KEY -- True --> POS
        KEY -- False --> RTN
    POS[set position <br> append to positions]
        POS --> KEY
    RTN[return positions]
        RTN --> END
    END([end])
```
```
findColumnPositions(headerLine, keys)
    SET positions <- []
    FOR key IN keys
        SET position <- headerLine.index OF key
        APPEND position TO positions
    RETURN positions
```
[️⬆️](#table)
---
### `_getSlice`
```mermaid
flowchart LR
    STR([start])
        STR --> PRCS
    PRCS[call findBoundaries <br> set start, end <br> return line.slice]
        PRCS --> END
    END([end])
```
```
getSlice(columnIndex, positionsList, line)
    SET start, end <- findBoundaries(columnIndex, positionsList, line)
    RETURN line[start:end]
```
[️⬆️](#table)
---
### `_findBoundaries`
[️⬆️](#table)
---
