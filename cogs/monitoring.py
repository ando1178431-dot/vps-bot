import psutil
import discord
from discord.ext import commands, tasks

class Monitoring(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="stats", help="Check real-time CPU, RAM, and Disk usage of the VPS.")
    async def stats(self, ctx):
        cpu_usage = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Color coding based on health
        embed_color = discord.Color.green() if cpu_usage < 80 else discord.Color.red()
        
        embed = discord.Embed(title="🖥️ Disknogamerz Node Performance", color=embed_color)
        embed.add_field(name="CPU Utilization", value=f"`{cpu_usage}%`", inline=True)
        embed.add_field(name="RAM Allocation", value=f"`{memory.percent}%`\n({memory.used // (1024**2)}MB / {memory.total // (1024**2)}MB)", inline=True)
        embed.add_field(name="Disk Storage", value=f"`{disk.percent}%`\n({disk.used // (1024**3)}GB / {disk.total // (1024**3)}GB)", inline=True)
        embed.set_footer(text="Powered by Disknogamerz VPS Infrastructure Engine")
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Monitoring(bot))
