import os
import json
import asyncio
import discord
from discord.ext import commands

CONFIG_FILE = "config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

config = load_config()
TOKEN = config.get("token")
PREFIX = config.get("prefix", "!")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print("--------------------------------------------------")
    print(f"Logged in as: {bot.user.name} (ID: {bot.user.id})")
    print(f"Disknogamerz Modular VPS Bot is Online & Ready!")
    print("--------------------------------------------------")
    await bot.change_presence(activity=discord.Game(name="Disknogamerz Hosting | !stats"))

async def load_extensions():
    if not os.path.exists("./cogs"):
        os.makedirs("./cogs")
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            extension_name = f"cogs.{filename[:-3]}"
            try:
                await bot.load_extension(extension_name)
                print(f"[+] Loaded extension: {filename}")
            except Exception as e:
                print(f"[!] Failed to load {filename}: {e}")

async def main():
    if not TOKEN:
        print("[!] Error: No token found in config.json! Run installer.py first.")
        return
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
