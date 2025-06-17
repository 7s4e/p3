class Terminal {
    [void]Clear() {
        [Console]::Clear()
    }

    [char]ReadKey() {
        return [Console]::ReadKey($true).KeyChar
    }

    [string]ReadLine() {
        return [Console]::ReadLine()
    }

    [void]ResetColor() {
        [Console]::ResetColor()
    }

    [void]SetForegroundColor([ConsoleColor]$color) {
        [Console]::ForegroundColor = $color
    }

    [void]Write([string]$text) {
        [Console]::Write($text)
    }

    [void]WriteLine([string]$text) {
        [Console]::WriteLine($text)
    }
}
