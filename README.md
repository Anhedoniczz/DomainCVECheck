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

1. Clone the repository:
   ```bash
   git clone https://github.com/anhedoniczz/VulnScope
   cd VulnScope
   chmod +x VulnScope.sh installer.sh
   unzip cvedb.zip
   rm -f cvedb.zip
   ```
