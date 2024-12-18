# Domain Subdomain and Vulnerability Scanner

## Overview

This tool automates the process of discovering subdomains, checking for live subdomains, fetching IP addresses, and querying these IPs for vulnerabilities. It then parses the results and organizes them in a structured way, with information on open ports, hostnames, CVEs (Common Vulnerabilities and Exposures), and more.

### Key Features:
- **Subdomain Discovery**: Uses `assetfinder` and `subfinder` to gather subdomains of a given domain.
- **Live Subdomain Detection**: Verifies live subdomains using `httpx-toolkit` on common ports.
- **IP Extraction**: Extracts unique IPs for each live subdomain using `dig`.
- **Shodan API Integration**: Queries Shodan for each IP to gather detailed information on vulnerabilities (CVEs), open ports, CPES (Common Platform Enumeration), hostnames, and more.
- **Data Organization**: Saves all relevant information in neatly structured files for analysis.
- **Efficient**: Processes only unique IPs to avoid duplicate queries.

## Requirements

- **assetfinder**
- **subfinder**
- **httpx-toolkit**
- **dig**
- **jq**
- **curl**

You can install the necessary tools using package managers like `apt` or `brew`, or follow their installation guides on their respective GitHub repositories.

## Installation

Clone the repository:
   ```bash
   git clone https://github.com/anhedoniczz/VulnScope
   cd VulnScope
   chmod +x VulnScope.sh installer.sh
   ```
## Usage 

1. Run the script
   ```bash
   ./VulnScope.sh -u example.com
   ```
   Replace example.com with the domain you want to scan. The script will create a folder with the domain name and save the results there.

2. View the results:

The validdomains file contains the live subdomains.
The CVES/ folder contains the detailed vulnerability data for each unique IP.
## Example output
```
validdomains/
    |- example1.com
    |- example2.com

CVES/
    |- example1.com_cves
        |- IP: 192.168.1.1
        |- CPES: cpe:/a:nginx:nginx:1.19.6
        |- Open Ports: 80, 443, 8080
        |- Hostnames: example1.com
        |- Tags: eol-product
        |- CVEs:
            - CVE-2020-12345 - Description of the CVE
    |- example2.com_cves
        |- IP: 192.168.1.2
        |- CPES: cpe:/a:nodejs:node.js:14.0.0
        |- Open Ports: 80, 443
        |- Hostnames: example2.com
        |- Tags: active
        |- CVEs:
            - CVE-2021-12345 - Description of the CVE
```

## Contributing
Feel free to fork the repository, make changes, and submit pull requests. If you have any suggestions or issues, open an issue and we will address it as soon as possible.

