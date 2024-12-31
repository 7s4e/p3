# getDisk Script
## Structure Chart
```mermaid
flowchart
    classDef complete color:#0f0,stroke:#0f0,fill:#555
    classDef working color:#ff0,stroke:#ff0,fill:#555
    classDef library color:#0ff,stroke:#0ff,fill:#555

    %% Structure
    IF([start])
        IF --> TRM
        IF --> MAIN
    MAIN[main]
        MAIN --> CON
        MAIN --> GD
    GD[getDisk]
        GD --> CON
        GD --> INSP
        GD --> GDS
        GD --> CCP
        GD --> SD
        GD --> CD
        GD --> CMD
    GDS[getDisks]
        GDS --> CMD
        GDS --> TBL
    SD[selectDisk]
        SD --> MNU
    CD[confirmDisk]
        CD --> CMD
        CD --> TBL
        CD --> CCP

    %% Modules
    TRM(blessed.Terminal):::library
    INSP(inspect):::library
    CMD(commands):::complete
    CON(Console):::complete
    CCP(ConsolePrompt):::complete
    CCT(ConsoleTable):::complete
    TBL(Table):::complete
        TBL --> CCT
    MNU(Menu):::complete
```
## Module and Classes
* [commands](commands.md)
* [Console](console.md#console)
* [Console](console.md#consoleprompt)
* [Console](console.md#consoletable)
* [Menu](menu.md)
* [Table](table.md)
