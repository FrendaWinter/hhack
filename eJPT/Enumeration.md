# Enumeration

The goal is gather additional info about host and the service run on it
    - Like account name, shares folder, misconfigured service and so on

## MSF - Metasploit Framework

- `db_status` Check db status
    - `msfdb init` to create db (first time use)
- `msfconsole` Open console
- `db_import` import nmap xml output
    - `hosts` view hosts
    - `services` view services
    - `vulns` view vulns (if any)
- `db_nmap <nmap options>` Run nmap and export db in msf itself.

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