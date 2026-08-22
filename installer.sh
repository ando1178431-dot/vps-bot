#!/bin/bash

# ==========================================
# DISKNOGAMERZ VPS BOT - ENTERPRISE SUITE
# ==========================================

PROJECT_DIR="/root/vps-bot"
REPO_URL="https://github.com/ando1178431-dot/vps-bot.git"

# Advanced TrueColor & Styling Definitions
RESTORE='\033[0m'
BLACK='\033[0;30m'
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
B_RED='\033[1;31m'
B_GREEN='\033[1;32m'
B_CYAN='\033[1;36m'
BG_BLUE='\033[44m'
BG_DARK='\033[40m'

clear

# Gorgeous ASCII Header Banner
echo -e "${B_CYAN}================================================================${RESTORE}"
echo -e "${BG_BLUE}${WHITE}          ⚡ DISKNOGAMERZ ENTERPRISE HOSTING PANEL ⚡           ${RESTORE}"
echo -e "${B_CYAN}================================================================${RESTORE}"
echo -e "${PURPLE}  [i] Target Node Core: ${WHITE}Ubuntu Linux / Docker Engine${RESTORE}"
echo -e "${PURPLE}  [i] Author Framework: ${WHITE}Disknogamerz Automation Daemon${RESTORE}"
echo -e "${B_CYAN}----------------------------------------------------------------${RESTORE}"

# 1. Directory & Git Synchronization with Aesthetic Output
if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${YELLOW}[+] Deploying workspace repository into ${WHITE}$PROJECT_DIR${YELLOW}...${RESTORE}"
    git clone "$REPO_URL" "$PROJECT_DIR" > /dev/null 2>&1
else
    echo -e "${GREEN}[✔] Existing project directory detected. Syncing updates...${RESTORE}"
    cd "$PROJECT_DIR" || exit
    git pull origin main || git pull origin master > /dev/null 2>&1
fi

cd "$PROJECT_DIR" || exit

# 2. Python Environment & Requirements Setup
echo -e "${YELLOW}[*] Validating dependencies & updating environment packages...${RESTORE}"
python3 -m pip install --upgrade pip > /dev/null 2>&1
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt > /dev/null 2>&1
else
    pip3 install discord.py psutil requests aiohttp rsa > /dev/null 2>&1
fi

# 3. Configuration Check
if [ ! -f "config.json" ]; then
    echo -e "\n${B_RED}[!] CRITICAL WARNING: No active config.json found!${RESTORE}"
    echo -e "${YELLOW}[*] Launching configuration wizard to link your bot token...${RESTORE}"
    python3 installer.py
fi

# 4. Safe Bot Execution (Background Daemon Mode)
echo -e "${CYAN}[*] Flushing legacy background processes and starting bot core...${RESTORE}"
pkill -f main.py > /dev/null 2>&1
nohup python3 main.py > bot.log 2>&1 &

echo -e "\n${B_GREEN}╔══════════════════════════════════════════════════════════════╗${RESTORE}"
echo -e "${B_GREEN}║             🚀 BOT IS ONLINE & HEALTHY IN BACKGROUND        ║${RESTORE}"
echo -e "${B_GREEN}╚══════════════════════════════════════════════════════════════╝${RESTORE}"
echo -e "📄 Live Stream File: ${CYAN}$PROJECT_DIR/bot.log${RESTORE}\n"

# 5. Interactive Colorful Manager Loop
while true; do
    echo -e "${B_CYAN}┌──────────────────────────────────────────────────────────────┐${RESTORE}"
    echo -e "${B_CYAN}│                   🛡️  CONTROL CENTER MENU                    │${RESTORE}"
    echo -e "${B_CYAN}├──────────────────────────────────────────────────────────────┤${RESTORE}"
    echo -e "${B_CYAN}│${RESTORE}  ${GREEN}[1]${RESTORE} 📋 View Live Bot Console Logs                          ${B_CYAN}│${RESTORE}"
    echo -e "${B_CYAN}│${RESTORE}  ${GREEN}[2]${RESTORE} 🔄 Restart Bot Daemon Instance                         ${B_CYAN}│${RESTORE}"
    echo -e "${B_CYAN}│${RESTORE}  ${GREEN}[3]${RESTORE} 🌐 Pull GitHub Updates & Re-deploy                     ${B_CYAN}│${RESTORE}"
    echo -e "${B_CYAN}│${RESTORE}  ${GREEN}[4]${RESTORE} 🐳 Inspect Active Docker Containers                    ${B_CYAN}│${RESTORE}"
    echo -e "${B_CYAN}│${RESTORE}  ${GREEN}[5]${RESTORE} ⚙️  Configure / Re-link Bot Token (installer.py)       ${B_CYAN}│${RESTORE}"
    echo -e "${B_CYAN}│${RESTORE}  ${GREEN}[6]${RESTORE} 🚪 Exit to Shell (Bot keeps running safely)          ${B_CYAN}│${RESTORE}"
    echo -e "${B_CYAN}└──────────────────────────────────────────────────────────────┘${RESTORE}"
    
    echo -ne "${YELLOW}🎛️ Select control index [1-6]: ${RESTORE}"
    read -r choice

    case $choice in
        1)
            echo -e "\n${PURPLE}=== [ LAST 30 LINES OF BOT LOGS ] ===${RESTORE}"
            tail -n 30 bot.log
            echo -e "${PURPLE}=====================================${RESTORE}\n"
            ;;
        2)
            echo -e "\n${YELLOW}[*] Restarting bot core process...${RESTORE}"
            pkill -f main.py
            nohup python3 main.py > bot.log 2>&1 &
            sleep 1
            echo -e "${B_GREEN}[✔] Bot core restarted successfully!${RESTORE}\n"
            ;;
        3)
            echo -e "\n${YELLOW}[*] Pulling latest repository code from GitHub...${RESTORE}"
            git pull origin main || git pull origin master
            pip3 install -r requirements.txt > /dev/null 2>&1
            pkill -f main.py
            nohup python3 main.py > bot.log 2>&1 &
            echo -e "${B_GREEN}[✔] System updated, dependencies refreshed, & bot restarted!${RESTORE}\n"
            ;;
        4)
            echo -e "\n${PURPLE}=== [ ACTIVE DOCKER CONTAINERS ] ===${RESTORE}"
            docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
            echo -e "${PURPLE}====================================${RESTORE}\n"
            ;;
        5)
            echo -e "\n${YELLOW}[*] Opening configuration setup utility...${RESTORE}"
            python3 installer.py
            pkill -f main.py
            nohup python3 main.py > bot.log 2>&1 &
            echo -e "${B_GREEN}[✔] New token profile saved and bot re-launched!${RESTORE}\n"
            ;;
        6)
            echo -e "\n${CYAN}Exiting panel manager. Your bot remains fully secure in the background.${RESTORE}"
            exit 0
            ;;
        *)
            echo -e "\n${B_RED}[x] Invalid option selection! Please pick a number from 1 to 6.${RESTORE}\n"
            ;;
    esac
done
