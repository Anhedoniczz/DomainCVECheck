#!/bin/bash

usage() {
    echo "Usage: $0 -u <domain>"
    exit 1
}

if [ $# -eq 0 ]; then
    usage
fi

while getopts ":u:" opt; do
    case ${opt} in
        u )
            domain=$OPTARG
            ;;
        \? )
            echo "Invalid option: $OPTARG" 1>&2
            usage
            ;;
        : )
            echo "Invalid option: $OPTARG requires an argument" 1>&2
            usage
            ;;
    esac
done
shift $((OPTIND -1))

if [ -z "$domain" ]; then
    echo "Domain is required"
    usage
fi

mkdir -p "$domain"
echo "[+] Step 1: Subdomain searching for $domain..."
assetfinder -subs-only "$domain" | uniq | sort > "$domain/subdomains_assetfinder"
subfinder -d "$domain" -silent > "$domain/subdomains_subfinder"
cat "$domain/subdomains_assetfinder" "$domain/subdomains_subfinder" | sort -u > "$domain/subdomains"
echo "[+] Subdomains saved to $domain/subdomains."

echo "[+] Step 2: Checking for live subdomains using httpx-toolkit..."
httpx-toolkit -l "$domain/subdomains" -ports 80,443,8000,8080,8888 -threads 200 -o "$domain/alivesubs"
awk -F'//' '{print $2}' "$domain/alivesubs" | sort -u > "$domain/validdomains"
echo "[+] Live subdomains saved to $domain/validdomains."

echo "[+] Step 3: Extracting unique IPs for live subdomains..."
while read -r subdomain; do
    ips=$(dig +short "$subdomain" | grep -Eo '([0-9]{1,3}\.){3}[0-9]{1,3}')
    if [ -n "$ips" ]; then
        for ip in $ips; do
            echo "$ip,$subdomain" >> "$domain/ip_subdomain_map"
        done
    fi
done < "$domain/validdomains"
awk -F',' '!seen[$1]++' "$domain/ip_subdomain_map" > "$domain/unique_ips"
echo "[+] Unique IPs and subdomains saved."

echo "[+] Step 4: Querying IPs for vulnerabilities..."
mkdir -p "$domain/CVES"
while IFS=',' read -r ip subdomain; do
    output=$(curl -s "https://internetdb.shodan.io/$ip")
    if ! echo "$output" | jq -e . > /dev/null 2>&1; then
        echo "[!] Invalid JSON for IP: $ip"
        continue
    fi
    cves=$(echo "$output" | jq -r '.vulns[]?')
    if [ -n "$cves" ]; then
        file="$domain/CVES/${subdomain}_cves"
        echo "IP: $ip" > "$file"
        echo -e "\nCPES:" >> "$file"
        echo "$output" | jq -r '.cpes[]?' >> "$file"
        echo -e "\nOpen Ports:" >> "$file"
        echo "$output" | jq -r '.ports[]?' >> "$file"
        echo -e "\nHostnames:" >> "$file"
        echo "$output" | jq -r '.hostnames[]?' >> "$file"
        echo -e "\nTags:" >> "$file"
        echo "$output" | jq -r '.tags[]?' >> "$file"
        echo -e "\nCVEs:" >> "$file"
        while read -r cve; do
            description=$(grep "$cve" cvedb.csv | cut -d',' -f2)
            echo "$cve - $description" >> "$file"
        done <<< "$cves"
        echo "[+] Saved CVEs for $subdomain ($ip)."
    fi
done < "$domain/unique_ips"

echo "[+] Cleaning up intermediate files..."
rm -f "$domain/subdomains" "$domain/alivesubs" "$domain/ip_subdomain_map" "$domain/unique_ips" "$domain/subdomains_subfinder" "$domain/subdomains_assetfinder"
echo "[+] Processing completed. Only validdomains retained."
