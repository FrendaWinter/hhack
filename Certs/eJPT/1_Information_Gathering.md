# Information Gathering

🗒️ **Passive information gathering**: Obtaining as much data as possible without actively interacting with the target.

🗒️ **Active information gathering**: Obtaining as much information as possible by actively engaging with the target.

| What to look for in a Website? |
| ------------------------------ |
| IP addresses of the web server |
| Hidden directories             |
| Names, Email addresses         |
| Phone numbers                  |
| Physical Addresses             |
| Web technologies               |

## Passive gathering

### Website Reconnaissance & Footprinting

Some method can use to do this:
- Using command `host <target>` to get ip, email, etc
    - If the website have 2 and more IP addresses found, mean that the website maybe are behind some proxy or filewall.
    - Can looking up more info by check with `https://dnslytics.com/`
- Social Links at the bottom of the main page
- Looking up for `robots.txt` file
    - **`/wp-content`** indicates that the website is running Wordpress
- Looking for `sitemap.xml` file: Used to provide search engines with an organized way of indexing the website.
- Some broswer add-on to look up the tech of the website:
    - [Wappalyzer](https://www.wappalyzer.com/)
    - [BuiltWith](https://builtwith.com/)
- `whatweb` command
- To download the entire website for more analysis, use [HTTrack](https://www.httrack.com/)
- `whois <target>` command 
- `netcraft` [netcraft](https://www.netcraft.com/)
- DNS recon `dnsrecon -d <target>` command
    - It responds with the NameServer addresses (NS)
    - A record - IPv4 address of the website
    - AAAA record - IPv6 addresses
    - MX record - mail server address
    - TXT record - domain/site verification or other values (SPF ...)
- [DNSDumpster](https://dnsdumpster.com/), have virualize the dns by graph, some more info, more action, port scan, etc
- Use `dirb <target>` to find folder, hidden file.
    - Listable folder is folder that can access from internet, try to find some infor if it open

### Advance

#### **`WAF` (Web app firewall) detection with [Wafw00f](https://github.com/EnableSecurity/wafw00f)**
- `wafw00f <tartget> -a`

#### **Subdomain Enumeration With `Sublist3r`**

#### **Google Dorks**

Use Case | Operator | Example Usage
--|--|--
Searching Within a Specific Website | `site:` | `site:nytimes.com cybersecurity`
Finding Specific File Types | `filetype:` | `filetype:pdf machine learning`
Searching for Pages with Specific Titles | `intitle:` | `intitle:”data privacy”`
Finding Pages that Link to a Specific URL | `link:` | `link:bbc.co.uk/news/technology-57339947`
Searching for Specific Text on a Web Page| `intext:` | `intext:”cyber threat”`

You can try to search for `intitle: index of` `inurl: admin`

**Wayback machine**: Looking for old version or history of the website [Wayback machine](https://web.archive.org/)

Some example for google dorks https://www.exploit-db.com/google-hacking-database

#### Email harvestiong with theHarvester

[Repo](https://github.com/laramies/theHarvester)

#### Leaked Password Database

- [Have been passwd](https://haveibeenpwned.com/)

## Active gathering

### DNS Zone tranfers

**DNS Records**


| Record Type | Description                                                              |
| :---------: | ------------------------------------------------------------------------ |
|    **A**    | Holds/Resolves the IPv4 address of a domain/hostname                     |
|   **AAAA**  | Holds/Resolves the IPv6 address of a domain/hostname                     |
|  **CNAME**  | Used for domain aliases, forwards one domain/subdomain to another domain |
|    **MX**   | Resolves a domain to a mail server                                       |
|   **TXT**   | Used for admin text notes, often used for email security                 |
|    **NS**   | Reference to the domains name server                                     |
|   **SOA**   | Stores admin information about a domain (domain authority)               |
|  **HINFO**  | Host information                                                         |
|   **SRV**   | Specific services records                                                |
|   **PTR**   | Resolves an IP address to a hostname - reverse lookups                   |


* A **zone transfer** occurs when a system admin may want to _copy or transfer zone files_ (containing domain records) from one DNS server to another.
* _This functionality can be abused by attackers when left misconfigured, to copy the zone file from the primary DNS to another DNS server._
* It can give penetration testers a complete picture of the network architecture of an organization and internal network addresses may be found.

**How?**
- `dnsenum` command for looking for dns zome transfer `dnsenum zonetransfer.me`
- `dig axfi @<domain name> <name server>`
- `fierce -dns <target>`

### Host discover with Nmap

Command `sudo nmap -sn <target_network>`

Command `sudo netdiscover -i <interface> -r <target_network>` 

### Port scan

Windows usally disable ping scan, so to perform check, use `-Pn` option

`nmap <host> -Pn`

- Use `-p-` to discover all port
- Can use `-p` to perform scan for a specific port or range of port
- `-F` for 100 first port
- Use `-sU` to discover UDP port as well
- Use `-v` for verbose
- Use `-sV` for detect version of the service
- Use `-O` for detect OS
- Use `-sC` to perform nmap default script scan (Maybe have more info)
- Use `-A` to combine 3 options `-O` `-sv` `-sC`
- More usage of nmap `man nmap`
- Use `-T<number>` to define timing template, 0 to 5, 5 mean fastest
- Use `-oN` to output scan in normal format
    - `-oX` metasploit format
