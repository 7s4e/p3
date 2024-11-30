# Menu Module
## `Menu`
* [\_\_init__](#__init__)
* [setPrompt](#setprompt)
* [run](#run)
* [getSelection](#getselection)
* [Table](../table/design.md)
* [ConsolePrompt](../console/design.md)
```mermaid
graph
    style MNYU fill:#4682b4,stroke:#b97d4b,stroke-width:2px,color:#0ff
    style T fill:#b97d4b,stroke:#4682b4,stroke-width:2px
    style CP fill:#b97d4b,stroke:#4682b4,stroke-width:2px
    classDef method fill:#4682b4,stroke:#b97d4b,stroke-width:2px
    STRT([start])
        STRT -- options
                title
                prompt  --> INIT
    INIT(*init*):::method
        INIT -- options
                title   --> TBLE
        INIT            --> CREC
        INIT -- prompt  --> SPMT
        INIT            --> MNYU
    MNYU([**Menu**])
        MNYU -- prompt  --> SPMT
        MNYU -- key     --> GSLC
        MNYU -- console --> RNMN
    SPMT(setPrompt):::method
        SPMT -- prompt --> CPMT
    RNMN(run):::method
        RNMN -- console
                isMenu  --> PTBL
        RNMN -- console --> CLLP
        RNMN -- index   --> GREC
    GSLC(getSelection):::method
    subgraph T [**Table**]
        TBLE(Table)
        CREC(countRecords)
        PTBL(putTable)
        GREC(getRecord)
    end
    subgraph CP [**ConsolePrompt**]
        CPMT(ConsolePrompt)
        CLLP(call)
    end
```
---
### `__init__`
```mermaid
flowchart 
    classDef this fill:#4682b4,stroke:#b97d4b,stroke-width:2px
    classDef that fill:#b97d4b,stroke:#4682b4,stroke-width:2px
    STRT([start])
        STRT --> ROTP
    ROTP[\options
          title
          prompt\]
        ROTP --> OTYP
    OTYP{options.type}
        OTYP -- Table --> SOPT
        OTYP -- list  --> FOPT
    SOPT[/options/]
        SOPT --> CREC
    FOPT{option}
        FOPT -- True  --> SDTA
        SDTA          --> FOPT
        FOPT -- False --> CTBL
    SDTA[OPTION: option]
    CTBL[[Table]]:::that
        CTBL --> SOPT
    CREC[[countRecords]]:::that
        CREC --> SCNT
    SCNT[/count/]
        SCNT --> SPMT
    SPMT[[setPrompt]]:::this
        SPMT --> THEE
    THEE([**Menu**]):::this
```
```
init(options, title, prompt)
    IF options.type IS Table
        SET self.options <- options
    ELSE
        FOR option IN options
            SET data["OPTION"] <- option
        SET self.options <- Table(title, data)
    SET self.count <- self.options.countRecords()
    self.setPrompt(prompt)
END
```
[️⬆️](#menu)
---
### `setPrompt`
```
content
```
[️⬆️](#menu)
---
### `run`
```
content
```
[️⬆️](#menu)
---
### `getSelection`
```
content
```
[️⬆️](#menu)
---
