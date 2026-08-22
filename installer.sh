#!/bin/bash

# ==========================================
# DISKNOGAMERZ VPS BOT - ENTERPRISE INSTALLER
# ==========================================

PROJECT_DIR="/root/vps-bot"
REPO_URL="https://github.com/ando1178431-dot/vps-bot.git"

# Text Styling
RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

clear
echo "===================================================="
echo "        DISKNOGAMERZ ENTERPRISE HOSTING SUITE       "
echo "===================================================="

# 1. Directory & Git Synchronization
if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${YELLOW}[+] Cloning repository...${NC}"
    git clone "$REPO_URL" "$PROJECT_DIR"
else
    echo -e "${YELLOW}[+] Pulling latest updates...${NC}"
    cd "$PROJECT_DIR" || exit
    git pull origin main || git pull origin master
fi

cd "$PROJECT_DIR" || exit

# 2. Setup
python3 -m pip install --upgrade pip > /dev/null 2>&1
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt > /dev/null 2>&1
fi

# 3. Check config
if [ ! -f "config.json" ]; then
    echo -e "${RED}[!] No config.json found. Running installer.py...${NC}"
    python3 installer.py
fi

# 4. Start Bot
echo -e "${CYAN}[*] Starting bot...${NC}"
pkill -f main.py > /dev/null 2>&1
nohup python3 main.py > bot.log 2>&1 &
echo -e "${GREEN}[✔] BOT SUCCESSFULLY STARTED!${NC}"

# 5. Interactive Loop
while true; do
    echo ""
    echo "--- DISKNOGAMERZ VPS CONTROL PANEL ---"
    echo "1) View Live Bot Logs"
    echo "2) Restart Bot Process"
    echo "3) Pull Latest GitHub Updates & Restart"
    echo "4) Check Docker Container Status"
    echo "5) Make / Reconfigure Bot (Run installer.py)"
    echo "6) Exit to Shell"
    read -p "Select an option [1-6]: " choice

    case $choice in
        1)
            tail -n 30 bot.log
            ;;
        2)
            pkill -f main.py
            nohup python3 main.py > bot.log 2>&1 &
            echo -e "${GREEN}[✔] Bot restarted!${NC}"
            ;;
        3)
            git pull origin main || git pull origin master
            pip3 install -r requirements.txt > /dev/null 2>&1
            pkill -f main.py
            nohup python3 main.py > bot.log 2>&1 &
            echo -e "${GREEN}[✔] Updated and restarted!${NC}"
            ;;
        4)
            docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
            ;;
        5)
            python3 installer.py
            pkill -f main.py
            nohup python3 main.py > bot.log 2>&1 &
            echo -e "${GREEN}[✔] Reconfigured and restarted!${NC}"
            ;;
        6)
            exit 0
            ;;
        *)
            echo "Invalid option."
            ;;
    esac
done
