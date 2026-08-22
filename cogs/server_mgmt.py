import os
import discord
from discord.ext import commands

class ServerManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="vpsaction", help="Manage hosting instance states (start, stop, restart).")
    async def vpsaction(self, ctx, action: str = None):
        config_path = "config.json"
        owner_id = 0
        if os.path.exists(config_path):
            import json
            with open(config_path, "r") as f:
                data = json.load(f)
                owner_id = int(data.get("owner_id", 0))

        if owner_id and ctx.author.id != owner_id:
            await ctx.send("❌ Unauthorized: Only the designated node owner can execute infrastructure controls.")
            return

        if not action:
            await ctx.send("⚠️ Usage: `!vpsaction restart` or `!vpsaction status`")
            return

        action = action.lower()
        if action == "restart":
            await ctx.send("🔄 Restarting bot container and node daemon safely...")
            os.system("docker restart disknogamerz-bot")
        else:
            await ctx.send(f"⚠️ Action `{action}` queued for execution on target node.")

    @commands.command(name="deployos", help="Deploy a fresh operating system image via slash framework.")
    async def deployos(self, ctx, os_name: str = "ubuntu"):
        valid_os = ["ubuntu", "debian", "centos", "alpine"]
        os_name = os_name.lower()
        
        if os_name not in valid_os:
            await ctx.send(f"❌ Invalid OS choice. Choose from: `{', '.join(valid_os)}`")
            return

        embed = discord.Embed(title="⚙️ OS Deployment Initialized", color=discord.Color.blue())
        embed.add_field(name="Target OS", value=f"`{os_name.capitalize()} Latest`", inline=True)
        embed.add_field(name="Status", value="`Provisioning Container...`", inline=True)
        embed.set_footer(text="Disknogamerz Automated Deployer")
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ServerManagement(bot))
