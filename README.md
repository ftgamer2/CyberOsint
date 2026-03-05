# CyberOSINT 🔍

<p align="center">
  <img src="https://raw.githubusercontent.com/ftgamer2/CyberOsint/main/assets/banner.jpg" alt="CyberOSINT Banner" width="800">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Version-3.0-blue" alt="Version">
  <img src="https://img.shields.io/badge/Termux-Compatible-brightgreen" alt="Termux">
  <img src="https://img.shields.io/badge/Python-3.8+-yellow" alt="Python">
  <img src="https://img.shields.io/badge/Modules-25+-orange" alt="Modules">
  <img src="https://img.shields.io/badge/License-MIT-red" alt="License">
  <img src="https://img.shields.io/github/stars/ftgamer2/CyberOsint?style=social" alt="Stars">
</p>

<p align="center">
  <strong>All-in-One Open Source Intelligence Toolkit for Android Termux</strong><br>
  <em>Uncover digital footprints, analyze data, and conduct reconnaissance — all from your Android device</em>
</p>

---

## 🔥 What's New in V3.0

Three powerful new modules have been added:

**📱 Phone Number Details Lookup** — Complete phone number information including name, address, father name, circle details, and alternative mobile numbers.

**🚗 Vehicle RC Information** — Dual API integration for maximum accuracy. Comprehensive vehicle ownership details including insurance, registration, and RTO information.

**💣 SMS/Call Bomber *(Educational Use Only)*** — Multi-service testing with call, WhatsApp, and SMS capabilities. Includes detailed success/failure statistics and **strong legal warnings**.

---

## 🌟 Features

### 25+ Powerful OSINT Modules

| # | Module | Description | Status |
|---|--------|-------------|--------|
| 1 | IP Tracker | Real-time IP geolocation & ISP information | ✅ |
| 2 | Username Search | Check username across 50+ social platforms | ✅ |
| 3 | Email Investigator | Email analysis & breach checking | ✅ |
| 4 | Instagram Advanced | Profile analysis & data extraction | ✅ |
| 5 | Domain Intelligence | WHOIS, DNS, SSL analysis | ✅ |
| 6 | Image EXIF Analyzer | Extract metadata from images | ✅ |
| 7 | Phone Tracker | Phone number info & carrier lookup | ✅ |
| 8 | Phone to Name | Reverse phone number lookup | ✅ |
| 9 | IFSC Code Lookup | Indian bank IFSC code information | ✅ |
| 10 | Google Dorks | Generate advanced search queries | ✅ |
| 11 | Subdomain Enumerator | Discover subdomains | ✅ |
| 12 | Reverse Image Search | Search images across engines | ✅ |
| 13 | Email Breach Checker | Check data breach exposure | ✅ |
| 14 | Password Strength | Security analysis & hash generation | ✅ |
| 15 | Wayback Machine | Historical website snapshots | ✅ |
| 16 | DNSDumpster Tool | DNS reconnaissance | ✅ |
| 17 | Sherlock Search | Username search across 50+ sites | ✅ |
| 18 | Technology Detector | Website tech stack analysis | ✅ |
| 19 | AbuseIPDB Checker | IP reputation checking | ✅ |
| 20 | Phone Number Details | Complete phone information lookup | 🆕 |
| 21 | Vehicle RC Info | Dual-API vehicle registration check | 🆕 |
| 22 | SMS/Call Bomber | Multi-service testing tool | 🆕 |
| 23 | View Reports | Browse saved investigation reports | ✅ |
| 24 | Install Dependencies | One-click setup for all requirements | ✅ |

### ✨ Key Advantages

- **25+ Modules** — Most comprehensive Termux OSINT toolkit available
- **No API Keys Required** — Works without external API registration
- **Termux Optimized** — Designed specifically for Android Termux
- **Beautiful UI** — Colorful terminal interface with dynamic ASCII banner
- **Auto-Save Reports** — All results saved in organized directories
- **Multi-Threaded** — Fast operations with parallel processing
- **Privacy Focused** — No data logging, runs locally
- **Educational Focus** — Perfect for learning OSINT techniques

---

## 🚀 Quick Start

### One-Command Installation

```bash
# Clone the repository
git clone https://github.com/ftgamer2/CyberOsint.git

# Navigate to directory
cd CyberOsint

# Run the tool
python cyberosint.py
```

**What's included:**
- 25+ OSINT modules — from IP tracking to vehicle RC lookup
- Termux-optimized — works perfectly on Android
- Colorful UI — easy-to-use menu system
- Auto-reporting — all findings saved automatically
- Multi-source verification — cross-check data from multiple APIs

### Manual Installation

```bash
# Update Termux
pkg update && pkg upgrade -y

# Install core packages
pkg install python git curl wget exiftool nmap -y

# Install Python modules
pip install requests beautifulsoup4 phonenumbers python-whois dnspython Pillow

# Optional: Install toutatis for Instagram advanced
# pip install toutatis

# Run the tool
python cyberosint.py
```

---

## 📱 Usage

### Starting the Tool

```bash
# After cloning
cd CyberOsint
python cyberosint.py

# Or create an alias in .bashrc
echo "alias cyberosint='cd ~/CyberOsint && python cyberosint.py'" >> ~/.bashrc
source ~/.bashrc
cyberosint
```

### New Features Demo

```bash
# 1. Phone Number Details
Enter phone number: 6205075067
# Shows: Name, Address, Father Name, Circle, Alt Mobile

# 2. Vehicle RC Information
Enter vehicle number: KA01AB1234
# Uses TWO APIs for verification
# Shows: Owner, Model, RTO, Insurance, Registration Date

# 3. SMS/Call Testing (Educational)
Enter phone number: 9805696906
# ⚠️ LEGAL WARNING DISPLAYED
# Tests multiple services with statistics
```

### Example Commands

```bash
# Track IP address
Enter IP: 8.8.8.8
# Shows: Country, ISP, Location, Coordinates

# Search username
Username: johndoe
# Checks: GitHub, Twitter, Instagram, Facebook, etc.

# Analyze domain
Domain: example.com
# Shows: WHOIS, DNS records, SSL, Subdomains
```

### Reports & Output

All reports are automatically saved to:

```
~/storage/shared/OSINT_Reports/
  OR
~/CyberOsint/OSINT_Reports/
```

**Categories:** IP · Username · Email · Instagram · Domain · Phone · Vehicle RC · Bombing (Educational) · and more

**Formats:** JSON for structured data · TXT for quick viewing · Organized by date and module

---

## 🛠️ Modules Overview

### New in V3.0

**📱 Phone Number Details**
- Complete personal information lookup
- Address and location details
- Family information & service provider data
- Circle details via custom FTGAMER integration

**🚗 Vehicle RC Information**
- Dual API verification for accuracy
- Comprehensive ownership, insurance & registration details
- RTO and jurisdictional data
- Custom owner name modification

**💣 SMS/Call Testing Tool *(Educational)***
- Multi-service testing with call, WhatsApp & SMS
- Detailed success/failure statistics
- Strong legal warnings enforced
- For authorized testing only

### Core Modules

**IP Intelligence** — Real-time geolocation, ISP & organization info, connection type and proxy detection, multi-source aggregation

**Digital Footprint Analysis** — Cross-platform username checking, social media profile discovery, email pattern analysis and verification

**Media Analysis** — Image metadata extraction (EXIF), reverse image search across 5+ engines, GPS coordinate extraction, camera and device info

**Domain & Network Recon** — WHOIS lookup, DNS record enumeration, SSL certificate analysis, subdomain discovery, technology stack detection

**Phone Intelligence** — Carrier & operator identification, geographic location approximation, number validation and reverse lookup

**Security Tools** — Password strength analysis, hash generation & comparison, email breach checking, security header analysis

---

## 📁 Project Structure

```
CyberOsint/
├── cyberosint.py           # Main script (25 modules)
├── setup.sh                # Installation script
├── requirements.txt        # Python dependencies
├── README.md               # This documentation
├── .gitignore              # Git ignore rules
├── assets/
│   └── banner.jpg          # Repository banner
└── OSINT_Reports/          # Auto-generated reports
    ├── IP_*.json
    ├── USERNAME_*.json
    ├── VEHICLE_RC_*.json
    ├── PHONE_DETAILS_*.json
    └── BOMBING_*.json
```

---

## 🎨 Terminal Banner

```
 $$$$$$\            $$\                            $$$$$$\   $$$$$$\  $$$$$$\ $$\   $$\ $$$$$$$$\
$$  __$$\           $$ |                          $$  __$$\ $$  __$$\ \_$$  _|$$$\  $$ |\__$$  __|
$$ /  \__|$$\   $$\ $$$$$$$\   $$$$$$\   $$$$$$\  $$ /  $$ |$$ /  \__|  $$ |  $$$$\ $$ |   $$ |
$$ |      $$ |  $$ |$$  __$$\ $$  __$$\ $$  __$$\ $$ |  $$ |\$$$$$$\    $$ |  $$ $$\$$ |   $$ |
$$ |      $$ |  $$ |$$ |  $$ |$$$$$$$$ |$$ |  \__|$$ |  $$ | \____$$\   $$ |  $$ \$$$$ |   $$ |
$$ |  $$\ $$ |  $$ |$$ |  $$ |$$   ____|$$ |      $$ |  $$ |$$\   $$ |  $$ |  $$ |\$$$ |   $$ |
\$$$$$$  |\$$$$$$$ |$$$$$$$  |\$$$$$$$\ $$ |       $$$$$$  |\$$$$$$  |$$$$$$\ $$ | \$$ |   $$ |
 \______/  \____$$ |\_______/  \_______|\__|        \______/  \______/ \______|\__|  \__|   \__|
          $$\   $$ |
          \$$$$$$  |
           \______/
```

**Dynamic Features:** Rainbow color cycling · Terminal size adaptation · Multiple display modes (lolcat, quick) · Auto-centering for all screen sizes

---

## ⚙️ Technical Details

### Requirements

- Android device with Termux
- Internet connection & storage permissions
- Python 3.8+

### Dependencies

```
# Core (auto-installed)
requests, beautifulsoup4, phonenumbers, python-whois, dnspython, Pillow

# Optional
exiftool    # for image analysis
nmap        # for network scanning
toutatis    # for Instagram advanced
```

### Compatibility

| Platform | Support |
|----------|---------|
| Android 7+ with Termux | ✅ |
| Rooted & Non-rooted devices | ✅ |
| ARM, ARM64, x86 architectures | ✅ |
| WiFi & Mobile data | ✅ |
| All screen sizes (responsive UI) | ✅ |

### API Integrations

**New in V3.0:**
- `https://check-api-sigma.vercel.app` — Phone number details
- `http://toji-rc.vercel.app/api` — Vehicle RC (API 1)
- `http://Tobi-rc-api.vercel.app` — Vehicle RC (API 2)
- `https://toji-bomber.vercel.app` — SMS/Call testing

**Existing:** Abbas APIs for IP, Instagram, IFSC lookup · Various public APIs · No API keys required for core functionality

---

## 🤝 Contributing

Contributions are welcome!

**Reporting Issues** — Found a bug? Open an issue on GitHub.

**Adding Features:**
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/AmazingFeature`
3. Commit your changes: `git commit -m 'Add AmazingFeature'`
4. Push to branch: `git push origin feature/AmazingFeature`
5. Open a Pull Request

**Development Guidelines:** Follow existing code style · Add comments for complex logic · Test on Termux before submitting · Update documentation · Include legal disclaimers for new modules

---

## ⚠️ Legal & Ethical Use

> **CRITICAL WARNING** — The SMS/Call Bomber module is for **EDUCATIONAL PURPOSES ONLY**

### Authorized Use Cases
- ✅ Security research and education
- ✅ Testing your own systems and accounts
- ✅ Authorized penetration testing
- ✅ Learning OSINT techniques
- ✅ Digital forensics training
- ✅ **Only on numbers you own or have explicit written permission to test**

### Prohibited Activities
- ❌ Unauthorized system access
- ❌ Privacy violation or harassment
- ❌ Stalking or illegal surveillance
- ❌ Data theft or fraud
- ❌ Sending unsolicited communications
- ❌ Violating telecommunications laws

### Legal Disclaimer

The author (ftgamer2) is **NOT RESPONSIBLE** for any misuse of this tool. By using this tool, you agree to:

1. Comply with all applicable laws (Telecom Regulations, IT Act, etc.)
2. Obtain proper authorization before any testing
3. Use only for legitimate security research
4. Respect privacy and consent
5. Accept full responsibility for your actions

---

## 🙏 Acknowledgments

**Core Credits**
- **ftgamer2** — Project creator & maintainer
- **Termux Community** — Android terminal support
- **Contributors** — Everyone who helped improve this project
- **API Providers** — For free access to their services

**New API Credits (V3.0)**
- **@Ros3_Zii** — Phone number details API
- **Toji** — Vehicle RC API & SMS testing tool
- **Paras Chourasiya** — Alternative Vehicle RC API

**Special Thanks** — Abbas API · Sherlock Project · OSINT community · GitHub

---

## 📞 Contact & Support

- **GitHub:** [ftgamer2](https://github.com/ftgamer2)
- **Repository:** [CyberOsint](https://github.com/ftgamer2/CyberOsint)
- **Issues:** [GitHub Issues](https://github.com/ftgamer2/CyberOsint/issues)

---

<p align="center">
  <strong>Made with ❤️ by ftgamer2</strong><br>
  <em>Empowering digital investigators worldwide</em><br><br>
  <img src="https://komarev.com/ghpvc/?username=ftgamer2&label=Repository+Views&color=blue&style=flat" alt="Repository Views">
</p>

---

<p align="center">
  ⭐ <strong>Star this repo if you find it useful!</strong> ⭐<br><br>
  <em>"Knowledge is power. Use it responsibly."</em><br><br>
  🛡️ Respect Privacy &nbsp;·&nbsp; ⚖️ Follow Laws &nbsp;·&nbsp; 🎓 Learn Ethically &nbsp;·&nbsp; 🤝 Help Others &nbsp;·&nbsp; 🔒 Stay Secure
</p>

---

*Updated: January 2026 | Version 3.0 | 25+ Modules*
