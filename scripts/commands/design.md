# Commands Module
* [listBlockDevices](#listblockdevices)
* [runBadblocks](#runbadblocks)
* [runCommand](#runcommand)
* [unmountDisk](#unmountdisk)
---
### `listBlockDevices`
```mermaid
flowchart LR
    STR([start])
        STR --> PRCS
    PRCS[set path, output, deps]
        PRCS --> RTN
    RTN[return runCommand]
        RTN --> END
    END([end])
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
flowchart LR
    STR([start])
        STR --> PRCS
    PRCS[set mode, command]
        PRCS --> CAPT
    CAPT{captureOutput}
        CAPT -- True --> RTNC
        CAPT -- False --> CALL
    RTNC[return runCommand]
        RTNC --> END
    CALL[call runCommand]
        CALL --> RTNN
    RTNN[return None]
        RTNN --> END
    END([end])
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
flowchart LR
    STR([start])
        STR --> PRCS
    PRCS[set result]
        PRCS --> ERR
    ERR{error}
        ERR -- True --> RSE
        ERR -- False --> CAPT
    RSE[raise error]
        RSE --> END
    CAPT{captureOutput}
        CAPT -- True --> RTNR
        CAPT -- False --> RTNN
    RTNR[return result]
        RTNR --> END
    RTNN[return None]
        RTNN --> END
    END([end])
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
flowchart LR
    STR([start])
        STR --> SET1
    SET1[set output, diskPaths]
        SET1 --> FLTR
    FLTR[filter diskPaths]
        FLTR --> FOR
    FOR{for diskPaths record}
        FOR -- True --> SET2
        FOR -- False --> END
    SET2[set cmdStr]
        SET2 --> CALL
    CALL[call runCommand]
        CALL --> FOR
    END([end])
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