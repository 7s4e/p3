# Menu Module
## `Menu`
| Constructor | Public Methods | Dependencies |
| --- | --- | --- |
| [\_\_init__](#__init__) | [setPrompt](#setprompt) | [Table](table.md) |
| | [run](#run) | [ConsolePrompt](console.md) |
| | [getSelection](#getselection) | |

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
        MNYU            --> RNMN
    SPMT(setPrompt):::method
        SPMT -- prompt --> CPMT
    RNMN(run):::method
        RNMN -- isMenu --> PTBL
        RNMN           --> CLLP
        RNMN -- index  --> GREC
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
```mermaid
flowchart LR
    classDef this fill:#4682b4,stroke:#b97d4b,stroke-width:2px
    classDef that fill:#b97d4b,stroke:#4682b4,stroke-width:2px
    MNYU([*init*
          *Menu*]):::this
        MNYU --> GPCT
    GPCT[\prompt
          count\]
        GPCT --> IFPT
    IFPT{prompt}
        IFPT -- True  --> EKIV
        IFPT -- False --> SPMT
    SPMT[prompt]
        SPMT --> EKIV
    EKIV[expectKeystroke
         integerValidation]
        EKIV --> CONP
    CONP[[ConsolePrompt]]:::that
        CONP --> SLFP
    SLFP[/prompt/]
        SLFP --> THEE
    THEE([end])
```
```
setPrompt(prompt)
    IF NOT prompt
        SET prompt
    SET expectKeystroke <- self.count < 10
    SET integerValidation <- (1, self.count)
    SET self.prompt <- ConsolePrompt(prompt, expectKeystroke, 
                                     validateInteger=True, integerValidation)
END
```
[️⬆️](#menu)
---
### `run`
```mermaid
flowchart LR
    classDef this fill:#4682b4,stroke:#b97d4b,stroke-width:2px
    classDef that fill:#b97d4b,stroke:#4682b4,stroke-width:2px
    MNYU([**Menu**]):::this
        MNYU --> PTBL
    PTBL[[putTable]]:::that
        PTBL --> CPMT
    CPMT[[call]]:::that
        CPMT --> SIDX
    SIDX[index]
        SIDX --> GREC
    GREC[[getRecord]]:::that
        GREC --> SLCT
    SLCT[/selection/]
        SLCT --> THEE
    THEE([end])
```
```
run(console)
    self.options.putTable(isMenu=True)
    SET index <- self.prompt.call() - 1
    SET self.selection <- self.options.getRecord(index)
END
```
[️⬆️](#menu)
---
### `getSelection`
```mermaid
flowchart LR
    classDef this fill:#4682b4,stroke:#b97d4b,stroke-width:2px
    MNYU([**Menu**]):::this
        MNYU --> GSLC
    GSLC[\key
          selection\]
        GSLC --> RSLC
    RSLC([selection.key])
```
```
getSelection(key)
    RETURN self.selection[key]
END
```
[️⬆️](#menu)
---
