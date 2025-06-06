# getBonds Script
## Structure Charts
### Overview
```mermaid
flowchart LR
    classDef complete color:#0f0,stroke:#0f0,fill:#555
    classDef working color:#ff0,stroke:#ff0,fill:#555
    classDef library color:#0ff,stroke:#0ff,fill:#555

    %% Structure
    BEG([start])
        BEG --> MAIN
    MAIN[main]
        MAIN --> CON
        MAIN --> FB
    FB[findBonds]
        FB --> PUTY
        FB --> PREP
        FB --> EB
        FB --> PUT
    PREP[prepareData]
    EB[evaluateBonds]
        EB --> SR
    SR[setReturns]
    PUT[putData]
        PUT --> FR
        PUT --> PANDAS
    FR[filterReturns]

    %% Modules
    CON(Console):::complete
    PUTY(pandaUtilities):::working
    PANDAS(pandas):::library
```
#### `prepareData()`
```mermaid
flowchart LR
    classDef complete color:#0f0,stroke:#0f0,fill:#555
    classDef working color:#ff0,stroke:#ff0,fill:#555
    classDef library color:#0ff,stroke:#0ff,fill:#555

    %% Structure
    PREP[prepareData]
        PREP --> RF
        PREP --> COMB
        PREP --> FF
        PREP --> MD
        PREP --> FC
    RF[readFiles]
        RF --> UTLY
        RF --> PUTY
    COMB[combineData]
        COMB --> PDFS
        COMB --> SDFS
        COMB --> PANDAS
        COMB --> PDF
    PDFS[processDataFrames]
        PDFS --> PUTY
    SDFS[sourceDataFrames]
    PDF[processDataFrame]
        PDF --> PUTY
    FF[filterFrequency]
    MD[modifyData]
        MD --> SFM
        MD --> SCS
    SFM[setFrequencyMap]
    SCS[setCreditScore]
        SCS --> PANDAS
    FC[filterCredit]

    %% Modules
    PUTY(pandaUtilities):::working
    UTLY(utilities):::working
    PANDAS(pandas):::library
```
#### `setReturns()`
```mermaid
flowchart LR
    classDef complete color:#0f0,stroke:#0f0,fill:#555
    classDef working color:#ff0,stroke:#ff0,fill:#555
    classDef library color:#0ff,stroke:#0ff,fill:#555

    %% Structure
    SR[setReturns]
        SR --> ITRTLS
        SR --> LCFD
        SR --> CR
        SR --> MINN
        SR --> RP
    LCFD[listCashFlowDates]
        LCFD --> CLCTS
        LCFD --> PUTY
    CR[computeReturn]
        CR --> LCFA
        CR --> PANDAS
        CR --> CXIRR
    LCFA[listCashFlowAmounts]
        LCFA --> GMTR
        LCFA --> GCGR
        LCFA --> CAI
    GMTR[getMarginalTaxRate]
        GMTR --> PANDAS
    GCGR[getCapitalGainsRate]
        GCGR --> PUTY
    CAI[computeAccruedInterests]
    CXIRR[computeXIRR]
        CXIRR --> NPV
    NPV[npv]
    MINN[minIfNotNA]
    RP[roundPercentage]

    %% Modules
    ITRTLS(itertools):::library
    CLCTS(collections):::library
    PUTY(pandaUtilities):::working
    PANDAS(pandas):::library
```
## Module and Classes
* [commands](commands.md)
* [Console](console.md#console)
* [Console](console.md#consoleprompt)
* [Console](console.md#consoletable)
* [Menu](menu.md)
* [Table](table.md)
