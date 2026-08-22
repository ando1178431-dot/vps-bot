#!/bin/bash

# Colors for Disknogamerz GUI styling
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

clear
echo -e "${BLUE}==================================================${NC}"
echo -e "${GREEN}        DISKNOGAMERZ VPS BOT INSTALLER            ${NC}"
echo -e "${BLUE}==================================================${NC}"

# Step 1: Check & Install Dependencies
echo -e "\n[*] Checking system dependencies..."
if ! command -v python3 &> /dev/null; then
    echo "[!] Python3 not found. Installing..."
    sudo apt update && sudo apt install -y python3 python3-pip git
else
    echo "[+] Python3 is installed."
fi

if ! command -v docker &> /dev/null; then
    echo "[!] Docker not found. Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
else
    echo "[+] Docker is installed."
fi

# Step 2: Set up Project Directory
INSTALL_DIR="/opt/disknogamerz-vps-bot"
echo -e "\n[*] Setting up workspace in $INSTALL_DIR..."
sudo mkdir -p $INSTALL_DIR
sudo chown -R $USER:$USER $INSTALL_DIR

# Clone or pull files from GitHub repo
if [ -d "$INSTALL_DIR/.git" ]; then
    echo "[*] Updating existing repository..."
    cd $INSTALL_DIR
    git pull
else
    echo "[*] Downloading files from GitHub..."
    git clone https://github.com/ando1178431-dot/vps-bot.git $INSTALL_DIR
    cd $INSTALL_DIR
fi

# Step 3: Launch Python GUI
echo -e "\n${GREEN}[+] Launching Disknogamerz Choice-able GUI...${NC}"
sleep 2
python3 installer.py
