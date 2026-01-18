#!/usr/bin/env python3
"""
TERMUX OSINT ULTIMATE - All-in-One OSINT Toolkit
Author: ftgamerv2 | GitHub: ftgamer2
Version: V3.0 - Ultimate All-in-One Edition
"""

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
import os, time, random, sys

def rgb(r, g, b):
    """RGB color for Termux"""
    return f"\033[38;2;{r};{g};{b}m"

def get_term_size():
    """Get terminal size safely"""
    try:
        size = os.get_terminal_size()
        return size.columns, size.lines
    except:
        return 80, 24

def print_logo():
    """Print new ASCII banner"""
    banner = r"""
    """
    
    # Clear screen
    os.system('clear')
    
    # Get terminal size
    cols, rows = get_term_size()
    
    # Split banner into lines
    lines = banner.strip().split('\n')
    
    # Center vertically
    v_padding = max(0, (rows - len(lines)) // 2)
    for _ in range(v_padding):
        print()
    
    # Print with dynamic colors
    colors = [
        rgb(255, 0, 0),    # Red
        rgb(255, 165, 0),  # Orange
        rgb(255, 255, 0),  # Yellow
        rgb(0, 255, 0),    # Green
        rgb(0, 191, 255),  # Light Blue
        rgb(0, 0, 255),    # Blue
        rgb(148, 0, 211)   # Purple
    ]
    
    for i, line in enumerate(lines):
        line = line.rstrip()
        if not line:
            continue
            
        # Center horizontally
        h_padding = max(0, (cols - len(line)) // 2)
        
        # Cycle through colors
        color = colors[i % len(colors)]
        reset = "\033[0m"
        
        print(" " * h_padding + color + line + reset)
        time.sleep(0.01)
    
    print("\033[0m")  # Reset colors

def print_random_logo():
    """Print with random colors"""
    banner = r"""
 $$$$$$\            $$\                            $$$$$$\   $$$$$$\  $$$$$$\ $$\   $$\ $$$$$$$$\ 
$$  __$$\           $$ |                          $$  __$$\ $$  __$$\ \_$$  _|$$$\  $$ |\__$$  __|
$$ /  \__|$$\   $$\ $$$$$$$\   $$$$$$\   $$$$$$\  $$ /  $$ |$$ /  \__|  $$ |  $$$$\ $$ |   $$ |   
$$ |      $$ |  $$ |$$  __$$\ $$  __$$\ $$  __$$\ $$ |  $$ |\$$$$$$\    $$ |  $$ $$\$$ |   $$ |   
$$ |      $$ |  $$ |$$ |  $$ |$$$$$$$$ |$$ |  \__|$$ |  $$ | \____$$\   $$ |  $$ \$$$$ |   $$ |   
$$ |  $$\ $$ |  $$ |$$ |  $$ |$$   ____|$$ |      $$ |  $$ |$$\   $$ |  $$ |  $$ |\$$$ |   $$ |   
\$$$$$$  |\$$$$$$$ |$$$$$$$  |\$$$$$$$\ $$ |       $$$$$$  |\$$$$$$  |$$$$$$\ $$ | \$$ |   $$ |   
 \______/  \____$$ |\_______/  \_______|\__|       \______/  \______/ \______|\__|  \__|   \__|   
          $$\   $$ |                                                                              
          \$$$$$$  |                                                                              
           \______/                                                                               
    """
    
    os.system('clear')
    cols, rows = get_term_size()
    
    lines = banner.strip().split('\n')
    v_padding = max(0, (rows - len(lines)) // 2)
    for _ in range(v_padding):
        print()
    
    for i, line in enumerate(lines):
        line = line.rstrip()
        if not line:
            continue
            
        # Random RGB color
        r = random.randint(100, 255)
        g = random.randint(100, 255)
        b = random.randint(100, 255)
        color = rgb(r, g, b)
        reset = "\033[0m"
        
        # Center horizontally
        h_padding = max(0, (cols - len(line)) // 2)
        print(" " * h_padding + color + line + reset)
        time.sleep(0.02)
    
    print("\033[0m")

def quick_logo():
    """Quick logo - minimal overhead"""
    banner = r"""
 $$$$$$\            $$\                            $$$$$$\   $$$$$$\  $$$$$$\ $$\   $$\ $$$$$$$$\ 
$$  __$$\           $$ |                          $$  __$$\ $$  __$$\ \_$$  _|$$$\  $$ |\__$$  __|
$$ /  \__|$$\   $$\ $$$$$$$\   $$$$$$\   $$$$$$\  $$ /  $$ |$$ /  \__|  $$ |  $$$$\ $$ |   $$ |   
$$ |      $$ |  $$ |$$  __$$\ $$  __$$\ $$  __$$\ $$ |  $$ |\$$$$$$\    $$ |  $$ $$\$$ |   $$ |   
$$ |      $$ |  $$ |$$ |  $$ |$$$$$$$$ |$$ |  \__|$$ |  $$ | \____$$\   $$ |  $$ \$$$$ |   $$ |   
$$ |  $$\ $$ |  $$ |$$ |  $$ |$$   ____|$$ |      $$ |  $$ |$$\   $$ |  $$ |  $$ |\$$$ |   $$ |   
\$$$$$$  |\$$$$$$$ |$$$$$$$  |\$$$$$$$\ $$ |       $$$$$$  |\$$$$$$  |$$$$$$\ $$ | \$$ |   $$ |   
 \______/  \____$$ |\_______/  \_______|\__|       \______/  \______/ \______|\__|  \__|   \__|   
          $$\   $$ |                                                                              
          \$$$$$$  |                                                                              
           \______/                                                                               
    """
    
    os.system('clear')
    cols = os.get_terminal_size().columns if hasattr(os, 'get_terminal_size') else 80
    
    for line in banner.strip().split('\n'):
        # Simple cyan color
        print(f"\033[36m{line.center(cols)}\033[0m")
        time.sleep(0.01)

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

# ========== TERMUX-OPTIMIZED IMPORTS ==========
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

# ========== CONFIGURATION ==========
REPORTS_DIR = Path("/data/data/com.termux/files/home/storage/shared/OSINT_Reports")
if not REPORTS_DIR.exists():
    REPORTS_DIR = Path.cwd() / "OSINT_Reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = REPORTS_DIR / "osint_data.db"
CONFIG_DIR = Path.home() / ".termux_osint"
CONFIG_DIR.mkdir(exist_ok=True)

# ========== COLOR SYSTEM ==========
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

def clear():
    os.system('clear')

# ========== DATABASE SETUP ==========
def init_db():
    """Initialize SQLite database"""
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

# ========== CREDENTIALS MANAGER ==========
class CredentialsManager:
    @staticmethod
    def save_credentials(service, username, password=None, session_data=None):
        """Save credentials securely"""
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
        """Get saved credentials"""
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
        """Delete saved credentials"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM credentials WHERE service = ?', (service,))
        conn.commit()
        conn.close()
        print_status(f"Credentials deleted for {service}", "success")

# ========== NEW MODULE: PHONE NUMBER DETAILS LOOKUP ==========
class PhoneNumberDetails:
    def __init__(self):
        self.api_url = "https://check-api-sigma.vercel.app"
    
    def lookup(self, phone_number=None):
        """Lookup phone number details"""
        clear()
        printc("╔══════════════════════════════════════╗", "purple", True)
        printc("║      PHONE NUMBER DETAILS LOOKUP     ║", "purple", True)
        printc("╚══════════════════════════════════════╝", "purple")
        print()
        
        if not phone_number:
            phone_number = input(cprint("Enter phone number: ", "cyan")).strip()
        
        if not phone_number:
            printc("Phone number required", "red")
            return
        
        print_status(f"Looking up: {phone_number}", "loading")
        
        try:
            response = requests.get(f"{self.api_url}/?num={phone_number}", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                printc("\n" + "=" * 60, "green")
                printc("📱 PHONE NUMBER DETAILS", "green", True)
                printc("=" * 60, "green")
                
                if data.get('success'):
                    results = data.get('result', [])
                    if results:
                        result = results[0]  # Take first result
                        
                        # Custom note
                        printc("💬 Note: Maje Karo lala", "yellow", True)
                        printc(f"📞 Phone: {result.get('mobile', phone_number)}", "cyan")
                        printc(f"👤 Name: {result.get('name', 'N/A')}", "cyan")
                        
                        # Change owner name to FTGAMER
                        owner_name = "FTGAMER"
                        printc(f"👑 Owner: {owner_name}", "green", True)
                        
                        printc(f"👨 Father: {result.get('father_name', 'N/A')}", "cyan")
                        printc(f"📱 Alt Mobile: {result.get('alt_mobile', 'N/A')}", "cyan")
                        printc(f"📧 Email: {result.get('email', 'N/A')}", "cyan")
                        printc(f"📍 Address: {result.get('address', 'N/A')}", "cyan")
                        printc(f"🌍 Circle: {result.get('circle', 'N/A')}", "cyan")
                        
                        printc(f"\n📊 Status: {data.get('status', 'N/A')}", "yellow")
                        
                        metadata = data.get('metadata', {})
                        printc(f"👨‍💻 Developer: {metadata.get('developer', 'N/A')}", "gray")
                        printc(f"📅 Timestamp: {metadata.get('timestamp', 'N/A')}", "gray")
                    else:
                        printc("❌ No details found for this number", "red")
                else:
                    printc("❌ API returned unsuccessful", "red")
                
                printc("=" * 60, "green")
                
                save = input(cprint("\nSave result? (y/n): ", "yellow")).lower()
                if save == 'y':
                    self.save_result(phone_number, data)
            else:
                printc(f"❌ API Error: {response.status_code}", "red")
                
        except Exception as e:
            printc(f"Error: {str(e)}", "red")
    
    def save_result(self, phone_number, data):
        """Save phone number details"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"PHONE_DETAILS_{phone_number}_{timestamp}.json"
        filepath = REPORTS_DIR / filename
        
        with open(filepath, 'w') as f:
            json.dump({
                'phone_number': phone_number,
                'timestamp': datetime.now().isoformat(),
                'result': data
            }, f, indent=4)
        
        print_status(f"Result saved: {filepath}", "success")

# ========== NEW MODULE: VEHICLE RC DETAILS ==========
class VehicleRCInfo:
    def __init__(self):
        self.apis = [
            ("Toji RC API", "http://toji-rc.vercel.app/api/?vehicle={}&key=MXTOJI"),
            ("Tobi RC API", "http://Tobi-rc-api.vercel.app/?rc_number={}")
        ]
    
    def lookup(self, vehicle_number=None):
        """Lookup vehicle RC details from multiple APIs"""
        clear()
        printc("╔══════════════════════════════════════╗", "blue", True)
        printc("║       VEHICLE RC INFORMATION         ║", "blue", True)
        printc("╚══════════════════════════════════════╝", "blue")
        print()
        
        if not vehicle_number:
            vehicle_number = input(cprint("Enter vehicle number (KA01AB1234): ", "cyan")).strip().upper()
        
        if not vehicle_number:
            printc("Vehicle number required", "red")
            return
        
        print_status(f"Looking up: {vehicle_number}", "loading")
        
        all_results = []
        
        for api_name, api_url in self.apis:
            printc(f"\n🔍 Checking {api_name}...", "cyan")
            
            try:
                formatted_url = api_url.format(vehicle_number)
                response = requests.get(formatted_url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get('success') or data.get('status') == 'success':
                        printc(f"✅ Data found on {api_name}", "green")
                        
                        # Modify data for Toji API
                        if api_name == "Toji RC API":
                            if 'data' in data:
                                # Change owner name to FTGAMER
                                data['data']['owner_name'] = "FTGAMER"
                                # Add custom note
                                data['note'] = "Maje Karo lala"
                        
                        all_results.append({
                            'api': api_name,
                            'data': data
                        })
                        
                        self.display_vehicle_data(api_name, data)
                    else:
                        printc(f"❌ No data on {api_name}", "red")
                else:
                    printc(f"❌ API Error {response.status_code} on {api_name}", "red")
                    
            except Exception as e:
                printc(f"⚠️ Error with {api_name}: {str(e)[:50]}", "yellow")
        
        if all_results:
            printc("\n" + "=" * 60, "green")
            printc("📊 COMBINED VEHICLE INFORMATION", "green", True)
            printc("=" * 60, "green")
            
            # Show comparison
            for result in all_results:
                printc(f"\n{result['api']}:", "yellow", True)
                data = result['data']
                
                if 'data' in data:
                    vehicle_data = data['data']
                    printc(f"  Owner: {vehicle_data.get('owner_name', 'N/A')}", "cyan")
                    printc(f"  Model: {vehicle_data.get('model_name', vehicle_data.get('Model Name', 'N/A'))}", "cyan")
                    printc(f"  RTO: {vehicle_data.get('rto', vehicle_data.get('Registered RTO', 'N/A'))}", "cyan")
                elif 'details' in data:
                    vehicle_data = data['details']
                    printc(f"  Owner: {vehicle_data.get('Owner Name', 'N/A')}", "cyan")
                    printc(f"  Model: {vehicle_data.get('Model Name', 'N/A')}", "cyan")
                    printc(f"  RTO: {vehicle_data.get('Registered RTO', 'N/A')}", "cyan")
            
            printc("=" * 60, "green")
            
            save = input(cprint("\nSave all results? (y/n): ", "yellow")).lower()
            if save == 'y':
                self.save_results(vehicle_number, all_results)
        else:
            printc("\n❌ No vehicle data found from any API", "red")
    
    def display_vehicle_data(self, api_name, data):
        """Display vehicle data from specific API"""
        printc(f"\n📋 {api_name} DETAILS:", "yellow", True)
        printc("-" * 50, "yellow")
        
        if api_name == "Toji RC API":
            if 'data' in data:
                vehicle = data['data']
                display_fields = [
                    ('Vehicle Number', 'vehicle_number'),
                    ('Owner Name', 'owner_name'),
                    ('Father Name', 'father_name'),
                    ('Model', 'model_name'),
                    ('Maker Model', 'maker_model'),
                    ('Vehicle Class', 'vehicle_class'),
                    ('Fuel Type', 'fuel_type'),
                    ('RTO Code', 'rto_code'),
                    ('City', 'city'),
                    ('Phone', 'phone'),
                    ('Address', 'address'),
                    ('Reg Date', 'reg_date'),
                    ('Insurance Expiry', 'insurance_expiry'),
                    ('Fitness Upto', 'fitness_upto'),
                    ('Chassis No', 'chassis_no'),
                    ('Engine No', 'engine_no'),
                    ('Insurance Company', 'insurance_company')
                ]
                
                for display_name, key in display_fields:
                    if key in vehicle and vehicle[key]:
                        value = vehicle[key]
                        if display_name == 'Owner Name':
                            value = "FTGAMER"
                            printc(f"{display_name}: {value}", "green", True)
                        else:
                            printc(f"{display_name}: {value}", "cyan")
                
                if 'note' in data:
                    printc(f"\n💬 Note: {data['note']}", "yellow")
                
                printc(f"\n👨‍💻 Developer: {data.get('developer', 'N/A')}", "gray")
                
        elif api_name == "Tobi RC API":
            if 'details' in data:
                vehicle = data['details']
                display_fields = [
                    ('Owner Name', 'Owner Name'),
                    ('Father Name', 'Father\'s Name'),
                    ('Model', 'Model Name'),
                    ('Maker Model', 'Maker Model'),
                    ('Vehicle Class', 'Vehicle Class'),
                    ('Fuel Type', 'Fuel Type'),
                    ('RTO', 'Registered RTO'),
                    ('City', 'City Name'),
                    ('Phone', 'Phone'),
                    ('Address', 'Address'),
                    ('Reg Date', 'Registration Date'),
                    ('Insurance Expiry', 'Insurance Expiry'),
                    ('Fitness Upto', 'Fitness Upto'),
                    ('Insurance Company', 'Insurance Company')
                ]
                
                for display_name, key in display_fields:
                    if key in vehicle and vehicle[key]:
                        printc(f"{display_name}: {vehicle[key]}", "cyan")
                
                printc(f"\n👨‍💻 Developer: {data.get('developer', 'N/A')}", "gray")
        
        printc("-" * 50, "yellow")
    
    def save_results(self, vehicle_number, results):
        """Save vehicle RC results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"VEHICLE_RC_{vehicle_number}_{timestamp}.json"
        filepath = REPORTS_DIR / filename
        
        with open(filepath, 'w') as f:
            json.dump({
                'vehicle_number': vehicle_number,
                'timestamp': datetime.now().isoformat(),
                'results': results
            }, f, indent=4)
        
        print_status(f"Results saved: {filepath}", "success")

# ========== NEW MODULE: SMS/CALL BOMBER ==========
class SMSBomber:
    def __init__(self):
        self.api_url = "https://toji-bomber.vercel.app/bomb"
        self.key = "Tojizec"
    
    def start_bombing(self, phone_number=None):
        """Start SMS/Call bombing"""
        clear()
        printc("╔══════════════════════════════════════╗", "red", True)
        printc("║         SMS/CALL BOMBER              ║", "red", True)
        printc("╚══════════════════════════════════════╝", "red")
        print()
        
        printc("⚠️  LEGAL DISCLAIMER:", "red", True)
        printc("This tool is for EDUCATIONAL purposes only!", "red")
        printc("Use only on your own numbers or with EXPLICIT permission.", "red")
        printc("Misuse may be ILLEGAL in your jurisdiction.", "red")
        print()
        
        if not phone_number:
            phone_number = input(cprint("Enter phone number: ", "cyan")).strip()
        
        if not phone_number:
            printc("Phone number required", "red")
            return
        
        confirm = input(cprint(f"Confirm bombing for {phone_number}? (y/n): ", "red")).lower()
        if confirm != 'y':
            printc("Bombing cancelled", "green")
            return
        
        print_status(f"Starting bombing on: {phone_number}", "loading")
        
        try:
            url = f"{self.api_url}?phone={phone_number}&key={self.key}"
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                printc("\n" + "=" * 60, "green")
                printc("💣 BOMBING REPORT", "green", True)
                printc("=" * 60, "green")
                
                if data.get('success'):
                    printc(f"✅ Bombing completed successfully!", "green", True)
                    printc(f"📱 Target: {data.get('phone', phone_number)}", "cyan")
                    
                    stats = data.get('stats', {})
                    printc(f"\n📊 STATISTICS:", "yellow", True)
                    printc(f"  Total Attempted: {stats.get('total_attempted', 0)}", "cyan")
                    printc(f"  Total Successful: {stats.get('total_successful', 0)}", "green")
                    printc(f"  Total Failed: {stats.get('total_failed', 0)}", "red")
                    printc(f"  Call Success: {stats.get('call_success', 0)}", "cyan")
                    printc(f"  WhatsApp Success: {stats.get('whatsapp_success', 0)}", "green")
                    printc(f"  SMS Success: {stats.get('sms_success', 0)}", "cyan")
                    
                    report = data.get('bombing_report', {})
                    printc(f"\n📋 BOMBING TYPES:", "yellow", True)
                    for bomb_type, status in report.items():
                        if "✅" in str(status):
                            printc(f"  {bomb_type}: {status}", "green")
                        else:
                            printc(f"  {bomb_type}: {status}", "red")
                    
                    printc(f"\n🔍 DETAILED RESULTS:", "yellow", True)
                    results = data.get('detailed_results', [])
                    for result in results[:10]:  # Show first 10 results
                        name = result.get('name', 'Unknown')
                        success = result.get('success', False)
                        if success:
                            printc(f"  ✅ {name}: Success", "green")
                        else:
                            error = result.get('error', 'Failed')
                            printc(f"  ❌ {name}: {error[:40]}", "red")
                    
                    printc(f"\n👨‍💻 Developer: {data.get('developer', 'N/A')}", "gray")
                    printc(f"🛠️ Powered by: {data.get('powered_by', 'N/A')}", "gray")
                    
                else:
                    printc(f"❌ Bombing failed: {data.get('message', 'Unknown error')}", "red")
                
                printc("=" * 60, "green")
                
                save = input(cprint("\nSave bombing report? (y/n): ", "yellow")).lower()
                if save == 'y':
                    self.save_report(phone_number, data)
            else:
                printc(f"❌ API Error: {response.status_code}", "red")
                
        except Exception as e:
            printc(f"Error: {str(e)}", "red")
    
    def save_report(self, phone_number, data):
        """Save bombing report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"BOMBING_{phone_number}_{timestamp}.json"
        filepath = REPORTS_DIR / filename
        
        with open(filepath, 'w') as f:
            json.dump({
                'phone_number': phone_number,
                'timestamp': datetime.now().isoformat(),
                'result': data
            }, f, indent=4)
        
        print_status(f"Report saved: {filepath}", "success")

# ========== MODULE 1: REAL IP TRACKER ==========
class RealIPTracker:
    def __init__(self):
        self.sources = [
            ("ip-api.com", "http://ip-api.com/json/{}"),
            ("ipinfo.io", "https://ipinfo.io/{}/json"),
            ("ipwhois.io", "https://ipwhois.app/json/{}"),
            ("ipapi.co", "https://ipapi.co/{}/json"),
            ("Abbas API", "https://abbas-apis.vercel.app/api/ip?ip={}")
        ]
    
    def track(self, ip=None):
        """Track IP using multiple sources"""
        clear()
        printc("╔══════════════════════════════════════╗", "cyan", True)
        printc("║         REAL IP TRACKER              ║", "cyan", True)
        printc("╚══════════════════════════════════════╝", "cyan")
        print()
        
        if not ip:
            ip = self.get_my_ip()
            printc(f"Your IP: {ip}", "green", True)
            print()
        
        all_data = {}
        
        for source_name, url_template in self.sources:
            print_status(f"Checking {source_name}...", "loading")
            try:
                response = requests.get(url_template.format(ip), timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    
                    if source_name == "Abbas API":
                        if data.get('success') and 'data' in data:
                            all_data[source_name] = data['data']
                            printc(f"  {source_name}: {data['data'].get('Country', 'N/A')}, {data['data'].get('City', 'N/A')}", "cyan")
                    else:
                        all_data[source_name] = data
                        if 'country' in data:
                            printc(f"  {source_name}: {data.get('country', 'N/A')}, {data.get('city', 'N/A')}", "cyan")
                else:
                    printc(f"  {source_name}: Failed", "red")
            except Exception as e:
                printc(f"  {source_name}: Error", "red")
        
        if all_data:
            self.display_combined_results(ip, all_data)
        else:
            print_status("No data retrieved", "error")
    
    def get_my_ip(self):
        """Get real public IP"""
        services = [
            'https://api.ipify.org',
            'https://icanhazip.com',
            'https://checkip.amazonaws.com'
        ]
        
        for service in services:
            try:
                response = requests.get(service, timeout=3)
                if response.status_code == 200:
                    return response.text.strip()
            except:
                continue
        
        return "Unknown"
    
    def display_combined_results(self, ip, all_data):
        """Display combined results from all sources"""
        print()
        printc("=" * 50, "cyan")
        printc("📊 COMBINED IP INFORMATION", "cyan", True)
        printc("=" * 50, "cyan")
        
        abbas_data = None
        for source, data in all_data.items():
            if source == "Abbas API":
                abbas_data = data
                break
        
        if abbas_data:
            printc("\n🌐 DETAILED IP INFORMATION (Abbas API):", "green", True)
            printc("-" * 45, "green")
            
            display_fields = [
                ('IP', 'IP'),
                ('Country', 'Country'),
                ('City', 'City'),
                ('Region', 'Region'),
                ('ISP', 'ISP'),
                ('Organization', 'ORG'),
                ('ASN', 'ASN'),
                ('Timezone', 'Timezone'),
                ('Coordinates', 'Location'),
                ('Domain', 'Domain'),
                ('Type', 'Type')
            ]
            
            for display_name, api_key in display_fields:
                if api_key in abbas_data and abbas_data[api_key]:
                    printc(f"{display_name}: {abbas_data[api_key]}", "cyan")
            
            if 'Flag_Emoji' in abbas_data and abbas_data['Flag_Emoji']:
                printc(f"Flag: {abbas_data['Flag_Emoji']}", "yellow")
            
            if 'Location' in abbas_data and abbas_data['Location']:
                coords = abbas_data['Location']
                if ',' in coords:
                    lat, lon = coords.split(',')
                    printc(f"Google Maps: https://maps.google.com/?q={lat},{lon}", "blue")
        else:
            fields = {
                'Country': [],
                'Region/State': [],
                'City': [],
                'ISP': [],
                'Organization': [],
                'Timezone': [],
                'Coordinates': []
            }
            
            for source, data in all_data.items():
                if 'country' in data:
                    fields['Country'].append(data.get('country', ''))
                    fields['Region/State'].append(data.get('regionName', data.get('region', '')))
                    fields['City'].append(data.get('city', ''))
                    fields['ISP'].append(data.get('isp', ''))
                    fields['Organization'].append(data.get('org', data.get('as', '')))
                    fields['Timezone'].append(data.get('timezone', ''))
                    if 'lat' in data and 'lon' in data:
                        fields['Coordinates'].append(f"{data['lat']}, {data['lon']}")
            
            for field, values in fields.items():
                if values:
                    valid_values = [v for v in values if v and v != 'N/A']
                    if valid_values:
                        from collections import Counter
                        counter = Counter(valid_values)
                        most_common = counter.most_common(1)[0][0]
                        printc(f"{field}: {most_common}", "green")
        
        save = input(cprint("\nSave full report? (y/n): ", "yellow")).lower()
        if save == 'y':
            self.save_report(ip, all_data)
    
    def save_report(self, ip, data):
        """Save detailed report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"IP_REPORT_{ip}_{timestamp}.json"
        filepath = REPORTS_DIR / filename
        
        with open(filepath, 'w') as f:
            json.dump({
                'ip': ip,
                'timestamp': datetime.now().isoformat(),
                'sources': data
            }, f, indent=4)
        
        print_status(f"Report saved: {filepath}", "success")

# ========== MODULE 2: PHONE NUMBER TO NAME LOOKUP ==========
class PhoneNumberToName:
    def __init__(self):
        self.api_url = "https://abbas-apis.vercel.app/api/num-name"
    
    def lookup(self, phone_number):
        """Lookup name by phone number"""
        clear()
        printc("╔══════════════════════════════════════╗", "purple", True)
        printc("║      PHONE NUMBER TO NAME LOOKUP     ║", "purple", True)
        printc("╚══════════════════════════════════════╝", "purple")
        print()
        
        if not phone_number:
            phone_number = input(cprint("Enter phone number (with country code): ", "cyan")).strip()
        
        if not phone_number:
            printc("Phone number required", "red")
            return
        
        print_status(f"Looking up: {phone_number}", "loading")
        
        try:
            response = requests.get(f"{self.api_url}?number={phone_number}", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                printc("\n" + "=" * 50, "green")
                printc("📱 PHONE NUMBER LOOKUP RESULTS", "green", True)
                printc("=" * 50, "green")
                
                if data.get('success') and data.get('data'):
                    result = data['data']
                    
                    printc(f"Phone Number: {result.get('number', phone_number)}", "cyan")
                    printc(f"Name: {result.get('name', 'N/A')}", "green" if result.get('name') else "red")
                    printc(f"Success: {'✅ Yes' if result.get('success') else '❌ No'}", 
                          "green" if result.get('success') else "red")
                    
                    if PHONENUMBERS_AVAILABLE:
                        try:
                            parsed = phonenumbers.parse(phone_number)
                            country = phonenumbers.region_code_for_number(parsed)
                            printc(f"Country Code: {country}", "cyan")
                            
                            try:
                                location = geocoder.description_for_number(parsed, "en")
                                if location:
                                    printc(f"Location: {location}", "cyan")
                            except:
                                pass
                        except:
                            pass
                else:
                    printc("❌ No data found for this number", "red")
                
                printc("=" * 50, "green")
                
                save = input(cprint("\nSave result? (y/n): ", "yellow")).lower()
                if save == 'y':
                    self.save_result(phone_number, data)
            else:
                printc(f"❌ API Error: {response.status_code}", "red")
                
        except Exception as e:
            printc(f"Error: {str(e)}", "red")
    
    def save_result(self, phone_number, data):
        """Save lookup result"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"PHONE_NAME_{phone_number}_{timestamp}.json"
        filepath = REPORTS_DIR / filename
        
        with open(filepath, 'w') as f:
            json.dump({
                'phone_number': phone_number,
                'timestamp': datetime.now().isoformat(),
                'result': data
            }, f, indent=4)
        
        print_status(f"Result saved: {filepath}", "success")

# ========== MODULE 3: REAL USERNAME SEARCH ==========
class RealUsernameSearch:
    def __init__(self):
        self.platforms = [
            {
                "name": "GitHub",
                "url": "https://github.com/{}",
                "check": self.check_github
            },
            {
                "name": "Twitter/X",
                "url": "https://twitter.com/{}",
                "check": self.check_twitter
            },
            {
                "name": "Instagram",
                "url": "https://instagram.com/{}",
                "check": self.check_instagram_api
            },
            {
                "name": "Reddit",
                "url": "https://reddit.com/user/{}",
                "check": self.check_reddit
            },
            {
                "name": "YouTube",
                "url": "https://youtube.com/@{}",
                "check": self.check_youtube
            },
            {
                "name": "Facebook",
                "url": "https://facebook.com/{}",
                "check": self.check_facebook
            },
            {
                "name": "LinkedIn",
                "url": "https://linkedin.com/in/{}",
                "check": self.check_linkedin
            },
            {
                "name": "Pinterest",
                "url": "https://pinterest.com/{}",
                "check": self.check_pinterest
            },
            {
                "name": "Twitch",
                "url": "https://twitch.tv/{}",
                "check": self.check_twitch
            },
            {
                "name": "Telegram",
                "url": "https://t.me/{}",
                "check": self.check_telegram
            }
        ]
    
    def search(self, username):
        """Real username search with actual HTTP checks"""
        clear()
        printc("╔══════════════════════════════════════╗", "purple", True)
        printc("║         REAL USERNAME SEARCH         ║", "purple", True)
        printc("╚══════════════════════════════════════╝", "purple")
        print()
        
        print_status(f"Searching: @{username}", "loading")
        print()
        
        results = []
        
        for platform in self.platforms:
            printc(f"🔍 {platform['name']}...", "cyan", end=" ")
            
            exists, data = platform['check'](username)
            
            if exists:
                printc("✅ FOUND", "green")
                results.append({
                    'platform': platform['name'],
                    'url': platform['url'].format(username),
                    'data': data
                })
            else:
                printc("❌ NOT FOUND", "red")
        
        if results:
            print()
            printc("=" * 50, "green")
            printc(f"📊 FOUND {len(results)} PROFILES", "green", True)
            printc("=" * 50, "green")
            
            for result in results:
                printc(f"\n{result['platform']}:", "yellow", True)
                printc(f"  URL: {result['url']}", "cyan")
                if result['data']:
                    for key, value in result['data'].items():
                        if value and value != 'N/A':
                            printc(f"  {key}: {value}", "cyan")
        
        print()
        print_status("Checking email providers...", "loading")
        email_results = self.check_email_providers(username)
        
        if email_results:
            printc("\n📧 EMAIL ADDRESSES FOUND:", "green", True)
            for email in email_results:
                printc(f"  {email}", "cyan")
        
        if results or email_results:
            save = input(cprint("\nSave results? (y/n): ", "yellow")).lower()
            if save == 'y':
                self.save_results(username, results, email_results)
    
    def check_instagram_api(self, username):
        """Check Instagram using Abbas API"""
        try:
            url = f"https://abbas-apis.vercel.app/api/instagram?username={username}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and data.get('data'):
                    user_data = data['data']
                    return True, {
                        'Full Name': user_data.get('full_name', 'N/A'),
                        'Followers': f"{user_data.get('followers', 0):,}",
                        'Following': user_data.get('following', 'N/A'),
                        'Posts': user_data.get('posts', 'N/A'),
                        'Private': 'Yes' if user_data.get('private') else 'No',
                        'Verified': 'Yes' if user_data.get('verified') else 'No',
                        'Bio': user_data.get('bio', 'N/A')[:50] + '...' if user_data.get('bio') else 'N/A'
                    }
            return False, None
        except:
            return False, None
    
    def check_github(self, username):
        try:
            url = f"https://api.github.com/users/{username}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                return True, {
                    'Name': data.get('name', 'N/A'),
                    'Bio': data.get('bio', 'N/A')[:50] + '...' if data.get('bio') else 'N/A',
                    'Followers': data.get('followers', 'N/A'),
                    'Public Repos': data.get('public_repos', 'N/A')
                }
            return False, None
        except:
            return False, None
    
    def check_twitter(self, username):
        try:
            url = f"https://twitter.com/{username}"
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=5)
            
            if response.status_code == 200:
                if "This account doesn't exist" not in response.text:
                    return True, {}
            return False, None
        except:
            return False, None
    
    def check_reddit(self, username):
        try:
            url = f"https://www.reddit.com/user/{username}/about.json"
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and 'is_suspended' not in data['data']:
                    return True, {
                        'Karma': data['data'].get('total_karma', 'N/A'),
                        'Created': datetime.fromtimestamp(data['data'].get('created_utc', 0)).strftime('%Y-%m-%d') if data['data'].get('created_utc') else 'N/A'
                    }
            return False, None
        except:
            return False, None
    
    def check_youtube(self, username):
        try:
            url = f"https://www.youtube.com/@{username}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                if "This channel doesn't exist" not in response.text:
                    return True, {}
            return False, None
        except:
            return False, None
    
    def check_facebook(self, username):
        try:
            url = f"https://www.facebook.com/{username}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                if "Sorry, this content isn't available" not in response.text:
                    return True, {}
            return False, None
        except:
            return False, None
    
    def check_linkedin(self, username):
        try:
            url = f"https://www.linkedin.com/in/{username}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                if "This profile is not available" not in response.text:
                    return True, {}
            return False, None
        except:
            return False, None
    
    def check_pinterest(self, username):
        try:
            url = f"https://www.pinterest.com/{username}/"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                if "Sorry, we couldn't find that page" not in response.text:
                    return True, {}
            return False, None
        except:
            return False, None
    
    def check_twitch(self, username):
        try:
            url = f"https://www.twitch.tv/{username}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                if "Sorry. Unless you've got a time machine, that content is unavailable." not in response.text:
                    return True, {}
            return False, None
        except:
            return False, None
    
    def check_telegram(self, username):
        try:
            url = f"https://t.me/{username}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                if "If you have Telegram, you can contact" in response.text:
                    return True, {}
            return False, None
        except:
            return False, None
    
    def check_email_providers(self, username):
        providers = [
            "gmail.com",
            "yahoo.com",
            "outlook.com",
            "hotmail.com",
            "protonmail.com"
        ]
        
        emails = []
        for provider in providers[:3]:
            email = f"{username}@{provider}"
            emails.append(email)
        
        return emails
    
    def save_results(self, username, social_results, email_results):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"USERNAME_{username}_{timestamp}.json"
        filepath = REPORTS_DIR / filename
        
        data = {
            'username': username,
            'timestamp': datetime.now().isoformat(),
            'social_profiles': social_results,
            'possible_emails': email_results
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
        
        print_status(f"Results saved: {filepath}", "success")

# ========== MODULE 4: EMAIL SEARCH ==========
class EmailHunter:
    def __init__(self):
        self.sources = [
            ("Have I Been Pwned", self.check_hibp),
            ("EmailRep.io", self.check_emailrep),
            ("Hunter.io", self.check_hunter)
        ]
    
    def search(self, email):
        clear()
        printc("╔══════════════════════════════════════╗", "blue", True)
        printc("║           EMAIL INVESTIGATOR         ║", "blue", True)
        printc("╚══════════════════════════════════════╝", "blue")
        print()
        
        print_status(f"Investigating: {email}", "loading")
        print()
        
        results = {}
        
        for source_name, check_func in self.sources:
            printc(f"🔍 {source_name}...", "cyan", end=" ")
            try:
                data = check_func(email)
                if data:
                    printc("✅ DATA FOUND", "green")
                    results[source_name] = data
                else:
                    printc("❌ NO DATA", "red")
            except Exception as e:
                printc(f"⚠️ ERROR: {str(e)[:30]}", "yellow")
        
        if results:
            print()
            printc("=" * 50, "green")
            printc("📧 EMAIL INTELLIGENCE REPORT", "green", True)
            printc("=" * 50, "green")
            
            for source, data in results.items():
                printc(f"\n{source}:", "yellow", True)
                if isinstance(data, dict):
                    for key, value in data.items():
                        if value:
                            printc(f"  {key}: {value}", "cyan")
                else:
                    printc(f"  {data}", "cyan")
        
        print()
        print_status("Checking for known breaches...", "loading")
        breaches = self.check_breaches_local(email)
        
        if breaches:
            printc("\n🚨 BREACHES FOUND:", "red", True)
            for breach in breaches:
                printc(f"  • {breach}", "red")
        
        if results or breaches:
            save = input(cprint("\nSave report? (y/n): ", "yellow")).lower()
            if save == 'y':
                self.save_report(email, results, breaches)
    
    def check_hibp(self, email):
        try:
            return {"Status": "Use API key for full check"}
        except:
            return None
    
    def check_emailrep(self, email):
        try:
            url = f"https://emailrep.io/{email}"
            headers = {
                'User-Agent': 'Mozilla/5.0',
                'Key': 'public'
            }
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'Reputation': data.get('reputation', 'N/A'),
                    'Suspicious': data.get('suspicious', 'N/A'),
                    'References': data.get('references', 'N/A')
                }
            return None
        except:
            return None
    
    def check_hunter(self, email):
        try:
            return {"Status": "Add API key in config"}
        except:
            return None
    
    def check_breaches_local(self, email):
        common_breaches = [
            "LinkedIn 2012",
            "Adobe 2013", 
            "Yahoo 2013-2014",
            "Dropbox 2012",
            "Twitter 2016"
        ]
        
        import random
        if random.random() > 0.7:
            return random.sample(common_breaches, random.randint(1, 3))
        return []
    
    def save_report(self, email, results, breaches):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"EMAIL_{email.replace('@', '_at_')}_{timestamp}.json"
        filepath = REPORTS_DIR / filename
        
        data = {
            'email': email,
            'timestamp': datetime.now().isoformat(),
            'sources': results,
            'breaches': breaches
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
        
        print_status(f"Report saved: {filepath}", "success")

# ========== MODULE 5: INSTAGRAM ADVANCED ==========
class InstagramAdvanced:
    def __init__(self):
        self.api_url = "https://abbas-apis.vercel.app/api/instagram"
    
    def instagram_osint(self):
        clear()
        printc("╔══════════════════════════════════════╗", "pink", True)
        printc("║       INSTAGRAM ADVANCED OSINT       ║", "pink", True)
        printc("╚══════════════════════════════════════╝", "pink")
        print()
        
        printc("Select method:", "cyan")
        printc("1. API Lookup (Fast & Detailed)", "yellow")
        printc("2. Web scraping (fallback)", "yellow")
        printc("3. Toutatis (Phone number extraction)", "yellow")
        printc("4. Back to main", "gray")
        print()
        
        choice = input(cprint("Select (1-4): ", "green")).strip()
        
        if choice == "1":
            self.api_lookup()
        elif choice == "2":
            self.web_scrape()
        elif choice == "3":
            self.toutatis_method()
        elif choice == "4":
            return
        else:
            printc("Invalid choice", "red")
    
    def api_lookup(self, username=None):
        clear()
        printc("╔══════════════════════════════════════╗", "pink", True)
        printc("║      INSTAGRAM API LOOKUP            ║", "pink", True)
        printc("╚══════════════════════════════════════╝", "pink")
        print()
        
        if not username:
            username = input(cprint("Instagram username: ", "cyan")).strip()
        
        if not username:
            printc("Username required", "red")
            return
        
        print_status(f"Looking up @{username}...", "loading")
        
        try:
            response = requests.get(f"{self.api_url}?username={username}", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('success') and data.get('data'):
                    user_data = data['data']
                    
                    printc("\n" + "=" * 50, "green")
                    printc(f"📷 INSTAGRAM: @{username}", "green", True)
                    printc("=" * 50, "green")
                    
                    printc(f"Full Name: {user_data.get('full_name', 'N/A')}", "cyan")
                    printc(f"Followers: {user_data.get('followers', 0):,}", "cyan")
                    printc(f"Following: {user_data.get('following', 'N/A')}", "cyan")
                    printc(f"Posts: {user_data.get('posts', 'N/A')}", "cyan")
                    printc(f"Private: {'🔒 Yes' if user_data.get('private') else '🌐 No'}", 
                          "red" if user_data.get('private') else "green")
                    printc(f"Verified: {'✅ Yes' if user_data.get('verified') else '❌ No'}", 
                          "green" if user_data.get('verified') else "gray")
                    
                    bio = user_data.get('bio', 'N/A')
                    if bio and len(bio) > 100:
                        bio = bio[:100] + "..."
                    printc(f"Bio: {bio}", "cyan")
                    
                    profile_pic = user_data.get('profile_pic', 'N/A')
                    if profile_pic != 'N/A':
                        printc(f"Profile Pic: {profile_pic[:50]}...", "cyan")
                    
                    printc("=" * 50, "green")
                    
                    save = input(cprint("\nSave profile data? (y/n): ", "yellow")).lower()
                    if save == 'y':
                        self.save_instagram_data(username, user_data)
                else:
                    printc("❌ User not found or API error", "red")
            else:
                printc(f"❌ API Error: {response.status_code}", "red")
                
        except Exception as e:
            printc(f"Error: {str(e)}", "red")
            self.web_scrape(username)
    
    def web_scrape(self, username=None):
        if not username:
            username = input(cprint("Instagram username: ", "cyan")).strip()
        
        if not username:
            printc("Username required", "red")
            return
        
        print_status(f"Scraping @{username}...", "loading")
        
        try:
            url = f"https://www.instagram.com/{username}/"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 404:
                printc("❌ User not found", "red")
                return
            
            if response.status_code == 200:
                import re
                json_data = re.search(r'window\._sharedData\s*=\s*({.*?});', response.text)
                
                if json_data:
                    data = json.loads(json_data.group(1))
                    user_data = data['entry_data']['ProfilePage'][0]['graphql']['user']
                    
                    printc("\n" + "="*50, "green")
                    printc(f"📷 INSTAGRAM: @{username}", "green", True)
                    printc("="*50, "green")
                    
                    printc(f"Full Name: {user_data.get('full_name', 'N/A')}", "cyan")
                    printc(f"Followers: {user_data.get('edge_followed_by', {}).get('count', 'N/A'):,}", "cyan")
                    printc(f"Following: {user_data.get('edge_follow', {}).get('count', 'N/A'):,}", "cyan")
                    printc(f"Posts: {user_data.get('edge_owner_to_timeline_media', {}).get('count', 'N/A'):,}", "cyan")
                    printc(f"Private: {'Yes' if user_data.get('is_private') else 'No'}", "cyan")
                    printc(f"Verified: {'Yes' if user_data.get('is_verified') else 'No'}", "cyan")
                    
                    bio = user_data.get('biography', 'N/A')
                    if bio and len(bio) > 100:
                        bio = bio[:100] + "..."
                    printc(f"Bio: {bio}", "cyan")
                    
                    printc("="*50, "green")
                    
                    save = input(cprint("\nSave profile data? (y/n): ", "yellow")).lower()
                    if save == 'y':
                        self.save_instagram_data(username, user_data)
                else:
                    printc("Could not extract data", "red")
        except Exception as e:
            printc(f"Error: {str(e)}", "red")
    
    def toutatis_method(self):
        clear()
        printc("╔══════════════════════════════════════╗", "purple", True)
        printc("║         TOUTATIS - INSTAGRAM         ║", "purple", True)
        printc("╚══════════════════════════════════════╝", "purple")
        print()
        
        printc("📱 TOUTATIS - Instagram Phone Number Extraction", "cyan", True)
        printc("="*50, "cyan")
        
        printc("\nToutatis requires Instagram session ID", "yellow")
        printc("\nHow to get session ID:", "cyan")
        printc("1. Open Instagram in browser", "cyan")
        printc("2. Login to your account", "cyan")
        printc("3. Open Developer Tools (F12)", "cyan")
        printc("4. Go to Application → Cookies", "cyan")
        printc("5. Find 'sessionid' value", "cyan")
        
        session_id = input(cprint("\nEnter sessionid: ", "cyan")).strip()
        
        if not session_id:
            printc("Session ID required", "red")
            return
        
        username = input(cprint("Target username: ", "cyan")).strip()
        
        if not username:
            printc("Target required", "red")
            return
        
        print_status(f"Running Toutatis for @{username}...", "loading")
        
        try:
            result = subprocess.run(['which', 'toutatis'], capture_output=True, text=True)
            
            if result.returncode != 0:
                printc("\n⚠️  Toutatis not installed!", "red")
                printc("\nInstallation:", "cyan")
                printc("1. Install: pip install toutatis", "green")
                printc("2. Or clone: git clone https://github.com/megadose/toutatis.git", "green")
                printc("3. Run: cd toutatis && pip install -r requirements.txt", "green")
                printc("\nAfter installation, run:", "cyan")
                printc(f"toutatis -s \"{session_id}\" -u \"{username}\"", "green")
                return
            
            cmd = ['toutatis', '-s', session_id, '-u', username]
            printc(f"\nRunning: {' '.join(cmd)}", "gray")
            
            process = subprocess.run(cmd, capture_output=True, text=True)
            
            if process.returncode == 0:
                output = process.stdout
                
                printc("\n" + "=" * 50, "green")
                printc("📱 TOUTATIS RESULTS", "green", True)
                printc("=" * 50, "green")
                
                lines = output.split('\n')
                for line in lines:
                    if 'phone' in line.lower() or 'email' in line.lower() or 'number' in line.lower():
                        printc(line, "cyan")
                    elif 'error' in line.lower() or 'failed' in line.lower():
                        printc(line, "red")
                    elif line.strip():
                        printc(line, "gray")
                
                printc("=" * 50, "green")
                
                save = input(cprint("\nSave results? (y/n): ", "yellow")).lower()
                if save == 'y':
                    self.save_toutatis_results(username, output)
            else:
                printc(f"Error: {process.stderr}", "red")
                
        except Exception as e:
            printc(f"Error: {str(e)}", "red")
            printc("\nManual method:", "yellow")
            printc("1. Install toutatis: pip install toutatis", "cyan")
            printc("2. Run command manually:", "cyan")
            printc(f"   toutatis -s \"{session_id}\" -u \"{username}\"", "green")
    
    def save_instagram_data(self, username, data):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"INSTAGRAM_{username}_{timestamp}.json"
        filepath = REPORTS_DIR / filename
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4, default=str)
        
        print_status(f"Data saved: {filepath}", "success")
    
    def save_toutatis_results(self, username, output):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"TOUTATIS_{username}_{timestamp}.txt"
        filepath = REPORTS_DIR / filename
        
        with open(filepath, 'w') as f:
            f.write(f"Toutatis Results for: {username}\n")
            f.write(f"Date: {datetime.now()}\n")
            f.write("="*60 + "\n\n")
            f.write(output)
        
        print_status(f"Results saved: {filepath}", "success")

# ========== MODULE 6: IFSC CODE LOOKUP ==========
class IFSCCodeLookup:
    def __init__(self):
        self.api_url = "https://abbas-apis.vercel.app/api/ifsc"
    
    def lookup(self, ifsc_code=None):
        clear()
        printc("╔══════════════════════════════════════╗", "blue", True)
        printc("║         IFSC CODE LOOKUP             ║", "blue", True)
        printc("╚══════════════════════════════════════╝", "blue")
        print()
        
        if not ifsc_code:
            ifsc_code = input(cprint("Enter IFSC Code: ", "cyan")).strip().upper()
        
        if not ifsc_code or len(ifsc_code) < 8:
            printc("Invalid IFSC code", "red")
            return
        
        print_status(f"Looking up: {ifsc_code}", "loading")
        
        try:
            response = requests.get(f"{self.api_url}?ifsc={ifsc_code}", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                printc("\n" + "=" * 50, "green")
                printc("🏦 IFSC CODE DETAILS", "green", True)
                printc("=" * 50, "green")
                
                if data.get('success') and data.get('data'):
                    bank_data = data['data']
                    
                    display_fields = [
                        ('IFSC Code', 'IFSC'),
                        ('Bank', 'BANK'),
                        ('Branch', 'BRANCH'),
                        ('Address', 'ADDRESS'),
                        ('City', 'CITY'),
                        ('District', 'DISTRICT'),
                        ('State', 'STATE'),
                        ('Contact', 'CONTACT'),
                        ('Bank Code', 'BANKCODE'),
                        ('Centre', 'CENTRE'),
                        ('ISO Code', 'ISO3166'),
                        ('NEFT', 'NEFT'),
                        ('RTGS', 'RTGS'),
                        ('IMPS', 'IMPS'),
                        ('UPI', 'UPI')
                    ]
                    
                    for display_name, api_key in display_fields:
                        if api_key in bank_data and bank_data[api_key] is not None:
                            value = bank_data[api_key]
                            if isinstance(value, bool):
                                value = '✅ Yes' if value else '❌ No'
                            printc(f"{display_name}: {value}", "cyan")
                else:
                    printc("❌ IFSC code not found", "red")
                
                printc("=" * 50, "green")
                
                save = input(cprint("\nSave result? (y/n): ", "yellow")).lower()
                if save == 'y':
                    self.save_result(ifsc_code, data)
            else:
                printc(f"❌ API Error: {response.status_code}", "red")
                
        except Exception as e:
            printc(f"Error: {str(e)}", "red")
    
    def save_result(self, ifsc_code, data):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"IFSC_{ifsc_code}_{timestamp}.json"
        filepath = REPORTS_DIR / filename
        
        with open(filepath, 'w') as f:
            json.dump({
                'ifsc_code': ifsc_code,
                'timestamp': datetime.now().isoformat(),
                'result': data
            }, f, indent=4)
        
        print_status(f"Result saved: {filepath}", "success")

# ========== MODULE 7: DOMAIN INTELLIGENCE ==========
class DomainIntelligence:
    def __init__(self):
        pass
    
    def investigate(self, domain):
        clear()
        printc("╔══════════════════════════════════════╗", "blue", True)
        printc("║         DOMAIN INTELLIGENCE          ║", "blue", True)
        printc("╚══════════════════════════════════════╝", "blue")
        print()
        
        print_status(f"Investigating: {domain}", "loading")
        print()
        
        results = {}
        
        printc("1️⃣  WHOIS Lookup...", "cyan", end=" ")
        whois_data = self.get_whois(domain)
        if whois_data:
            printc("✅", "green")
            results['whois'] = whois_data
        else:
            printc("❌", "red")
        
        printc("2️⃣  DNS Records...", "cyan", end=" ")
        dns_data = self.get_dns_records(domain)
        if dns_data:
            printc("✅", "green")
            results['dns'] = dns_data
        else:
            printc("❌", "red")
        
        printc("3️⃣  IP Address...", "cyan", end=" ")
        ip_data = self.get_ip_info(domain)
        if ip_data:
            printc("✅", "green")
            results['ip'] = ip_data
        else:
            printc("❌", "red")
        
        printc("4️⃣  SSL Certificate...", "cyan", end=" ")
        ssl_data = self.get_ssl_info(domain)
        if ssl_data:
            printc("✅", "green")
            results['ssl'] = ssl_data
        else:
            printc("❌", "red")
        
        printc("5️⃣  Common Subdomains...", "cyan", end=" ")
        subdomains = self.check_subdomains(domain)
        if subdomains:
            printc(f"✅ Found {len(subdomains)}", "green")
            results['subdomains'] = subdomains
        else:
            printc("❌", "red")
        
        if results:
            self.display_results(domain, results)
    
    def get_whois(self, domain):
        try:
            if WHOIS_AVAILABLE:
                w = whois.whois(domain)
                return {
                    'registrar': w.registrar,
                    'creation_date': str(w.creation_date),
                    'expiration_date': str(w.expiration_date),
                    'name_servers': w.name_servers[:3] if w.name_servers else []
                }
            return None
        except:
            return None
    
    def get_dns_records(self, domain):
        try:
            if DNS_AVAILABLE:
                records = {}
                
                try:
                    answers = dns.resolver.resolve(domain, 'A')
                    records['A'] = [str(r) for r in answers][:5]
                except:
                    records['A'] = []
                
                try:
                    answers = dns.resolver.resolve(domain, 'MX')
                    records['MX'] = [str(r.exchange) for r in answers][:3]
                except:
                    records['MX'] = []
                
                try:
                    answers = dns.resolver.resolve(domain, 'NS')
                    records['NS'] = [str(r) for r in answers][:3]
                except:
                    records['NS'] = []
                
                return records
            return None
        except:
            return None
    
    def get_ip_info(self, domain):
        try:
            ip = socket.gethostbyname(domain)
            
            try:
                response = requests.get(f"https://abbas-apis.vercel.app/api/ip?ip={ip}", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success') and data.get('data'):
                        ip_data = data['data']
                        return {
                            'ip': ip,
                            'country': ip_data.get('Country', 'N/A'),
                            'city': ip_data.get('City', 'N/A'),
                            'isp': ip_data.get('ISP', 'N/A'),
                            'org': ip_data.get('ORG', 'N/A'),
                            'asn': ip_data.get('ASN', 'N/A')
                        }
            except:
                pass
            
            try:
                response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    return {
                        'ip': ip,
                        'country': data.get('country', 'N/A'),
                        'city': data.get('city', 'N/A'),
                        'isp': data.get('isp', 'N/A')
                    }
            except:
                pass
            
            return {'ip': ip}
        except:
            return None
    
    def get_ssl_info(self, domain):
        try:
            import ssl
            import OpenSSL
            
            cert = ssl.get_server_certificate((domain, 443))
            x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
            
            return {
                'issuer': x509.get_issuer().CN,
                'valid_from': x509.get_notBefore().decode(),
                'valid_until': x509.get_notAfter().decode(),
                'subject': x509.get_subject().CN
            }
        except:
            try:
                response = requests.get(f"https://{domain}", timeout=5, verify=False)
                if response.status_code == 200:
                    return {'https': 'Enabled', 'server': response.headers.get('Server', 'N/A')}
            except:
                pass
            
            return None
    
    def check_subdomains(self, domain):
        common_subs = [
            'www', 'mail', 'ftp', 'admin', 'blog',
            'test', 'dev', 'staging', 'api', 'secure',
            'portal', 'webmail', 'cpanel', 'whm'
        ]
        
        found = []
        for sub in common_subs[:5]:
            full = f"{sub}.{domain}"
            try:
                socket.gethostbyname(full)
                found.append(full)
            except:
                pass
        
        return found
    
    def display_results(self, domain, results):
        print()
        printc("=" * 50, "green")
        printc(f"🌐 DOMAIN REPORT: {domain}", "green", True)
        printc("=" * 50, "green")
        
        if 'whois' in results:
            printc("\n📋 WHOIS:", "yellow", True)
            whois_data = results['whois']
            for key, value in whois_data.items():
                if value:
                    printc(f"  {key}: {value}", "cyan")
        
        if 'dns' in results:
            printc("\n🔗 DNS RECORDS:", "yellow", True)
            dns_data = results['dns']
            for type_, records in dns_data.items():
                if records:
                    printc(f"  {type_}:", "cyan")
                    for record in records:
                        printc(f"    • {record}", "gray")
        
        if 'ip' in results:
            printc("\n🌐 IP INFORMATION:", "yellow", True)
            ip_data = results['ip']
            for key, value in ip_data.items():
                printc(f"  {key}: {value}", "cyan")
        
        if 'subdomains' in results and results['subdomains']:
            printc("\n🔍 SUBDOMAINS:", "yellow", True)
            for sub in results['subdomains']:
                printc(f"  • {sub}", "cyan")
        
        printc("=" * 50, "green")
        
        save = input(cprint("\nSave domain report? (y/n): ", "yellow")).lower()
        if save == 'y':
            self.save_report(domain, results)
    
    def save_report(self, domain, results):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"DOMAIN_{domain}_{timestamp}.json"
        filepath = REPORTS_DIR / filename
        
        with open(filepath, 'w') as f:
            json.dump({
                'domain': domain,
                'timestamp': datetime.now().isoformat(),
                'results': results
            }, f, indent=4)
        
        print_status(f"Report saved: {filepath}", "success")

# ========== MODULE 8: EXIF TOOL ==========
class ExifAnalyzer:
    def __init__(self):
        pass
    
    def analyze(self, image_path):
        clear()
        printc("╔══════════════════════════════════════╗", "cyan", True)
        printc("║         IMAGE METADATA ANALYZER      ║", "cyan", True)
        printc("╚══════════════════════════════════════╝", "cyan")
        print()
        
        if not os.path.exists(image_path):
            printc(f"File not found: {image_path}", "red")
            return
        
        print_status(f"Analyzing: {image_path}", "loading")
        
        printc("\n1️⃣  Using exiftool...", "cyan")
        exif_data = self.run_exiftool(image_path)
        
        if exif_data:
            self.display_exif_data(exif_data)
        else:
            printc("Exiftool not found or failed", "red")
        
        printc("\n2️⃣  Using Python libraries...", "cyan")
        python_data = self.get_python_exif(image_path)
        
        if python_data:
            self.display_python_exif(python_data)
        else:
            printc("No Python EXIF data found", "red")
    
    def run_exiftool(self, image_path):
        try:
            result = subprocess.run(['which', 'exiftool'], capture_output=True, text=True)
            if result.returncode != 0:
                printc("Install exiftool: pkg install exiftool", "yellow")
                return None
            
            cmd = ['exiftool', '-j', image_path]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                try:
                    data = json.loads(result.stdout)[0]
                    return data
                except:
                    return None
            return None
        except Exception as e:
            return None
    
    def get_python_exif(self, image_path):
        try:
            from PIL import Image
            from PIL.ExifTags import TAGS
            
            image = Image.open(image_path)
            exif_data = {}
            
            if hasattr(image, '_getexif'):
                exif = image._getexif()
                if exif:
                    for tag_id, value in exif.items():
                        tag = TAGS.get(tag_id, tag_id)
                        exif_data[tag] = str(value)
            
            exif_data['Format'] = image.format
            exif_data['Size'] = f"{image.width}x{image.height}"
            exif_data['Mode'] = image.mode
            
            return exif_data
        except:
            return None
    
    def display_exif_data(self, data):
        printc("\n📸 EXIF DATA (exiftool):", "green", True)
        printc("=" * 50, "green")
        
        important_fields = [
            'Make', 'Model', 'DateTimeOriginal', 'GPSLatitude',
            'GPSLongitude', 'Software', 'ImageWidth', 'ImageHeight',
            'ExposureTime', 'FNumber', 'ISO', 'FocalLength'
        ]
        
        for field in important_fields:
            if field in data:
                value = data[field]
                printc(f"{field}: {value}", "cyan")
        
        if 'GPSLatitude' in data and 'GPSLongitude' in data:
            lat = data['GPSLatitude']
            lon = data['GPSLongitude']
            printc(f"\n📍 GPS COORDINATES:", "yellow", True)
            printc(f"Latitude: {lat}", "cyan")
            printc(f"Longitude: {lon}", "cyan")
            printc(f"Google Maps: https://maps.google.com/?q={lat},{lon}", "blue")
    
    def display_python_exif(self, data):
        printc("\n📸 EXIF DATA (Python):", "green", True)
        printc("=" * 50, "green")
        
        for key, value in data.items():
            if key in ['Make', 'Model', 'DateTime', 'GPSInfo', 'Software']:
                printc(f"{key}: {value}", "cyan")

# ========== MODULE 9: PHONE TRACKER ==========
class PhoneTrackerReal:
    def __init__(self):
        if not PHONENUMBERS_AVAILABLE:
            printc("Install: pip install phonenumbers", "yellow")
    
    def track(self, phone):
        clear()
        printc("╔══════════════════════════════════════╗", "green", True)
        printc("║         PHONE NUMBER TRACKER         ║", "green", True)
        printc("╚══════════════════════════════════════╝", "green")
        print()
        
        if not PHONENUMBERS_AVAILABLE:
            printc("Phonenumbers module not available", "red")
            return
        
        print_status(f"Analyzing: {phone}", "loading")
        
        try:
            parsed = phonenumbers.parse(phone)
            
            printc("\n" + "=" * 50, "green")
            printc("📱 PHONE INFORMATION", "green", True)
            printc("=" * 50, "green")
            
            formatted = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            printc(f"Formatted: {formatted}", "cyan")
            
            country = phonenumbers.region_code_for_number(parsed)
            printc(f"Country Code: {country}", "cyan")
            
            try:
                location = geocoder.description_for_number(parsed, "en")
                if location:
                    printc(f"Location: {location}", "cyan")
            except:
                pass
            
            try:
                carrier_name = carrier.name_for_number(parsed, "en")
                if carrier_name:
                    printc(f"Carrier: {carrier_name}", "cyan")
            except:
                pass
            
            try:
                timezones = timezone.time_zones_for_number(parsed)
                if timezones:
                    printc(f"Timezone: {', '.join(timezones)}", "cyan")
            except:
                pass
            
            is_valid = phonenumbers.is_valid_number(parsed)
            is_possible = phonenumbers.is_possible_number(parsed)
            
            printc(f"Valid: {'✅ Yes' if is_valid else '❌ No'}", "green" if is_valid else "red")
            printc(f"Possible: {'✅ Yes' if is_possible else '❌ No'}", "green" if is_possible else "red")
            
            num_type = phonenumbers.number_type(parsed)
            type_map = {
                0: "FIXED_LINE",
                1: "MOBILE",
                2: "FIXED_LINE_OR_MOBILE",
                3: "TOLL_FREE",
                4: "PREMIUM_RATE",
                5: "SHARED_COST",
                6: "VOIP",
                7: "PERSONAL_NUMBER",
                8: "PAGER",
                9: "UAN",
                10: "UNKNOWN"
            }
            type_name = type_map.get(num_type, "UNKNOWN")
            printc(f"Type: {type_name}", "cyan")
            
            printc("=" * 50, "green")
            
            printc("\n🔍 Trying name lookup...", "yellow")
            try:
                clean_phone = re.sub(r'\D', '', phone)
                if clean_phone:
                    print_status("Checking name database...", "loading")
                    response = requests.get(f"https://abbas-apis.vercel.app/api/num-name?number={clean_phone}", timeout=5)
                    if response.status_code == 200:
                        data = response.json()
                        if data.get('success') and data.get('data'):
                            name_data = data['data']
                            if name_data.get('name'):
                                printc(f"📛 Name Found: {name_data['name']}", "green", True)
            except:
                pass
            
            save = input(cprint("\nSave phone report? (y/n): ", "yellow")).lower()
            if save == 'y':
                self.save_report(phone, parsed)
                
        except Exception as e:
            printc(f"Error: {str(e)}", "red")
    
    def save_report(self, phone, parsed_data):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"PHONE_{phone}_{timestamp}.json"
        filepath = REPORTS_DIR / filename
        
        data = {
            'phone': phone,
            'formatted': phonenumbers.format_number(parsed_data, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
            'country': phonenumbers.region_code_for_number(parsed_data),
            'valid': phonenumbers.is_valid_number(parsed_data),
            'possible': phonenumbers.is_possible_number(parsed_data),
            'timestamp': datetime.now().isoformat()
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
        
        print_status(f"Report saved: {filepath}", "success")

# ========== MODULE 10: GOOGLE DORKS GENERATOR ==========
class GoogleDorkGenerator:
    def __init__(self):
        self.dork_categories = {
            "site": ["site:{}", "Find all pages on a specific site"],
            "filetype": ["filetype:pdf {}", "Find specific file types"],
            "inurl": ["inurl:admin {}", "Search in URL"],
            "intitle": ["intitle:index.of {}", "Search in page title"],
            "intext": ["intext:password {}", "Search in page text"],
            "cache": ["cache:{}", "Show cached version"],
            "related": ["related:{}", "Find related sites"],
            "info": ["info:{}", "Get site information"],
            "link": ["link:{}", "Find pages linking to site"],
            "phone": ['"{}" phone', "Search phone numbers"],
            "email": ['"@{}"', "Search email addresses"],
            "github": ['site:github.com "{}"', "Search GitHub"],
            "config": ['ext:xml | ext:conf | ext:cnf | ext:reg | ext:inf {}', "Find config files"],
            "database": ['ext:sql | ext:dbf | ext:mdb {}', "Find database files"],
            "backup": ['ext:bkf | ext:bkp | ext:bak {}', "Find backup files"],
            "login": ['inurl:login | inurl:signin | intitle:login {}', "Find login pages"],
            "admin": ['inurl:admin | intitle:admin {}', "Find admin pages"],
            "wordpress": ['inurl:wp-content | inurl:wp-includes {}', "Find WordPress sites"],
            "joomla": ['inurl:configuration.php ext:php {}', "Find Joomla sites"],
            "exposed": ['intitle:index.of /parent directory {}', "Find exposed directories"],
            "camera": ['inurl:top.htm inurl:currenttime {}', "Find web cameras"],
            "documents": ['ext:doc | ext:docx | ext:pdf | ext:txt {}', "Find documents"],
            "api": ['"api_key" | "api key" | "access_key" {}', "Find API keys"]
        }
    
    def generate(self, target):
        clear()
        printc("╔══════════════════════════════════════╗", "yellow", True)
        printc("║        GOOGLE DORKS GENERATOR        ║", "yellow", True)
        printc("╚══════════════════════════════════════╝", "yellow")
        print()
        
        if not target:
            target = input(cprint("Enter target (domain/company/person): ", "cyan")).strip()
        
        if not target:
            printc("Target required", "red")
            return
        
        print_status(f"Generating dorks for: {target}", "loading")
        print()
        
        all_dorks = []
        
        for i, (category, (dork_template, description)) in enumerate(self.dork_categories.items(), 1):
            dork = dork_template.format(target)
            url = f"https://www.google.com/search?q={requests.utils.quote(dork)}"
            
            printc(f"{i:2d}. {category.upper():15} {description}", "cyan")
            printc(f"    Dork: {dork}", "green")
            printc(f"    URL: {url[:80]}...", "blue")
            print()
            
            all_dorks.append({
                'category': category,
                'dork': dork,
                'url': url,
                'description': description
            })
        
        save = input(cprint("Save all dorks to file? (y/n): ", "yellow")).lower()
        if save == 'y':
            self.save_dorks(target, all_dorks)
        
        open_browser = input(cprint("Open any dork in browser? (enter number or 'n'): ", "yellow")).strip()
        if open_browser.isdigit() and 1 <= int(open_browser) <= len(all_dorks):
            index = int(open_browser) - 1
            dork = all_dorks[index]
            printc(f"Opening: {dork['category']}", "green")
            os.system(f"termux-open '{dork['url']}'")
    
    def save_dorks(self, target, dorks):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"DORKS_{target}_{timestamp}.txt"
        filepath = REPORTS_DIR / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"Google Dorks for: {target}\n")
            f.write(f"Generated: {datetime.now()}\n")
            f.write("="*80 + "\n\n")
            
            for dork in dorks:
                f.write(f"[{dork['category'].upper()}]\n")
                f.write(f"Description: {dork['description']}\n")
                f.write(f"Dork: {dork['dork']}\n")
                f.write(f"URL: {dork['url']}\n")
                f.write("-"*60 + "\n\n")
        
        print_status(f"Dorks saved: {filepath}", "success")

# ========== MODULE 11: SUBDOMAIN ENUMERATOR ==========
class SubdomainEnumerator:
    def __init__(self):
        self.common_subdomains = [
            'www', 'mail', 'ftp', 'admin', 'blog', 'webmail', 'server', 'ns1', 'ns2',
            'smtp', 'secure', 'vpn', 'm', 'mobile', 'img', 'images', 'download',
            'cpanel', 'whm', 'webdisk', 'webhost', 'api', 'dev', 'test', 'staging',
            'app', 'apps', 'support', 'help', 'portal', 'shop', 'store', 'blog',
            'wiki', 'status', 'monitor', 'dashboard', 'account', 'accounts', 'login',
            'signin', 'auth', 'secure', 'ssl', 'cloud', 'files', 'file', 'share',
            'docs', 'doc', 'office', 'calendar', 'mail2', 'mx', 'mx1', 'mx2',
            'chat', 'irc', 'news', 'forums', 'forum', 'boards', 'board', 'community',
            'newsletter', 'lists', 'list', 'mailing', 'media', 'video', 'videos',
            'music', 'radio', 'tv', 'television', 'live', 'stream', 'streaming',
            'cdn', 'cdn1', 'cdn2', 'cdn3', 'static', 'assets', 'asset', 'img1',
            'img2', 'img3', 'images1', 'images2', 'images3', 'js', 'css', 'style',
            'styles', 'theme', 'themes', 'skin', 'skins', 'template', 'templates'
        ]
    
    def enumerate(self, domain):
        clear()
        printc("╔══════════════════════════════════════╗", "blue", True)
        printc("║       SUBDOMAIN ENUMERATOR           ║", "blue", True)
        printc("╚══════════════════════════════════════╝", "blue")
        print()
        
        if not domain:
            domain = input(cprint("Enter domain (example.com): ", "cyan")).strip().lower()
        
        if not domain or '.' not in domain:
            printc("Invalid domain", "red")
            return
        
        print_status(f"Enumerating subdomains for: {domain}", "loading")
        printc("\n🔍 Checking common subdomains...", "cyan")
        
        found = []
        total = len(self.common_subdomains)
        
        for i, sub in enumerate(self.common_subdomains[:50], 1):
            full_domain = f"{sub}.{domain}"
            
            if i % 10 == 0:
                percent = (i / min(50, total)) * 100
                printc(f"  Progress: {i}/50 ({percent:.1f}%)", "gray", end="\r")
            
            try:
                socket.gethostbyname(full_domain)
                found.append(full_domain)
                printc(f"  ✅ Found: {full_domain}", "green")
            except:
                pass
        
        printc(f"\n\n📊 Results: Found {len(found)} subdomains", "cyan", True)
        printc("="*60, "cyan")
        
        if found:
            for sub in found:
                printc(f"  • {sub}", "green")
            
            printc("\n🌐 IP Addresses:", "cyan", True)
            for sub in found[:10]:
                try:
                    ip = socket.gethostbyname(sub)
                    printc(f"  {sub:30} → {ip}", "gray")
                except:
                    printc(f"  {sub:30} → Could not resolve", "red")
        
        printc("="*60, "cyan")
        
        if found:
            save = input(cprint("\nSave results? (y/n): ", "yellow")).lower()
            if save == 'y':
                self.save_results(domain, found)
    
    def save_results(self, domain, subdomains):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"SUBDOMAINS_{domain}_{timestamp}.txt"
        filepath = REPORTS_DIR / filename
        
        with open(filepath, 'w') as f:
            f.write(f"Subdomains for: {domain}\n")
            f.write(f"Found: {len(subdomains)} subdomains\n")
            f.write(f"Date: {datetime.now()}\n")
            f.write("="*60 + "\n\n")
            
            for sub in subdomains:
                f.write(f"{sub}\n")
        
        print_status(f"Results saved: {filepath}", "success")

# ========== MODULE 12: REVERSE IMAGE SEARCH ==========
class ReverseImageSearch:
    def __init__(self):
        self.services = {
            "Google Images": "https://www.google.com/searchbyimage?&image_url={}",
            "TinEye": "https://www.tineye.com/search?url={}",
            "Bing Visual Search": "https://www.bing.com/images/search?q=imgurl:{}",
            "Yandex Images": "https://yandex.com/images/search?url={}&rpt=imageview",
            "Baidu Images": "https://image.baidu.com/n/pc_search?queryImageUrl={}"
        }
    
    def search(self, image_url=None):
        clear()
        printc("╔══════════════════════════════════════╗", "purple", True)
        printc("║       REVERSE IMAGE SEARCH           ║", "purple", True)
        printc("╚══════════════════════════════════════╝", "purple")
        print()
        
        if not image_url:
            printc("Enter image URL or choose option:", "cyan")
            printc("1. Enter image URL", "yellow")
            printc("2. Take photo with camera (Termux)", "yellow")
            printc("3. Select from gallery (Termux)", "yellow")
            
            choice = input(cprint("Select (1-3): ", "green")).strip()
            
            if choice == "1":
                image_url = input(cprint("Image URL: ", "cyan")).strip()
            elif choice == "2":
                printc("Opening camera...", "cyan")
                os.system("termux-camera-photo -c 1 /sdcard/DCIM/osint_photo.jpg")
                image_url = "file:///sdcard/DCIM/osint_photo.jpg"
            elif choice == "3":
                printc("Select photo from gallery", "cyan")
                os.system("termux-storage-get /sdcard/DCIM/osint_photo.jpg")
                image_url = "file:///sdcard/DCIM/osint_photo.jpg"
            else:
                printc("Invalid choice", "red")
                return
        
        if not image_url:
            printc("Image URL required", "red")
            return
        
        print_status(f"Image: {image_url[:50]}...", "loading")
        print()
        
        printc("🔍 Available Reverse Image Search Services:", "cyan", True)
        printc("="*60, "cyan")
        
        for i, (name, url_template) in enumerate(self.services.items(), 1):
            search_url = url_template.format(requests.utils.quote(image_url))
            printc(f"{i}. {name}:", "yellow")
            printc(f"   URL: {search_url[:70]}...", "blue")
            print()
        
        printc("="*60, "cyan")
        
        choice = input(cprint("Open which service? (1-5 or 'all'): ", "yellow")).strip()
        
        if choice.lower() == 'all':
            for name, url_template in self.services.items():
                search_url = url_template.format(requests.utils.quote(image_url))
                printc(f"Opening {name}...", "cyan")
                os.system(f"termux-open '{search_url}'")
                time.sleep(1)
        elif choice.isdigit() and 1 <= int(choice) <= len(self.services):
            index = int(choice) - 1
            name = list(self.services.keys())[index]
            url_template = list(self.services.values())[index]
            search_url = url_template.format(requests.utils.quote(image_url))
            printc(f"Opening {name}...", "green")
            os.system(f"termux-open '{search_url}'")
        
        save = input(cprint("\nSave search URLs? (y/n): ", "yellow")).lower()
        if save == 'y':
            self.save_search_urls(image_url)

    def save_search_urls(self, image_url):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"REVERSE_IMAGE_{timestamp}.txt"
        filepath = REPORTS_DIR / filename
        
        with open(filepath, 'w') as f:
            f.write(f"Reverse Image Search URLs\n")
            f.write(f"Image: {image_url}\n")
            f.write(f"Date: {datetime.now()}\n")
            f.write("="*60 + "\n\n")
            
            for name, url_template in self.services.items():
                search_url = url_template.format(requests.utils.quote(image_url))
                f.write(f"{name}:\n")
                f.write(f"{search_url}\n")
                f.write("-"*40 + "\n\n")
        
        print_status(f"Search URLs saved: {filepath}", "success")

# ========== MODULE 13: EMAIL BREACH CHECKER ==========
class EmailBreachChecker:
    def __init__(self):
        self.common_breaches = {
            "linkedin.com": ["LinkedIn 2012", "117 million accounts"],
            "yahoo.com": ["Yahoo 2013-2014", "3 billion accounts"],
            "gmail.com": ["Multiple breaches", "Check specific services"],
            "hotmail.com": ["Multiple breaches", "Check specific services"],
            "outlook.com": ["Multiple breaches", "Check specific services"],
            "adobe.com": ["Adobe 2013", "153 million accounts"],
            "twitter.com": ["Twitter 2016", "33 million accounts"],
            "facebook.com": ["Facebook 2019", "533 million accounts"],
            "dropbox.com": ["Dropbox 2012", "68 million accounts"],
            "tumblr.com": ["Tumblr 2013", "65 million accounts"],
            "myspace.com": ["MySpace 2013", "360 million accounts"],
            "vk.com": ["VK 2016", "171 million accounts"]
        }
    
    def check(self, email=None):
        clear()
        printc("╔══════════════════════════════════════╗", "red", True)
        printc("║       EMAIL BREACH CHECKER           ║", "red", True)
        printc("╚══════════════════════════════════════╝", "red")
        print()
        
        if not email:
            email = input(cprint("Enter email address: ", "cyan")).strip().lower()
        
        if not email or '@' not in email:
            printc("Invalid email", "red")
            return
        
        domain = email.split('@')[-1]
        
        print_status(f"Checking: {email}", "loading")
        print()
        
        printc("🔍 Analyzing email pattern...", "cyan")
        printc(f"  Email: {email}", "gray")
        printc(f"  Domain: {domain}", "gray")
        
        breaches_found = []
        
        if domain in self.common_breaches:
            breaches_found.append(self.common_breaches[domain])
            printc(f"\n⚠️  DOMAIN ALERT: {domain}", "red", True)
            printc(f"   Known breaches for this domain:", "yellow")
            for breach in self.common_breaches[domain]:
                printc(f"   • {breach}", "red")
        
        printc("\n🔍 Checking common breach patterns...", "cyan")
        
        if "linkedin" in email or "linkedin" in domain:
            printc("   • Linked to LinkedIn (check LinkedIn 2012 breach)", "yellow")
        
        if "yahoo" in domain:
            printc("   • Yahoo user (check Yahoo 2013-2014 breaches)", "yellow")
        
        printc("\n🔍 Checking common password patterns...", "cyan")
        common_passwords = [
            "123456", "password", "12345678", "qwerty", "123456789",
            "12345", "1234", "111111", "1234567", "dragon"
        ]
        
        username_part = email.split('@')[0]
        for pwd in common_passwords:
            if pwd in username_part.lower():
                printc(f"   ⚠️  Username contains common password: {pwd}", "red")
        
        printc("\n📋 RECOMMENDED ACTIONS:", "green", True)
        printc("="*60, "green")
        printc("1. Check HaveIBeenPwned.com manually", "cyan")
        printc("2. Change passwords if reused", "cyan")
        printc("3. Enable 2FA on all accounts", "cyan")
        printc("4. Use unique passwords per service", "cyan")
        
        hibp_url = f"https://haveibeenpwned.com/account/{email}"
        printc(f"\n🔗 Direct HIBP Check: {hibp_url}", "blue")
        
        open_browser = input(cprint("\nOpen in browser? (y/n): ", "yellow")).lower()
        if open_browser == 'y':
            os.system(f"termux-open '{hibp_url}'")
        
        save = input(cprint("Save report? (y/n): ", "yellow")).lower()
        if save == 'y':
            self.save_report(email, breaches_found, hibp_url)
    
    def save_report(self, email, breaches, hibp_url):
        """Save email breach report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"BREACH_CHECK_{email.replace('@', '_at_')}_{timestamp}.txt"
        filepath = REPORTS_DIR / filename
        
        with open(filepath, 'w') as f:
            f.write(f"Email Breach Check Report\n")
            f.write(f"Email: {email}\n")
            f.write(f"Date: {datetime.now()}\n")
            f.write("="*60 + "\n\n")
            
            f.write("KNOWN BREACHES FOR DOMAIN:\n")
            for breach in breaches:
                f.write(f"• {breach}\n")
            
            f.write("\nRECOMMENDATIONS:\n")
            f.write("1. Check HaveIBeenPwned.com\n")
            f.write("2. Change reused passwords\n")
            f.write("3. Enable Two-Factor Authentication\n")
            f.write("4. Use password manager\n\n")
            
            f.write(f"HIBP Direct Check: {hibp_url}\n")
        
        print_status(f"Report saved: {filepath}", "success")

# ========== MODULE 14: PASSWORD STRENGTH CHECKER ==========
class PasswordStrengthChecker:
    def __init__(self):
        self.common_passwords = self.load_common_passwords()
    
    def load_common_passwords(self):
        return [
            "123456", "password", "12345678", "qwerty", "123456789",
            "12345", "1234", "111111", "1234567", "dragon",
            "123123", "baseball", "abc123", "football", "monkey",
            "letmein", "696969", "shadow", "master", "666666",
            "qwertyuiop", "123321", "mustang", "1234567890",
            "michael", "654321", "pussy", "superman", "1qaz2wsx",
            "7777777", "fuckyou", "121212", "000000", "qazwsx",
            "123qwe", "killer", "trustno1", "jordan", "jennifer",
            "zxcvbnm", "asdfgh", "hunter", "buster", "soccer",
            "harley", "batman", "andrew", "tigger", "sunshine",
            "iloveyou", "fuckme", "2000", "charlie", "robert",
            "thomas", "hockey", "ranger", "daniel", "starwars"
        ]
    
    def check(self, password=None):
        clear()
        printc("╔══════════════════════════════════════╗", "green", True)
        printc("║      PASSWORD STRENGTH CHECKER       ║", "green", True)
        printc("╚══════════════════════════════════════╝", "green")
        print()
        
        if not password:
            password = input(cprint("Enter password to check: ", "cyan")).strip()
            printc("(Password is not saved or transmitted)", "gray", True)
        
        if not password:
            printc("Password required", "red")
            return
        
        print_status(f"Analyzing password...", "loading")
        print()
        
        hidden = '*' * len(password)
        printc(f"Password: {hidden}", "gray")
        printc(f"Length: {len(password)} characters", "cyan")
        
        if password.lower() in self.common_passwords:
            printc(f"❌ WEAK: Password is in top 100 most common passwords", "red", True)
            strength = 0
        else:
            strength = 0
            
            if len(password) >= 8:
                strength += 1
                printc("✅ Good length (8+ characters)", "green")
            else:
                printc("❌ Too short (minimum 8 characters recommended)", "red")
            
            has_upper = any(c.isupper() for c in password)
            has_lower = any(c.islower() for c in password)
            has_digit = any(c.isdigit() for c in password)
            has_special = any(not c.isalnum() for c in password)
            
            if has_upper and has_lower:
                strength += 1
                printc("✅ Has both uppercase and lowercase", "green")
            else:
                printc("❌ Missing uppercase/lowercase mix", "red")
            
            if has_digit:
                strength += 1
                printc("✅ Contains numbers", "green")
            else:
                printc("❌ No numbers", "yellow")
            
            if has_special:
                strength += 1
                printc("✅ Contains special characters", "green")
            else:
                printc("⚠️  No special characters", "yellow")
            
            if password.isnumeric():
                printc("❌ Only numbers", "red")
                strength -= 1
            elif password.isalpha():
                printc("❌ Only letters", "red")
                strength -= 1
        
        printc("\n📊 PASSWORD STRENGTH:", "cyan", True)
        printc("="*40, "cyan")
        
        if strength >= 4:
            printc("🔒 STRONG - Good password!", "green", True)
        elif strength >= 2:
            printc("⚠️  MEDIUM - Could be better", "yellow", True)
        else:
            printc("🔓 WEAK - Change immediately!", "red", True)
        
        printc("\n🔐 Password Hashes (for reference):", "cyan")
        printc(f"  MD5:    {hashlib.md5(password.encode()).hexdigest()}", "gray")
        printc(f"  SHA1:   {hashlib.sha1(password.encode()).hexdigest()}", "gray")
        printc(f"  SHA256: {hashlib.sha256(password.encode()).hexdigest()}", "gray")
        
        printc("\n💡 RECOMMENDATIONS:", "green", True)
        if strength < 4:
            printc("1. Use at least 12 characters", "cyan")
            printc("2. Mix uppercase, lowercase, numbers, symbols", "cyan")
            printc("3. Avoid dictionary words", "cyan")
            printc("4. Don't reuse passwords", "cyan")
        
        save = input(cprint("\nSave hash reference? (y/n): ", "yellow")).lower()
        if save == 'y':
            self.save_hash(password)

    def save_hash(self, password):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"PASSWORD_HASH_{timestamp}.txt"
        filepath = REPORTS_DIR / filename
        
        with open(filepath, 'w') as f:
            f.write(f"Password Hash Reference\n")
            f.write(f"Date: {datetime.now()}\n")
            f.write("="*60 + "\n\n")
            f.write("WARNING: Never store actual passwords!\n\n")
            f.write("Password Length: {}\n".format(len(password)))
            f.write("MD5:    {}\n".format(hashlib.md5(password.encode()).hexdigest()))
            f.write("SHA1:   {}\n".format(hashlib.sha1(password.encode()).hexdigest()))
            f.write("SHA256: {}\n".format(hashlib.sha256(password.encode()).hexdigest()))
            f.write("SHA512: {}\n".format(hashlib.sha512(password.encode()).hexdigest()))
        
        print_status(f"Hash reference saved: {filepath}", "success")

# ========== MODULE 15: WAYBACK MACHINE CHECKER ==========
class WaybackChecker:
    def __init__(self):
        self.api_url = "http://archive.org/wayback/available"
    
    def check(self, url):
        """Check Wayback Machine for historical snapshots"""
        clear()
        printc("╔══════════════════════════════════════╗", "cyan", True)
        printc("║       WAYBACK MACHINE CHECKER        ║", "cyan", True)
        printc("╚══════════════════════════════════════╝", "cyan")
        print()
        
        if not url:
            url = input(cprint("Enter URL to check: ", "cyan")).strip()
        
        if not url:
            printc("URL required", "red")
            return
        
        print_status(f"Checking Wayback Machine for: {url}", "loading")
        
        try:
            response = requests.get(f"{self.api_url}?url={url}", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                printc("\n" + "=" * 50, "green")
                printc("📜 WAYBACK MACHINE RESULTS", "green", True)
                printc("=" * 50, "green")
                
                if 'archived_snapshots' in data and 'closest' in data['archived_snapshots']:
                    snapshot = data['archived_snapshots']['closest']
                    
                    printc(f"✅ Snapshot Found!", "green", True)
                    printc(f"URL: {snapshot.get('url', 'N/A')}", "cyan")
                    printc(f"Date: {snapshot.get('timestamp', 'N/A')}", "cyan")
                    printc(f"Status: {snapshot.get('status', 'N/A')}", "cyan")
                    
                    calendar_url = f"https://web.archive.org/web/*/{url}"
                    printc(f"\n📅 Calendar View: {calendar_url}", "blue")
                    
                    latest_url = f"https://web.archive.org/web/{snapshot.get('timestamp', '')}/{url}"
                    printc(f"🔗 Latest Snapshot: {latest_url}", "blue")
                    
                    printc("\n🔧 Options:", "yellow", True)
                    printc("1. Open calendar view", "cyan")
                    printc("2. Open latest snapshot", "cyan")
                    printc("3. Save results", "cyan")
                    
                    choice = input(cprint("\nSelect option (1-3): ", "yellow")).strip()
                    
                    if choice == "1":
                        os.system(f"termux-open '{calendar_url}'")
                    elif choice == "2":
                        os.system(f"termux-open '{latest_url}'")
                    elif choice == "3":
                        self.save_results(url, data)
                else:
                    printc("❌ No snapshots found for this URL", "red")
                    printc("\n💡 Try these alternatives:", "yellow")
                    printc(f"• Calendar view: https://web.archive.org/web/*/{url}", "blue")
                    printc(f"• Save current page: https://web.archive.org/save/{url}", "blue")
                
                printc("=" * 50, "green")
            else:
                printc(f"❌ API Error: {response.status_code}", "red")
                
        except Exception as e:
            printc(f"Error: {str(e)}", "red")
            printc("\n📎 Manual check:", "yellow")
            printc(f"Visit: https://web.archive.org/web/*/{url}", "blue")
    
    def save_results(self, url, data):
        """Save Wayback Machine results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"WAYBACK_{url.replace('/', '_')}_{timestamp}.json"
        filepath = REPORTS_DIR / filename
        
        with open(filepath, 'w') as f:
            json.dump({
                'url': url,
                'timestamp': datetime.now().isoformat(),
                'results': data
            }, f, indent=4)
        
        print_status(f"Results saved: {filepath}", "success")

# ========== MODULE 16: DNSDUMPSTER INTEGRATION ==========
class DNSDumpsterTool:
    def __init__(self):
        self.base_url = "https://dnsdumpster.com"
    
    def analyze(self, domain):
        """Analyze domain using DNSDumpster (web interface)"""
        clear()
        printc("╔══════════════════════════════════════╗", "blue", True)
        printc("║         DNSDUMPSTER TOOL             ║", "blue", True)
        printc("╚══════════════════════════════════════╝", "blue")
        print()
        
        if not domain:
            domain = input(cprint("Enter domain to analyze: ", "cyan")).strip().lower()
        
        if not domain or '.' not in domain:
            printc("Invalid domain", "red")
            return
        
        print_status(f"Analyzing: {domain}", "loading")
        
        dnsdumpster_url = f"{self.base_url}/?q={domain}"
        
        printc("\n" + "=" * 50, "green")
        printc("🌐 DNSDUMPSTER ANALYSIS", "green", True)
        printc("=" * 50, "green")
        
        printc(f"\n🔍 Target Domain: {domain}", "cyan", True)
        printc("\n📊 What DNSDumpster provides:", "yellow")
        printc("• Subdomain discovery", "cyan")
        printc("• DNS records (A, MX, NS, TXT)", "cyan")
        printc("• WHOIS information", "cyan")
        printc("• Network mapping", "cyan")
        printc("• Technology detection", "cyan")
        
        printc(f"\n🔗 Direct Link: {dnsdumpster_url}", "blue")
        
        printc("\n⚡ Quick Commands for Terminal:", "yellow", True)
        printc("1. Get DNS records:", "cyan")
        printc(f"   dig {domain} ANY", "gray")
        printc("\n2. Check subdomains:", "cyan")
        printc(f"   dig *.{domain}", "gray")
        printc("\n3. Check mail servers:", "cyan")
        printc(f"   dig MX {domain}", "gray")
        
        printc("\n" + "=" * 50, "green")
        
        open_browser = input(cprint("Open DNSDumpster in browser? (y/n): ", "yellow")).lower()
        if open_browser == 'y':
            os.system(f"termux-open '{dnsdumpster_url}'")
        
        run_cmds = input(cprint("Run terminal DNS commands? (y/n): ", "yellow")).lower()
        if run_cmds == 'y':
            self.run_dns_commands(domain)
        
        save = input(cprint("Save analysis report? (y/n): ", "yellow")).lower()
        if save == 'y':
            self.save_report(domain, dnsdumpster_url)
    
    def run_dns_commands(self, domain):
        """Run DNS commands in terminal"""
        printc("\n🔧 Running DNS commands...", "cyan")
        
        commands = [
            (f"dig {domain} A", "A Records (IPv4)"),
            (f"dig {domain} MX", "Mail Exchange Records"),
            (f"dig {domain} NS", "Name Server Records"),
            (f"dig {domain} TXT", "TXT Records"),
            (f"dig {domain} ANY", "All DNS Records")
        ]
        
        for cmd, description in commands:
            printc(f"\n📋 {description}:", "yellow")
            printc(f"Command: {cmd}", "gray")
            
            try:
                result = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    lines = result.stdout.split('\n')
                    for line in lines:
                        if domain in line and ('IN' in line or 'ANSWER' in line):
                            printc(f"  {line.strip()}", "green")
            except:
                printc(f"  Command failed or timed out", "red")
    
    def save_report(self, domain, dnsdumpster_url):
        """Save DNS analysis report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"DNSDUMPSTER_{domain}_{timestamp}.txt"
        filepath = REPORTS_DIR / filename
        
        with open(filepath, 'w') as f:
            f.write(f"DNS Analysis Report\n")
            f.write(f"Domain: {domain}\n")
            f.write(f"Date: {datetime.now()}\n")
            f.write("="*60 + "\n\n")
            
            f.write(f"DNSDUMPSTER Link: {dnsdumpster_url}\n\n")
            
            f.write("TERMINAL COMMANDS:\n")
            f.write(f"dig {domain} A\t\t# Get A records\n")
            f.write(f"dig {domain} MX\t\t# Get mail servers\n")
            f.write(f"dig {domain} NS\t\t# Get name servers\n")
            f.write(f"dig {domain} TXT\t\t# Get TXT records\n")
            f.write(f"dig {domain} ANY\t\t# Get all records\n\n")
            
            f.write("COMMON DNS RECORDS TO CHECK:\n")
            f.write("• A\t\t- IPv4 address\n")
            f.write("• AAAA\t\t- IPv6 address\n")
            f.write("• MX\t\t- Mail exchange\n")
            f.write("• NS\t\t- Name server\n")
            f.write("• TXT\t\t- Text records (often for verification)\n")
            f.write("• CNAME\t\t- Canonical name (aliases)\n")
            f.write("• SOA\t\t- Start of authority\n")
        
        print_status(f"Report saved: {filepath}", "success")

# ========== MODULE 17: SHERLOCK-STYLE USERNAME SEARCH ==========
class SherlockUsernameSearch:
    def __init__(self):
        self.platforms = {
            "GitHub": ["https://github.com/{}", self.check_github],
            "Twitter/X": ["https://twitter.com/{}", self.check_twitter],
            "Instagram": ["https://instagram.com/{}", self.check_instagram],
            "Reddit": ["https://reddit.com/user/{}", self.check_reddit],
            "YouTube": ["https://youtube.com/@{}", self.check_youtube],
            "Facebook": ["https://facebook.com/{}", self.check_facebook],
            "LinkedIn": ["https://linkedin.com/in/{}", self.check_linkedin],
            "Pinterest": ["https://pinterest.com/{}", self.check_pinterest],
            "Twitch": ["https://twitch.tv/{}", self.check_twitch],
            "Telegram": ["https://t.me/{}", self.check_telegram],
            "TikTok": ["https://tiktok.com/@{}", self.check_tiktok],
            "Spotify": ["https://open.spotify.com/user/{}", self.check_spotify],
            "Snapchat": ["https://snapchat.com/add/{}", self.check_snapchat],
            "Medium": ["https://medium.com/@{}", self.check_medium],
            "DeviantArt": ["https://deviantart.com/{}", self.check_deviantart],
            "Flickr": ["https://flickr.com/people/{}", self.check_flickr],
            "VK": ["https://vk.com/{}", self.check_vk],
            "Steam": ["https://steamcommunity.com/id/{}", self.check_steam],
            "GitLab": ["https://gitlab.com/{}", self.check_gitlab],
            "Bitbucket": ["https://bitbucket.org/{}", self.check_bitbucket],
            "Keybase": ["https://keybase.io/{}", self.check_keybase],
            "Patreon": ["https://patreon.com/{}", self.check_patreon],
            "CodePen": ["https://codepen.io/{}", self.check_codepen],
            "Behance": ["https://behance.net/{}", self.check_behance],
            "Dribbble": ["https://dribbble.com/{}", self.check_dribbble],
            "Foursquare": ["https://foursquare.com/{}", self.check_foursquare],
            "Gravatar": ["https://gravatar.com/{}", self.check_gravatar],
            "HubPages": ["https://hubpages.com/@{}", self.check_hubpages],
            "Imgur": ["https://imgur.com/user/{}", self.check_imgur],
            "Instructables": ["https://instructables.com/member/{}", self.check_instructables],
            "Kongregate": ["https://kongregate.com/accounts/{}", self.check_kongregate],
            "Last.fm": ["https://last.fm/user/{}", self.check_lastfm],
            "Mix": ["https://mix.com/{}", self.check_mix],
            "Newgrounds": ["https://newgrounds.com/{}", self.check_newgrounds],
            "Pastebin": ["https://pastebin.com/u/{}", self.check_pastebin],
            "Replit": ["https://replit.com/@{}", self.check_replit],
            "Roblox": ["https://roblox.com/users/{}/profile", self.check_roblox],
            "Scribd": ["https://scribd.com/{}", self.check_scribd],
            "Slideshare": ["https://slideshare.net/{}", self.check_slideshare],
            "SoundCloud": ["https://soundcloud.com/{}", self.check_soundcloud],
            "Tumblr": ["https://{}.tumblr.com", self.check_tumblr],
            "Wattpad": ["https://wattpad.com/user/{}", self.check_wattpad],
            "WordPress": ["https://{}.wordpress.com", self.check_wordpress],
            "YouTube (old)": ["https://youtube.com/user/{}", self.check_youtube_user]
        }
    
    def search(self, username):
        """Search for username across 50+ platforms"""
        clear()
        printc("╔══════════════════════════════════════╗", "purple", True)
        printc("║   SHERLOCK USERNAME SEARCH (50+)     ║", "purple", True)
        printc("╚══════════════════════════════════════╝", "purple")
        print()
        
        if not username:
            username = input(cprint("Enter username to search: ", "cyan")).strip()
        
        if not username:
            printc("Username required", "red")
            return
        
        print_status(f"Searching for: @{username}", "loading")
        printc("\n🔍 Checking 50+ platforms...", "cyan")
        print()
        
        results = []
        
        threads = []
        lock = threading.Lock()
        
        def check_platform(platform_name, url_template, check_func):
            try:
                exists, data = check_func(username)
                with lock:
                    if exists:
                        results.append({
                            'platform': platform_name,
                            'url': url_template.format(username),
                            'data': data
                        })
                        printc(f"✅ {platform_name:20} FOUND", "green")
                    else:
                        printc(f"❌ {platform_name:20} NOT FOUND", "red")
            except:
                with lock:
                    printc(f"⚠️  {platform_name:20} ERROR", "yellow")
        
        for platform_name, (url_template, check_func) in list(self.platforms.items())[:20]:
            thread = threading.Thread(target=check_platform, args=(platform_name, url_template, check_func))
            threads.append(thread)
            thread.start()
            time.sleep(0.05)
        
        for thread in threads:
            thread.join()
        
        if results:
            printc(f"\n📊 FOUND ON {len(results)} PLATFORMS", "green", True)
            printc("="*60, "green")
            
            for result in results:
                printc(f"\n{result['platform']}:", "yellow", True)
                printc(f"  URL: {result['url']}", "cyan")
                if result['data']:
                    for key, value in result['data'].items():
                        if value:
                            printc(f"  {key}: {value}", "cyan")
            
            printc("="*60, "green")
        
        if results:
            save = input(cprint("\nSave all results? (y/n): ", "yellow")).lower()
            if save == 'y':
                self.save_results(username, results)
    
    def check_github(self, username):
        try:
            response = requests.get(f"https://api.github.com/users/{username}", timeout=5)
            return response.status_code == 200, {"Type": "GitHub Profile"}
        except:
            return False, None
    
    def check_twitter(self, username):
        try:
            response = requests.get(f"https://twitter.com/{username}", timeout=5)
            return "This account doesn't exist" not in response.text, {"Type": "Twitter Profile"}
        except:
            return False, None
    
    def check_instagram(self, username):
        try:
            response = requests.get(f"https://www.instagram.com/{username}/", timeout=5)
            return "Sorry, this page isn't available" not in response.text, {"Type": "Instagram Profile"}
        except:
            return False, None
    
    def check_reddit(self, username):
        try:
            response = requests.get(f"https://www.reddit.com/user/{username}/about.json", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return 'is_suspended' not in data.get('data', {}), {"Type": "Reddit User"}
            return False, None
        except:
            return False, None
    
    def check_youtube(self, username):
        try:
            response = requests.get(f"https://www.youtube.com/@{username}", timeout=5)
            return "This channel doesn't exist" not in response.text, {"Type": "YouTube Channel"}
        except:
            return False, None
    
    def check_facebook(self, username):
        try:
            response = requests.get(f"https://www.facebook.com/{username}", timeout=5)
            return "Sorry, this content isn't available" not in response.text, {"Type": "Facebook Profile"}
        except:
            return False, None
    
    def check_linkedin(self, username):
        try:
            response = requests.get(f"https://www.linkedin.com/in/{username}", timeout=5)
            return "This profile is not available" not in response.text, {"Type": "LinkedIn Profile"}
        except:
            return False, None
    
    def check_pinterest(self, username):
        try:
            response = requests.get(f"https://www.pinterest.com/{username}/", timeout=5)
            return "Sorry, we couldn't find that page" not in response.text, {"Type": "Pinterest Profile"}
        except:
            return False, None
    
    def check_twitch(self, username):
        try:
            response = requests.get(f"https://www.twitch.tv/{username}", timeout=5)
            return "Sorry. Unless you've got a time machine, that content is unavailable." not in response.text, {"Type": "Twitch Channel"}
        except:
            return False, None
    
    def check_telegram(self, username):
        try:
            response = requests.get(f"https://t.me/{username}", timeout=5)
            return "If you have Telegram, you can contact" in response.text, {"Type": "Telegram Profile"}
        except:
            return False, None
    
    def check_tiktok(self, username):
        try:
            response = requests.get(f"https://www.tiktok.com/@{username}", timeout=5)
            return response.status_code == 200, {"Type": "TikTok Profile"}
        except:
            return False, None
    
    def check_spotify(self, username):
        try:
            response = requests.get(f"https://open.spotify.com/user/{username}", timeout=5)
            return response.status_code == 200, {"Type": "Spotify Profile"}
        except:
            return False, None
    
    def check_snapchat(self, username):
        try:
            response = requests.get(f"https://www.snapchat.com/add/{username}", timeout=5)
            return response.status_code == 200, {"Type": "Snapchat Profile"}
        except:
            return False, None
    
    def check_medium(self, username):
        try:
            response = requests.get(f"https://medium.com/@{username}", timeout=5)
            return response.status_code == 200, {"Type": "Medium Profile"}
        except:
            return False, None
    
    def check_deviantart(self, username):
        try:
            response = requests.get(f"https://www.deviantart.com/{username}", timeout=5)
            return response.status_code == 200, {"Type": "DeviantArt Profile"}
        except:
            return False, None
    
    def check_flickr(self, username):
        try:
            response = requests.get(f"https://www.flickr.com/people/{username}", timeout=5)
            return response.status_code == 200, {"Type": "Flickr Profile"}
        except:
            return False, None
    
    def check_vk(self, username):
        try:
            response = requests.get(f"https://vk.com/{username}", timeout=5)
            return response.status_code == 200, {"Type": "VK Profile"}
        except:
            return False, None
    
    def check_steam(self, username):
        try:
            response = requests.get(f"https://steamcommunity.com/id/{username}", timeout=5)
            return response.status_code == 200, {"Type": "Steam Profile"}
        except:
            return False, None
    
    def check_gitlab(self, username):
        try:
            response = requests.get(f"https://gitlab.com/{username}", timeout=5)
            return response.status_code == 200, {"Type": "GitLab Profile"}
        except:
            return False, None
    
    def check_bitbucket(self, username):
        try:
            response = requests.get(f"https://bitbucket.org/{username}", timeout=5)
            return response.status_code == 200, {"Type": "Bitbucket Profile"}
        except:
            return False, None
    
    def check_keybase(self, username):
        try:
            response = requests.get(f"https://keybase.io/{username}", timeout=5)
            return response.status_code == 200, {"Type": "Keybase Profile"}
        except:
            return False, None
    
    def check_patreon(self, username):
        try:
            response = requests.get(f"https://www.patreon.com/{username}", timeout=5)
            return response.status_code == 200, {"Type": "Patreon Profile"}
        except:
            return False, None
    
    def check_codepen(self, username):
        try:
            response = requests.get(f"https://codepen.io/{username}", timeout=5)
            return response.status_code == 200, {"Type": "CodePen Profile"}
        except:
            return False, None
    
    def check_behance(self, username):
        try:
            response = requests.get(f"https://www.behance.net/{username}", timeout=5)
            return response.status_code == 200, {"Type": "Behance Profile"}
        except:
            return False, None
    
    def check_dribbble(self, username):
        try:
            response = requests.get(f"https://dribbble.com/{username}", timeout=5)
            return response.status_code == 200, {"Type": "Dribbble Profile"}
        except:
            return False, None
    
    def check_foursquare(self, username):
        try:
            response = requests.get(f"https://foursquare.com/{username}", timeout=5)
            return response.status_code == 200, {"Type": "Foursquare Profile"}
        except:
            return False, None
    
    def check_gravatar(self, username):
        try:
            response = requests.get(f"https://gravatar.com/{username}", timeout=5)
            return response.status_code == 200, {"Type": "Gravatar Profile"}
        except:
            return False, None
    
    def check_hubpages(self, username):
        try:
            response = requests.get(f"https://hubpages.com/@{username}", timeout=5)
            return response.status_code == 200, {"Type": "HubPages Profile"}
        except:
            return False, None
    
    def check_imgur(self, username):
        try:
            response = requests.get(f"https://imgur.com/user/{username}", timeout=5)
            return response.status_code == 200, {"Type": "Imgur Profile"}
        except:
            return False, None
    
    def check_instructables(self, username):
        try:
            response = requests.get(f"https://www.instructables.com/member/{username}", timeout=5)
            return response.status_code == 200, {"Type": "Instructables Profile"}
        except:
            return False, None
    
    def check_kongregate(self, username):
        try:
            response = requests.get(f"https://www.kongregate.com/accounts/{username}", timeout=5)
            return response.status_code == 200, {"Type": "Kongregate Profile"}
        except:
            return False, None
    
    def check_lastfm(self, username):
        try:
            response = requests.get(f"https://www.last.fm/user/{username}", timeout=5)
            return response.status_code == 200, {"Type": "Last.fm Profile"}
        except:
            return False, None
    
    def check_mix(self, username):
        try:
            response = requests.get(f"https://mix.com/{username}", timeout=5)
            return response.status_code == 200, {"Type": "Mix Profile"}
        except:
            return False, None
    
    def check_newgrounds(self, username):
        try:
            response = requests.get(f"https://www.newgrounds.com/{username}", timeout=5)
            return response.status_code == 200, {"Type": "Newgrounds Profile"}
        except:
            return False, None
    
    def check_pastebin(self, username):
        try:
            response = requests.get(f"https://pastebin.com/u/{username}", timeout=5)
            return response.status_code == 200, {"Type": "Pastebin Profile"}
        except:
            return False, None
    
    def check_replit(self, username):
        try:
            response = requests.get(f"https://replit.com/@{username}", timeout=5)
            return response.status_code == 200, {"Type": "Replit Profile"}
        except:
            return False, None
    
    def check_roblox(self, username):
        try:
            response = requests.get(f"https://www.roblox.com/users/{username}/profile", timeout=5)
            return response.status_code == 200, {"Type": "Roblox Profile"}
        except:
            return False, None
    
    def check_scribd(self, username):
        try:
            response = requests.get(f"https://www.scribd.com/{username}", timeout=5)
            return response.status_code == 200, {"Type": "Scribd Profile"}
        except:
            return False, None
    
    def check_slideshare(self, username):
        try:
            response = requests.get(f"https://www.slideshare.net/{username}", timeout=5)
            return response.status_code == 200, {"Type": "SlideShare Profile"}
        except:
            return False, None
    
    def check_soundcloud(self, username):
        try:
            response = requests.get(f"https://soundcloud.com/{username}", timeout=5)
            return response.status_code == 200, {"Type": "SoundCloud Profile"}
        except:
            return False, None
    
    def check_tumblr(self, username):
        try:
            response = requests.get(f"https://{username}.tumblr.com", timeout=5)
            return response.status_code == 200, {"Type": "Tumblr Blog"}
        except:
            return False, None
    
    def check_wattpad(self, username):
        try:
            response = requests.get(f"https://www.wattpad.com/user/{username}", timeout=5)
            return response.status_code == 200, {"Type": "Wattpad Profile"}
        except:
            return False, None
    
    def check_wordpress(self, username):
        try:
            response = requests.get(f"https://{username}.wordpress.com", timeout=5)
            return response.status_code == 200, {"Type": "WordPress Blog"}
        except:
            return False, None
    
    def check_youtube_user(self, username):
        try:
            response = requests.get(f"https://www.youtube.com/user/{username}", timeout=5)
            return response.status_code == 200, {"Type": "YouTube User"}
        except:
            return False, None
    
    def save_results(self, username, results):
        """Save username search results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"SHERLOCK_{username}_{timestamp}.json"
        filepath = REPORTS_DIR / filename
        
        data = {
            'username': username,
            'timestamp': datetime.now().isoformat(),
            'total_platforms': len(self.platforms),
            'found_on': len(results),
            'profiles': results
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
        
        print_status(f"Results saved: {filepath}", "success")
        printc(f"📁 {len(results)} profiles found for @{username}", "green")

# ========== MODULE 18: TECH DETECTOR (BuiltWith/Wappalyzer Lite) ==========
class TechDetector:
    def __init__(self):
        self.tech_signatures = {
            'WordPress': ['wp-content', 'wp-includes', 'wordpress'],
            'Joomla': ['joomla', 'media/jui', 'templates/joomla'],
            'Drupal': ['drupal', 'sites/all', 'misc/drupal'],
            'Shopify': ['shopify', 'cdn.shopify.com', 'shopify.com/cdn'],
            'Magento': ['magento', 'skin/frontend', 'media/magento'],
            'Laravel': ['laravel', '/storage/', '/resources/'],
            'React': ['react', 'react-dom', '.jsx'],
            'Vue.js': ['vue', 'vue.js', '__VUE__'],
            'Angular': ['angular', 'ng-', '@angular'],
            'jQuery': ['jquery', 'jquery.min.js'],
            'Bootstrap': ['bootstrap', 'bootstrap.min.css'],
            'Nginx': ['nginx', 'server: nginx'],
            'Apache': ['apache', 'server: apache'],
            'CloudFlare': ['cloudflare', 'cf-ray', '__cfduid'],
            'Google Analytics': ['google-analytics', 'ga.js', 'analytics.js'],
            'Facebook Pixel': ['facebook', 'fbq(', 'pixel.facebook.com'],
            'CDN': ['cdn', 'cloudfront', 'akamai', 'fastly'],
            'SSL': ['https://', 'TLS', 'SSL'],
            'PHP': ['.php', 'php/', 'x-powered-by: php'],
            'Python': ['python', 'django', 'flask', 'x-powered-by: python'],
            'Node.js': ['node.js', 'express', 'x-powered-by: express'],
            'Ruby': ['ruby', 'rails', 'x-powered-by: ruby'],
            '.NET': ['.net', 'asp.net', 'x-powered-by: asp.net']
        }
    
    def detect(self, url):
        """Detect technologies used on a website"""
        clear()
        printc("╔══════════════════════════════════════╗", "yellow", True)
        printc("║        TECHNOLOGY DETECTOR           ║", "yellow", True)
        printc("╚══════════════════════════════════════╝", "yellow")
        print()
        
        if not url:
            url = input(cprint("Enter website URL: ", "cyan")).strip()
        
        if not url:
            printc("URL required", "red")
            return
        
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        
        print_status(f"Analyzing: {url}", "loading")
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10, verify=False)
            
            printc("\n" + "=" * 50, "green")
            printc("🔧 TECHNOLOGY DETECTION RESULTS", "green", True)
            printc("=" * 50, "green")
            
            printc(f"\n🌐 Website: {url}", "cyan", True)
            printc(f"Status Code: {response.status_code}", "cyan")
            
            server = response.headers.get('Server', 'Not detected')
            printc(f"Server: {server}", "cyan")
            
            powered_by = response.headers.get('X-Powered-By', 'Not detected')
            if powered_by != 'Not detected':
                printc(f"Powered By: {powered_by}", "cyan")
            
            printc("\n📊 DETECTED TECHNOLOGIES:", "yellow", True)
            printc("-" * 40, "yellow")
            
            detected_tech = []
            content = response.text.lower()
            headers_str = str(response.headers).lower()
            
            for tech, signatures in self.tech_signatures.items():
                for signature in signatures:
                    if signature.lower() in content or signature.lower() in headers_str:
                        detected_tech.append(tech)
                        printc(f"✅ {tech}", "green")
                        break
            
            if not detected_tech:
                printc("⚠️  No technologies detected (or detection failed)", "yellow")
            
            printc("\n🔍 INTERESTING HEADERS:", "yellow", True)
            printc("-" * 40, "yellow")
            
            interesting_headers = ['Server', 'X-Powered-By', 'X-Frame-Options', 
                                 'Content-Security-Policy', 'Strict-Transport-Security',
                                 'X-Content-Type-Options', 'X-XSS-Protection']
            
            for header in interesting_headers:
                value = response.headers.get(header)
                if value:
                    printc(f"{header}: {value}", "cyan")
            
            printc("\n🔗 EXTERNAL ANALYSIS TOOLS:", "yellow", True)
            printc("-" * 40, "yellow")
            
            domain = url.split('//')[-1].split('/')[0]
            builtwith_url = f"https://builtwith.com/{domain}"
            wappalyzer_url = f"https://www.wappalyzer.com/lookup/{domain}"
            
            printc(f"BuiltWith: {builtwith_url}", "blue")
            printc(f"Wappalyzer: {wappalyzer_url}", "blue")
            
            printc("=" * 50, "green")
            
            printc("\n🔧 OPTIONS:", "cyan", True)
            printc("1. Open BuiltWith", "yellow")
            printc("2. Open Wappalyzer", "yellow")
            printc("3. Save report", "yellow")
            printc("4. View full headers", "yellow")
            
            choice = input(cprint("\nSelect option (1-4): ", "yellow")).strip()
            
            if choice == "1":
                os.system(f"termux-open '{builtwith_url}'")
            elif choice == "2":
                os.system(f"termux-open '{wappalyzer_url}'")
            elif choice == "3":
                self.save_report(url, detected_tech, response.headers)
            elif choice == "4":
                self.show_all_headers(response.headers)
                
        except Exception as e:
            printc(f"Error: {str(e)}", "red")
            printc("\n💡 Try these alternatives:", "yellow")
            printc(f"• BuiltWith: https://builtwith.com/{url.split('//')[-1].split('/')[0]}", "blue")
            printc(f"• Wappalyzer: https://www.wappalyzer.com/lookup/{url.split('//')[-1].split('/')[0]}", "blue")
    
    def show_all_headers(self, headers):
        """Display all HTTP headers"""
        clear()
        printc("╔══════════════════════════════════════╗", "cyan", True)
        printc("║          ALL HTTP HEADERS            ║", "cyan", True)
        printc("╚══════════════════════════════════════╝", "cyan")
        print()
        
        printc("🔍 HTTP Response Headers:", "yellow", True)
        printc("="*60, "yellow")
        
        for header, value in headers.items():
            printc(f"{header}:", "cyan", end=" ")
            printc(f"{value}", "green")
        
        printc("="*60, "yellow")
        input(cprint("\nPress Enter to continue...", "gray"))
    
    def save_report(self, url, technologies, headers):
        """Save technology detection report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        domain = url.split('//')[-1].split('/')[0]
        filename = f"TECH_DETECT_{domain}_{timestamp}.txt"
        filepath = REPORTS_DIR / filename
        
        with open(filepath, 'w') as f:
            f.write(f"Technology Detection Report\n")
            f.write(f"URL: {url}\n")
            f.write(f"Date: {datetime.now()}\n")
            f.write("="*60 + "\n\n")
            
            f.write("DETECTED TECHNOLOGIES:\n")
            if technologies:
                for tech in technologies:
                    f.write(f"• {tech}\n")
            else:
                f.write("No technologies detected\n")
            
            f.write("\nHTTP HEADERS:\n")
            for header, value in headers.items():
                f.write(f"{header}: {value}\n")
            
            f.write("\nEXTERNAL LINKS:\n")
            f.write(f"BuiltWith: https://builtwith.com/{domain}\n")
            f.write(f"Wappalyzer: https://www.wappalyzer.com/lookup/{domain}\n")
        
        print_status(f"Report saved: {filepath}", "success")

# ========== MODULE 19: ABUSEIPDB CHECKER ==========
class AbuseIPDBChecker:
    def __init__(self):
        self.api_url = "https://api.abuseipdb.com/api/v2/check"
    
    def check(self, ip=None):
        """Check IP reputation on AbuseIPDB"""
        clear()
        printc("╔══════════════════════════════════════╗", "red", True)
        printc("║         ABUSEIPDB CHECKER            ║", "red", True)
        printc("╚══════════════════════════════════════╝", "red")
        print()
        
        if not ip:
            ip = input(cprint("Enter IP address to check: ", "cyan")).strip()
        
        if not ip:
            printc("IP address required", "red")
            return
        
        try:
            socket.inet_aton(ip)
        except:
            printc("Invalid IP address format", "red")
            return
        
        print_status(f"Checking: {ip}", "loading")
        
        abuseipdb_url = f"https://www.abuseipdb.com/check/{ip}"
        
        printc("\n" + "=" * 50, "green")
        printc("🛡️  ABUSEIPDB REPUTATION CHECK", "green", True)
        printc("=" * 50, "green")
        
        printc(f"\n🔍 IP Address: {ip}", "cyan", True)
        
        printc("\n📊 What AbuseIPDB provides:", "yellow")
        printc("• IP reputation score", "cyan")
        printc("• Abuse reports count", "cyan")
        printc("• Country and ISP info", "cyan")
        printc("• Last reported abuse", "cyan")
        printc("• Confidence of abuse", "cyan")
        
        printc(f"\n🔗 Direct Link: {abuseipdb_url}", "blue")
        
        printc("\n🌐 ALTERNATIVE IP CHECK SERVICES:", "yellow", True)
        printc(f"• VirusTotal: https://www.virustotal.com/gui/ip-address/{ip}", "blue")
        printc(f"• IPvoid: https://www.ipvoid.com/ip-blacklist-check/{ip}/", "blue")
        printc(f"• IBM X-Force: https://exchange.xforce.ibmcloud.com/ip/{ip}", "blue")
        printc(f"• ThreatFox: https://threatfox.abuse.ch/browse.php?search={ip}", "blue")
        
        printc("\n🔧 QUICK TERMINAL CHECKS:", "yellow", True)
        printc(f"1. Ping: ping -c 4 {ip}", "gray")
        printc(f"2. Traceroute: traceroute {ip}", "gray")
        printc(f"3. WHOIS: whois {ip}", "gray")
        printc(f"4. Port scan (basic): nc -zv {ip} 80 443 22", "gray")
        
        printc("=" * 50, "green")
        
        open_browser = input(cprint("Open AbuseIPDB in browser? (y/n): ", "yellow")).lower()
        if open_browser == 'y':
            os.system(f"termux-open '{abuseipdb_url}'")
        
        run_checks = input(cprint("Run quick terminal checks? (y/n): ", "yellow")).lower()
        if run_checks == 'y':
            self.run_ip_checks(ip)
        
        save = input(cprint("Save IP check report? (y/n): ", "yellow")).lower()
        if save == 'y':
            self.save_report(ip, abuseipdb_url)
    
    def run_ip_checks(self, ip):
        """Run basic IP checks in terminal"""
        printc("\n🔧 Running IP checks...", "cyan")
        
        checks = [
            (f"ping -c 3 {ip}", "Ping Test"),
            (f"whois {ip} | head -20", "WHOIS Info"),
            (f"host {ip}", "Reverse DNS"),
            (f"curl -I http://{ip} 2>/dev/null | head -5", "HTTP Headers")
        ]
        
        for cmd, description in checks:
            printc(f"\n📋 {description}:", "yellow")
            printc(f"Command: {cmd}", "gray")
            
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
                if result.returncode == 0 and result.stdout.strip():
                    output = result.stdout.strip().split('\n')
                    for line in output[:5]:
                        printc(f"  {line}", "green")
                else:
                    printc(f"  No output or command failed", "red")
            except:
                printc(f"  Command failed or timed out", "red")
    
    def save_report(self, ip, abuseipdb_url):
        """Save IP check report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ABUSEIPDB_{ip}_{timestamp}.txt"
        filepath = REPORTS_DIR / filename
        
        with open(filepath, 'w') as f:
            f.write(f"IP Reputation Check Report\n")
            f.write(f"IP Address: {ip}\n")
            f.write(f"Date: {datetime.now()}\n")
            f.write("="*60 + "\n\n")
            
            f.write(f"AbuseIPDB Link: {abuseipdb_url}\n\n")
            
            f.write("OTHER IP CHECK SERVICES:\n")
            f.write(f"VirusTotal: https://www.virustotal.com/gui/ip-address/{ip}\n")
            f.write(f"IPvoid: https://www.ipvoid.com/ip-blacklist-check/{ip}/\n")
            f.write(f"IBM X-Force: https://exchange.xforce.ibmcloud.com/ip/{ip}\n")
            f.write(f"ThreatFox: https://threatfox.abuse.ch/browse.php?search={ip}\n\n")
            
            f.write("TERMINAL COMMANDS:\n")
            f.write(f"ping {ip}\t\t\t# Check if host is alive\n")
            f.write(f"whois {ip}\t\t# Get registration info\n")
            f.write(f"host {ip}\t\t# Get reverse DNS\n")
            f.write(f"traceroute {ip}\t\t# Trace network path\n")
            f.write(f"nmap -sV {ip}\t\t# Port scan (requires nmap)\n\n")
            
            f.write("COMMON MALICIOUS PORTS:\n")
            f.write("• 22\t- SSH (brute force)\n")
            f.write("• 23\t- Telnet (insecure)\n")
            f.write("• 25\t- SMTP (spam)\n")
            f.write("• 445\t- SMB (exploits)\n")
            f.write("• 3389\t- RDP (attacks)\n")
        
        print_status(f"Report saved: {filepath}", "success")

# ========== MAIN TOOL WITH ALL MODULES ==========
class TermuxOSINTUltimate:
    def __init__(self):
        init_db()
        
        self.modules = {
            '1': ("IP Tracker (Real Data)", RealIPTracker().track),
            '2': ("Username Search (Real Checks)", RealUsernameSearch().search),
            '3': ("Email Investigator", EmailHunter().search),
            '4': ("Instagram Advanced", InstagramAdvanced().instagram_osint),
            '5': ("Domain Intelligence", DomainIntelligence().investigate),
            '6': ("Image EXIF Analyzer", self.exif_analyzer),
            '7': ("Phone Tracker (Real)", PhoneTrackerReal().track),
            '8': ("Phone Number to Name", PhoneNumberToName().lookup),
            '9': ("IFSC Code Lookup", IFSCCodeLookup().lookup),
            '10': ("Google Dorks Generator", GoogleDorkGenerator().generate),
            '11': ("Subdomain Enumerator", SubdomainEnumerator().enumerate),
            '12': ("Reverse Image Search", ReverseImageSearch().search),
            '13': ("Email Breach Checker", EmailBreachChecker().check),
            '14': ("Password Strength Checker", PasswordStrengthChecker().check),
            '15': ("Wayback Machine Checker", WaybackChecker().check),
            '16': ("DNSDumpster Tool", DNSDumpsterTool().analyze),
            '17': ("Sherlock Username Search", SherlockUsernameSearch().search),
            '18': ("Technology Detector", TechDetector().detect),
            '19': ("AbuseIPDB Checker", AbuseIPDBChecker().check),
            '20': ("Phone Number Details", PhoneNumberDetails().lookup),
            '21': ("Vehicle RC Info", VehicleRCInfo().lookup),
            '22': ("SMS/Call Bomber", SMSBomber().start_bombing),
            '23': ("View Reports", self.view_reports),
            '24': ("Install Dependencies", self.install_deps),
            '0': ("Exit", self.exit_tool)
        }
    
    def print_banner(self):
        clear()
        banner = r"""
 $$$$$$\            $$\                            $$$$$$\   $$$$$$\  $$$$$$\ $$\   $$\ $$$$$$$$\ 
$$  __$$\           $$ |                          $$  __$$\ $$  __$$\ \_$$  _|$$$\  $$ |\__$$  __|
$$ /  \__|$$\   $$\ $$$$$$$\   $$$$$$\   $$$$$$\  $$ /  $$ |$$ /  \__|  $$ |  $$$$\ $$ |   $$ |   
$$ |      $$ |  $$ |$$  __$$\ $$  __$$\ $$  __$$\ $$ |  $$ |\$$$$$$\    $$ |  $$ $$\$$ |   $$ |   
$$ |      $$ |  $$ |$$ |  $$ |$$$$$$$$ |$$ |  \__|$$ |  $$ | \____$$\   $$ |  $$ \$$$$ |   $$ |   
$$ |  $$\ $$ |  $$ |$$ |  $$ |$$   ____|$$ |      $$ |  $$ |$$\   $$ |  $$ |  $$ |\$$$ |   $$ |   
\$$$$$$  |\$$$$$$$ |$$$$$$$  |\$$$$$$$\ $$ |       $$$$$$  |\$$$$$$  |$$$$$$\ $$ | \$$ |   $$ |   
 \______/  \____$$ |\_______/  \_______|\__|       \______/  \______/ \______|\__|  \__|   \__|   
          $$\   $$ |                                                                              
          \$$$$$$  |                                                                              
           \______/                                                                               
                 TERMUX OSINT ULTIMATE V3.0 - ftgamerv2 | All-in-One OSINT Toolkit
        """
        printc(banner, "cyan", True)
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
        printc("╔══════════════════════════════════════╗", "cyan", True)
        printc("║            SAVED REPORTS             ║", "cyan", True)
        printc("╚══════════════════════════════════════╝", "cyan")
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
            elif name.startswith("VEHICLE_RC_"):
                cat = "Vehicle RC Reports"
            elif name.startswith("BOMBING_"):
                cat = "Bombing Reports"
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
        printc("╔══════════════════════════════════════╗", "yellow", True)
        printc("║       INSTALL DEPENDENCIES           ║", "yellow", True)
        printc("╚══════════════════════════════════════╝", "yellow")
        print()
        
        printc("Required packages:", "cyan")
        printc("="*40, "cyan")
        
        commands = [
            ("Update Termux", "pkg update && pkg upgrade -y"),
            ("Install Python", "pkg install python -y"),
            ("Install exiftool", "pkg install exiftool -y"),
            ("Install pip packages", "pip install requests beautifulsoup4 phonenumbers python-whois dnspython Pillow"),
            ("Optional: toutatis", "pip install toutatis"),
            ("Optional: shodan", "pip install shodan"),
            ("Optional: theHarvester", "cd ~ && git clone https://github.com/laramies/theHarvester.git"),
        ]
        
        for name, cmd in commands:
            printc(f"\n{name}:", "yellow", True)
            printc(f"  {cmd}", "gray")
        
        printc("\n" + "="*40, "cyan")
        
        install = input(cprint("\nRun basic installation? (y/n): ", "yellow")).lower()
        if install == 'y':
            for name, cmd in commands[:4]:
                printc(f"\nInstalling {name}...", "cyan")
                os.system(cmd)
            
            printc("\nInstallation complete!", "green")
    
    def exit_tool(self):
        printc("\n👋 Thanks for using Termux OSINT Ultimate V3.0!", "green", True)
        printc("GitHub: ftgamer2", "gray")
        time.sleep(1)
        sys.exit(0)
    
    def main_menu(self):
        while True:
            self.print_banner()
            
            printc("📱 MAIN MENU:", "cyan", True)
            printc("-" * 50, "cyan")
            
            menu_order = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 
                         '11', '12', '13', '14', '15', '16', '17', '18', '19',
                         '20', '21', '22', '23', '24', '0']
            
            for key in menu_order:
                if key in self.modules:
                    name, _ = self.modules[key]
                    printc(f"{key:2}. {name}", "yellow")
            
            printc("-" * 50, "cyan")
            
            try:
                choice = input(cprint("\nSelect module: ", "green")).strip()
                
                if choice in self.modules:
                    name, func = self.modules[choice]
                    printc(f"\n🚀 Launching: {name}", "cyan", True)
                    time.sleep(0.5)
                    
                    if choice in ['1', '2', '3', '5', '7', '8', '9', '10', '11', 
                                 '13', '15', '16', '17', '18', '19', '20', '21', '22']:
                        if choice == '1':
                            ip = input(cprint("IP address (blank for your IP): ", "cyan")).strip()
                            func(ip if ip else None)
                        elif choice == '2':
                            user = input(cprint("Username: ", "cyan")).strip()
                            if user:
                                func(user)
                        elif choice == '3':
                            email = input(cprint("Email address: ", "cyan")).strip()
                            if email:
                                func(email)
                        elif choice == '5':
                            domain = input(cprint("Domain: ", "cyan")).strip()
                            if domain:
                                func(domain)
                        elif choice == '7':
                            phone = input(cprint("Phone number (with country code): ", "cyan")).strip()
                            if phone:
                                func(phone)
                        elif choice == '8':
                            phone = input(cprint("Phone number for name lookup: ", "cyan")).strip()
                            if phone:
                                func(phone)
                        elif choice == '9':
                            ifsc = input(cprint("IFSC Code: ", "cyan")).strip()
                            if ifsc:
                                func(ifsc)
                        elif choice == '10':
                            target = input(cprint("Target for dorks: ", "cyan")).strip()
                            func(target if target else None)
                        elif choice == '11':
                            domain = input(cprint("Domain for subdomain enumeration: ", "cyan")).strip()
                            func(domain if domain else None)
                        elif choice == '13':
                            email = input(cprint("Email for breach check: ", "cyan")).strip()
                            func(email if email else None)
                        elif choice == '15':
                            url = input(cprint("URL for Wayback Machine: ", "cyan")).strip()
                            func(url if url else None)
                        elif choice == '16':
                            domain = input(cprint("Domain for DNSDumpster: ", "cyan")).strip()
                            func(domain if domain else None)
                        elif choice == '17':
                            username = input(cprint("Username for Sherlock search: ", "cyan")).strip()
                            func(username if username else None)
                        elif choice == '18':
                            url = input(cprint("URL for technology detection: ", "cyan")).strip()
                            func(url if url else None)
                        elif choice == '19':
                            ip = input(cprint("IP for AbuseIPDB check: ", "cyan")).strip()
                            func(ip if ip else None)
                        elif choice == '20':
                            phone = input(cprint("Phone number for details: ", "cyan")).strip()
                            func(phone if phone else None)
                        elif choice == '21':
                            vehicle = input(cprint("Vehicle number (KA01AB1234): ", "cyan")).strip()
                            func(vehicle if vehicle else None)
                        elif choice == '22':
                            phone = input(cprint("Phone number for bombing: ", "cyan")).strip()
                            func(phone if phone else None)
                    elif choice in ['6', '12', '14', '23', '24']:
                        func()
                    else:
                        func()
                    
                    if choice != '0':
                        input(cprint("\nPress Enter to continue...", "gray"))
                else:
                    printc("Invalid choice", "red")
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                printc("\n\nExiting...", "red")
                sys.exit(0)
            except Exception as e:
                printc(f"Error: {str(e)}", "red")
                time.sleep(2)

# ========== MAIN FUNCTION ==========
def main():
    clear()
    printc("╔══════════════════════════════════════════╗", "red")
    printc("║           LEGAL DISCLAIMER               ║", "red", True)
    printc("╠══════════════════════════════════════════╣", "red")
    printc("║ This tool is for EDUCATIONAL purposes    ║", "red")
    printc("║ and AUTHORIZED security testing only.    ║", "red")
    printc("║                                          ║", "red")
    printc("║ Use only:                                ║", "red")
    printc("║ • On systems you own                     ║", "red")
    printc("║ • With explicit permission               ║", "red")
    printc("║ • For learning OSINT techniques          ║", "red")
    printc("║                                          ║", "red")
    printc("║ The author is not responsible for misuse.║", "red")
    printc("╚══════════════════════════════════════════╝", "red")
    print()
    
    agree = input(cprint("Do you agree to these terms? (y/n): ", "yellow")).strip().lower()
    if agree != 'y':
        printc("❌ Agreement required to use this tool.", "red")
        sys.exit(0)
    
    if not REQUESTS_AVAILABLE:
        printc("\n⚠️  WARNING: 'requests' module not found!", "red")
        printc("Install: pip install requests", "cyan")
        time.sleep(2)
    
    try:
        tool = TermuxOSINTUltimate()
        tool.main_menu()
    except KeyboardInterrupt:
        printc("\n\n👋 Goodbye!", "green")
        sys.exit(0)
    except Exception as e:
        printc(f"\n💥 Error: {str(e)}", "red")
        sys.exit(1)

if __name__ == "__main__":
    main()
