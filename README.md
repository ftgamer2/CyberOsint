# CyberOSINT

<p align="center">
  <img src="https://raw.githubusercontent.com/ftgamer2/CyberOsint/main/assets/banner.jpg" alt="CyberOSINT Banner" width="800">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Version-4.0-blue?style=flat-square" alt="Version">
  <img src="https://img.shields.io/badge/Python-3.8%2B-yellow?style=flat-square" alt="Python">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Android%20%7C%20Linux-brightgreen?style=flat-square" alt="Platform">
  <img src="https://img.shields.io/badge/Modules-40%2B-orange?style=flat-square" alt="Modules">
  <img src="https://img.shields.io/badge/License-MIT-red?style=flat-square" alt="License">
  <img src="https://img.shields.io/github/stars/ftgamer2/CyberOsint?style=social" alt="Stars">
</p>

<p align="center">
  <b>All-in-One OSINT Toolkit</b> — 40+ reconnaissance modules, cross-platform, zero API keys.
</p>

---

## Features

- **40+ modules** — IP, domains, social media, phone, Indian OSINT, data analysis, gaming lookups
- **No API keys** — all modules use public/free sources
- **Cross-platform** — works on Windows, Android (Termux), Linux
- **Live spinners** — real-time loading indicators for all network operations
- **Auto-reporting** — JSON/TXT reports saved to organized directories
- **Zero dependencies on setup** — built-in dependency installer

---

## Quick Start

```bash
git clone https://github.com/ftgamer2/CyberOsint.git
cd CyberOsint
python cyberOSNT.py
```

The tool auto-detects your OS and runs the matching dependency installer.

---

## Module Reference

### Network Intelligence
| Module | Source |
|--------|--------|
| IP Address Lookup | ip-api.com |
| DNS Records (A, AAAA, MX, TXT, NS, CNAME) | System DNS resolver |
| DNS Dumpster | DNS queries |
| Domain Intelligence | HTTP probe + socket |
| Subdomain Enumerator | DNS brute-force |
| SSL Certificate Check | Socket + ssl |
| Technology Detector | HTTP headers |
| Wayback Machine | archive.org API |
| AbuseIPDB Checker | ip-api.com + reference links |

### Social / Username
| Module | Check |
|--------|-------|
| Instagram Lookup | HTTP profile check |
| Telegram Lookup | HTTP existence check |
| Telegram ID Info | HTTP profile verification |
| Snapchat Lookup | HTTP existence check |
| Sherlock Username Search | 25+ platforms |
| Reverse Image Search | Opens 4 engines |

### Phone Intelligence
| Module | Description |
|--------|-------------|
| Advanced Phone Lookup | Carrier, location, line type via phonenumbers |
| Number Leak Check | Number validation + carrier |
| Pakistan Number Lookup | Format validation |
| Number to UPI | UPI handle suggestions |

### Indian OSINT
| Module | Description |
|--------|-------------|
| Aadhaar Lookup | 12-digit + Verhoeff checksum |
| PAN to GST | PAN format + type detection |
| Vehicle Info | RTO decode + VIN WMI lookup |
| Pincode Lookup | India Post API |
| UPI Verify | Handle format validation |

### Data Analysis
| Module | Description |
|--------|-------------|
| Email Breach Checker | HIBP + breach DB links |
| GitHub Email Lookup | GitHub API profile search |
| Password Strength Checker | Entropy + character analysis |
| Hash Generator | MD5 / SHA1 / SHA256 / SHA512 |
| Text Encoder/Decoder | Base64, Hex, URL |
| BIN/IIN Lookup | Bank/issuer lookup |
| Temporary Email Detector | Disposable domain check |
| MAC Address Lookup | Vendor/OUI lookup |
| URL Expander | Unshortens t.co, bit.ly, etc |
| Google Dork Generator | Query templates |
| Leak Info Tool | Breach database references |
| CVE Search | MITRE/CIRCL CVE database |

### Gaming
| Module | Description |
|--------|-------------|
| Free Fire ID Lookup | UID format validation |
| BGMI Player Lookup | Player ID format validation |

### Utilities
| Module | Description |
|--------|-------------|
| EXIF Analyzer | Image metadata |
| WiFi Scanner | Windows `netsh wlan` |
| CVSS Calculator | CVSS vector parser |

---

## Usage

```
[1]  IP Address Lookup
[2]  DNS Records Lookup
[3]  Subdomain Enumerator
[4]  Domain Intelligence
...
[40] WiFi Scanner

Select module: 1
Enter target: 8.8.8.8
```

---

## Platform Support

| Platform | Status |
|----------|--------|
| Windows 10 / 11 | ✅ Tested |
| Android (Termux) | ✅ Tested |
| Linux (Debian/Ubuntu) | ✅ Tested |

### Requirements
- Python 3.8+
- Internet connection

---

## Project Structure

```
CyberOsint/
├── cyberOSNT.py        # Main script (40+ modules)
├── README.md           # This file
├── assets/
│   └── banner.jpg      # Repository banner
└── OSINT_Reports/      # Auto-saved reports
```

---

## License

MIT

---

<p align="center">
  <a href="https://github.com/ftgamer2/CyberOsint/issues">Report Issue</a>
  ·
  <a href="https://github.com/ftgamer2/CyberOsint">GitHub</a>
</p>

<p align="center">
  <sub>Updated: Middle of June 2026 | 40+ Modules</sub>
</p>
