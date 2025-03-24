# Exploit

Methodology:
- Identify vuln service
- Identify and prepare exploit code
- Gain access, both automated and manual
- Obtain remote access on target system.
- Bypass AV detection
- Pivot on the other target

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