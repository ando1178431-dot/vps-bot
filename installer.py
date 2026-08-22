import os
import sys
import json
import subprocess
import time

CONFIG_FILE = "config.json"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    print("=" * 50)
    print("        DISKNOGAMERZ VPS BOT MANAGER (v1.0)")
    print("=" * 50)

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

def setup_bot():
    clear_screen()
    print_banner()
    print("\n--- INITIAL BOT CONFIGURATION ---")
    try:
        token = input("Enter your Discord Bot Token: ").strip()
        owner_id = input("Enter your Discord Admin/Owner User ID: ").strip()
        prefix = input("Enter Bot Command Prefix (e.g., !): ").strip() or "!"
    except (KeyboardInterrupt, EOFError):
        return

    config = {
        "token": token,
        "owner_id": owner_id,
        "prefix": prefix
    }
    save_config(config)
    
    print("\n[+] Configuration saved successfully!")
    
    # Try Docker first, otherwise fallback to running Python directly
    print("[*] Attempting to start bot...")
    docker_check = subprocess.run(["docker", "ps"], capture_output=True, text=True)
    
    if docker_check.returncode == 0 and os.path.exists("docker-compose.yml"):
        print("[+] Docker detected. Starting via Docker Compose...")
        subprocess.run(["docker", "compose", "up", "-d", "--build"])
    else:
        print("[!] Docker unavailable. Launching bot directly with Python (Background mode)...")
        # Install requirements just in case
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "-q"])
        # Run main.py in background using nohup or screen equivalent, or just start it
        subprocess.Popen([sys.executable, "main.py"])
        print("[+] Bot started successfully in background!")
    
    input("\nPress Enter to go to the Management Dashboard...")
    manage_vps_dashboard()

def manage_bot_files():
    clear_screen()
    print_banner()
    print("\n--- MANAGE BOT & EXECUTE COMMANDS ---")
    print(" [1] Pull latest updates from GitHub")
    print(" [2] View live bot status / restart")
    print(" [3] Back to Dashboard")
    
    try:
        choice = input("\nSelect an option [1-3]: ").strip()
    except (KeyboardInterrupt, EOFError):
        return manage_vps_dashboard()
    
    if choice == "1":
        print("[*] Pulling latest code from GitHub...")
        subprocess.run(["git", "pull"])
        input("\nUpdate complete. Press Enter to continue...")
        manage_bot_files()
    elif choice == "2":
        print("[*] Restarting Python bot service...")
        os.system("pkill -f main.py")
        subprocess.Popen([sys.executable, "main.py"])
        print("[+] Bot service restarted and brought online!")
        time.sleep(2)
        manage_bot_files()
    elif choice == "3":
        manage_vps_dashboard()
    else:
        manage_bot_files()

def manage_vps_config():
    clear_screen()
    print_banner()
    print("\n--- MANAGE VPS BOT CONFIG ---")
    config = load_config()
    print(f"Current Token: {config.get('token', 'Not Set')[:10]}...")
    print(f"Current Owner ID: {config.get('owner_id', 'Not Set')}")
    print(f"Current Prefix: {config.get('prefix', '!')}")
    
    try:
        choice = input("\nDo you want to update these credentials? (y/n): ").strip().lower()
    except (KeyboardInterrupt, EOFError):
        return manage_vps_dashboard()

    if choice == 'y':
        setup_bot()
    else:
        manage_vps_dashboard()

def manage_vps_dashboard():
    while True:
        clear_screen()
        print_banner()
        print("\n             BOT SUCCESSFULLY CREATED!")
        print("=" * 50)
        print(" [1] Manage Bot & Execute Commands")
        print(" [2] Manage VPS Bot Config (Change Tokens)")
        print(" [3] Exit to Terminal")
        print("=" * 50)
        
        try:
            choice = input("Select an option [1-3]: ").strip()
        except (KeyboardInterrupt, EOFError):
            sys.exit(0)
        
        if choice == "1":
            manage_bot_files()
        elif choice == "2":
            manage_vps_config()
        elif choice == "3":
            print("Exiting manager. Bot is running safely!")
            sys.exit(0)

def main_menu():
    while True:
        clear_screen()
        print_banner()
        print(" [1] Make Bot (Initial Setup & Configuration)")
        print(" [2] Exit")
        print("=" * 50)
        
        try:
            choice = input("Select an option [1-2]: ").strip()
        except (KeyboardInterrupt, EOFError):
            sys.exit(0)
        
        if choice == "1":
            if os.path.exists(CONFIG_FILE):
                print("\n[!] Configuration already exists!")
                print(" [1] Reconfigure / Make New")
                print(" [2] Open Management Dashboard")
                try:
                    sub = input("Select option [1-2]: ").strip()
                except (KeyboardInterrupt, EOFError):
                    continue
                if sub == "1":
                    setup_bot()
                else:
                    manage_vps_dashboard()
            else:
                setup_bot()
        elif choice == "2":
            print("Goodbye!")
            sys.exit(0)

if __name__ == "__main__":
    main_menu()
