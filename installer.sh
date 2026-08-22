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
    token = input("Enter your Discord Bot Token: ").strip()
    owner_id = input("Enter your Discord Admin/Owner User ID: ").strip()
    prefix = input("Enter Bot Command Prefix (e.g., ! or /): ").strip() or "!"

    config = {
        "token": token,
        "owner_id": owner_id,
        "prefix": prefix
    }
    save_config(config)
    
    print("\n[+] Configuration saved successfully!")
    print("[+] Building environment & starting bot container...")
    
    # Check if docker-compose or docker is available to run the bot
    if os.path.exists("docker-compose.yml"):
        subprocess.run(["docker", "compose", "up", "-d", "--build"])
    else:
        print("[!] Warning: docker-compose.yml not found. Make sure bot dependencies are handled.")
    
    input("\nPress Enter to go to the Management Dashboard...")
    manage_vps_dashboard()

def manage_bot_files():
    clear_screen()
    print_banner()
    print("\n--- MANAGE BOT & EXECUTE COMMANDS ---")
    print(" [1] Pull latest updates from GitHub")
    print(" [2] View live bot container logs")
    print(" [3] Restart Bot Container")
    print(" [4] Back to Dashboard")
    
    choice = input("\nSelect an option [1-4]: ").strip()
    
    if choice == "1":
        print("[*] Pulling latest code from GitHub...")
        subprocess.run(["git", "pull"])
        input("\nUpdate complete. Press Enter to continue...")
        manage_bot_files()
    elif choice == "2":
        print("[*] Streaming logs (Press Ctrl+C to exit logs)...")
        try:
            subprocess.run(["docker", "logs", "-f", "disknogamerz-bot"])
        except KeyboardInterrupt:
            pass
        manage_bot_files()
    elif choice == "3":
        print("[*] Restarting bot container...")
        subprocess.run(["docker", "restart", "disknogamerz-bot"])
        print("[+] Bot restarted!")
        time.sleep(2)
        manage_bot_files()
    elif choice == "4":
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
    
    print("\nDo you want to update these credentials? (y/n)")
    if input("> ").lower() == 'y':
        setup_bot()
    else:
        manage_vps_dashboard()

def manage_vps_dashboard():
    while True:
        clear_screen()
        print_banner()
        print("\n             BOT SUCCESSFULLY CREATED!")
        print("=" * 50)
        print(" [1] Manage Bot & Execute Commands (Logs, Files, Updates)")
        print(" [2] Manage VPS Bot Config (Change Tokens & Versions)")
        print(" [3] Exit to Terminal")
        print("=" * 50)
        
        choice = input("Select an option [1-3]: ").strip()
        
        if choice == "1":
            manage_bot_files()
        elif choice == "2":
            manage_vps_config()
        elif choice == "3":
            print("Exiting manager. Bot is running safely in background!")
            sys.exit(0)

def main_menu():
    while True:
        clear_screen()
        print_banner()
        print(" [1] Make Bot (Initial Setup & Configuration)")
        print(" [2] Exit")
        print("=" * 50)
        
        choice = input("Select an option [1-2]: ").strip()
        
        if choice == "1":
            if os.path.exists(CONFIG_FILE):
                print("\n[!] Configuration already exists!")
                print(" [1] Reconfigure / Make New")
                print(" [2] Open Management Dashboard")
                sub = input("Select option [1-2]: ").strip()
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
