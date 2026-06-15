import os
import sys
import json
import time
import re
import random
import socket
import subprocess
import threading
import sqlite3
import hashlib
import base64
from datetime import datetime, timedelta
from pathlib import Path
import argparse

def rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"

def get_term_size():
    try:
        size = os.get_terminal_size()
        return size.columns, size.lines
    except:
        return 80, 24

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_logo():
    clear()
    cols, rows = get_term_size()

    skull_lines = [
        "▄████▄▓██   ██▓ ▄▄▄▄   ▓█████  ██▀███   ▒█████    ██████  ██▓ ███▄    █ ▄▄▄█████▓",
        "▒██▀ ▀█ ▒██  ██▒▓█████▄ ▓█   ▀ ▓██ ▒ ██▒▒██▒  ██▒▒██    ▒ ▓██▒ ██ ▀█   █ ▓  ██▒ ▓▒",
        "▒▓█    ▄ ▒██ ██░▒██▒ ▄██▒███   ▓██ ░▄█ ▒▒██░  ██▒░ ▓██▄   ▒██▒▓██  ▀█ ██▒▒ ▓██░ ▒░",
        "▒▓▓▄ ▄██▒░ ▐██▓░▒██░█▀  ▒▓█  ▄ ▒██▀▀█▄  ▒██   ██░  ▒   ██▒░██░▓██▒  ▐▌██▒░ ▓██▓ ░ ",
        "▒ ▓███▀ ░░ ██▒▓░░▓█  ▀█▓░▒████▒░██▓ ▒██▒░ ████▓▒░▒██████▒▒░██░▒██░   ▓██░  ▒██▒ ░ ",
        "░ ░▒ ▒  ░ ██▒▒▒ ░▒▓███▀▒░░ ▒░ ░░ ▒▓ ░▒▓░░ ▒░▒░▒░ ▒ ▒▓▒ ▒ ░░▓  ░ ▒░   ▒ ▒   ▒ ░░   ",
        "  ░  ▒  ▓██ ░▒░ ▒░▒   ░  ░ ░  ░  ░▒ ░ ▒░  ░ ▒ ▒░ ░ ░▒  ░ ░ ▒ ░░ ░░   ░ ▒░    ░    ",
        "░       ▒ ▒ ░░   ░    ░    ░     ░░   ░ ░ ░ ░ ▒  ░  ░  ░   ▒ ░   ░   ░ ░   ░      ",
        "░ ░     ░ ░      ░         ░  ░   ░         ░ ░        ░   ░           ░          ",
        "░       ░ ░           ░ ",
    ]

    v_padding = max(0, (rows - len(skull_lines)) // 2)
    for _ in range(v_padding):
        print()

    for i, line in enumerate(skull_lines):
        line = line.rstrip()
        if not line:
            print()
            continue

        h_padding = max(0, (cols - len(line)) // 2)

        ratio = i / (len(skull_lines) - 1) if len(skull_lines) > 1 else 0
        r = int(255 - (155 * ratio))
        g = int(215 - (65 * ratio))
        b = int(0 + (255 * ratio))
        color = rgb(max(0, r), max(0, g), min(255, b))
        reset = "\033[0m"

        print(" " * h_padding + color + line + reset)
        time.sleep(0.01)

    print("\033[0m")

def print_random_logo():
    clear()
    cols, rows = get_term_size()

    lines = ["CyberOSINT Tool"]

    v_padding = max(0, (rows - 1) // 2)
    for _ in range(v_padding):
        print()

    for i, line in enumerate(lines):
        line = line.rstrip()
        if not line:
            continue

        r = random.randint(100, 255)
        g = random.randint(100, 255)
        b = random.randint(100, 255)
        color = rgb(r, g, b)
        reset = "\033[0m"

        h_padding = max(0, (cols - len(line)) // 2)
        print(" " * h_padding + color + line + reset)
        time.sleep(0.02)

    print("\033[0m")

def quick_logo():
    clear()
    cols = os.get_terminal_size().columns if hasattr(os, 'get_terminal_size') else 80

    print(f"\033[36m{'CyberOSINT Tool'.center(cols)}\033[0m")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "lolcat":
            print_random_logo()
        elif sys.argv[1] == "quick":
            quick_logo()
        else:
            print_logo()
    else:
        print_logo()

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("[!] Install: pip install requests")

try:
    import phonenumbers
    from phonenumbers import carrier, geocoder, timezone
    PHONENUMBERS_AVAILABLE = True
except ImportError:
    PHONENUMBERS_AVAILABLE = False

try:
    import whois
    WHOIS_AVAILABLE = True
except ImportError:
    WHOIS_AVAILABLE = False

try:
    import dns.resolver
    DNS_AVAILABLE = True
except ImportError:
    DNS_AVAILABLE = False

try:
    from bs4 import BeautifulSoup
    BEAUTIFULSOUP_AVAILABLE = True
except ImportError:
    BEAUTIFULSOUP_AVAILABLE = False

REPORTS_DIR = Path("/data/data/com.termux/files/home/storage/shared/OSINT_Reports")
if not REPORTS_DIR.exists():
    REPORTS_DIR = Path.cwd() / "OSINT_Reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = REPORTS_DIR / "osint_data.db"
CONFIG_DIR = Path.home() / ".termux_osint"
CONFIG_DIR.mkdir(exist_ok=True)

API_KEY = ""

def ft_api(endpoint, params=None):
    if params is None:
        params = {}
    params['key'] = API_KEY
    url = f"https://ft-osint-api.duckdns.org/api/{endpoint}"
    try:
        resp = requests.get(url, params=params, timeout=25)
        remaining = resp.headers.get('X-RateLimit-Remaining', '?')
        if resp.status_code == 200:
            data = resp.json()
            data['_remaining'] = remaining
            return data
        elif resp.status_code == 403:
            printc("❌ Invalid or expired API key", "red")
        elif resp.status_code == 429:
            printc(f"❌ Daily quota exceeded (remaining: {remaining})", "red")
        else:
            error = resp.json().get('error', 'Unknown error') if resp.text else 'Unknown'
            printc(f"❌ API error: {error}", "red")
        return None
    except requests.Timeout:
        printc("❌ API request timed out (25s)", "red")
    except Exception as e:
        printc(f"❌ API Error: {str(e)}", "red")
    return None

def live_spinner(text="Loading..."):
    """Context manager — shows spinner while blocking code runs (threading)."""
    import threading as _t, sys as _sys
    class _Spinner:
        def __init__(self):
            self._run = False; self._th = None
        def __enter__(self):
            self._run = True
            self._th = _t.Thread(target=self._spin, daemon=True)
            self._th.start()
            return self
        def _spin(self):
            chars = "\u280b\u2819\u2839\u2838\u283c\u2834\u2826\u2827\u280f\u280b"
            i = 0
            while self._run:
                print(f"\r{chars[i % 10]} {text}", end="")
                _sys.stdout.flush(); time.sleep(0.08); i += 1
        def __exit__(self, *a):
            self._run = False
            if self._th: self._th.join(0.3)
            print("\r" + " " * (len(text) + 4) + "\r", end="")
            _sys.stdout.flush()
    return _Spinner()

def typewrite(text, color=None, bold=False, delay=0.02):
    """Print text with typewriter character-by-character effect."""
    import sys as _sys
    prefix = ""
    if color:
        cu = color.upper()
        if hasattr(Colors, cu): prefix = getattr(Colors, cu)
        if bold: prefix += Colors.BOLD
    for ch in str(text):
        print(f"{prefix}{ch}{Colors.RESET}", end="", flush=True)
        time.sleep(delay)
    print()

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def cprint(text, color="white", bold=False):
    colors = {
        'red': Colors.RED, 'green': Colors.GREEN, 'yellow': Colors.YELLOW,
        'blue': Colors.BLUE, 'purple': Colors.PURPLE, 'cyan': Colors.CYAN,
        'white': Colors.WHITE, 'gray': Colors.GRAY
    }
    color_code = colors.get(color.lower(), Colors.WHITE)
    bold_code = Colors.BOLD if bold else ""
    return f"{bold_code}{color_code}{text}{Colors.RESET}"

def printc(text, color="white", bold=False, end="\n"):
    print(cprint(text, color, bold), end=end)

def print_status(msg, status="info"):
    icons = {"info": "ℹ️", "success": "✅", "error": "❌", "warning": "⚠️", "loading": "⏳"}
    colors = {"info": "cyan", "success": "green", "error": "red", "warning": "yellow"}

    icon = icons.get(status, "•")
    color = colors.get(status, "white")
    printc(f"{icon} {msg}", color)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS credentials (
            id INTEGER PRIMARY KEY,
            service TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT,
            session_data TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(service, username)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS results_cache (
            id INTEGER PRIMARY KEY,
            query_type TEXT NOT NULL,
            query_value TEXT NOT NULL,
            result_data TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(query_type, query_value)
        )
    ''')

    conn.commit()
    conn.close()



def _show_all(data, label="Results", emoji="\U0001f4ca"):
    """Show ALL fields from API response recursively - no truncation."""
    from collections import OrderedDict
    if not data:
        printc(f"  {emoji} No data found", "red")
        return
    if isinstance(data, dict):
        # Skip metadata keys
        skip_keys = {"_remaining", "success", "message"}
        for k, v in data.items():
            if k in skip_keys:
                continue
            if isinstance(v, (dict, list)) and v:
                printc(f"\n  {k}:", "cyan", True)
                _show_all(v, label, emoji)
            else:
                val = str(v) if v is not None else "N/A"
                printc(f"  {k:20s}: {val}", "yellow")
    elif isinstance(data, list):
        for idx, item in enumerate(data):
            printc(f"\n  {'='*50}", "blue")
            printc(f"  Entry #{idx+1}", "cyan", True)
            printc(f"  {'='*50}", "blue")
            if isinstance(item, dict):
                for k, v in item.items():
                    val = str(v) if v is not None else "N/A"
                    printc(f"  {k:20s}: {val}", "yellow")
            else:
                printc(f"  {str(item)}", "yellow")
    else:
        printc(f"  {str(data)}", "yellow")

class CredentialsManager:
    @staticmethod
    def save_credentials(service, username, password=None, session_data=None):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        encoded_pass = base64.b64encode(password.encode()).decode() if password else None
        encoded_session = base64.b64encode(session_data.encode()).decode() if session_data else None

        cursor.execute('''
            INSERT OR REPLACE INTO credentials (service, username, password, session_data)
            VALUES (?, ?, ?, ?)
        ''', (service, username, encoded_pass, encoded_session))

        conn.commit()
        conn.close()
        print_status(f"Credentials saved for {service}", "success")

    @staticmethod
    def get_credentials(service):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute('SELECT username, password, session_data FROM credentials WHERE service = ?', (service,))
        row = cursor.fetchone()
        conn.close()

        if row:
            username, enc_pass, enc_session = row
            password = base64.b64decode(enc_pass).decode() if enc_pass else None
            session = base64.b64decode(enc_session).decode() if enc_session else None
            return username, password, session
        return None, None, None

    @staticmethod
    def delete_credentials(service):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM credentials WHERE service = ?', (service,))
        conn.commit()
        conn.close()
        print_status(f"Credentials deleted for {service}", "success")



class IPAddressLookup:
    def lookup(self, ip=None):
        clear()
        printc("\u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557", "cyan", True)
        printc("\u2551             IP ADDRESS LOOKUP               \u2551", "cyan", True)
        printc("\u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2559", "cyan")
        print()
        if not ip:
            ip = input(cprint("IP Address: ", "cyan")).strip()
        if not ip:
            printc("\u274c Valid input required", "red")
            return
        try:
            import json as _j
            with live_spinner(f"Looking up {ip}..."):
                r = requests.get(f"http://ip-api.com/json/{ip}", timeout=15,
                    headers={'User-Agent': 'Mozilla/5.0'})
            data = r.json()
        except Exception as e:
            printc(f"\n    \u274c Error: {e}", "red")
            print(); input(cprint("Press Enter to continue...", "yellow")); return
        if data.get('status') == 'fail':
            printc(f"\n    \u274c {data.get('message', 'Invalid IP')}", "red")
            print(); input(cprint("Press Enter to continue...", "yellow")); return
        printc("\n\u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557", "green", True)
        printc("\u2551                 RESULTS                       \u2551", "green", True)
        printc("\u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2559", "green")
        for k, v in data.items():
            if k == 'status': continue
            printc(f"    \u25b6 {k:15s}: {v}", "white")
        print()
        save = input(cprint("\n\U0001f4be Save result? (y/n): ", "yellow")).strip().lower()
        if save == 'y':
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            fp = REPORTS_DIR / f"IP_{ip}_{ts}.json"
            with open(fp, "w") as f:
                json.dump(data, f, indent=2)

class AbuseIPDBChecker:
    def check(self, ip=None):
        clear()
        printc("\u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557", "red", True)
        printc("\u2551          ABUSE IP CHECKER                  \u2551", "red", True)
        printc("\u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2559", "red")
        print()
        if not ip:
            ip = input(cprint("IP Address: ", "cyan")).strip()
        if not ip:
            printc("\u274c Valid input required", "red")
            return
        try:
            with live_spinner("Checking IP reputation..."):
                r = requests.get(f"http://ip-api.com/json/{ip}", timeout=15,
                    headers={'User-Agent': 'Mozilla/5.0'})
            data = r.json()
        except Exception as e:
            printc(f"\n    \u274c Error: {e}", "red")
            print(); input(cprint("Press Enter to continue...", "yellow")); return
        if data.get('status') == 'fail':
            printc(f"\n    \u274c {data.get('message', 'Invalid IP')}", "red")
            print(); input(cprint("Press Enter to continue...", "yellow")); return
        abuseipdb_url = f"https://www.abuseipdb.com/check/{ip}"
        printc("\n\u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557", "green", True)
        printc("\u2551                 RESULTS                       \u2551", "green", True)
        printc("\u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2559", "green")
        for k, v in data.items():
            if k == 'status': continue
            printc(f"    \u25b6 {k:15s}: {v}", "white")
        printc(f"\n    \u25b6 AbuseIPDB:  {abuseipdb_url}", "cyan")
        printc("\n    \u25b6 Other check services:", "yellow")
        printc(f"      https://www.virustotal.com/gui/ip-address/{ip}", "blue")
        printc(f"      https://www.ipvoid.com/ip-blacklist-check/{ip}/", "blue")
        printc(f"      https://exchange.xforce.ibmcloud.com/ip/{ip}", "blue")
        print()
        save = input(cprint("Save report? (y/n): ", "yellow")).strip().lower()
        if save == 'y':
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            fp = REPORTS_DIR / f"ABUSE_{ip}_{ts}.json"
            with open(fp, "w") as f:
                json.dump(data, f, indent=2)

class MACAddressLookup:
    def lookup(self, mac=None):
        if not mac:
            mac = input(cprint("MAC address (e.g., 00:11:22:33:44:55): ", "cyan")).strip()
        if not mac or not re.match(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$', mac):
            printc("Invalid MAC address format. Use xx:xx:xx:xx:xx:xx", "red")
            return
        try:
            response = requests.get(f"https://api.macvendors.com/{mac}", timeout=10)
            if response.status_code == 200:
                printc(f"\n✅ MAC: {mac}", "green")
                printc(f"🏢 Vendor: {response.text.strip()}", "yellow", True)
            else:
                printc(f"\n❌ No vendor found for {mac}", "red")
        except Exception as e:
            printc(f"\n❌ Error: {str(e)}", "red")

class DNSRecordsLookup:
    def lookup(self, domain=None):
        if not domain:
            domain = input(cprint("Domain: ", "cyan")).strip()
        if not domain:
            printc("Domain required", "red")
            return
        printc(f"\n🔍 DNS Records for {domain}:", "cyan", True)
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA']
        for rtype in record_types:
            try:
                if DNS_AVAILABLE:
                    import dns.resolver
                    answers = dns.resolver.resolve(domain, rtype)
                    for ans in answers:
                        printc(f"  {rtype:6} → {ans}", "yellow")
                else:
                    if rtype == 'A':
                        try:
                            ip = socket.gethostbyname(domain)
                            printc(f"  {rtype:6} → {ip}", "yellow")
                        except:
                            pass
            except Exception:
                pass
        printc("\n✅ DNS lookup complete", "green")

class SSLChecker:
    def check(self, host=None):
        if not host:
            host = input(cprint("Domain (e.g., google.com): ", "cyan")).strip()
        if not host:
            printc("Domain required", "red")
            return
        port = 443
        if ':' in host:
            host, port_str = host.split(':', 1)
            port = int(port_str)
        import ssl
        try:
            ctx = ssl.create_default_context()
            with ctx.wrap_socket(socket.socket(), server_hostname=host) as s:
                s.settimeout(10)
                s.connect((host, port))
                cert = s.getpeercert()
                printc(f"\n🔒 SSL Certificate for {host}:{port}", "cyan", True)
                subject = dict(cert['subject'][0])
                printc(f"  Common Name: {subject.get('commonName', 'N/A')}", "yellow")
                issuer = dict(cert['issuer'][0])
                printc(f"  Issuer: {issuer.get('organizationName', 'N/A')}", "yellow")
                printc(f"  Valid From: {cert['notBefore']}", "yellow")
                printc(f"  Valid Until: {cert['notAfter']}", "yellow")
                printc(f"  Serial: {cert.get('serialNumber', 'N/A')}", "yellow")
                printc(f"\n  ✅ Certificate is valid", "green", True)
        except ssl.SSLCertVerificationError:
            printc("\n❌ SSL certificate verification failed", "red")
        except Exception as e:
            printc(f"\n❌ Error: {str(e)}", "red")

class URLExpander:
    def expand(self, url=None):
        if not url:
            url = input(cprint("Short URL: ", "cyan")).strip()
        if not url:
            printc("URL required", "red")
            return
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        printc(f"\n🔗 Expanding: {url}", "cyan")
        try:
            with live_spinner("Fetching redirect chain..."):
                resp = requests.get(url, allow_redirects=True, timeout=10)
            printc(f"  Status: {resp.status_code}", "yellow")
            printc(f"  Final URL: {resp.url}", "green", True)
            for i, h in enumerate(resp.history):
                printc(f"  Hop {i+1}: {h.url} → {h.status_code}", "gray")
            printc(f"\n✅ Expanded {len(resp.history)} hop(s)", "green")
        except Exception as e:
            printc(f"\n❌ Error: {str(e)}", "red")

class TempMailDetector:
    DISPOSABLE_DOMAINS = {
        'mailinator.com', 'guerrillamail.com', 'tempmail.com', 'temp-mail.org',
        '10minutemail.com', 'throwaway.email', 'yopmail.com', 'sharklasers.com',
        'grr.la', 'maildrop.cc', 'getairmail.com', 'trashmail.com',
        'dispostable.com', 'spambox.us', 'spamgourmet.com', 'mailnator.com',
        'tempinbox.com', 'tempemail.co', 'tempmail.net', 'mailexpire.com',
    }

    def check(self, email=None):
        if not email:
            email = input(cprint("Email address: ", "cyan")).strip()
        if not email or '@' not in email:
            printc("Invalid email", "red")
            return
        domain = email.split('@')[1].lower()
        local, dom = email.rsplit('@', 1)
        printc(f"\n📧 Email: {email}", "cyan", True)
        printc(f"  Domain: {dom}", "yellow")
        if dom.lower() in self.DISPOSABLE_DOMAINS:
            printc("  Status: ⚠️ DISPOSABLE / TEMPORARY", "red", True)
            printc("  This email is from a known temporary email provider", "red")
        else:
            printc("  Status: ✅ Looks like a permanent email", "green", True)
            mx_found = False
            try:
                if DNS_AVAILABLE:
                    import dns.resolver
                    dns.resolver.resolve(dom, 'MX')
                    printc("  MX Records: ✅ Domain accepts mail", "green")
                    mx_found = True
            except Exception:
                pass
            if not mx_found:
                try:
                    socket.gethostbyname(dom)
                    printc("  Domain resolves: ✅", "green")
                except:
                    printc("  Domain: ⚠️ Does not resolve", "red")
        printc(f"\n✅ Check complete", "green")

class BINLookup:
    def lookup(self, bin_code=None):
        if not bin_code:
            bin_code = input(cprint("BIN (first 6 digits of card): ", "cyan")).strip()
        if not bin_code or not bin_code.isdigit() or len(bin_code) < 6:
            printc("Invalid BIN. Enter at least 6 digits.", "red")
            return
        try:
            response = requests.get(f"https://lookup.binlist.net/{bin_code[:6]}",
                                    headers={'Accept-Version': '3'}, timeout=10)
            if response.status_code == 200:
                data = response.json()
                printc(f"\n💳 BIN: {bin_code[:6]}", "cyan", True)
                printc(f"  Scheme: {data.get('scheme', 'N/A')}", "yellow")
                printc(f"  Type: {data.get('type', 'N/A')}", "yellow")
                printc(f"  Brand: {data.get('brand', 'N/A')}", "yellow")
                printc(f"  Bank: {data.get('bank', {}).get('name', 'N/A')}", "yellow")
                country = data.get('country', {})
                printc(f"  Country: {country.get('name', 'N/A')} ({country.get('alpha2', '')})", "yellow")
            else:
                printc(f"\n❌ BIN not found", "red")
        except Exception as e:
            printc(f"\n❌ Error: {str(e)}", "red")

class CVESearch:
    def search(self, query=None):
        if not query:
            query = input(cprint("CVE ID (e.g., CVE-2024-1234) or keyword: ", "cyan")).strip()
        if not query:
            printc("Query required", "red")
            return
        query = query.strip().upper()
        if query.startswith('CVE-'):
            url = f"https://cve.circl.lu/api/cve/{query}"
        else:
            url = f"https://cve.circl.lu/api/search/{query}"
        printc(f"\n🔍 Searching: {query}", "cyan")
        try:
            with live_spinner("Querying CVE database..."):
                resp = requests.get(url, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                if isinstance(data, list):
                    results = data[:5]
                else:
                    results = [data]
                for cve in results:
                    cve_id = cve.get('id', 'N/A')
                    cvss = cve.get('cvss', 'N/A')
                    summary = cve.get('summary', 'No description')
                    printc(f"  [{cve_id}] (CVSS: {cvss})", "yellow", True)
                    printc(f"    {summary[:150]}...", "gray")
                printc(f"\n✅ Found {len(results)} result(s)", "green")
            else:
                printc(f"\n❌ No results or API error", "red")
        except Exception as e:
            printc(f"\n❌ Error: {str(e)}", "red")

class HashGenerator:
    def generate(self, text=None):
        if text is None:
            text = input(cprint("Text to hash: ", "cyan")).strip()
        if not text:
            file_path = input(cprint("Or file path: ", "cyan")).strip()
            if file_path and os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    text = f.read()
                printc(f"\n📄 File: {file_path} ({len(text)} bytes)", "cyan", True)
            else:
                printc("No input provided", "red")
                return
        else:
            text = text.encode()
        printc("\n🔐 Hash Results:", "cyan", True)
        printc(f"  MD5:     {hashlib.md5(text).hexdigest()}", "yellow")
        printc(f"  SHA1:    {hashlib.sha1(text).hexdigest()}", "yellow")
        printc(f"  SHA256:  {hashlib.sha256(text).hexdigest()}", "yellow")
        printc(f"  SHA512:  {hashlib.sha512(text).hexdigest()}", "yellow")
        printc("\n✅ Hash generation complete", "green")

class TextEncoder:
    def run(self, text=None):
        printc("\n🔤 TEXT ENCODER / DECODER", "cyan", True)
        if text is None:
            printc("1. Base64 Encode", "yellow")
            printc("2. Base64 Decode", "yellow")
            printc("3. Hex Encode", "yellow")
            printc("4. Hex Decode", "yellow")
            printc("5. URL Encode", "yellow")
            printc("6. URL Decode", "yellow")
            choice = input(cprint("\nSelect: ", "green")).strip()
            text = input(cprint("Text: ", "cyan")).strip()
            if not text:
                printc("No text provided", "red")
                return
        else:
            choice = '1'
        result = ""
        try:
            if choice == '1':
                result = base64.b64encode(text.encode()).decode()
            elif choice == '2':
                result = base64.b64decode(text).decode()
            elif choice == '3':
                result = text.encode().hex()
            elif choice == '4':
                result = bytes.fromhex(text).decode()
            elif choice == '5':
                from urllib.parse import quote
                result = quote(text)
            elif choice == '6':
                from urllib.parse import unquote
                result = unquote(text)
            else:
                printc("Invalid choice", "red")
                return
            printc(f"\n✅ Result: {result}", "green", True)
        except Exception as e:
            printc(f"\n❌ Error: {str(e)}", "red")

class WiFiScanner:
    def scan(self):
        printc("\n📡 Scanning for WiFi networks...", "cyan")
        try:
            if os.name == 'nt':
                result = subprocess.run(['netsh', 'wlan', 'show', 'networks'],
                                      capture_output=True, text=True, timeout=15)
                if result.returncode == 0:
                    lines = result.stdout.split('\n')
                    found = False
                    for line in lines:
                        if 'SSID' in line and 'BSSID' not in line and ':' in line:
                            ssid = line.split(':', 1)[1].strip()
                            if ssid:
                                printc(f"  📶 {ssid}", "yellow")
                                found = True
                    if not found:
                        printc("  No networks found or WiFi is disabled", "yellow")
                    else:
                        printc(f"\n✅ Scan complete", "green")
                else:
                    printc("WiFi scanning not available. Run as Admin?", "red")
            else:
                result = subprocess.run(['iwlist', 'scan'], capture_output=True, text=True, timeout=15)
                if result.returncode == 0:
                    for line in result.stdout.split('\n'):
                        if 'ESSID:' in line:
                            ssid = line.split('ESSID:')[1].strip().strip('"')
                            if ssid:
                                printc(f"  📶 {ssid}", "yellow")
                    printc(f"\n✅ Scan complete", "green")
                else:
                    printc("WiFi scanning requires root on Linux", "red")
        except subprocess.TimeoutExpired:
            printc("\n⏳ Scan timed out", "red")
        except Exception as e:
            printc(f"\n❌ Error: {str(e)}", "red")


# ====== FT API MODULE CLASSES ======

# ====== NEW FT API MODULES ======


class AadhaarLookup:
    def lookup(self, an=None):
        clear()
        printc(f"╔═══════════════════════════════════════════════╗", "cyan", True)
        printc(f"║          \U0001f9fe AADHAAR LOOKUP                  ║", "cyan", True)
        printc(f"╚═══════════════════════════════════════════════╝", "cyan")
        print()
        if not an:
            an = input(cprint("Aadhaar Number (12 digits): ", "cyan")).strip()
        if not an or not an.isdigit() or len(an) != 12:
            printc("\u274c Valid 12-digit Aadhaar number required", "red")
            return
        # Verify checksum using Verhoeff algorithm
        d = [[0,1,2,3,4,5,6,7,8,9],[1,2,3,4,0,6,7,8,9,5],[2,3,4,0,1,7,8,9,5,6],
             [3,4,0,1,2,8,9,5,6,7],[4,0,1,2,3,9,5,6,7,8],[5,9,8,7,6,0,4,3,2,1],
             [6,5,9,8,7,1,0,4,3,2],[7,6,5,9,8,2,1,0,4,3],[8,7,6,5,9,3,2,1,0,4],
             [9,8,7,6,5,4,3,2,1,0]]
        p = [[0,1,2,3,4,5,6,7,8,9],[1,5,7,6,2,8,3,0,9,4],
             [5,8,0,3,7,9,6,1,4,2],[8,9,1,6,0,4,3,5,2,7],
             [9,4,5,3,1,2,6,8,7,0],[4,2,8,6,5,7,3,9,0,1],
             [2,7,9,3,8,0,6,4,1,5],[7,0,4,6,9,1,3,2,5,8]]
        c = 0
        for i, digit in enumerate(reversed(an)):
            c = d[c][p[i%8][int(digit)]]
        valid = (c == 0)
        printc("\n╔═══════════════════════════════════════════════╗\n║                 AADHAAR INFO                  ║\n╚═══════════════════════════════════════════════╝", "green", True)
        printc(f"    \u25b6 Aadhaar:     {an[:4]}-{an[4:8]}-{an[8:]}", "white")
        printc(f"    \u25b6 Format:      {'\u2705 Valid' if valid else '\u274c Invalid'} (checksum)", "green" if valid else "red")
        if valid:
            printc(f"    \u25b6 Issued by:  UIDAI (Unique Identification Authority of India)", "white")
        printc(f"    \n    \u26a0\ufe0f  Aadhaar lookup via public API is restricted by Indian law.", "yellow")
        printc(f"    \u26a0\ufe0f  This tool validates format/checksum only.", "yellow")
        result = {"aadhaar": an[:4]+"-"+an[4:8]+"-"+an[8:], "valid_checksum": valid}
        print()
        save = input(cprint(f"💾 Save result? (y/n): ", "yellow")).strip().lower()
        if save == 'y':
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            fp = REPORTS_DIR / f"AADHAAR_{an[-4:]}_{ts}.json"
            with open(fp, "w") as f:
                json.dump(result, f, indent=2)


class UpiVerify:
    def verify(self, ui=None):
        clear()
        printc(f"╔═══════════════════════════════════════════════╗", "cyan", True)
        printc(f"║          \U0001f4b1 UPI VERIFY                       ║", "cyan", True)
        printc(f"╚═══════════════════════════════════════════════╝", "cyan")
        print()
        if not ui:
            ui = input(cprint("UPI ID (e.g., name@upi): ", "cyan")).strip()
        if not ui or '@' not in ui:
            printc("\u274c Valid UPI ID required (e.g., name@upi)", "red")
            return
        parts = ui.split('@')
        if len(parts) != 2 or not parts[0] or not parts[1]:
            printc("\u274c Invalid UPI ID format", "red")
            return
        valid_handles = ['upi', 'ybl', 'paytm', 'okhdfcbank', 'oksbi', 'okicici',
                         'okaxis', 'ikman', 'axl', 'payu', 'phonepe', 'apl',
                         'yo', 'freecharge', 'mobikwik', 'airtel', 'amazon']
        handle = parts[1].lower()
        suggested = handle in valid_handles
        printc("\n╔═══════════════════════════════════════════════╗\n║                UPI INFORMATION                ║\n╚═══════════════════════════════════════════════╝", "green", True)
        printc(f"    \u25b6 UPI ID:       {ui}", "white")
        printc(f"    \u25b6 Name:         {parts[0]}", "white")
        printc(f"    \u25b6 Handle:       @{handle}", "white")
        printc(f"    \u25b6 Known:        {'\u2705 Recognized handle' if suggested else '\u26a0\ufe0f Unknown handle'}", "green" if suggested else "yellow")
        printc(f"    \u25b6 Format:       {'\u2705 Valid' if suggested else '\u26a0\ufe0f Proceed with caution'}", "green" if suggested else "yellow")
        printc(f"    \u26a0\ufe0f UPI verification requires NPCI APIs (restricted). Format validation only.", "yellow")
        result = {"upi_id": ui, "known_handle": suggested}
        print()
        save = input(cprint(f"💾 Save result? (y/n): ", "yellow")).strip().lower()
        if save == 'y':
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            fp = REPORTS_DIR / f"UPI_{parts[0]}_{ts}.json"
            with open(fp, "w") as f:
                json.dump(result, f, indent=2)


class PanToGst:
    def lookup(self, pan=None):
        clear()
        printc(f"╔═══════════════════════════════════════════════╗", "cyan", True)
        printc(f"║          \U0001f4c4 PAN TO GST CONVERTER              ║", "cyan", True)
        printc(f"╚═══════════════════════════════════════════════╝", "cyan")
        print()
        if not pan:
            pan = input(cprint("PAN Number: ", "cyan")).strip().upper()
        if not pan or len(pan) != 10 or not re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]$', pan):
            printc("\u274c Valid 10-char PAN required (e.g., ABCDE1234F)", "red")
            return
        # GENERATE GUESSED GST based on PAN
        # Format: XXPANXXXXXZX01 (state code + PAN + entity + checksum)
        state_codes = {"AN":"Andaman","AP":"Andhra","AR":"Arunachal","AS":"Assam","BR":"Bihar",
            "CH":"Chandigarh","CT":"Chhattisgarh","DN":"Dadra","DD":"Daman","DL":"Delhi",
            "GA":"Goa","GJ":"Gujarat","HR":"Haryana","HP":"Himachal","JK":"Jammu",
            "JH":"Jharkhand","KA":"Karnataka","KL":"Kerala","LD":"Lakshadweep",
            "MP":"Madhya","MH":"Maharashtra","MN":"Manipur","ML":"Meghalaya","MZ":"Mizoram",
            "NL":"Nagaland","OR":"Odisha","PY":"Puducherry","PB":"Punjab","RJ":"Rajasthan",
            "SK":"Sikkim","TN":"Tamil","TG":"Telangana","TR":"Tripura","UP":"Uttar",
            "UK":"Uttarakhand","WB":"West Bengal"}
        printc("\n╔═══════════════════════════════════════════════╗\n║                PAN & GST INFO                 ║\n╚═══════════════════════════════════════════════╝", "green", True)
        printc(f"    \u25b6 PAN:         {pan}", "white")
        # PAN structure
        ent = pan[3]
        ent_type = {"A":"Association","B":"Body of Individuals","C":"Company","F":"Firm",
            "G":"Government","H":"HUF","J":"Artificial Judicial","L":"Local Authority",
            "P":"Individual","T":"Trust","N":"Non-Resident"}.get(ent, "Unknown")
        printc(f"    \u25b6 Type:        {ent_type}", "white")
        printc(f"    \u25b6 Status:      \u2705 Valid PAN format", "green")
        printc(f"\n    \u26a0\ufe0f  GST lookup requires GST portal API (restricted).", "yellow")
        printc(f"    \u26a0\ufe0f  To calculate GST: PAN + State Code + Entity Code + Checksum", "yellow")
        sc = input(cprint("\n    Enter state code for GST guess (e.g., MH, KA, DL) or Enter to skip: ", "cyan")).strip().upper()
        if sc in state_codes:
            guessed_gst = f"{sc}{pan}1ZV"
            printc(f"    \u25b6 Guessed GST: {guessed_gst} (verify with GST portal)", "cyan")
        print()
        save = input(cprint(f"💾 Save result? (y/n): ", "yellow")).strip().lower()
        if save == 'y':
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            fp = REPORTS_DIR / f"PAN_{pan}_{ts}.json"
            with open(fp, "w") as f:
                json.dump({"pan": pan, "type": ent_type}, f, indent=2)


class PincodeLookup:
    def lookup(self, pin=None):
        clear()
        printc("╔═══════════════════════════════════════════════╗", "cyan", True)
        printc("║          \U0001f4cd PINCODE LOOKUP                    ║", "cyan", True)
        printc("╚═══════════════════════════════════════════════╝", "cyan")
        print()
        if not pin:
            pin = input(cprint("Pincode (6 digits): ", "cyan")).strip()
        if not pin or not pin.isdigit() or len(pin) != 6:
            printc("\u274c Valid 6-digit pincode required", "red")
            return
        
        try:
            with live_spinner(f"Looking up pincode {pin}..."):
                resp = requests.get(f"https://api.postalpincode.in/pincode/{pin}", timeout=15)
            data = resp.json()
            if not data or data[0].get("Status") != "Success":
                printc(f"\n    \u274c No data found for pincode {pin}", "red")
                print(); input(cprint("Press Enter to continue...", "yellow")); return
            posts = data[0].get("PostOffice", [])
        except Exception as e:
            printc(f"\n    \u274c API error: {e}", "red")
            print(); input(cprint("Press Enter to continue...", "yellow")); return

        printc("\n╔═══════════════════════════════════════════════╗", "green", True)
        printc("║               PINCODE INFO                    ║", "green", True)
        printc("╚═══════════════════════════════════════════════╝", "green")
        if posts:
            p = posts[0]
            printc(f"    \u25b6 Pincode:      {p.get('Pincode','?')}", "white")
            printc(f"    \u25b6 Office:       {p.get('Name','?')}", "white")
            printc(f"    \u25b6 District:     {p.get('District','?')}", "white")
            printc(f"    \u25b6 State:        {p.get('State','?')}", "white")
            printc(f"    \u25b6 Division:     {p.get('Division','?')}", "white")
            printc(f"    \u25b6 Region:       {p.get('Region','?')}", "white")
            printc(f"    \u25b6 Circle:       {p.get('Circle','?')}", "white")
            printc(f"    \u25b6 Delivery:     {p.get('DeliveryStatus','?')}", "white")
            printc(f"    \u25b6 Type:         {p.get('OfficeType','?')}", "white")

            if len(posts) > 1:
                printc(f"\n    \u25b6 Other offices ({len(posts)} total):", "cyan")
                for po in posts[:10]:
                    printc(f"      \u2022 {po.get('Name','?')} - {po.get('District','?')}", "gray")
                if len(posts) > 10:
                    printc(f"      ... and {len(posts)-10} more", "gray")
        
        result = {"pincode": pin, "data": posts[0] if posts else {}}
        print()
        save = input(cprint("\U0001f4be Save report? (y/n): ", "yellow")).strip().lower()
        if save == 'y':
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            fp = REPORTS_DIR / f"PINCODE_{pin}_{ts}.json"
            with open(fp, "w") as f:
                json.dump(result, f, indent=2)
            printc(f"\u2705 Saved: {fp}", "green")


class VehicleInfo:
    def lookup(self, vn=None):
        clear()
        printc("╔═══════════════════════════════════════════════╗", "cyan", True)
        printc("║          \U0001f697 VEHICLE INFO LOOKUP                ║", "cyan", True)
        printc("╚═══════════════════════════════════════════════╝", "cyan")
        print()
        if not vn:
            vn = input(cprint("Vehicle Number / VIN: ", "cyan")).strip().upper()
        if not vn:
            printc("\u274c Valid input required", "red")
            return

        rto_states = {
            "AN": "Andaman and Nicobar", "AP": "Andhra Pradesh", "AR": "Arunachal Pradesh",
            "AS": "Assam", "BR": "Bihar", "CH": "Chandigarh", "CG": "Chhattisgarh",
            "DD": "Daman and Diu", "DL": "Delhi", "DN": "Dadra and Nagar Haveli",
            "GA": "Goa", "GJ": "Gujarat", "HP": "Himachal Pradesh", "HR": "Haryana",
            "JH": "Jharkhand", "JK": "Jammu and Kashmir", "KA": "Karnataka",
            "KL": "Kerala", "LA": "Ladakh", "LD": "Lakshadweep", "MH": "Maharashtra",
            "ML": "Meghalaya", "MN": "Manipur", "MP": "Madhya Pradesh", "MZ": "Mizoram",
            "NL": "Nagaland", "OD": "Odisha", "PB": "Punjab", "PY": "Puducherry",
            "RJ": "Rajasthan", "SK": "Sikkim", "TN": "Tamil Nadu", "TR": "Tripura",
            "TS": "Telangana", "UK": "Uttarakhand", "UP": "Uttar Pradesh", "WB": "West Bengal"
        }

        vin_years = {
            "L": "1990","M":"1991","N":"1992","P":"1993","R":"1994","S":"1995",
            "T":"1996","V":"1997","W":"1998","X":"1999","Y":"2000","1":"2001",
            "2":"2002","3":"2003","4":"2004","5":"2005","6":"2006","7":"2007",
            "8":"2008","9":"2009","A":"2010","B":"2011","C":"2012","D":"2013",
            "E":"2014","F":"2015","G":"2016","H":"2017","J":"2018","K":"2019",
            "L":"2020","M":"2021","N":"2022","P":"2023","R":"2024","S":"2025",
            "T":"2026"
        }

        vin_manufacturers = {
            "AAV":"Volkswagen","AC5":"Hyundai","ADM":"GM","AFA":"Ford",
            "JA3":"Mitsubishi","JA4":"Mitsubishi","JAL":"Isuzu","JAM":"Isuzu",
            "JN1":"Nissan","JHM":"Honda","JHG":"Honda","KNA":"Kia","KMH":"Hyundai",
            "KL1":"GM Korea","KPT":"SsangYong","L56":"Renault","LBE":"Suzuki",
            "LDC":"Dongfeng","LDP":"Dongfeng","LEN":"Tata","LGH":"Great Wall",
            "LGW":"Great Wall","LHG":"Honda","LJC":"Toyota","LJ8":"Zotye",
            "LKL":"Suzuki","LLV":"Foton","LMG":"Geely","LNB":"BAIC",
            "LPA":"Changan","LSG":"Buick","LSJ":"MG","LSV":"Volkswagen",
            "LTV":"Toyota","LUC":"Honda","LVS":"Ford","LVV":"Chery",
            "LWV":"Great Wall","LZE":"Isuzu","LZG":"Shaanxi","LZM":"MAN",
            "LZP":"Zhonghua","MA3":"Suzuki","MAG":"Mahindra","MAJ":"Ford",
            "MAL":"Hyundai","MAT":"Tata","MB1":"Ashok Leyland","MBH":"Mercedes",
            "MCA":"Fiat","MCB":"GM","MCD":"GM","MCE":"Tata","MCF":"Tata",
            "MD2":"BMW","MHD":"VW","MJB":"Audi","MKA":"Toyota","MKB":"Toyota",
            "MLC":"Suzuki","MMB":"Mitsubishi","MMC":"Mitsubishi","MMT":"Mitsubishi",
            "MNM":"Chevrolet","MNT":"Nissan","MP1":"Toyota","MR0":"Toyota",
            "MR1":"Toyota","MS3":"Suzuki","MS5":"Mazda","N57":"Renault",
            "NLE":"Mercedes","NLH":"Mercedes","NM0":"Fiat","NM4":"VW",
            "NMT":"Toyota","PE1":"Ford","PE3":"Mazda","PL1":"Proton",
            "RLA":"BYD","SAL":"Land Rover","SAR":"Rover","SB1":"Toyota",
            "SCA":"Rolls Royce","SCB":"Bentley","SCC":"Lotus","SCE":"TVR",
            "SDA":"Dennis","SDL":"Dennis","SFA":"Ford","SFD":"Westfield",
            "SGA":"Honda","SHH":"Honda","SHS":"Honda","SJN":"Nissan",
            "SKA":"Iveco","SNE":"MAN","SNT":"MAN","SUL":"Fiat","SUP":"Daf",
            "SWV":"Weichai","TCC":"Toyota","TSM":"Suzuki","TMT":"Toyota",
            "U5Y":"Kia","U6Y":"Kia","VAG":"Volkswagen","VAN":"MAN",
            "VAV":"MAN","VBK":"Kia","VCC":"Opel","VF1":"Renault","VF2":"Renault",
            "VF3":"Peugeot","VF7":"Citroen","VF9":"Bugatti","VLU":"Scania",
            "VNE":"Irisbus","VSE":"BMC","VSK":"Volvo","VSS":"Seat","VSX":"Opel",
            "VX1":"Opel","VXL":"Opel","W04":"Buick","W06":"Cadillac",
            "W0L":"Opel","WBA":"BMW","WBS":"BMW M","WBY":"BMW","WDA":"Mercedes",
            "WDB":"Mercedes","WDC":"Mercedes","WDD":"Mercedes","WDF":"Mercedes",
            "WDP":"Mercedes","WD0":"Mercedes","WDR":"Mercedes","WDS":"Mercedes",
            "WDX":"Mercedes","WF0":"Ford","WMA":"MAN","WME":"smart","WMW":"Mini",
            "WP0":"Porsche","WU0":"Smart","WVW":"VW","WV1":"VW","WV2":"VW",
            "XLA":"DAF","XLB":"DAF","XLC":"DAF","XMC":"DAF","XLG":"DAF",
            "XLV":"DAF","XLY":"DAF","YAR":"Toyota","YV1":"Volvo","YV4":"Volvo",
            "YV5":"Volvo","YS2":"Scania","YS3":"Scania","YS4":"Scania",
            "YSC":"Scania","ZAA":"Iveco","ZAM":"Maserati","ZAR":"Alfa Romeo",
            "ZAT":"Iveco","ZCF":"Iveco","ZCG":"Iveco","ZDC":"Honda",
            "ZD0":"Yamaha","ZD3":"Yamaha","ZD4":"Yamaha","ZDM":"Ducati",
            "ZFA":"Fiat","ZFC":"Fiat","ZFF":"Ferrari","ZGU":"Moto Guzzi",
            "ZHW":"Lamborghini","ZLA":"Lamborghini","ZOM":"OM"}
        v_cat = {"M":"Motorcycle","S":"Scooter","C":"Car","T":"Truck","B":"Bus",
                 "E":"3-Wheeler","O":"Others"}

        print()
        printc("╔═══════════════════════════════════════════════╗", "green", True)
        printc("║               VEHICLE INFO                   ║", "green", True)
        printc("╚═══════════════════════════════════════════════╝", "green")

        vn_clean = vn.replace(" ", "")
        result = {}

        if len(vn_clean) == 17:
            wmi = vn_clean[:3]; vds = vn_clean[3:9]; vis = vn_clean[9:]
            manu = vin_manufacturers.get(wmi, "Unknown")
            year_code = vn_clean[9] if len(vn_clean) > 9 else "?"
            year = vin_years.get(year_code, "Unknown")
            result["Type"] = "VIN (17-digit)"
            result["Manufacturer"] = manu
            result["Model Year"] = year
            result["WMI"] = wmi
            result["Year Code"] = year_code
        else:
            # Indian registration number: XX-XX-XXXX
            vn_clean = vn_clean.replace("-", "").replace(" ", "")
            if len(vn_clean) >= 10:
                rto_code = vn_clean[:2].upper()
                state = rto_states.get(rto_code, "Unknown")
                district_num = vn_clean[2:4] if len(vn_clean) > 2 else "?"
                reg_body = vn_clean[4:]
                result["Type"] = "Indian Registration"
                result["State"] = state
                result["RTO Code"] = f"{rto_code}-{district_num}"
                result["Number"] = reg_body
                result["Full Number"] = f"{rto_code} {district_num} {reg_body}"
            else:
                result["Type"] = "Unknown format"
                result["Input"] = vn

        for k, v in result.items():
            printc(f"    \u25b6 {k:20s}: {v}", "white")

        if not vn_clean:
            printc("  No valid input", "red")

        print()
        save = input(cprint("\U0001f4be Save report? (y/n): ", "yellow")).strip().lower()
        if save == 'y':
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            fp = REPORTS_DIR / f"VEHICLE_{vn_clean}_{ts}.json"
            with open(fp, "w") as f:
                json.dump(result, f, indent=2)
            printc(f"\u2705 Saved: {fp}", "green")


class FreeFireLookup:
    def lookup(self, uid=None):
        clear()
        printc(f"╔═══════════════════════════════════════════════╗", "cyan", True)
        printc(f"║          \U0001f525 FREE FIRE LOOKUP                 ║", "cyan", True)
        printc(f"╚═══════════════════════════════════════════════╝", "cyan")
        print()
        if not uid:
            uid = input(cprint("Free Fire UID: ", "cyan")).strip()
        if not uid or not uid.isdigit():
            printc("\u274c Valid UID required (numeric)", "red")
            return
        printc("\n╔═══════════════════════════════════════════════╗\n║                  PLAYER INFO                  ║\n╚═══════════════════════════════════════════════╝", "green", True)
        printc(f"    \u25b6 UID:         {uid}", "white")
        printc(f"    \u25b6 Status:      Format validated", "yellow")
        printc(f"    \u25b6 \U0001f34e Free Fire lookup requires game API access.", "yellow")
        printc(f"    \u25b6 Use: https://ff.garena.com/ or FF in-game search", "cyan")
        result = {"uid": uid}
        print()
        save = input(cprint(f"💾 Save result? (y/n): ", "yellow")).strip().lower()
        if save == 'y':
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            fp = REPORTS_DIR / f"FREEFF_{uid}_{ts}.json"
            with open(fp, "w") as f:
                json.dump(result, f, indent=2)


class BgmiLookup:
    def lookup(self, uid=None):
        clear()
        printc(f"╔═══════════════════════════════════════════════╗", "cyan", True)
        printc(f"║          \U0001f3ae BGMI PLAYER LOOKUP                ║", "cyan", True)
        printc(f"╚═══════════════════════════════════════════════╝", "cyan")
        print()
        if not uid:
            uid = input(cprint("BGMI Player ID: ", "cyan")).strip()
        if not uid or not uid.isdigit():
            printc("\u274c Valid Player ID required (numeric)", "red")
            return
        printc("\n╔═══════════════════════════════════════════════╗\n║                  PLAYER INFO                  ║\n╚═══════════════════════════════════════════════╝", "green", True)
        printc(f"    \u25b6 Player ID:  {uid}", "white")
        printc(f"    \u25b6 Status:      Format validated", "yellow")
        printc(f"    \u25b6 \U0001f3ae BGMI requires game API access (restricted).", "yellow")
        printc(f"    \u25b6 Use: https://www.battlegroundsmobileindia.com/", "cyan")
        result = {"player_id": uid}
        print()
        save = input(cprint(f"💾 Save result? (y/n): ", "yellow")).strip().lower()
        if save == 'y':
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            fp = REPORTS_DIR / f"BGMI_{uid}_{ts}.json"
            with open(fp, "w") as f:
                json.dump(result, f, indent=2)


class GitHubLookup:
    def lookup(self, un=None):
        clear()
        printc("╔═══════════════════════════════════════════════╗", "cyan", True)
        printc("║          \U0001f418 GITHUB LOOKUP                     ║", "cyan", True)
        printc("╚═══════════════════════════════════════════════╝", "cyan")
        print()
        if not un:
            un = input(cprint("GitHub username: ", "cyan")).strip()
        if not un:
            printc("\u274c Valid input required", "red")
            return
        printc("    \u25b6 Fetching from GitHub API...", "cyan")
        try:
            with live_spinner(f"Looking up {un}..."):
                resp = requests.get(f"https://api.github.com/users/{un}", timeout=15, 
                    headers={'User-Agent': 'CyberOSINT'})
            if resp.status_code != 200:
                printc(f"    \u274c GitHub user not found (HTTP {resp.status_code})", "red")
                print(); input(cprint("Press Enter to continue...", "yellow")); return
            data = resp.json()
            with live_spinner("Fetching repos..."):
                repos_resp = requests.get(f"https://api.github.com/users/{un}/repos?per_page=5&sort=updated", 
                    timeout=10, headers={'User-Agent': 'CyberOSINT'})
            repos = repos_resp.json() if repos_resp.status_code == 200 else []
        except Exception as e:
            printc(f"    \u274c Error: {e}", "red")
            print(); input(cprint("Press Enter to continue...", "yellow")); return

        printc("\n╔═══════════════════════════════════════════════╗", "green", True)
        printc("║                 PROFILE                       ║", "green", True)
        printc("╚═══════════════════════════════════════════════╝", "green")
        printc(f"    \u25b6 Login:       {data.get('login','?')}", "white")
        printc(f"    \u25b6 Name:        {data.get('name','?') or '?'}", "white")
        printc(f"    \u25b6 Bio:         {data.get('bio','?') or '?'}", "white")
        printc(f"    \u25b6 Location:    {data.get('location','?') or '?'}", "white")
        printc(f"    \u25b6 Company:     {data.get('company','?') or '?'}", "white")
        printc(f"    \u25b6 Email:       {data.get('email','?') or '?'}", "white")
        printc(f"    \u25b6 Blog:        {data.get('blog','?') or '?'}", "white")
        printc(f"    \u25b6 Public repos: {data.get('public_repos',0)}", "white")
        printc(f"    \u25b6 Followers:   {data.get('followers',0)}", "white")
        printc(f"    \u25b6 Following:   {data.get('following',0)}", "white")
        printc(f"    \u25b6 Created:     {data.get('created_at','?')}", "white")
        printc(f"    \u25b6 Profile:     {data.get('html_url','?')}", "cyan")
        printc(f"    \u25b6 Avatar:      {data.get('avatar_url','?')}", "gray")

        if repos:
            printc("\n╔═══════════════════════════════════════════════╗", "cyan", True)
            printc("║             RECENT REPOS                     ║", "cyan", True)
            printc("╚═══════════════════════════════════════════════╝", "cyan")
            for r in repos[:5]:
                printc(f"    \u25b6 {r['name']:25s} \u2b50{r.get('stargazers_count',0)}  {r.get('description','') or ''}", "white")
        
        print()
        save = input(cprint("\U0001f4be Save report? (y/n): ", "yellow")).strip().lower()
        if save == 'y':
            data['recent_repos'] = [{'name': r['name'], 'stars': r.get('stargazers_count',0), 'desc': r.get('description','')} for r in repos[:5]]
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            fp = REPORTS_DIR / f"GITHUB_{un}_{ts}.json"
            with open(fp, "w") as f:
                json.dump(data, f, indent=2)
            printc(f"\u2705 Saved: {fp}", "green")
        print()
        input(cprint("Press Enter to continue...", "yellow"))


class TelegramLookup:
    def lookup(self, uid=None):
        clear()
        printc("╔═══════════════════════════════════════════════╗", "cyan", True)
        printc("║          \u2708\ufe0f TELEGRAM LOOKUP                  ║", "cyan", True)
        printc("╚═══════════════════════════════════════════════╝", "cyan")
        print()
        if not uid:
            uid = input(cprint("Telegram @username: ", "cyan")).strip().lstrip('@')
        if not uid:
            printc("\u274c Valid input required", "red")
            return
        try:
            with live_spinner(f"Checking @{uid} on Telegram..."):
                resp = requests.get(f"https://t.me/{uid}", timeout=15,
                    headers={'User-Agent': 'Mozilla/5.0'}, allow_redirects=True)
            code = resp.status_code
        except Exception as e:
            printc(f"\n    \u274c Error: {e}", "red")
            print(); input(cprint("Press Enter to continue...", "yellow")); return

        printc("\n╔═══════════════════════════════════════════════╗", "green", True)
        printc("║                 RESULTS                       ║", "green", True)
        printc("╚═══════════════════════════════════════════════╝", "green")
        if code == 200:
            printc(f"    \u2705 @{uid} exists on Telegram", "green")
            printc(f"    \u25b6 Profile: https://t.me/{uid}", "cyan")
            result = {"username": uid, "exists": True, "profile": f"https://t.me/{uid}"}
        else:
            printc(f"    \u274c @{uid} not found on Telegram", "red")
            result = {"username": uid, "exists": False}
        print()
        save = input(cprint("\U0001f4be Save report? (y/n): ", "yellow")).strip().lower()
        if save == 'y':
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            fp = REPORTS_DIR / f"TELEGRAM_{uid}_{ts}.json"
            with open(fp, "w") as f:
                json.dump(result, f, indent=2)


class SnapchatLookup:
    def lookup(self, un=None):
        clear()
        printc("\u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557", "cyan", True)
        printc("\u2551          \U0001f47b SNAPCHAT LOOKUP                   \u2551", "cyan", True)
        printc("\u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2559", "cyan", True)
        print()
        if not un:
            un = input(cprint("Snapchat username: ", "cyan")).strip()
        if not un:
            printc("\u274c Valid input required", "red")
            return
        try:
            with live_spinner(f"Checking @{un} on Snapchat..."):
                resp = requests.get(f"https://www.snapchat.com/add/{un}", timeout=15,
                    headers={'User-Agent': 'Mozilla/5.0'}, allow_redirects=True)
            code = resp.status_code
        except Exception as e:
            printc(f"\n    \u274c Error: {e}", "red")
            print(); input(cprint("Press Enter to continue...", "yellow")); return
        printc("\n\u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557", "green", True)
        printc("\u2551                 RESULTS                       \u2551", "green", True)
        printc("\u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2559", "green")
        if code == 200:
            printc(f"    \u2705 @{un} exists on Snapchat", "green")
            printc(f"    \u25b6 Profile: https://www.snapchat.com/add/{un}", "cyan")
            result = {"username": un, "exists": True}
        else:
            printc(f"    \u274c @{un} not found on Snapchat (HTTP {code})", "red")
            result = {"username": un, "exists": False}
        print()
        save = input(cprint("\U0001f4be Save report? (y/n): ", "yellow")).strip().lower()
        if save == 'y':
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            fp = REPORTS_DIR / f"SNAPCHAT_{un}_{ts}.json"
            with open(fp, "w") as f:
                json.dump(result, f, indent=2)


class AdvLookup:
    def lookup(self, pn=None):
        clear()
        printc(f"╔═══════════════════════════════════════════════╗", "cyan", True)
        printc(f"║          \U0001f4de ADV LOOKUP                       ║", "cyan", True)
        printc(f"╚═══════════════════════════════════════════════╝", "cyan")
        print()
        if not pn:
            pn = input(cprint("Phone number (with country code, e.g. +91): ", "cyan")).strip()
        if not pn:
            printc("\u274c Valid input required", "red")
            return
        try:
            import phonenumbers
            from phonenumbers import carrier, geocoder, timezone
            num = phonenumbers.parse(pn, None)
            valid = phonenumbers.is_valid_number(num)
            if valid:
                cn = carrier.name_for_number(num, "en") or "Unknown"
                loc = geocoder.description_for_number(num, "en") or "Unknown"
                tz = ', '.join(timezone.time_zones_for_number(num)) or "Unknown"
                nt = {0:"Fixed",1:"Mobile",2:"Fixed/Mobile",3:"Toll-free",4:"Premium",5:"Shared",7:"VoIP",8:"Pager"}.get(phonenumbers.number_type(num),"Unknown")
            else:
                cn = loc = tz = nt = "N/A"
        except ImportError:
            printc("\n    \u274c phonenumbers library not installed", "red")
            printc("    \u25b6 pip install phonenumbers", "cyan")
            print(); input(cprint("Press Enter to continue...", "yellow")); return
        except Exception as e:
            printc(f"\n    \u274c Error: {e}", "red")
            print(); input(cprint("Press Enter to continue...", "yellow")); return
        printc("\n╔═══════════════════════════════════════════════╗\n║                LOOKUP RESULTS                 ║\n╚═══════════════════════════════════════════════╝", "green", True)
        printc(f"    \u25b6 Number:      {pn}", "white")
        printc(f"    \u25b6 Valid:       {'\u2705 Yes' if valid else '\u274c No'}", "green" if valid else "red")
        if valid:
            printc(f"    \u25b6 Carrier:     {cn}", "white")
            printc(f"    \u25b6 Location:    {loc}", "white")
            printc(f"    \u25b6 Timezone:    {tz}", "white")
            printc(f"    \u25b6 Type:        {nt}", "white")
        result = {"number": pn, "valid": valid}
        if valid:
            result.update({"carrier": cn, "location": loc, "timezone": tz, "type": nt})
        print()
        save = input(cprint(f"💾 Save result? (y/n): ", "yellow")).strip().lower()
        if save == 'y':
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            fp = REPORTS_DIR / f"ADV_{pn}_{ts}.json"
            with open(fp, "w") as f:
                json.dump(result, f, indent=2)


class NumberLeak:
    def check(self, pn=None):
        clear()
        printc("\u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557", "cyan", True)
        printc("\u2551          \U0001f50d NUMBER LEAK CHECK               \u2551", "cyan", True)
        printc("\u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2559", "cyan", True)
        print()
        if not pn:
            pn = input(cprint("Phone number (10 digits): ", "cyan")).strip()
        if not pn or not pn.isdigit() or len(pn) < 10:
            printc("\u274c Valid phone number required", "red")
            return
        try:
            import phonenumbers
            from phonenumbers import carrier, geocoder, timezone
            num = phonenumbers.parse("+" + pn if not pn.startswith('+') else pn, None)
            valid = phonenumbers.is_valid_number(num)
            carrier_name = carrier.name_for_number(num, "en") if valid else "N/A"
            location = geocoder.description_for_number(num, "en") if valid else "N/A"
            num_type = {0:"Fixed",1:"Mobile",2:"Fixed/Mobile",3:"Toll-free",4:"Premium",5:"Shared",7:"VoIP",8:"Pager"}.get(phonenumbers.number_type(num),"Unknown")
        except:
            valid = False
            carrier_name = location = num_type = "N/A"
        printc("\n\u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557", "green", True)
        printc("\u2551               PHONE INFO                     \u2551", "green", True)
        printc("\u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2559", "green")
        printc(f"    \u25b6 Number:       {pn}", "white")
        printc(f"    \u25b6 Valid:        {'\u2705' if valid else '\u274c'}", "white")
        printc(f"    \u25b6 Carrier:      {carrier_name}", "white")
        printc(f"    \u25b6 Location:     {location}", "white")
        printc(f"    \u25b6 Type:         {num_type}", "white")
        result = {"number": pn, "valid": valid, "carrier": carrier_name, "location": location, "type": num_type}
        print()
        save = input(cprint("\U0001f4be Save report? (y/n): ", "yellow")).strip().lower()
        if save == 'y':
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            fp = REPORTS_DIR / f"NUMLK_{pn}_{ts}.json"
            with open(fp, "w") as f:
                json.dump(result, f, indent=2)


class NumberToUpi:
    def lookup(self, pn=None):
        clear()
        printc(f"╔═══════════════════════════════════════════════╗", "cyan", True)
        printc(f"║          \U0001f4f2 NUMBER TO UPI                    ║", "cyan", True)
        printc(f"╚═══════════════════════════════════════════════╝", "cyan")
        print()
        if not pn:
            pn = input(cprint("Phone number (10 digits): ", "cyan")).strip()
        if not pn or not pn.isdigit() or len(pn) < 10:
            printc("\u274c Valid 10-digit phone number required", "red")
            return
        banks = {"@ybl":"Yes Bank","@paytm":"Paytm Payments Bank","@okhdfcbank":"HDFC Bank",
            "@oksbi":"SBI","@okicici":"ICICI Bank","@okaxis":"Axis Bank","@apl":"Airtel",
            "@ikman":"Indian Bank","@axl":"Axis Bank","@payu":"PayU","@phonepe":"PhonePe",
            "@yo":"Kotak Mahindra","@freecharge":"Freecharge","@mobikwik":"MobiKwik"}
        printc("\n╔═══════════════════════════════════════════════╗\n║                UPI INFORMATION                ║\n╚═══════════════════════════════════════════════╝", "green", True)
        printc(f"    \u25b6 Number:      {pn}", "white")
        printc(f"    \u25b6 UPI handles: {', '.join(banks.keys())}", "white")
        printc(f"    \u25b6 Example:     {pn}@ybl", "cyan")
        printc(f"    \u26a0\ufe0f Actual UPI-to-number requires NPCI APIs (restricted).", "yellow")
        printc(f"    \u26a0\ufe0f Showing possible UPI formats only.", "yellow")
        result = {"phone": pn}
        print()
        save = input(cprint(f"💾 Save result? (y/n): ", "yellow")).strip().lower()
        if save == 'y':
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            fp = REPORTS_DIR / f"NUMUPI_{pn}_{ts}.json"
            with open(fp, "w") as f:
                json.dump(result, f, indent=2)


class PkNumberLookup:
    def lookup(self, pn=None):
        clear()
        printc(f"╔═══════════════════════════════════════════════╗", "cyan", True)
        printc(f"║          \U0001f4f1 PK NUMBER LOOKUP                 ║", "cyan", True)
        printc(f"╚═══════════════════════════════════════════════╝", "cyan")
        print()
        if not pn:
            pn = input(cprint("Pakistan mobile number (without +92): ", "cyan")).strip()
        if not pn or not pn.isdigit() or len(pn) < 10:
            printc("\u274c Valid Pakistan mobile number required", "red")
            return
        # Pakistani mobile prefix lookup
        prefixes = {"030":"Mobilink/Jazz","031":"Zong","032":"Warid","033":"Ufone",
            "034":"Telenor","035":"SCO Mobile","036":"SCO Mobile"}
        pref = pn[:3]
        ops = prefixes.get(pref, "Unknown operator")
        full = f"+92{pn}" if not pn.startswith('92') else f"+{pn}"
        printc("\n╔═══════════════════════════════════════════════╗\n║                  NUMBER INFO                  ║\n╚═══════════════════════════════════════════════╝", "green", True)
        printc(f"    \u25b6 Number:      {full}", "white")
        printc(f"    \u25b6 Operator:    {ops}", "white")
        printc(f"    \u25b6 Country:     Pakistan", "white")
        printc(f"    \u26a0\ufe0f Detailed lookup requires PTA/operator APIs.", "yellow")
        result = {"number": full, "operator": ops}
        print()
        save = input(cprint(f"💾 Save result? (y/n): ", "yellow")).strip().lower()
        if save == 'y':
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            fp = REPORTS_DIR / f"PKNUM_{pn}_{ts}.json"
            with open(fp, "w") as f:
                json.dump(result, f, indent=2)


class LeakInfoTool:
    def check(self, st=None):
        clear()
        printc(f"╔═══════════════════════════════════════════════╗", "cyan", True)
        printc(f"║          \U0001f50d LEAK INFO SEARCH                 ║", "cyan", True)
        printc(f"╚═══════════════════════════════════════════════╝", "cyan")
        print()
        if not st:
            st = input(cprint("Search term (email/username): ", "cyan")).strip()
        if not st:
            printc("\u274c Valid input required", "red")
            return
        # Generate breach check URLs
        sites = ["https://haveibeenpwned.com/","https://dehashed.com/","https://leakcheck.io/",
            "https://scylla.so/","https://scatteredsecrets.com/"]
        printc("\n╔═══════════════════════════════════════════════╗\n║                LEAK CHECK INFO                ║\n╚═══════════════════════════════════════════════╝", "green", True)
        printc(f"    \u25b6 Searched:    {st}", "white")
        printc(f"    \u25b6 Check these sites manually:", "yellow")
        for s in sites:
            printc(f"      \u25b6 {s}", "cyan")
        printc(f"    \n    \u26a0\ufe0f Breach database APIs are restricted or paid.", "yellow")
        printc(f"    \u26a0\ufe0f Opening HaveIBeenPwned for manual check:", "yellow")
        try:
            import webbrowser
            webbrowser.open(f"https://haveibeenpwned.com/account/{st}")
        except:
            pass
        result = {"searched": st, "sites": sites}
        print()
        save = input(cprint(f"💾 Save report? (y/n): ", "yellow")).strip().lower()
        if save == 'y':
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            fp = REPORTS_DIR / f"LEAK_{st}_{ts}.json"
            with open(fp, "w") as f:
                json.dump(result, f, indent=2)


class TelegramIdInfo:
    def lookup(self, tid=None):
        clear()
        printc(f"╔═══════════════════════════════════════════════╗", "cyan", True)
        printc(f"║          \U0001f916 TELEGRAM ID INFO                 ║", "cyan", True)
        printc(f"╚═══════════════════════════════════════════════╝", "cyan")
        print()
        if not tid:
            tid = input(cprint("Telegram @username (with or without @): ", "cyan")).strip().lstrip('@')
        if not tid:
            printc("\u274c Valid username required", "red")
            return
        try:
            with live_spinner(f"Checking @{tid}..."):
                resp = requests.get(f"https://t.me/{tid}", timeout=15,
                    headers={'User-Agent': 'Mozilla/5.0'}, allow_redirects=True)
        except Exception as e:
            printc(f"\n    \u274c Error: {e}", "red")
            print(); input(cprint("Press Enter to continue...", "yellow")); return
        printc("\n╔═══════════════════════════════════════════════╗\n║                 TELEGRAM INFO                 ║\n╚═══════════════════════════════════════════════╝", "green", True)
        printc(f"    \u25b6 Username:   @{tid}", "white")
        printc(f"    \u25b6 Status:     {'\u2705 Exists' if resp.status_code==200 else '\u274c Not found'}", "green" if resp.status_code==200 else "red")
        printc(f"    \u25b6 Link:       https://t.me/{tid}", "cyan")
        # Try to get name from page title
        if resp.status_code == 200 and 'text/html' in resp.headers.get('Content-Type',''):
            import re as re2
            title_m = re2.search(r'<title[^>]*>(.*?)</title>', resp.text, re2.IGNORECASE|re2.DOTALL)
            if title_m:
                title = title_m.group(1).strip()
                if 'Telegram' not in title:
                    printc(f"    \u25b6 Name:       {title}", "white")
        result = {"username": tid, "exists": resp.status_code==200}
        print()
        save = input(cprint(f"💾 Save report? (y/n): ", "yellow")).strip().lower()
        if save == 'y':
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            fp = REPORTS_DIR / f"TGID_{tid}_{ts}.json"
            with open(fp, "w") as f:
                json.dump(result, f, indent=2)


class DNSDumpsterTool:
    def analyze(self, domain=None):
        clear()
        printc(f"╔═══════════════════════════════════════════════╗", "cyan", True)
        printc(f"║          \U0001f4e1 DNS DUMPSTER                     ║", "cyan", True)
        printc(f"╚═══════════════════════════════════════════════╝", "cyan")
        print()
        if not domain:
            domain = input(cprint("Domain name (e.g., example.com): ", "cyan")).strip().lower()
        if not domain or '.' not in domain:
            printc("\u274c Valid domain required", "red")
            return
        try:
            import socket
            answers = socket.getaddrinfo(domain, 0)
            ips = sorted(set(a[4][0] for a in answers))
        except:
            ips = []
        try:
            import subprocess
            r = subprocess.run(['nslookup', '-type=ns', domain], capture_output=True, text=True, timeout=10)
            ns_lines = [l.strip() for l in r.stdout.split('\n') if 'nameserver' in l.lower() or 'NS' in l]
        except:
            ns_lines = []
        printc("\n╔═══════════════════════════════════════════════╗\n║                  DNS RECORDS                  ║\n╚═══════════════════════════════════════════════╝", "green", True)
        printc(f"    \u25b6 Domain:      {domain}", "white")
        printc(f"    \u25b6 IPs:         {', '.join(ips[:5]) if ips else 'No A records'}", "white")
        printc(f"    \u25b6 Nameservers:", "white")
        for ns in ns_lines[:5]:
            printc(f"      \u25b6 {ns}", "white")
        if not ns_lines:
            printc(f"      (try 'nslookup -type=ns {domain}' manually)", "yellow")
        result = {"domain": domain, "ips": ips, "nameservers": ns_lines}
        print()
        save = input(cprint(f"💾 Save result? (y/n): ", "yellow")).strip().lower()
        if save == 'y':
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            fp = REPORTS_DIR / f"DNS_{domain}_{ts}.json"
            with open(fp, "w") as f:
                json.dump(result, f, indent=2)


class TechDetector:
    def detect(self, url=None):
        clear()
        printc("\u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557", "cyan", True)
        printc("\u2551          \U0001f4bb TECH DETECTOR                   \u2551", "cyan", True)
        printc("\u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2559", "cyan", True)
        print()
        if not url:
            url = input(cprint("URL for technology detection: ", "cyan")).strip()
        if not url:
            printc("\u274c Valid input required", "red")
            return
        if not url.startswith('http'):
            url = 'https://' + url
        try:
            with live_spinner("Detecting technologies..."):
                resp = requests.get(url, timeout=20, headers={'User-Agent': 'Mozilla/5.0'},
                    allow_redirects=True)
            h = resp.headers
        except Exception as e:
            printc(f"\n    \u274c Error: {e}", "red")
            print(); input(cprint("Press Enter to continue...", "yellow")); return
        techs = {}
        if 'Server' in h: techs['Server'] = h['Server']
        if 'X-Powered-By' in h: techs['Framework'] = h['X-Powered-By']
        if 'X-Generator' in h: techs['Generator'] = h['X-Generator']
        if 'X-AspNet-Version' in h: techs['ASP.NET'] = h['X-AspNet-Version']
        if 'CF-RAY' in h: techs['Cloudflare'] = 'Yes'
        if 'x-amz-request-id' in h: techs['AWS'] = 'Yes'
        if 'nginx' in str(h).lower(): techs['Nginx'] = 'Detected'
        ct = h.get('Content-Type', '')
        if 'text/html' in ct:
            body = resp.text[:5000].lower()
            if 'wp-content' in body: techs['CMS'] = 'WordPress'
            elif 'drupal' in body: techs['CMS'] = 'Drupal'
            elif 'joomla' in body: techs['CMS'] = 'Joomla'
            if 'react' in body: techs['JS Framework'] = 'React'
            if 'angular' in body: techs['JS Framework'] = 'Angular'
            if 'vue' in body: techs['JS Framework'] = 'Vue.js'
            if 'jquery' in body: techs['JS Lib'] = 'jQuery'
            if 'bootstrap' in body: techs['CSS'] = 'Bootstrap'
            if 'tailwind' in body: techs['CSS'] = 'Tailwind'
        printc("\n\u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557", "green", True)
        printc("\u2551           DETECTED TECHNOLOGIES               \u2551", "green", True)
        printc("\u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2559", "green")
        if not techs:
            printc(f"    \u25b6 URL:          {url}", "white")
            printc(f"    \u25b6 HTTP Status:  {resp.status_code}", "white")
            printc(f"    \u25b6 No specific tech signatures found", "yellow")
        else:
            for k, v in techs.items():
                printc(f"    \u25b6 {k:15s}: {v}", "white")
        print()
        save = input(cprint("\U0001f4be Save report? (y/n): ", "yellow")).strip().lower()
        if save == 'y':
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            fp = REPORTS_DIR / f"TECH_{ts}.json"
            with open(fp, "w") as f:
                json.dump({"url": url, "tech": techs}, f, indent=2)


class DomainIntelligence:
    def investigate(self, domain=None):
        clear()
        printc(f"╔═══════════════════════════════════════════════╗", "cyan", True)
        printc(f"║          \U0001f310 DOMAIN INTELLIGENCE               ║", "cyan", True)
        printc(f"╚═══════════════════════════════════════════════╝", "cyan")
        print()
        if not domain:
            domain = input(cprint("Domain name: ", "cyan")).strip().lower()
        if not domain or '.' not in domain:
            printc("\u274c Valid domain required", "red")
            return
        info = {"domain": domain}
        # DNS records via socket
        try:
            import socket
            ip = socket.gethostbyname(domain)
            info['ip'] = ip
        except:
            info['ip'] = 'Unknown'
        # HTTP headers
        try:
            with live_spinner(f"Probing {domain}..."):
                r = requests.get(f"https://{domain}", timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            info['status'] = r.status_code
            info['server'] = r.headers.get('Server', 'Unknown')
        except:
            info['status'] = 'Timeout'
            info['server'] = 'N/A'
        printc("\n╔═══════════════════════════════════════════════╗\n║              DOMAIN INTELLIGENCE              ║\n╚═══════════════════════════════════════════════╝", "green", True)
        printc(f"    \u25b6 Domain:      {info['domain']}", "white")
        printc(f"    \u25b6 IP:          {info['ip']}", "white")
        printc(f"    \u25b6 HTTP Status: {info['status']}", "white")
        printc(f"    \u25b6 Server:      {info['server']}", "white")
        printc(f"    \u26a0\ufe0f WHOIS requires a paid API or local whois binary.", "yellow")
        printc(f"    \u26a0\ufe0f Try: whois {domain} (if whois is installed)", "yellow")
        print()
        save = input(cprint(f"💾 Save result? (y/n): ", "yellow")).strip().lower()
        if save == 'y':
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            fp = REPORTS_DIR / f"DOMINTEL_{domain}_{ts}.json"
            with open(fp, "w") as f:
                json.dump(info, f, indent=2)


class SubdomainEnumerator:
    def enumerate(self, domain=None):
        clear()
        printc(f"╔═══════════════════════════════════════════════╗", "cyan", True)
        printc(f"║          \U0001f50d SUBDOMAIN ENUMERATOR              ║", "cyan", True)
        printc(f"╚═══════════════════════════════════════════════╝", "cyan")
        print()
        if not domain:
            domain = input(cprint("Domain name: ", "cyan")).strip().lower()
        if not domain or '.' not in domain:
            printc("\u274c Valid domain required", "red")
            return
        # Common subdomains to check
        subs = ['www', 'mail', 'ftp', 'admin', 'blog', 'api', 'cdn', 'dev',
            'test', 'staging', 'vpn', 'webmail', 'portal', 'support', 'apps',
            'm', 'mobile', 'shop', 'help', 'forum', 'docs', 'status', 'ns1',
            'ns2', 'ns3', 'remote', 'ssl', 'smtp', 'imap', 'pop', 'mx']
        found = []
        import socket
        for s in subs:
            try:
                ip = socket.gethostbyname(f"{s}.{domain}")
                found.append((s, ip))
            except:
                pass
        printc("\n╔═══════════════════════════════════════════════╗\n║               SUBDOMAIN RESULTS               ║\n╚═══════════════════════════════════════════════╝", "green", True)
        printc(f"    \u25b6 Domain:      {domain}", "white")
        printc(f"    \u25b6 Found:       {len(found)} subdomains", "green" if found else "yellow")
        for s, ip in found:
            printc(f"      \u25b6 {s}.{domain:25s} -> {ip}", "white")
        if not found:
            printc(f"      (DNS resolution returned nothing - try with more tools)", "yellow")
        result = {"domain": domain, "subdomains": dict(found)}
        print()
        save = input(cprint(f"💾 Save result? (y/n): ", "yellow")).strip().lower()
        if save == 'y':
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            fp = REPORTS_DIR / f"SUBDOM_{domain}_{ts}.json"
            with open(fp, "w") as f:
                json.dump(result, f, indent=2)


class WaybackChecker:
    def check(self, url=None):
        clear()
        printc("\u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557", "cyan", True)
        printc("\u2551          \U0001f5d3 WAYBACK MACHINE CHECK             \u2551", "cyan", True)
        printc("\u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2559", "cyan", True)
        print()
        if not url:
            url = input(cprint("URL for Wayback check: ", "cyan")).strip()
        if not url:
            printc("\u274c Valid input required", "red")
            return
        if not url.startswith('http'):
            url = 'https://' + url
        try:
            with live_spinner("Checking archive.org..."):
                avail = requests.get(f"https://archive.org/wayback/available?url={url}", timeout=20).json()
            snap = avail.get('archived_snapshots', {}).get('closest', {})
        except Exception as e:
            printc(f"\n    \u274c Error: {e}", "red")
            print(); input(cprint("Press Enter to continue...", "yellow")); return
        printc("\n\u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557", "green", True)
        printc("\u2551               ARCHIVE HISTORY                   \u2551", "green", True)
        printc("\u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2559", "green")
        if snap and snap.get('available'):
            printc(f"    \u25b6 URL:          {url}", "white")
            printc(f"    \u25b6 Archived:     \u2705 Yes", "green")
            printc(f"    \u25b6 First seen:   {snap.get('timestamp','?')}", "white")
            printc(f"    \u25b6 Snapshot:     {snap.get('url','?')}", "cyan")
        else:
            printc(f"    \u25b6 URL:          {url}", "white")
            printc(f"    \u25b6 Archived:     \u274c No snapshots found", "yellow")
        print()
        save = input(cprint("\U0001f4be Save report? (y/n): ", "yellow")).strip().lower()
        if save == 'y':
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            fp = REPORTS_DIR / f"WAYBACK_{ts}.json"
            with open(fp, "w") as f:
                json.dump({"url": url, "available": bool(snap.get('available'))}, f, indent=2)


class SherlockUsernameSearch:
    def search(self, un=None):
        clear()
        printc("\u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557", "cyan", True)
        printc("\u2551         \U0001f575\ufe0f SHERLOCK USERNAME SEARCH        \u2551", "cyan", True)
        printc("\u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2559", "cyan", True)
        print()
        if not un:
            un = input(cprint("Username to search: ", "cyan")).strip()
        if not un:
            printc("\u274c Valid input required", "red")
            return
        print()
        printc("  \u2699 Checking platforms...", "cyan")

        platforms = [
            ("GitHub",      "https://github.com/{}"),
            ("Instagram",   "https://www.instagram.com/{}"),
            ("Twitter/X",   "https://x.com/{}"),
            ("Reddit",      "https://www.reddit.com/user/{}"),
            ("YouTube",     "https://www.youtube.com/@{}"),
            ("TikTok",      "https://www.tiktok.com/@{}"),
            ("Twitch",      "https://www.twitch.tv/{}"),
            ("Medium",      "https://medium.com/@{}"),
            ("Dev.to",      "https://dev.to/{}"),
            ("Keybase",     "https://keybase.io/{}"),
            ("Telegram",    "https://t.me/{}"),
            ("GitLab",      "https://gitlab.com/{}"),
            ("SoundCloud",  "https://soundcloud.com/{}"),
            ("Pinterest",   "https://www.pinterest.com/{}"),
            ("Spotify",     "https://open.spotify.com/user/{}"),
            ("Replit",      "https://replit.com/@{}"),
            ("Vimeo",       "https://vimeo.com/{}"),
            ("Pastebin",    "https://pastebin.com/u/{}"),
            ("HackerNews",  "https://news.ycombinator.com/user?id={}"),
            ("Flickr",      "https://www.flickr.com/people/{}"),
            ("Dribbble",    "https://dribbble.com/{}"),
            ("Behance",     "https://www.behance.net/{}"),
            ("BitBucket",   "https://bitbucket.org/{}"),
            ("Roblox",      "https://www.roblox.com/user.aspx?username={}"),
            ("Imgur",       "https://imgur.com/user/{}"),
        ]

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        found = []
        not_found = []
        errors = []

        printc("\n\u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557", "cyan", True)
        printc("\u2551                 RESULTS                       \u2551", "cyan", True)
        printc("\u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2559", "cyan")
        print()

        for name, url_template in platforms:
            url = url_template.format(un)
            try:
                resp = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
                code = resp.status_code

                if code == 200:
                    found.append(name)
                    printc(f"  \u2705 {name:15s} FOUND      ", "green")
                elif code in (301, 302, 303, 307, 308):
                    if any(x in resp.url.lower() for x in ['notfound', '404', 'error', 'signup', 'login']):
                        not_found.append(name)
                        printc(f"  \u274c {name:15s} NOT FOUND  ", "red")
                    else:
                        found.append(name)
                        printc(f"  \u2705 {name:15s} FOUND      ", "green")
                elif code == 404:
                    not_found.append(name)
                    printc(f"  \u274c {name:15s} NOT FOUND  ", "red")
                elif code == 403:
                    errors.append(name)
                    printc(f"  \u26a0\ufe0f {name:15s} RATE LIMITED", "yellow")
                else:
                    not_found.append(name)
                    printc(f"  \u2753 {name:15s} {code}        ", "yellow")
            except requests.Timeout:
                errors.append(name)
                printc(f"  \u23f1\ufe0f {name:15s} TIMEOUT    ", "yellow")
            except Exception:
                errors.append(name)
                printc(f"  \u274c {name:15s} ERROR      ", "red")

        print()
        printc(f"  \U0001f4ca Results: {len(found)} found, {len(not_found)} not found, {len(errors)} errors", "cyan")
        print()
        save = input(cprint("\U0001f4be Save report? (y/n): ", "yellow")).strip().lower()
        if save == 'y':
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            fp = REPORTS_DIR / f"SHERLOCK_{un}_{ts}.json"
            report = {
                "username": un,
                "found": found,
                "not_found": not_found,
                "errors": errors,
                "total_checked": len(platforms)
            }
            with open(fp, "w") as f:
                json.dump(report, f, indent=2)
            printc(f"\u2705 Saved: {fp}", "green")


class GoogleDorkGenerator:
    def generate(self, target=None):
        clear()
        printc("╔═══════════════════════════════════════════════╗", "cyan", True)
        printc("║          \U0001f3af GOOGLE DORK GENERATOR             ║", "cyan", True)
        printc("╚═══════════════════════════════════════════════╝", "cyan")
        print()
        if not target:
            target = input(cprint("Target domain/site: ", "cyan")).strip()
        if not target:
            printc("\u274c Valid input required", "red")
            return

        dorks = [
            f"site:{target}",
            f"site:{target} intitle:index.of",
            f"site:{target} inurl:admin",
            f"site:{target} inurl:login",
            f"site:{target} inurl:wp-admin",
            f"site:{target} ext:pdf",
            f"site:{target} ext:sql",
            f"site:{target} ext:log",
            f"site:{target} ext:conf",
            f"site:{target} ext:bak",
            f"site:{target} ext:txt password",
            f"site:{target} \"password\" filetype:txt",
            f"site:{target} intext:\"index of\"",
            f"site:{target} intext:\"sql dump\"",
            f"site:{target} inurl:php?id=",
            f"site:{target} inurl:/etc/passwd",
            f"site:{target} \"robots.txt\"",
            f"site:{target} intitle:\"phpinfo\"",
            f"site:{target} intitle:\"login\" inurl:admin",
            f"site:{target} inurl:backup",
            f"site:{target} \"@gmail.com\"",
            f"site:{target} \"@yahoo.com\"",
            f"site:{target} confidential",
            f"site:{target} internal",
            f"site:{target} \"API key\"",
            f"\"@{target}\"",
            f"inurl:dashboard site:{target}",
        ]

        printc(f"\n    Generating {len(dorks)} dork queries for: {target}", "cyan", True)
        printc("    Copy and paste into Google search", "gray")
        print()
        for i, dork in enumerate(dorks, 1):
            printc(f"    {i:2d}. {dork}", "white")
        
        result = {"target": target, "dorks": dorks}
        print()
        save = input(cprint("\U0001f4be Save dorks? (y/n): ", "yellow")).strip().lower()
        if save == 'y':
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            fp = REPORTS_DIR / f"DORKS_{target}_{ts}.json"
            with open(fp, "w") as f:
                json.dump(result, f, indent=2)
            printc(f"\u2705 Saved: {fp}", "green")


class PasswordStrengthChecker:
    def check(self, pwd=None):
        clear()
        printc("╔═══════════════════════════════════════════════╗", "cyan", True)
        printc("║          \U0001f511 PASSWORD STRENGTH CHECKER          ║", "cyan", True)
        printc("╚═══════════════════════════════════════════════╝", "cyan")
        print()
        if not pwd:
            pwd = input(cprint("Password to check: ", "cyan")).strip()
        if not pwd:
            printc("\u274c Valid input required", "red")
            return
        
        length = len(pwd)
        has_upper = any(c.isupper() for c in pwd)
        has_lower = any(c.islower() for c in pwd)
        has_digit = any(c.isdigit() for c in pwd)
        has_special = any(not c.isalnum() for c in pwd)
        
        score = 0
        if length >= 8: score += 25
        if length >= 12: score += 15
        if length >= 16: score += 10
        if has_upper: score += 15
        if has_lower: score += 10
        if has_digit: score += 10
        if has_special: score += 15
        
        if score >= 80: level = "Very Strong", "green"
        elif score >= 60: level = "Strong", "cyan"
        elif score >= 40: level = "Medium", "yellow"
        elif score >= 20: level = "Weak", "red"
        else: level = "Very Weak", "red"

        printc(f"\n    \u25b6 Length:        {length} chars", "white")
        printc(f"    \u25b6 Uppercase:     {'\u2705' if has_upper else '\u274c'}", "white")
        printc(f"    \u25b6 Lowercase:     {'\u2705' if has_lower else '\u274c'}", "white")
        printc(f"    \u25b6 Digits:        {'\u2705' if has_digit else '\u274c'}", "white")
        printc(f"    \u25b6 Special chars: {'\u2705' if has_special else '\u274c'}", "white")
        printc(f"    \u25b6 Score:         {score}/100", "white")
        printc(f"    \u25b6 Strength:      {level[0]}", level[1], True)
        
        result = {
            "password_length": length,
            "has_uppercase": has_upper,
            "has_lowercase": has_lower,
            "has_digit": has_digit,
            "has_special": has_special,
            "score": score,
            "strength": level[0]
        }
        print()
        save = input(cprint("\U0001f4be Save report? (y/n): ", "yellow")).strip().lower()
        if save == 'y':
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            fp = REPORTS_DIR / f"PASSWORD_{ts}.json"
            with open(fp, "w") as f:
                json.dump(result, f, indent=2)
            printc(f"\u2705 Saved: {fp}", "green")


class ReverseImageSearch:
    def search(self, img_url=None):
        clear()
        printc("╔═══════════════════════════════════════════════╗", "cyan", True)
        printc("║          \U0001f5bc REVERSE IMAGE SEARCH              ║", "cyan", True)
        printc("╚═══════════════════════════════════════════════╝", "cyan")
        print()
        if not img_url:
            img_url = input(cprint("Image URL: ", "cyan")).strip()
        if not img_url:
            printc("\u274c Valid input required", "red")
            return

        import webbrowser
        searches = {
            "Google": f"https://www.google.com/searchbyimage?image_url={img_url}",
            "Bing": f"https://www.bing.com/images/search?view=detailv2&iss=sbi&q=imgurl:{img_url}",
            "TinEye": f"https://tineye.com/search?url={img_url}",
            "Yandex": f"https://yandex.com/images/search?url={img_url}&rpt=imageview"
        }

        printc("\n    \u25b6 Opening Google Images reverse search...", "cyan")
        webbrowser.open(searches["Google"])
        printc("    \u25b6 Search URLs:", "yellow")
        for name, url in searches.items():
            printc(f"      {name}: {url}", "gray")

        open_all = input(cprint("\n    Open all search engines? (y/n): ", "yellow")).strip().lower()
        if open_all == 'y':
            for name, url in list(searches.items())[1:]:
                webbrowser.open(url)
            printc("    \u2705 All opened in browser", "green")

        printc("\n    \U0001f4ca Reverse image search opens your browser - no API needed", "cyan")
        print()
        input(cprint("Press Enter to continue...", "yellow"))


class ExifAnalyzer:
    def analyze(self, path):
        """Extract metadata from image (EXIF data)."""
        clear()
        printc("\u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557", "cyan", True)
        printc("\u2551          \U0001f4f7 EXIF ANALYZER                   \u2551", "cyan", True)
        printc("\u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2559", "cyan")
        print()
        try:
            from PIL import Image
            from PIL.ExifTags import TAGS
            img = Image.open(path)
            exif_data = img._getexif()
            if exif_data:
                printc("\n  EXIF Metadata:", "green", True)
                for tag_id, value in exif_data.items():
                    tag = TAGS.get(tag_id, tag_id)
                    printc(f"  {tag:25s}: {value}", "yellow")
            else:
                printc("  No EXIF data found", "yellow")
        except ImportError:
            printc("  Install Pillow: pip install Pillow", "red")
            # Try with subprocess
            try:
                import subprocess
                result = subprocess.run(["exiftool", path], capture_output=True, text=True)
                if result.stdout:
                    for line in result.stdout.split('\n')[:30]:
                        printc(f"  {line.strip()}", "yellow")
                else:
                    printc("  exiftool not available either", "red")
            except:
                printc("  No EXIF tool available", "red")

class InstagramLookup:
    def lookup(self, un=None):
        clear()
        printc("╔═══════════════════════════════════════════════╗", "cyan", True)
        printc("║          📷 INSTAGRAM LOOKUP                 ║", "cyan", True)
        printc("╚═══════════════════════════════════════════════╝", "cyan")
        print()
        if not un:
            un = input(cprint("Instagram username: ", "cyan")).strip()
        if not un:
            printc("❌ Valid input required", "red")
            return
        try:
            import requests as _r
            with live_spinner(f"Checking @{un}..."):
                resp = _r.get(f"https://www.instagram.com/{un}/", timeout=15,
                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'},
                    allow_redirects=True)
            code = resp.status_code
        except Exception as e:
            printc(f"\n    ❌ Error: {e}", "red")
            print()
            input(cprint("Press Enter to continue...", "yellow"))
            return
        printc("\n╔═══════════════════════════════════════════════╗", "green", True)
        printc("║                 RESULTS                       ║", "green", True)
        printc("╚═══════════════════════════════════════════════╝", "green")
        if code == 200:
            printc(f"    ✅ @{un} exists on Instagram", "green")
            printc(f"    ▶ Profile: https://www.instagram.com/{un}/", "cyan")
            printc(f"    ▶ Status:   {'Public' if 'This Account is Private' not in resp.text else 'Private'}", "yellow")
            import re as _re
            nm = _re.search(r'<meta[^>]*content="([^"]+)"[^>]*og:title', resp.text)
            if nm:
                printc(f"    ▶ Name:     {nm.group(1)}", "white")
            result = {"username": un, "exists": True}
        else:
            printc(f"    ❌ @{un} not found on Instagram", "red")
            result = {"username": un, "exists": False}
        print()
        save = input(cprint("💾 Save report? (y/n): ", "yellow")).strip().lower()
        if save == 'y':
            from datetime import datetime
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            fp = REPORTS_DIR / f"INSTAGRAM_{un}_{ts}.json"
            with open(fp, "w") as f:
                import json
                json.dump(result, f, indent=2)

class CyberOSint:
    def __init__(self):
        init_db()

        self.modules = {
            # Network
            '1': ("IP Address Lookup", IPAddressLookup().lookup),
            '2': ("MAC Address Lookup", MACAddressLookup().lookup),
            '3': ("DNS Records Lookup", DNSRecordsLookup().lookup),
            '4': ("DNSDumpster Tool", DNSDumpsterTool().analyze),
            '5': ("SSL Certificate Checker", SSLChecker().check),
            '6': ("Technology Detector", TechDetector().detect),
            '7': ("Pincode Lookup", PincodeLookup().lookup),
            # Domain
            '8': ("Domain Intelligence", DomainIntelligence().investigate),
            '9': ("Subdomain Enumerator", SubdomainEnumerator().enumerate),
            '10': ("Wayback Machine Checker", WaybackChecker().check),
            # People
            '14': ("Advanced Phone Lookup", AdvLookup().lookup),
            '15': ("Number Leak Check", NumberLeak().check),
            '16': ("Number to UPI", NumberToUpi().lookup),
            '17': ("Aadhaar Lookup", AadhaarLookup().lookup),
            # Financial
            '18': ("UPI Verify", UpiVerify().verify),
            '20': ("PAN to GST", PanToGst().lookup),
            # Email
            '23': ("Leak Info Check", LeakInfoTool().check),
            '24': ("Temp Mail Detector", TempMailDetector().check),
            # Vehicle
            '26': ("Vehicle Info Check", VehicleInfo().lookup),
            # Gaming
            '27': ("Free Fire Lookup", FreeFireLookup().lookup),
            '28': ("BGMI Lookup", BgmiLookup().lookup),
            # Social
            '31': ("GitHub Profile", GitHubLookup().lookup),
            '32': ("Telegram Lookup", TelegramLookup().lookup),
            '33': ("Snapchat Lookup", SnapchatLookup().lookup),
            '34': ("Telegram ID Deep Lookup", TelegramIdInfo().lookup),
            '35': ("Sherlock Username Search", SherlockUsernameSearch().search),
            '47': ("Instagram Lookup", InstagramLookup().lookup),
            # Utilities
            '36': ("Google Dorks Generator", GoogleDorkGenerator().generate),
            '37': ("Image EXIF Analyzer", self.exif_analyzer),
            '38': ("Password Strength Checker", PasswordStrengthChecker().check),
            '39': ("BIN Lookup", BINLookup().lookup),
            '40': ("Hash Generator", HashGenerator().generate),
            '41': ("Text Encoder/Decoder", TextEncoder().run),
            '42': ("URL Expander", URLExpander().expand),
            '43': ("Reverse Image Search", ReverseImageSearch().search),
            # Security
            '44': ("CVE Search", CVESearch().search),
            '45': ("AbuseIPDB Checker", AbuseIPDBChecker().check),
            # System
            '46': ("WiFi Network Scanner", WiFiScanner().scan),
            '48': ("Pakistan Number Lookup", PkNumberLookup().lookup),
            '49': ("View Reports", self.view_reports),
            '50': ("Install Dependencies", self.install_deps),
            '0': ("Exit", self.exit_tool),
        
}


        self.categories = [
            ("NETWORK", ['1', '2', '3', '4', '5', '6', '7']),
            ("DOMAIN", ['8', '9', '10']),
            ("PEOPLE", ['14', '15', '16', '17', '48']),
            ("FINANCIAL", ['18', '20']),
            ("EMAIL", ['23', '24']),
            ("VEHICLE", ['26']),
            ("GAMING", ['27', '28']),
            ("SOCIAL", ['31', '32', '33', '34', '35', '47']),
            ("UTILITIES", ['36', '37', '38', '39', '40', '41', '42', '43']),
            ("SECURITY", ['44', '45']),
            ("SYSTEM", ['46', '49', '50', '0']),
        ]
        self.module_inputs = {
            '1': "IP Address: ",
            '3': "Domain for DNS lookup: ",
            '4': "Domain for DNSDumpster: ",
            '5': "Domain (e.g., google.com): ",
            '6': "URL for technology detection: ",
            '7': "Pincode (6 digits): ",
            '8': "Domain: ",
            '9': "Domain for subdomain enumeration: ",
            '10': "URL for Wayback Machine: ",
            '14': "Phone number (10 digits): ",
            '15': "Phone number (10 digits): ",
            '16': "Phone number (10 digits): ",
            '17': "Aadhaar number (12 digits): ",
            '18': "UPI ID (e.g., name@ybl): ",
            '20': "PAN number: ",
            '23': "Search term (email/phone/username): ",
            '26': "Vehicle Number / VIN: ",
            '27': "Free Fire UID: ",
            '28': "BGMI UID: ",
            '31': "GitHub username: ",
            '32': "Telegram ID or @username: ",
            '33': "Snapchat username: ",
            '34': "Telegram user ID: ",
            '35': "Username for Sherlock search: ",
            '47': "Instagram username: ",
            '36': "Target for dorks (blank for generic): ",
            '39': "BIN (first 6 digits of card): ",
            '42': "Short URL: ",
            '43': "Image URL: ",
            '44': "CVE ID or keyword: ",
            '45': "IP for AbuseIPDB check: ",
            '48': "Pakistan phone number: ",
        
}
    def print_banner(self):
        clear()
        printc("CyberOSINT Toolkit", "cyan", True)
        printc(f"📁 Reports: {REPORTS_DIR}", "blue")
        printc("="*60, "cyan")

    def exif_analyzer(self):
        path = input(cprint("Image path: ", "cyan")).strip()
        if os.path.exists(path):
            ExifAnalyzer().analyze(path)
        else:
            printc("File not found", "red")

    def view_reports(self):
        clear()
        printc("\u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557", "cyan", True)
        printc("\u2551            SAVED REPORTS             \u2551", "cyan", True)
        printc("\u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2559", "cyan")
        print()

        if not REPORTS_DIR.exists():
            printc("No reports directory", "red")
            return

        files = list(REPORTS_DIR.glob("*"))

        if not files:
            printc("No reports found", "yellow")
            return

        printc(f"Found {len(files)} report(s):", "green")
        printc("="*50, "cyan")

        categories = {}
        for file in files:
            name = file.name
            if name.startswith("IP_"):
                cat = "IP Reports"
            elif name.startswith("USERNAME_"):
                cat = "Username Reports"
            elif name.startswith("EMAIL_"):
                cat = "Email Reports"
            elif name.startswith("INSTAGRAM_"):
                cat = "Instagram Reports"
            elif name.startswith("DOMAIN_"):
                cat = "Domain Reports"
            elif name.startswith("PHONE_"):
                cat = "Phone Reports"
            elif name.startswith("PHONE_NAME_"):
                cat = "Phone Name Reports"
            elif name.startswith("IFSC_"):
                cat = "IFSC Reports"
            elif name.startswith("DORKS_"):
                cat = "Dork Reports"
            elif name.startswith("SUBDOMAINS_"):
                cat = "Subdomain Reports"
            elif name.startswith("BREACH_"):
                cat = "Breach Reports"
            elif name.startswith("PASSWORD_"):
                cat = "Password Reports"
            elif name.startswith("WAYBACK_"):
                cat = "Wayback Machine Reports"
            elif name.startswith("DNSDUMPSTER_"):
                cat = "DNSDumpster Reports"
            elif name.startswith("SHERLOCK_"):
                cat = "Sherlock Reports"
            elif name.startswith("TECH_DETECT_"):
                cat = "Tech Detection Reports"
            elif name.startswith("ABUSEIPDB_"):
                cat = "AbuseIPDB Reports"
            elif name.startswith("PHONE_DETAILS_"):
                cat = "Phone Details Reports"
            elif name.startswith("VEHICLE_"):
                cat = "Vehicle Reports"
            elif name.startswith("BOMBING_"):
                cat = "Bombing Reports"
            elif name.startswith("MAC_"):
                cat = "MAC Address Reports"
            elif name.startswith("DNS_RECORDS_"):
                cat = "DNS Records Reports"
            elif name.startswith("SSL_"):
                cat = "SSL Reports"
            elif name.startswith("URL_"):
                cat = "URL Reports"
            elif name.startswith("BIN_"):
                cat = "BIN Reports"
            elif name.startswith("CVE_"):
                cat = "CVE Reports"
            elif name.startswith("HASH_"):
                cat = "Hash Reports"
            elif name.startswith("ENCODE_"):
                cat = "Encoder Reports"
            elif name.startswith("WIFI_"):
                cat = "WiFi Reports"
            else:
                cat = "Other Reports"

            if cat not in categories:
                categories[cat] = []
            categories[cat].append(name)

        for cat, files in categories.items():
            printc(f"\n{cat} ({len(files)}):", "yellow", True)
            for f in files[:3]:
                printc(f"  📄 {f}", "gray")
            if len(files) > 3:
                printc(f"  ... and {len(files)-3} more", "gray")

        printc("\n" + "="*50, "cyan")

        printc("\nOptions:", "cyan")
        printc("1. Open reports folder", "yellow")
        printc("2. Clear all reports", "yellow")
        printc("3. Back", "yellow")

        choice = input(cprint("\nSelect: ", "green")).strip()

        if choice == "1":
            self.open_folder()
        elif choice == "2":
            self.clear_reports()

    def open_folder(self):
        try:
            if os.path.exists("/data/data/com.termux"):
                os.system(f"termux-open {REPORTS_DIR}")
            else:
                printc(f"Folder: {REPORTS_DIR}", "cyan")
        except:
            printc("Could not open folder", "red")

    def clear_reports(self):
        confirm = input(cprint("Delete ALL reports? (y/n): ", "red")).lower()
        if confirm == 'y':
            for file in REPORTS_DIR.glob("*"):
                try:
                    file.unlink()
                except:
                    pass
            printc("Reports cleared", "green")

    def install_deps(self):
        clear()
        printc("╔═══════════════════════════════════════════════╗", "yellow", True)
        printc("║          INSTALL DEPENDENCIES               ║", "yellow", True)
        printc("╚═══════════════════════════════════════════════╝", "yellow")
        print()

        import platform as _pf
        sys_os = _pf.system().lower()

        if sys_os == 'windows':
            pm = None
            printc("  [SYSTEM] Windows detected", "cyan")
            printc("  [INFO] Python packages only (pip)", "cyan")
            printc("  [INFO] Install exiftool manually from: https://exiftool.org", "cyan")
        elif 'android' in sys_os or os.path.exists('/data/data/com.termux'):
            printc("  [SYSTEM] Termux/Android detected", "cyan")
            pm = "pkg"
        elif sys_os == 'linux':
            printc("  [SYSTEM] Linux detected", "cyan")
            pm = "sudo apt"
        else:
            printc("  [SYSTEM] Unknown platform, using pip only", "cyan")
            pm = None

        print()
        printc("╔═══════════════════════════════════════════════╗", "cyan", True)
        printc("║           AVAILABLE COMMANDS                 ║", "cyan", True)
        printc("╚═══════════════════════════════════════════════╝", "cyan")
        print()

        commands = []
        if pm:
            pm_name = "pkg" if "pkg" in pm else "apt"
            commands.append(("Update packages", f"{pm} update -y"))
            commands.append(("Install Python", f'{pm} install python -y' if 'pkg' in pm else f'{pm} install python3 python3-pip -y'))
            commands.append(("Install exiftool", f"{pm} install exiftool -y"))

        commands.append(("Install pip packages", "pip install requests beautifulsoup4 phonenumbers python-whois dnspython Pillow"))
        commands.append(("Optional: toutatis", "pip install toutatis"))
        commands.append(("Optional: shodan", "pip install shodan"))
        commands.append(("Optional: theHarvester", "cd ~ && git clone https://github.com/laramies/theHarvester.git"))

        for name, cmd in commands:
            printc(f"  \u25b6 {name}:", "yellow", True)
            printc(f"    {cmd}", "gray")
            print()

        printc("═"*50, "cyan")

        install = input(cprint("\nRun basic installation? (y/n): ", "yellow")).lower()
        if install == 'y':
            run_commands = [c for c in commands if not c[0].startswith("Optional")]
            for name, cmd in run_commands:
                printc(f"\n  Installing {name}...", "cyan")
                os.system(cmd)
            printc("\n  Installation complete!", "green")
            print()
            input(cprint("Press Enter to continue...", "yellow"))
        else:
            print()
            input(cprint("Press Enter to continue...", "yellow"))

    def exit_tool(self):
        import sys as _sys
        printc("\nShutting down...", "red")
        for c in "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏":
            print(f"\r{c} Cleaning up...", end="")
            _sys.stdout.flush(); time.sleep(0.08)
        print("\r" + " " * 30 + "\r", end="")
        printc("👋 Exited. Goodbye!", "green", True)
        sys.exit(0)

    def main_menu(self):
        while True:
            self.print_banner()

            printc("📱 MAIN MENU:", "cyan", True)
            for cat_name, cat_keys in self.categories:
                printc(f"\n  {cat_name}", "cyan", True)
                for key in cat_keys:
                    if key in self.modules:
                        name, _ = self.modules[key]
                        printc(f"    {key:2}. {name}", "yellow")

            printc("\n" + "-" * 50, "cyan")

            try:
                choice = input(cprint("\nSelect module: ", "green")).strip()

                if choice in self.modules:
                    name, func = self.modules[choice]
                    printc(f"\n🚀 Launching: {name}", "cyan", True)
                    time.sleep(0.5)

                    if choice == '0':
                        func()
                    elif choice in self.module_inputs:
                        prompt = self.module_inputs[choice]
                        val = input(cprint(prompt, "cyan")).strip()
                        func(val if val else None)
                    else:
                        func()

                    if choice != '0':
                        input(cprint("\nPress Enter to continue...", "gray"))
                else:
                    printc("Invalid choice", "red")
                    time.sleep(1)

            except KeyboardInterrupt:
                printc("\n\nExiting...", "yellow")
                import sys as _sys
                for c in "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏":
                    print(f"\r{c} Bye!", end="")
                    _sys.stdout.flush(); time.sleep(0.06)
                print("\r" + " " * 20 + "\r", end="")
                sys.exit(0)
            except Exception as e:
                printc(f"Error: {str(e)}", "red")
                time.sleep(2)

def setup_api_key():
    global API_KEY
    while True:
        printc("\n" + "="*50, "yellow")
        printc("🔑 API ACCESS", "yellow", True)
        printc("="*50, "yellow")
        printc("Do you have a premium API key?", "cyan", True)
        printc("  1. Yes, I have a key", "yellow")
        printc("  2. No, use demo key (50/day limit)", "yellow")
        printc("  3. Get a key", "yellow")
        choice = input(cprint("\nSelect (1/2/3): ", "green")).strip()
        if choice == '1':
            key = input(cprint("Paste your key: ", "cyan")).strip()
            if not key:
                printc("Invalid key", "red")
                continue
            printc("\n⏳ Verifying key...", "yellow")
            old_key = API_KEY
            API_KEY = key
            try:
                test = requests.get("http://ip-api.com/json/8.8.8.8", timeout=10,
                    headers={'User-Agent': 'Mozilla/5.0'})
                if test.status_code == 200:
                    printc("✅ Key accepted!", "green")
                    return key
                else:
                    printc("❌ Invalid key!", "red")
                    API_KEY = old_key
            except:
                printc("❌ Error validating key!", "red")
                API_KEY = old_key
        elif choice == '2':
            printc("\nℹ️  Using demo key (cyber-osint-demo)", "yellow")
            printc("   Daily limit: 50 requests", "yellow")
            return "cyber-osint-demo"
        elif choice == '3':
            printc("\n📩 Message me on Telegram: @ftgamer2", "yellow", True)
            printc("⚠️  Note: Key is NOT free", "red", True)
            input(cprint("\nPress Enter to go back...", "gray"))
        else:
            printc("Invalid choice", "red")

def main():
    global API_KEY
    clear()
    printc("╔═══════════════════════════════════════════════╗", "red")
    printc("║           LEGAL DISCLAIMER                    ║", "red", True)
    printc("║ This tool is for EDUCATIONAL purposes         ║", "red")
    printc("║ and AUTHORIZED security testing only.         ║", "red")
    printc("║                                               ║", "red")
    printc("║ Use only:                                     ║", "red")
    printc("║  • On systems you own                         ║", "red")
    printc("║  • With explicit permission                   ║", "red")
    printc("║  • For learning OSINT techniques              ║", "red")
    printc("║                                               ║", "red")
    printc("║ The author is not responsible for misuse.     ║", "red")
    printc("╚═══════════════════════════════════════════════╝", "red")
    print()

    agree = input(cprint("Do you agree to these terms? (y/n): ", "yellow")).strip().lower()
    if agree != 'y':
        printc("❌ Agreement required to use this tool.", "red")
        sys.exit(0)

    API_KEY = setup_api_key()

    if not REQUESTS_AVAILABLE:
        printc("\n⚠️  WARNING: 'requests' module not found!", "red")
        printc("Install: pip install requests", "cyan")
        time.sleep(2)

    try:
        tool = CyberOSint()
        tool.main_menu()
    except KeyboardInterrupt:
        printc("\n\n👋 Goodbye!", "green")
        sys.exit(0)
    except Exception as e:
        printc(f"\n💥 Error: {str(e)}", "red")
        sys.exit(1)

if __name__ == "__main__":
    main()

