# ECPPT Cheatsheet

## Powershell

```ps1
# Check if the Powershell that we running is 32 or 64 bit
[Enviroment]::Is64BitProcess

# Enable script running
powershell.exe - ExecutionPolicy Bypass .\script.ps1

# Hide the powershell windows from showing (Avoid noted from victim)
powershell.exe -WindowStyle Hidden .\script.ps1

# Don't use any powershell profile, avoid permission denial
powershell.exe -NoProfile

# Choose version of powershell that run the script
powershell.exe -Version 2

# Help for command
Get-help <command>
```