- [Information gathering \&\& reconnaissance](#information-gathering--reconnaissance)
  - [Search Engine Discovery](#search-engine-discovery)
  - [Fingerprint Web Server](#fingerprint-web-server)
    - [Subdomain](#subdomain)
    - [Web tech](#web-tech)
  - [Identify Application Entry Points](#identify-application-entry-points)
- [Config and deploy test](#config-and-deploy-test)
- [Identity Management Testing](#identity-management-testing)
- [Authentication Testing](#authentication-testing)
- [Authorization Testing](#authorization-testing)
- [Session Management Testing](#session-management-testing)
- [Input Validation Testing](#input-validation-testing)
- [Testing for Error Handling](#testing-for-error-handling)
- [Testing for Weak Cryptography](#testing-for-weak-cryptography)
- [Business Logic Testing](#business-logic-testing)
- [Client-side Testing](#client-side-testing)
  - [XSS](#xss)
    - [Reflected Cross Site Scripting](#reflected-cross-site-scripting)
    - [Stored Cross Site Scripting](#stored-cross-site-scripting)
- [API Testing](#api-testing)


# Information gathering && reconnaissance

## Search Engine Discovery

Tools: 
- `BigBountyRecon`

Search engine can try:
- `Baidu`, China’s most popular search engine.
- `Bing`, a search engine owned and operated by Microsoft, and the second most popular worldwide. Supports advanced search keywords.
- `binsearch.info`, a search engine for binary Usenet newsgroups.
- `Common Crawl`, an open repository of web crawl data that can be accessed and analyzed by anyone.
- `DuckDuckGo`, a privacy-focused search engine that compiles results from many different sources. Supports search syntax.
- `Google`, which offers the world’s most popular search engine, and uses a ranking system to attempt to return the most relevant results. Supports search operators.
- `Internet Archive Wayback Machine`, “building a digital library of internet sites and other cultural artifacts in digital form.”
- `Shodan`, a service for searching internet-connected devices and services. Usage options include a limited free plan as well as paid subscription plans.

## Fingerprint Web Server

### Subdomain

Passive with `subfinder` or `subenum` or `Sublist3r`

[Subfinder Repo](https://github.com/projectdiscovery/subfinder)

```sh
sublist3r -d <HOST>
theHarvester -d <HOST>
theHarvester -d <HOST> -b all
subfinder -dL target.txt --all --recursive -o Subs.txt
```

Check if the subdomain is alive
- `cat Subs.txt | httpx -oAliveSubs.txt`

Get all urls from `waybackurls`
- `cat Subs.txt | waybackurls | tee urls.txt`

### Web tech

Tools:
- `Nikto`
- `Wappalyzer`
- `https://sitereport.netcraft.com/`

## Identify Application Entry Points

Use Zap, passive discover the website, try to interact much as possible

# Config and deploy test

# Identity Management Testing

# Authentication Testing

# Authorization Testing

# Session Management Testing

## WSTG-SESS-06: Logout function

We can use cookie editor to try to import old sessions or cookie after logout, to check if it still keep the connection

Use Burp/Zap for individual request

# Input Validation Testing

# Testing for Error Handling

# Testing for Weak Cryptography

## WSTG-CRYP-04: Weak encrypt

- Offline: Testssl.sh -> We can use old version to test old encryption, the new version ssl may doesn't support old version.

`./testssl <domain>`


- Online: Nessus, Qualys

# Business Logic Testing

# Client-side Testing

## XSS

### Reflected Cross Site Scripting

### Stored Cross Site Scripting

# API Testing