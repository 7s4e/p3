# Console Module
* [clearStdscr](#clearstdscr)
* [putScriptBanner](#putscriptbanner)
* [ConsolePrompt](#consoleprompt)
### `clearStdscr`
```mermaid
flowchart LR
    A([start]) --> B[/print/]
    B --> C([end])
```
```
void clearStdscr(Terminal console)
    PUT console.home + console.clear
END
```
### `putScriptBanner`
```mermaid
flowchart LR
    A([start]) --> B[/print/]
    B --> C([end])
```
```
void putScriptBanner(Terminal console, string scriptName)
    PUT "Running {scriptName}..."
        + left-justified(console.width)
        + console.reverse
END
```
## `ConsolePrompt`
