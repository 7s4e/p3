# getDisk Script
```mermaid
flowchart LR
    classDef complete color:#0f0,stroke:#0f0,fill:#555
    classDef working color:#ff0,stroke:#ff0,fill:#555
    classDef library color:#0ff,stroke:#0ff,fill:#555
    IF([start])
        IF --> TRM
        IF --> MAIN
    TRM(blessed.Terminal):::library
    MAIN[main]
        MAIN --> CON
        MAIN --> GD
    CON(console):::complete
    GD[getDisk]:::working
        GD --> INSP
        GD --> GDS
        GD --> CCP
        GD --> SD
    INSP(inspect):::library
    GDS[getDisks]:::complete
        GDS --> CMD
        GDS --> TBL
    CCP(ConsolePrompt):::complete
    SD[selectDisk]:::working
        SD --> MNU
    CMD(commands):::complete
    TBL(Table):::complete
    MNU(Menu):::working
```
* [commands](../commands/design.md)
* [console](../console/design.md)
* [Table](../table/design.md)