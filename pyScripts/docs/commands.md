# Commands Module
* [listBlockDevices](#listblockdevices)
* [runBadblocks](#runbadblocks)
* [runCommand](#runcommand)
* [unmountDisk](#unmountdisk)
---
### `listBlockDevices`
```mermaid
flowchart
    classDef shape fill:#4682b4,stroke:#b97d4b,stroke-width:2px
    STRT([start]):::shape
        STRT --> ARGS
    ARGS[\"<span style='color:cyan;'>disk</span>
           <span style='color:magenta;'>columns</span>
           <span style='color:yellow;'>showDependents</span>"\]:::shape
        ARGS --> SPOD
    SPOD["<span style='color:cyan;'>path</span>
           <span style='color:magenta;'>output</span>
           <span style='color:yellow;'>deps</span>"]:::shape
        SPOD --> RCMD
    RCMD[[runCommand]]:::shape
        RCMD --> RTRN
    RTRN([result]):::shape
```
```
listBlockDevices(disk, columns, showDependents)
    IF disk
        SET path <- ""
    ELSE
        SET path <- "/dev/{disk}"
    IF columns
        SET columnString <- columns.join(,)
        SET output <- "--output {columnString}"
    ELSE
        SET output <- ""
    IF showDependents
        SET deps <- ""
    ELSE
        SET deps <- "--nodeps"
    RETURN runCommand("lsblk {deps} {output} {path}")
END
```
---
### `runBadblocks`
```mermaid
flowchart
    classDef shape fill:#4682b4,stroke:#b97d4b,stroke-width:2px
    STRT([start]):::shape
        STRT --> ARGS
    ARGS[\"<span style='color:cyan;'>disk</span>
           <span style='color:magenta;'>nonDestructive</span>
           <span style='color:yellow;'>captureOutput</span>"\]:::shape
        ARGS --> STMC
    STMC[\"<span style='color:magenta;'>mode</span>
           <span style='color:cyan;'>command</span>"\]:::shape
        STMC --> CAPT
    CAPT{"<span style='color:yellow;'>captureOutput</span>"}:::shape
        CAPT -- True  --> GETR
        CAPT -- False --> IGNR
    GETR[[runCommand]]:::shape
        GETR --> RTNR
    IGNR[[call runCommand]]:::shape
        IGNR --> RTNN
    RTNR([result]):::shape
    RTNN([None]):::shape
```
```
runBadblocks(disk, nonDestructive, captureOutput)
    IF nonDestructive
        SET mode <- "--non-destructive"
    ELSE
        SET mode <- "--write-mode"
    SET command <- "sudo badblocks {mode} --show-progress --verbose /dev/{disk}"
    IF captureOutput
        RETURN runCommand(command)
    runCommand(command, captureOutput)
    RETURN None
END
```
---
### `runCommand`
```mermaid
flowchart
    classDef shape fill:#4682b4,stroke:#b97d4b,stroke-width:2px
    STRT([start]):::shape
        STRT --> ARGS
    ARGS[\command
          captureOutput
          useShell\]:::shape
        ARGS --> SETR
    SETR[set result]:::shape
        SETR --> ERRR
    ERRR{error}:::shape
        ERRR -- True  --> RASE
        ERRR -- False --> CAPT
    RASE[/error/]:::shape
        RASE --> TEND
    CAPT{captureOutput}:::shape
        CAPT -- True  --> RTNR
        CAPT -- False --> RTNN
    RTNR([result]):::shape
    RTNN([None]):::shape
    TEND([end]):::shape
```
```
runCommand(command, captureOutput, useShell)
    IF captureOutput
        SET result <- subprocess.run(command, captureOutput, useShell)
    ELSE
        SET result <- subprocess.run(command, stdout, stderr, useShell)
    IF result.returncode != 0
        SET errorMessage <- result.stderr
        RAISE RuntimeError(errorMessage)
    IF captureOutput
        RETURN result.stdout
    ELSE
        RETURN None
END
```
---
### `unmountDisk`
```mermaid
flowchart
    classDef shape fill:#4682b4,stroke:#b97d4b,stroke-width:2px
    classDef alt fill:#b97d4b,stroke:#4682b4,stroke-width:2px
    STRT([start]):::shape
        STRT --> SOUT
    SOUT[output]:::shape
        SOUT --> STDP
    STDP(diskPaths):::alt
        STDP --> FLTR
    FLTR[filter]:::alt
        FLTR --> FRLP
    FRLP{diskPaths.record}:::shape
        FRLP -- True  --> SCMS
        RCMD          --> FRLP
        FRLP -- False --> TEND
    SCMS[cmdStr]:::shape
        SCMS --> RCMD
    RCMD[[call runCommand]]:::shape
    TEND([end]):::shape
```
```
unmountDisk(disk)
    SET output <- runCommand("lsblk --output PATH,MOUNTPOINT /dev/{disk}")
    SET diskPaths <- Table(output)
    diskPaths.filterNonempty("MOUNTPOINT")
    FOR i IN diskPaths.countRecords().range
        cmdStr <- "sudo umount --verbose {disk_paths.get_record(i)['PATH']}"
        runCommand(cmdStr, captureOutput=False)
END
```