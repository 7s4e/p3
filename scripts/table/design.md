# Table Module
## `Table`
* [\_\_init__](#__init__)
* [_capitalizeKeys](#_capitalizekeys)
* [_readTable](#_readtable)
* [_findColumnPositions](#_findcolumnpositions)
* [_getSlice](#_getslice)
* [_findBoundaries](#_findboundaries)
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
```mermaid
flowchart TB
    STR([start])
        STR --> SETSTR
    subgraph init [Initialize start, end]
        SETSTR[set current column as startPosition]
            SETSTR --> LSTCOL
        LSTCOL{last column}
            LSTCOL -- False --> SETEND1
            LSTCOL -- True --> SETEND2
    end
        SETEND1[set next column as endPosition]
            SETEND1 --> STRINLINE
        SETEND2[set line length as endPosition]
            SETEND2 --> STRINLINE
    subgraph start [Adjust start]
        STRINLINE{startPosition < line length}
            STRINLINE -- True --> STRISSPCE
            STRINLINE -- False --> RESETSTR
        STRISSPCE{startPosition is space}
            STRISSPCE -- True --> STRWHL1
            STRISSPCE -- False --> STRWHL2
        MOVSTRRGT[move startPosition right]
            MOVSTRRGT --> STRWHL1
        MOVSTRLFT[move startPosition left]
            MOVSTRLFT --> STRWHL2
    end
        STRWHL1{while startPosition < endPosition & is space}
            STRWHL1 -- True --> MOVSTRRGT
            STRWHL1 -- False --> ENDINLINE
        STRWHL2{while startPosition - 1 is not space}
            STRWHL2 -- True --> MOVSTRLFT
            STRWHL2 -- False --> ENDINLINE
        RESETSTR[reset startPosition as line length]
            RESETSTR --> ENDINLINE
    subgraph end [Adjust end]
        ENDINLINE{endPosition < line length}
            ENDINLINE -- True --> ENDWHL1
            ENDINLINE -- False --> RESETEND
        ENDWHL1{while endPosition is not space}
            ENDWHL1 -- True --> MOVENDLFT1
            ENDWHL1 -- False --> ENDWHL2
        MOVENDLFT1[move endPosition left]
            MOVENDLFT1 --> ENDWHL1
        MOVENDLFT2[move endPosition left]
            MOVENDLFT2 --> ENDWHL2
    end
        ENDWHL2{while endPosition - 1 is space}
            ENDWHL2 -- True --> MOVENDLFT2
            ENDWHL2 -- False --> RTN
        RESETEND[reset endPosition as line length]
            RESETEND --> RTN
    RTN[return startPosition, endPosition]
        RTN --> END
    END([end])
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
[️⬆️](#table)
---
