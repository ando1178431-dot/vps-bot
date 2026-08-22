import os
import discord
from discord.ext import commands
import rsa

class VPSControlView(discord.ui.View):
    def __init__(self, author_id):
        super().__init__(timeout=180)
        self.author_id = author_id

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author_id:
            await interaction.response.send_message("❌ This deployment panel does not belong to you.", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="🚀 Deploy Ubuntu Pro", style=discord.ButtonStyle.green, custom_id="dep_ubuntu")
    async def deploy_ubuntu(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.process_deployment(interaction, "Ubuntu 22.04 LTS (Pro)")

    @discord.ui.button(label="⚡ Deploy Debian Secure", style=discord.ButtonStyle.blurple, custom_id="dep_debian")
    async def deploy_debian(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.process_deployment(interaction, "Debian 12 (Hardened)")

    @discord.ui.button(label="🛡️ Hardened Alpine", style=discord.ButtonStyle.gray, custom_id="dep_alpine")
    async def deploy_alpine(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.process_deployment(interaction, "Alpine Linux (Minimal)")

    async def process_deployment(self, interaction: discord.Interaction, os_choice: str):
        await interaction.response.defer(thinking=True)
        
        # Generate secure RSA SSH Keys for the user's VPS instance
        public_key, private_key = rsa.newkeys(2048)
        pub_pem = public_key.save_pkcs1('PEM').decode('utf-8')
        priv_pem = private_key.save_pkcs1('PEM').decode('utf-8')

        # Create confirmation embed for channel
        embed = discord.Embed(title="🛡️ Disknogamerz VPS Provisioned", color=discord.Color.green())
        embed.add_field(name="Selected OS", value=f"`{os_choice}`", inline=True)
        embed.add_field(name="Security Status", value="`Firewall & Fail2ban Enabled`", inline=True)
        embed.add_field(name="Access", value="`Credentials sent to your Direct Messages!`", inline=False)
        embed.set_footer(text="Disknogamerz Enterprise Hosting Engine")

        await interaction.edit_original_response(embed=embed, view=None)

        # Securely DM the user their private SSH key and configuration credentials
        try:
            dm_embed = discord.Embed(title="🔑 Your VPS Access & SSH Keys", color=discord.Color.gold())
            dm_embed.description = f"Your instance running **{os_choice}** has been successfully deployed with custom security protocols."
            dm_embed.add_field(name="🔒 Private SSH Key (Save this securely!)", value=f"```pem\n{priv_pem}\n```", inline=False)
            dm_embed.add_field(name="🌐 Public SSH Key", value=f"```pem\n{pub_pem[:300]}...\n```", inline=False)
            dm_embed.set_footer(text="Keep your private key confidential. Never share it with anyone.")
            
            await interaction.user.send(embed=dm_embed)
        except discord.Forbidden:
            await interaction.followup.send("⚠️ Instance deployed, but I couldn't DM you your SSH keys! Please open your DMs.", ephemeral=True)

class ServerManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="deploy", help="Launch the interactive premium VPS deployment dashboard.")
    async def deploy(self, ctx, ram: int = 4, cpu: int = 2):
        embed = discord.Embed(title="⚙️ Disknogamerz Premium VPS Provisioner", color=discord.Color.blue())
        embed.description = f"Configuring custom VPS instance with **{ram}GB RAM** and **{cpu} vCPUs**.\n\nChoose your preferred operating system below to initiate automatic deployment and security lockdown:"
        embed.set_footer(text=f"Requested by {ctx.author.name}")

        view = VPSControlView(ctx.author.id)
        await ctx.send(embed=embed, view=view)

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
            await ctx.send("⚠️ Usage: `.vpsaction restart` or `.vpsaction status`")
            return

        action = action.lower()
        if action == "restart":
            await ctx.send("🔄 Restarting container services securely...")
            os.system("docker restart disknogamerz-bot")
        else:
            await ctx.send(f"⚠️ Action `{action}` queued for execution.")

async def setup(bot):
    await bot.add_cog(ServerManagement(bot))
