import discord
from discord.ext import commands

class HelpView(discord.ui.View):
    def __init__(self, author_id):
        super().__init__(timeout=120)
        self.author_id = author_id

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author_id:
            await interaction.response.send_message("❌ This help menu is not for you.", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="🛡️ Server Management", style=discord.ButtonStyle.blurple, custom_id="help_server")
    async def server_help(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="⚙️ Server Management & Deployment", color=discord.Color.blue())
        embed.description = (
            "• **.deploy [ram] [cpu]** - Open the interactive VPS provisioner with custom specs.\n"
            "• **.vpsaction [restart/status]** - Manage container infrastructure states."
        )
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="📊 Monitoring", style=discord.ButtonStyle.green, custom_id="help_monitor")
    async def monitor_help(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="📊 Node Performance & Stats", color=discord.Color.green())
        embed.description = (
            "• **.stats** - Real-time tracking of CPU, RAM, and Disk storage utilization."
        )
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="💳 Billing & Account", style=discord.ButtonStyle.grey, custom_id="help_billing")
    async def billing_help(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="💳 Billing & Profile Links", color=discord.Color.gold())
        embed.description = (
            "• **.plan** - View active hosting tier and hardware allocation specs.\n"
            "• **.link [email]** - Link your Discord profile to your hosting dashboard."
        )
        await interaction.response.edit_message(embed=embed, view=self)

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Remove default help command to prevent overlap
        self.bot.remove_command("help")

    @commands.command(name="help", help="Shows the interactive button help menu.")
    async def help(self, ctx):
        embed = discord.Embed(title="🌟 Disknogamerz VPS Bot - Help Desk", color=discord.Color.blurple())
        embed.description = "Select a category using the interactive buttons below to view available commands."
        embed.set_footer(text="Disknogamerz Enterprise Hosting Framework")
        
        view = HelpView(ctx.author.id)
        await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Help(bot))
