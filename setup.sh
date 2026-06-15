#!/data/data/com.termux/files/usr/bin/bash
# CyberOSINT - Fast Setup Script
# Author: ftgamer2
# GitHub: https://github.com/ftgamer2/CyberOSINT

# Function for colored output
color() {
    case $1 in
        red) echo -e "\e[91m$2\e[0m";;
        green) echo -e "\e[92m$2\e[0m";;
        yellow) echo -e "\e[93m$2\e[0m";;
        blue) echo -e "\e[94m$2\e[0m";;
        cyan) echo -e "\e[96m$2\e[0m";;
        magenta) echo -e "\e[95m$2\e[0m";;
        *) echo "$2";;
    esac
}

# Clear screen
clear

# Banner
color "cyan" "╔════════════════════════════════════════╗"
color "cyan" "║      F T G A M E R V 2  -  C Y B E R   ║"
color "cyan" "║            O S I N T  V 2 . 0          ║"
color "cyan" "╚════════════════════════════════════════╝"
echo ""
color "yellow" "Fast Setup Script for Termux"
echo ""

# Check if running on Termux
if [ ! -d "/data/data/com.termux" ]; then
    color "red" "Error: This script is for Termux only!"
    exit 1
fi

# Update packages
color "yellow" "[*] Updating packages..."
pkg update -y && pkg upgrade -y
color "green" "[+] Packages updated"

# Install basic tools
color "yellow" "[*] Installing basic tools..."
pkg install -y python git curl wget exiftool nmap -y
color "green" "[+] Basic tools installed"

# Install Python modules from requirements.txt
color "yellow" "[*] Installing Python modules..."
if [ -f "requirements.txt" ]; then
    grep -v "lxml\|cryptography\|pyopenssl\|selenium\|tqdm" requirements.txt > /tmp/req.txt 2>/dev/null
    pip install -r /tmp/req.txt 2>/dev/null || {
        color "yellow" "[*] Installing essential modules..."
        pip install requests beautifulsoup4 phonenumbers python-whois dnspython Pillow colorama
    }
else
    pip install requests beautifulsoup4 phonenumbers python-whois dnspython Pillow colorama
fi
color "green" "[+] Python modules installed"

# Create CyberOSINT directory
color "yellow" "[*] Setting up CyberOSINT..."
mkdir -p ~/CyberOSINT
if [ -f "cyberOSNT.py" ]; then
    if [ ! "$(pwd)" = "$HOME/CyberOSINT" ]; then
        cp -f cyberOSNT.py ~/CyberOSINT/
        chmod +x ~/CyberOSINT/cyberOSNT.py
        color "green" "[+] CyberOSINT script copied"
    fi

    if [ ! -L "/data/data/com.termux/files/usr/bin/cyberosint" ]; then
        ln -sf ~/CyberOSINT/cyberOSNT.py /data/data/com.termux/files/usr/bin/cyberosint 2>/dev/null
        color "green" "[+] Created 'cyberosint' command"
    fi

    if ! grep -q "alias cyberosint" ~/.bashrc 2>/dev/null; then
        echo "" >> ~/.bashrc
        echo "alias cyberosint='python ~/CyberOSINT/cyberOSNT.py'" >> ~/.bashrc
        echo "alias osint='cyberosint'" >> ~/.bashrc
        color "green" "[+] Added aliases to bashrc"
    fi

    mkdir -p ~/CyberOSINT/OSINT_Reports 2>/dev/null
    color "green" "[+] Created reports directory"
else
    color "red" "[-] Error: cyberOSNT.py not found"
    color "yellow" "[*] Make sure you're in the CyberOSINT directory"
fi

# Setup storage (skip if already done)
color "yellow" "[*] Setting up storage..."
if [ ! -d ~/storage ]; then
    termux-setup-storage
    color "green" "[+] Storage setup complete"
else
    color "green" "[+] Storage already setup"
fi

echo ""
color "cyan" "╔════════════════════════════════════════╗"
color "cyan" "║         INSTALLATION COMPLETE!         ║"
color "cyan" "╚════════════════════════════════════════╝"
echo ""
color "green" "CyberOSINT is ready to use!"
echo ""
color "yellow" "To run CyberOSINT:"
color "blue" "  cyberosint   or   osint"
echo ""
color "yellow" "Or:"
color "blue" "  cd ~/CyberOSINT && python cyberOSNT.py"
echo ""
color "red" "⚠ Use only for educational purposes!"
echo ""

source ~/.bashrc 2>/dev/null
