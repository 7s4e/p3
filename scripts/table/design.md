# Table Module
## `Table`
* [\_\_init__](#__init__)
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
    END([end])
```
[️⬆️](#table)
---
### `_readTable`
[️⬆️](#table)
