# Dot-source the class files to make them part of the module scope
. "$PSScriptRoot\Terminal.ps1"
. "$PSScriptRoot\ConsolePrompt.ps1"

# Export the classes so they are available when the module is imported
Export-ModuleMember -Class Terminal, Prompt
