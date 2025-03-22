## CTF
- There are a `wp-config.bak` file, backup of wordpress config.
- There is `phpinfo.php` file for website
- `nmap -sCV -A -O target.ine.local` - Show details version
    - `nmap -sC -sV target.ine.local --script vuln --min-rate 1000`
- Try to find keyword `secret` `passwords` `flag` ...
- `find . -type f -exec grep -l 'FL@G' {} +` Grep the result in folder
- In meterpreter, use `hashdump` to dump the hash of victim machine
- Should make sure all payload should match
- Need to use `migrate` to get into the context of target user.
- To see privilege, open cmd `whoami /priv`

Powershell for decode 64
```powershell
$password='<Hash_password>'
$password=[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($pa
ssword))
echo $password
```

- If we gain access but it a shell, we can try backup the sessions, and try to upgrade it to meterpreter
  - By `sessions -u 1` `-u` mean upgrade, `1` is sessions id