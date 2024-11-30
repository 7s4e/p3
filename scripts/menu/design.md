# Menu Module
## `Menu`
### Method Groups
* [Initialize Table Methods](#initialize-table-methods)
#### Initialize Table Methods
* [\_\_init__](#__init__)
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
    end
    TABL([**Table**])
        INIT --> TABL
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
```
```
init(tableData, tableString, title, rjustColLabel)
END
```
[️⬆️](#initialize-table-methods)
---
