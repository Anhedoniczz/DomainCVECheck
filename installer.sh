echo "deb http://http.kali.org/kali kali-rolling main non-free contrib" | sudo tee /etc/apt/sources.list.d/kali.list
wget -q -O - https://archive.kali.org/archive-key.asc | sudo apt-key add -

sudo apt update
sudo apt upgrade
sudo apt install golang-go
sudo apt-get install httpx-toolkit

go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install github.com/tomnomnom/assetfinder@latest
unzip cvedb.zip
rm -f cvedb.zip
