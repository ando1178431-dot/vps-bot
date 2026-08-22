#!/bin/bash

# ==========================================
# DISKNOGAMERZ VPS BOT - ENTERPRISE INSTALLER
# ==========================================

PROJECT_DIR="/root/vps-bot"
REPO_URL="https://github.com/ando1178431-dot/vps-bot.git"

# Text Styling Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

clear
echo -e "${CYAN}====================================================${NC}"
echo -e "${CYAN}        DISKNOGAMERZ ENTERPRISE HOSTING SUITE       ${NC}"
echo -e "${CYAN}====================================================${NC}"

# 1. System Dependency & Root Check
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}[x] Error: This installer must be run as root/sudo!${NC}"
    exit 1
fi

echo -e "${YELLOW}[*] Checking required system packages (git, python3, pip, docker)...${NC}"
apt-get update -y > /dev/null 2>&1
for pkg in git python3 python3-pip docker.io curl; do
    if ! command -v $pkg &> /dev/null; then
        echo -e "${YELLOW}[+] Installing missing dependency: $pkg...${NC}"
        apt-get install -y $pkg > /dev/null 2>&1
    fi
done

# Start Docker daemon if inactive
systemctl start docker > /dev/null 2>&1

# 2. Directory & Git Synchronization
if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${YELLOW}[+] Cloning Disknogamerz repository into $PROJECT_DIR...${NC}"
    git clone "$REPO_URL" "$PROJECT_DIR"
else
    echo -e "${YELLOW}[+] Repository found. Pulling latest code updates...${NC}"
    cd "$PROJECT_DIR" || exit
    git pull origin main || git pull origin master
fi

cd "$PROJECT_DIR" || exit

# 3. Python Environment & Requirements Setup
echo -e "${YELLOW}[*] Installing/updating Python modules from requirements.txt...${NC}"
python3 -m pip install --upgrade pip > /dev/null 2>&1
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt > /dev/null 2>&1
else
    echo -e "${RED}[x] Warning: requirements.txt not found! Installing core dependencies manually...${NC}"
    pip3 install discord.py psutil requests aiohttp rsa > /dev/null 2>&1
fi

# 4. Safe Bot Execution (Background Daemon Mode)
echo -e "${YELLOW}[*] Terminating any legacy bot instances...${NC}"
pkill -f main.py > /dev/null 2>&1

echo -e "${YELLOW}[*] Launching bot background daemon...${NC}"
nohup python3 main.py > bot.log 2>&1 &

echo -e "${GREEN}====================================================${NC}"
echo -e "${GREEN}      SUCCESS: BOT IS ONLINE AND RUNNING!           ${NC}"
echo -e "${GREEN}====================================================${NC}"
echo -e "Logs are streaming to: ${CYAN}$PROJECT_DIR/bot.log${NC}\n"

# 5. Interactive Manager Loop (Keeps the script alive and functional)
while true; do
    echo -e "${CYAN}--- DISKNOGAMERZ VPS CONTROL PANEL ---${NC}"
    echo "1) View Live Bot Logs"
    echo "2) Restart Bot Process"
    echo "3) Pull Latest GitHub Updates & Restart"
    echo "4) Check Docker Container Status"
    echo "5) Exit to Shell"
    read -p "Select an option [1-5]: " choice

    case $choice in
        1)
            echo -e "${YELLOW}[*] Showing last 30 lines of bot.log (Ctrl+C to exit log view):${NC}"
            sleep 1
            tail -n 30 bot.log
            echo ""
            ;;
        2)
            echo -e "${YELLOW}[*] Restarting bot...${NC}"
            pkill -f main.py
            nohup python3 main.py > bot.log 2>&1 &
            echo -e "${GREEN}[✔] Bot restarted successfully!${NC}\n"
            ;;
        3)
            echo -e "${YELLOW}[*] Pulling from GitHub and updating dependencies...${NC}"
            git pull origin main || git pull origin master
            pip3 install -r requirements.txt > /dev/null 2>&1
            pkill -f main.py
            nohup python3 main.py > bot.log 2>&1 &
            echo -e "${GREEN}[✔] Update complete and bot restarted!${NC}\n"
            ;;
        4)
            echo -e "${YELLOW}[*] Active Docker containers on this node:${NC}"
            docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
            echo ""
            ;;
        5)
            echo -e "${CYAN}Exiting manager panel. Bot remains running safely in background.${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}[x] Invalid option. Please choose between 1 and 5.${NC}\n"
            ;;
    esac
done
