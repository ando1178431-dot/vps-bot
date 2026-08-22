#!/bin/bash

# Define project directory
PROJECT_DIR="/root/vps-bot"

echo "=========================================="
echo "    DISKNOGAMERZ VPS BOT AUTO-INSTALLER   "
echo "=========================================="

# Check if project folder exists, if not clone it
if [ ! -d "$PROJECT_DIR" ]; then
    echo "[+] Cloning repository..."
    git clone https://github.com/ando1178431-dot/vps-bot.git "$PROJECT_DIR"
fi

# Navigate into project directory
cd "$PROJECT_DIR" || exit

echo "[+] Pulling latest updates from GitHub..."
git pull origin main

echo "[+] Installing/updating Python dependencies..."
pip3 install -r requirements.txt

echo "[+] Restarting bot safely..."
pkill -f main.py
nohup python3 main.py > bot.log 2>&1 &

echo "=========================================="
echo "     BOT SUCCESSFULLY STARTED & UPDATED!    "
echo "=========================================="
