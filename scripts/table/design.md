# Table Module
## `Table`
### Initialize Table
* [\_\_init__](#__init__)
* [_capitalizeKeys](#_capitalizekeys)
* [_readTable](#_readtable)
* [_findColumnPositions](#_findcolumnpositions)
* [_getSlice](#_getslice)
* [_findBoundaries](#_findboundaries)
* [_addRjustColLabel](#_addrjustcollabel)
### Modify Table
* [filterNonempty](#filternonempty)
* [filterStartswith](#filterstartswith)
* [resizeColumns](#resizecolumns)
### Display Table
* [putTable](#puttable)
* [_numberRecords](#_numberrecords)
* [_calculateWidths](#_calculatewidths)
### Getters
* [getRecord](#getrecord)
* [getTitle](#gettitle)
* [getHeadings](#getheadings)
* [getTableWidth](#gettablewidth)
* [getRjustColumns](#getrjustcolumns)
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
        CR -- recordsCount --> MAIN
        GH -- headings --> MAIN
        GCW -- columnWidths --> MAIN
        GRCD -- record --> MAIN
        GRJC -- rightJustifiedColumns --> MAIN
        GTW -- tableWidth --> MAIN
        GTTL -- title --> MAIN
    subgraph inititialize [Initialize Table]
        INIT(*init*)
            INIT -- tableData --> CK
            INIT -- tableString --> RT
        CK(_capitalizeKeys)
        RT(_readTable)
            RT -- headerLine
                  keys
               --> FCP
            RT -- columnIndex
                  positionsList
                  line
               --> GS
        FCP(_findColumnPositions)
            FCP -- columnPositions --> RT
        GS(_getSlice)
            GS -- columnIndex
                  positionsList
                  line
               --> FB
            GS -- slice --> RT
        FB(_findBoundaries)
            FB -- boundaries --> GS
    end
    subgraph modify [Modify Table]
        FNE(filterNonempty)
        FSW(filterStartswith)
        RC(resizeColumns)
    end
    subgraph display [Display Table]
        PT(putTable)
            PT --> NR
            PT --> CW
        NR(_numberRecords)
        CW(_calculateWidths)
    end
    subgraph getters [Getters]
        CR(countRecords)
        GH(getHeadings)
        GCW(getColumnWidths)
        GRCD(getRecord)
        GRJC(getRjustColumns)
        GTW(getTableWidth)
        GTTL(getTitle)
    end
    ARJCL(_addRjustColLabel)
        INIT -- rjustColumns --> ARJCL
        NR -- No. --> ARJCL
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
        STRWHL2{while left of startPosition is not space}
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
        ENDWHL2{while left of endPosition is space}
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
### `_addRjustColLabel`
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
[️⬆️](#table)
---
### `filterNonempty`
```mermaid
flowchart LR
    STR([start])
        STR --> RCD
    RCD{record in existing dataset}
        RCD -- True --> KEY
        RCD -- False --> SET
    KEY{key in record}
        KEY -- True --> ADD
        KEY -- False --> RCD
    ADD[add record to new dataset]
        ADD --> RCD
    SET[replace exisiting dataset with new]
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
[️⬆️](#table)
---
### `filterStartswith`
```mermaid
flowchart LR
    STR([start])
        STR --> RCD
    RCD{record in existing dataset}
        RCD -- True --> KEY
        RCD -- False --> SET
    KEY{key start with prefix}
        KEY -- True --> ADD
        KEY -- False --> RCD
    ADD[add record to new dataset]
        ADD --> RCD
    SET[replace exisiting dataset with new]
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
[️⬆️](#table)
---
### `resizeColumns`
```
    def resize_columns(self, width_limit: int) -> None:
        """Resize column widths to fit within the specified width limit.
        Args:
            width_limit (int): The maximum allowable width for the 
                table.
        """
        # Calculate the total width to trim
        trim_length = self._table_width - width_limit
        # Continue trimming column widths until the trim length is 
        # satisfied
        while trim_length > 0:
            # Find the column with the maximum width
            widest_column = max(self._column_widths, 
                                key=self._column_widths.get)
            # Reduce the width of the widest column
            self._column_widths[widest_column] -= 1
        
            # Update the total width to be trimmed
            trim_length -= 1
            # Update the current table width
            self._table_width -= 1
```
[️⬆️](#table)
---
### `putTable`
```
    def put_table(self, 
                  console: Terminal,
                  is_menu: bool = False) -> None:
        """Format and display a table with the given dataset.
        Args:
            console (Terminal): The Terminal object used for displaying 
                the table.
            is_menu (bool, optional): Whether the table is being 
                displayed as a menu. Defaults to False.
        """
        if is_menu:
            self._number_records()
        self._calculate_widths()
        # Create an instance of Console_Table with the current 
        # instance's data
        table = Console_Table(self)
        # Display the table using the provided Terminal object
        table.display(console)
```
[️⬆️](#table)
---
### `_numberRecords`
```
    def _number_records(self) -> None:
        """Add a numerical index to each record in the dataset and 
            update column labels.
        This method adds a numerical index to each record in the 
        dataset, with the index starting at 1. It also updates the 
        column labels to ensure proper right-justification for the index 
        column.
        """
        # Add a numerical index to each record, starting from 1
        self._dataset = [{"#": i + 1, **record} 
                         for i, record in enumerate(self._dataset)]
        # Update the column label for the index to ensure right-
        # justification
        self._add_rjust_col_label("#")
```
[️⬆️](#table)
---
### `_calculateWidths`
```
    def _calculate_widths(self) -> None:
        """Calculate the width of each column and the total table width 
            based on the dataset.
        Updates:
            Updates self._column_widths with the width of each column.
            Updates self._table_width with the total width of the table 
                including column separators.
        """
        self._column_widths = {
            key: max(len(key), 
                     max(len(str(record[key])) for record in self._dataset))
            for key in self._dataset[0].keys()
        }
        self._table_width = (sum(self._column_widths.values()) 
                             + 2 * (len(self._column_widths) - 1))
```
[️⬆️](#table)
---
### `getRecord`
```
    def get_record(self, index: int) -> dict[str, str]:
        """Retrieve a specific record from the dataset.
        Args:
            index (int): The index of the record to retrieve.
        Returns:
            dict[str, str]: The record at the specified index.
    
        Raises:
            IndexError: If the index is out of range of the dataset.
        """
        if index < 0 or index >= len(self._dataset):
            raise IndexError("Index out of range.")
        return self._dataset[index]
```
[️⬆️](#table)
---
### `getTitle`
```
    def get_title(self) -> str:
        """Return the title of the table.
        Returns:
            str: The title of the table.
        """
        return self._title
```
[️⬆️](#table)
---
### `getHeadings`
```
    def get_headings(self) -> dict[str, str]:
        """Return a dictionary of column headings where each key is 
            mapped to itself.
        Returns:
            dict[str, str]: A dictionary with column names as both keys 
                and values.
        """
        return {key: key for key in self._dataset[0].keys()}
```
[️⬆️](#table)
---
### `getTableWidth`
```
    def get_table_width(self) -> int:
        """Return the width of the table.
        Returns:
            int: The width of the table.
        """
        return self._table_width
```
[️⬆️](#table)
---
### `getRjustColumns`
```
    def get_rjust_columns(self) -> set[str]:
        """Return a set of column names that are right-justified.
        Returns:
            set[str]: A set of column names that are right-justified.
        """
        return self._right_justified_columns
```    def filter_nonempty(self, key: str) -> None:
        """Filter records to include only those where the value for the 
            specified key is non-empty.
        Args:
            key (str): The key in the records to check for non-empty 
                values.
        Updates:
            Filters self._dataset in place to include only records where 
            the value for the specified key is non-empty. Updates 
            self._records_count to reflect the new number of records.
        """
        self._dataset = [record for record in self._dataset 
                         if record.get(key.upper(), '').strip()]
        self._records_count = len(self._dataset)

[️⬆️](#table)
---
### `getColumnWidths`
```
    def get_column_widths(self) -> dict[str, int]:
        """Return a dictionary of column widths.
        Returns:
            dict[str, int]: A dictionary with column names as keys and 
                their widths as values.
        """
        return self._column_widths
```
### `countRecords`
```
    def count_records(self) -> int:
        """Return the number of records in the dataset.

        Returns:
            int: The count of records.
        """
        return self._records_count
```