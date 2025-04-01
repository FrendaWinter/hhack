### Wordpress 6.1

- Use module `use auxiliary/scanner/http/wordpress_scanner` for scanning vuln plugin
- The specific version of Duplicator plugin have a vuln to read a file. Use `msf` module to exploit

### Httpd Apache - FlatCore CMS

The version 2.0.7 have server side vuln [Exploit-50262](https://www.exploit-db.com/exploits/50262)
- Download and run with python3 (Must have creds)

## Note
- `netstat -antp` Check open port on host
