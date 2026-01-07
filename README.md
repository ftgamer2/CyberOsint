# CyberOSINT 🔍

**Ultimate Termux OSINT Toolkit | No API Keys Required**

<p align="center">
  <img src="https://lucifer-nexus-files.pages.dev/img/cba7f728-7d9d-4700-8104-583d2f1a8777.jpg" alt="CyberOSINT Banner" width="800">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Version-2.0-blue" alt="Version">
  <img src="https://img.shields.io/badge/Termux-Compatible-brightgreen" alt="Termux">
  <img src="https://img.shields.io/badge/Python-3.8+-yellow" alt="Python">
  <img src="https://img.shields.io/badge/Modules-21+-orange" alt="Modules">
  <img src="https://img.shields.io/badge/License-MIT-red" alt="License">
  <img src="https://img.shields.io/github/stars/ftgamer2/CyberOSINT?style=social" alt="Stars">
</p>

<p align="center">
  <strong>All-in-One Open Source Intelligence Toolkit for Android Termux</strong><br>
  <i>Uncover digital footprints, analyze data, and conduct reconnaissance - All from your Android device</i>
</p>

---

## 🌟 Features

### 🎯 21+ Powerful OSINT Modules

| Module | Description | Icon |
|--------|-------------|------|
| **IP Tracker** | Real-time IP geolocation & ISP information | 🌐 |
| **Username Search** | Check username across 50+ social platforms | 👤 |
| **Email Investigator** | Email analysis & breach checking | 📧 |
| **Instagram Advanced** | Profile analysis & data extraction | 📷 |
| **Domain Intelligence** | WHOIS, DNS, SSL analysis | 🔗 |
| **Image EXIF Analyzer** | Extract metadata from images | 📸 |
| **Phone Tracker** | Phone number information & carrier lookup | 📱 |
| **Phone to Name** | Reverse phone number lookup | 👤➡️📱 |
| **IFSC Code Lookup** | Indian bank IFSC code information | 🏦 |
| **Google Dorks** | Generate advanced search queries | 🔎 |
| **Subdomain Enumerator** | Discover subdomains | 🌐🔍 |
| **Reverse Image Search** | Search images across engines | 🖼️🔍 |
| **Email Breach Checker** | Check data breach exposure | 🔓 |
| **Password Strength** | Security analysis & hash generation | 🔐 |
| **Wayback Machine** | Historical website snapshots | 🕰️ |
| **DNSDumpster Tool** | DNS reconnaissance | 🛰️ |
| **Sherlock Search** | Username search across 50+ sites | 🕵️ |
| **Technology Detector** | Website tech stack analysis | 🔧 |
| **AbuseIPDB Checker** | IP reputation checking | 🛡️ |

### ✨ Key Advantages

- ✅ **No API Keys Required** - All modules work without external APIs
- ✅ **Termux Optimized** - Designed specifically for Android Termux
- ✅ **Beautiful UI** - Colorful terminal interface with animations
- ✅ **Auto-Save Reports** - All results saved in organized directories
- ✅ **Fast & Efficient** - Multi-threaded operations for speed
- ✅ **Privacy Focused** - No data logging, runs locally

---

## 🚀 Quick Start

### One-Command Installation

```bash
# Clone the repository
git clone https://github.com/ftgamer2/CyberOSINT.git

# Navigate to directory
cd CyberOSINT

# Run installation script
chmod +x setup.sh
./setup.sh
```

What Setup Script Installs

· ✅ Python & essential packages
· ✅ All required Python modules
· ✅ OSINT tools (Toutatis, etc.)
· ✅ Termux storage configuration
· ✅ Command shortcuts (cyberosint, osint)

Manual Installation

```bash
# Install dependencies
pkg update && pkg upgrade -y
pkg install python git curl wget exiftool nmap -y

# Install Python modules
pip install requests beautifulsoup4 phonenumbers python-whois dnspython Pillow

# Run the tool
python cyberosint.py
```

---

📱 Usage

Starting the Tool

```bash
# After installation
cyberosint

# Or use alias
osint

# Or manual method
cd ~/CyberOSINT
python cyberosint.py
```

Example Commands

```bash
# Track IP address
>>> Enter IP: 8.8.8.8
# Shows: Country, ISP, Location, Coordinates

# Search username
>>> Username: johndoe
# Checks: GitHub, Twitter, Instagram, Facebook, etc.

# Analyze domain
>>> Domain: example.com
# Shows: WHOIS, DNS records, SSL, Subdomains
```

Reports & Output

All reports are automatically saved to:

```
~/CyberOSINT/reports/
```

· JSON format for structured data
· TXT format for quick viewing
· Organized by date and module

---

🛠️ Modules Overview

🔍 IP Intelligence

· Real-time geolocation tracking
· ISP and organization information
· Connection type and proxy detection
· Multiple data source aggregation

👤 Digital Footprint Analysis

· Cross-platform username checking
· Social media profile discovery
· Email address pattern analysis
· Profile verification and validation

📷 Media Analysis

· Image metadata extraction (EXIF)
· Reverse image search across 5+ engines
· GPS coordinate extraction and mapping
· Camera and device information

🌐 Domain & Network Recon

· WHOIS information lookup
· DNS record enumeration
· SSL certificate analysis
· Subdomain discovery
· Technology stack detection

📱 Phone Intelligence

· Carrier and operator identification
· Geographic location approximation
· Number validation and formatting
· Reverse lookup capabilities

🔐 Security Tools

· Password strength analysis
· Hash generation and comparison
· Email breach checking
· Security header analysis

---

📁 Project Structure

```
CyberOSINT/
├── cyberosint.py          # Main script (21 modules)
├── setup.sh              # Installation script
├── requirements.txt      # Python dependencies
├── README.md            # This documentation
├── .gitignore          # Git ignore rules
└── reports/            # Auto-generated reports
```

---

🎨 Terminal Art

```
################&&&&&&&&&&####&#######&&##&#######
############&&&&#BPGBBB###&&&&&&#####&############
###########&#G5J~::.:::^~?GBBBBB&####&#B##########
##########&G!.. ..........~P##BP#&####&&##########
#########&P^ ..............!B###&#################
########&&Y:.............^!?P&&&##################
#######&##7..........:^~!~~YG#&###################
######&#BB?^.::.:^~~~^:..:!G&&&&&&&&&&#####&######
######&BPGG5JJJ?^::......:.^~?J55PPB#&&&&&########
#######&###BGBGB!:................::^!7JG&&#######
#########&&#&&GY7^......................:7B&######
###########&#7:..:::......................~#&#####
###########&Y.:............................5&#####
##########&&?::::........................:.~B&####
###########&P:::::........................:.~B&###
############&J::::.........................:.!#&#&
############&5::..:::.......................:.Y&##
###########&#!::...:::...............::!~.....~#&#
###########&B::..:^:::...............::PB^.....5&#
###########&P.:.:^Y::................:?&&B!....^B&
&&&#######&&7...:!B:................:~B&#&#^....P&
BB#&######&P...::?Y.................:?&###&?....7&
```

---

⚙️ Technical Details

Requirements

· Android device with Termux
· Internet connection
· Storage permissions
· Python 3.8+

Dependencies

```txt
# Core dependencies
requests, beautifulsoup4, phonenumbers
python-whois, dnspython, Pillow
colorama, pyfiglet, termcolor

# OSINT tools
toutatis (with Termux fix)
exiftool, nmap
```

Compatibility

· ✅ Android 7+ with Termux
· ✅ Rooted & Non-rooted devices
· ✅ ARM, ARM64, x86 architectures
· ✅ WiFi & Mobile data connections

---

🤝 Contributing

We welcome contributions! Here's how you can help:

Reporting Issues

Found a bug? Open an issue

Adding Features

1. Fork the repository
2. Create a feature branch (git checkout -b feature/AmazingFeature)
3. Commit changes (git commit -m 'Add AmazingFeature')
4. Push to branch (git push origin feature/AmazingFeature)
5. Open a Pull Request

Development Guidelines

· Follow existing code style
· Add comments for complex logic
· Test on Termux before submitting
· Update documentation if needed

---

⚠️ Legal & Ethical Use

IMPORTANT: This tool is for EDUCATIONAL PURPOSES ONLY

Authorized Use Cases

· ✅ Security research and education
· ✅ Testing your own systems and accounts
· ✅ Authorized penetration testing
· ✅ Learning OSINT techniques
· ✅ Digital forensics training

Prohibited Activities

· ❌ Unauthorized system access
· ❌ Privacy violation
· ❌ Harassment or stalking
· ❌ Illegal surveillance
· ❌ Data theft or fraud

Disclaimer

The author (ftgamer2) is not responsible for any misuse of this tool. Users must comply with all applicable laws and regulations. Always obtain proper authorization before conducting any security testing.

---

📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

```
MIT License
Copyright (c) 2026 ftgamer2
```

Permissions

· Commercial use
· Modification
· Distribution
· Private use

Conditions

· Include copyright notice
· Include license copy

Limitations

· No liability
· No warranty

---

🙏 Acknowledgments

Credits

· ftgamer2 - Project creator & maintainer
· Termux Community - Android terminal support
· Open Source Tools - Various libraries and utilities
· Contributors - Everyone who helped improve this project

Special Thanks

· Abbas API for free services
· Sherlock Project for inspiration
· OSINT community for techniques
· GitHub for hosting

Support the Project

If you find this tool useful, please:

· ⭐ Star the repository
· 🐛 Report issues
· 💡 Suggest features
· 🔄 Share with others

---

📞 Contact & Support

· GitHub: ftgamer2
· Repository: CyberOSINT
· Issues: GitHub Issues
· Questions: Open a GitHub discussion

---

<p align="center">
  <strong>Made with ❤️ by ftgamer2</strong><br>
  <i>Empowering digital investigators worldwide</i><br><br>
  <img src="https://komarev.com/ghpvc/?username=ftgamer2&label=Repository+Views&color=blue&style=flat" alt="Repository Views">
</p>

---

⭐ Star this repo if you find it useful! ⭐

"Knowledge is power. Use it responsibly."
