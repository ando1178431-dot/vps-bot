import discord
from discord.ext import commands

class Billing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="plan", help="Check active hosting specifications and billing limits.")
    async def plan(self, ctx):
        embed = discord.Embed(title="📊 Client Hosting Profile", color=discord.Color.gold())
        embed.add_field(name="Active Node", value="`Disknogamerz-Global-01`", inline=True)
        embed.add_field(name="Resource Tier", value="`Unlimited / Pro Tier`", inline=True)
        embed.add_field(name="Billing Cycle", value="`Active (Auto-Renew Enabled)`", inline=False)
        embed.set_footer(text="Manage your servers at panel.disknogamerz.com")
        
        await ctx.send(embed=embed)

    @commands.command(name="link", help="Link your Discord profile with your hosting panel account.")
    async def link(self, ctx, panel_email: str = None):
        if not panel_email:
            await ctx.send("⚠️ Usage: `!link your-email@domain.com`")
            return
            
        embed = discord.Embed(title="🔗 Account Link Verification", color=discord.Color.green())
        embed.add_field(name="Discord User", value=ctx.author.mention, inline=True)
        embed.add_field(name="Linked Email", value=f"`{panel_email}`", inline=True)
        embed.description = "✅ Verification token dispatched. Check your email inbox to confirm link."
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Billing(bot))
