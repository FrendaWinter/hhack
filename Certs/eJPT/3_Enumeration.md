# Enumeration

The goal is gather additional info about host and the service run on it
    - Like account name, shares folder, misconfigured service and so on

### MSF - Metasploit Framework

- `db_status` Check db status
    - `msfdb init` to create db (first time use)
- `msfconsole` Open console
- `db_import` import nmap xml output
    - `hosts` view hosts
    - `services` view services
    - `vulns` view vulns (if any)
- `db_nmap <nmap options>` Run nmap and export db in msf itself.

**Note**
- We can set global var for modules with `setg RHOSTS ..`
### Auxiliary Modules - of MSF

Used to perform functionality like scanning, discovery and fuzzing.

Stronger at port scanning than `nmap`

- `search <modules>` Search for the modules
- `use <module>` use modules
    - `show options` Show options for the modules
- Postscan modules
    - `set RHOSTS <ip>` - Set host ip
    - `run` -> `curl <ip>` -> `search <service>` Search for vuln 
    - `exploit` Try to exploit the hosts
    - Meterpreter sessions (Console exploit)
        - `run autoroute -s <ip>` Add ip to metasploit ip table


## FTP 

1. MSF - Portscan
2. `search type:auxiliary name:ftp`
   1. Scan version -> Set RHOSTS -> Set user/pass -> `run`
   2. `search ProFTPD` (`OroFTPD` is one type of ftp)
3. We can use brute force to find username and password
   1. Set `RHOSTS` `USER_FILE` `PASS_FILE`
   2. `run`
4. Login from MSF
5. Use module `scanner/ftp/ftp_login` for login
   1. Login normally `ftp <target>`

## SMB - 445, 139 (old windows)
- Use `smb_version` to check version
- Use `smb_enumusers` for user enumeration
- Use `smb_enumshares` for share enumeration
- Use `smb_login` for login or brute force
    - For normal login `smbclient -L \\\\<ip>\\ -U <username>` or `smbclient \\\\<ip>\\<folder> -U <username>`

Script for shares brute force

```bash
#!/bin/bash

# Define the target and wordlist location
TARGET="target.ine.local"
WORDLIST="/root/Desktop/wordlists/shares.txt"

# Check if the wordlist file exists
if [ ! -f "$WORDLIST" ]; then
    echo "Wordlist not found: $WORDLIST"
    exit 1
fi

# Loop through each share in the wordlist
while read -r SHARE; do
    echo "Testing share: $SHARE"
    smbclient //$TARGET/$SHARE -N -c "ls" &>/dev/null

    if [ $? -eq 0 ]; then
        echo "[+] Anonymous access allowed for: $SHARE"
    fi
done < "$WORDLIST"
```

### Web server
- Auxiliary `http_version` - Check version
    - Use port `443` and `SSL` = true
- Auxiliary `http_header` - Get http header
- Auxiliary `robots_txt` - Get robots file
- Scanner `dir_scanner` - Search for dir in website
- Auxiliary `files_dir` - Search files
- Auxiliary `http_login` - Brute force login http
- Auxiliary `apache_userdir_enum` - Identify user on apache (More specific function for apache)

### MySQL ~ 3306
- Auxiliary `mysql_version` - check version
- Auxiliary `mysql_login` - login
- Auxiliary `mysql_enum` - simple enumertion.
- Auxiliary `mysql_sql` - simple query
- Auxiliary `mysql_schemadump` - Dump schema

### SSH 21
- `ssh_version`
- `ssh_login` for Brute force

### SMTP 25,465,587
- `smtp_version`
- `smtp_enum`
