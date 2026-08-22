import os
import subprocess
import discord
from discord.ext import commands
import rsa

class VPSControlView(discord.ui.View):
    def __init__(self, author_id, ram, cpu):
        super().__init__(timeout=180)
        self.author_id = author_id
        self.ram = ram
        self.cpu = cpu

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author_id:
            await interaction.response.send_message("❌ This deployment panel does not belong to you.", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="🚀 Deploy Ubuntu Pro", style=discord.ButtonStyle.green, custom_id="dep_ubuntu")
    async def deploy_ubuntu(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.execute_vps_pipeline(interaction, "ubuntu:latest")

    @discord.ui.button(label="⚡ Deploy Debian", style=discord.ButtonStyle.blurple, custom_id="dep_debian")
    async def deploy_debian(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.execute_vps_pipeline(interaction, "debian:latest")

    async def execute_vps_pipeline(self, interaction: discord.Interaction, base_image: str):
        await interaction.response.defer(thinking=True)

        container_name = f"vps-instance-{interaction.user.id}"
        
        try:
            # 1. Clean up any existing container for this user
            subprocess.run(["docker", "rm", "-f", container_name], capture_output=True)

            # 2. Generate RSA Keypair (2048 bit)
            pub_key, priv_key = rsa.newkeys(2048)
            pub_pem = pub_key.save_pkcs1('PEM').decode('utf-8')
            priv_pem = priv_key.save_pkcs1('PEM').decode('utf-8')
            
            # Convert RSA public key to OpenSSH format string for authorized_keys injection
            # (Or store pem directly depending on login shell requirements)
            ssh_pub_line = f"ssh-rsa {pub_key.n} disknogamerz-vps-key\n"

            # 3. Spin up the isolated container instance with resource limits
            run_cmd = [
                "docker", "run", "-d",
                "--name", container_name,
                f"--memory={self.ram}g",
                f"--cpus={float(self.cpu)}",
                base_image,
                "sh", "-c", "apt-get update && apt-get install -y openssh-server && mkdir -p /root/.ssh && sleep infinity"
            ]
            res = subprocess.run(run_cmd, capture_output=True, text=True)
            
            if res.returncode != 0:
                raise Exception(f"Docker spawn failed: {res.stderr.strip()}")

            # 4. Inject the Public Key into /root/.ssh/authorized_keys inside the container
            inject_cmd = [
                "docker", "exec", container_name,
                "sh", "-c", f"echo '{ssh_pub_line}' >> /root/.ssh/authorized_keys && chmod 600 /root/.ssh/authorized_keys"
            ]
            subprocess.run(inject_cmd, capture_output=True)

            # Retrieve container IP address dynamically
            ip_cmd = ["docker", "inspect", "-f", "{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}", container_name]
            ip_res = subprocess.run(ip_cmd, capture_output=True, text=True)
            container_ip = ip_res.stdout.strip() or "Internal Docker Bridge IP"

            # 5. Public channel success response
            embed = discord.Embed(title="🛡️ VPS Node Successfully Provisioned", color=discord.Color.green())
            embed.add_field(name="Target Container", value=f"`{container_name}`", inline=True)
            embed.add_field(name="Hardware Specs", value=f"`{self.ram}GB RAM` | `{self.cpu} vCPU`", inline=True)
            embed.description = "🔒 Your private SSH key and connection parameters have been sent securely to your DMs."
            embed.set_footer(text="Disknogamerz Automated Virtualization Engine")

            await interaction.edit_original_response(embed=embed, view=None)

            # 6. Deliver Private Key File via Direct Message (DM)
            key_filename = f"{container_name}_id_rsa"
            with open(key_filename, "w") as f:
                f.write(priv_pem)

            dm_embed = discord.Embed(title="🔑 Your VPS Access & Private Key", color=discord.Color.gold())
            dm_embed.description = (
                f"Your isolated virtual server instance is online!\n\n"
                f"• **Image:** `{base_image}`\n"
                f"• **Container IP:** `{container_ip}`\n"
                f"• **Username:** `root`\n\n"
                f"**Connection Command:**\n`ssh -i {key_filename} root@{container_ip}`"
            )
            
            file_to_send = discord.File(key_filename, filename="id_rsa")
            await interaction.user.send(embed=dm_embed, file=file_to_send)

            # Clean up temporary local key file from host disk immediately after sending
            if os.path.exists(key_filename):
                os.remove(key_filename)

        except Exception as e:
            err_embed = discord.Embed(title="❌ Provisioning Failed", color=discord.Color.red())
            err_embed.description = f"An error occurred while building your container instance:\n```prolog\n{str(e)}\n```"
            await interaction.edit_original_response(embed=err_embed, view=None)

class ServerManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="deploy", help="Deploy custom VPS container instances with button layout.")
    async def deploy(self, ctx, ram: int = 2, cpu: int = 1):
        embed = discord.Embed(title="⚙️ Disknogamerz VPS Provisioner", color=discord.Color.blue())
        embed.description = (
            f"Configuring resource allocation pool:\n"
            f"• **RAM Memory:** `{ram} GB`\n"
            f"• **vCPU Cores:** `{cpu}`\n\n"
            f"Select your desired operating system image below to build your container:"
        )
        embed.set_footer(text=f"Requested by {ctx.author.name}")

        view = VPSControlView(ctx.author.id, ram, cpu)
        await ctx.send(embed=embed, view=view)

    @commands.command(name="vpsaction", help="Manage hosting instance states.")
    async def vpsaction(self, ctx, action: str = None, target_user_id: int = None):
        if not action:
            await ctx.send("⚠️ Usage: `.vpsaction restart` or `.vpsaction status`")
            return
        
        target_container = f"vps-instance-{target_user_id or ctx.author.id}"
        
        if action.lower() == "restart":
            res = subprocess.run(["docker", "restart", target_container], capture_output=True)
            if res.returncode == 0:
                await ctx.send(f"🔄 Container `{target_container}` was restarted successfully.")
            else:
                await ctx.send(f"❌ Could not find an active container named `{target_container}`.")
        elif action.lower() == "status":
            res = subprocess.run(["docker", "inspect", "-f", "{{.State.Status}}", target_container], capture_output=True, text=True)
            status = res.stdout.strip()
            if status:
                await ctx.send(f"📊 Container `{target_container}` status: **{status.upper()}**")
            else:
                await ctx.send(f"❌ No active instance found for `{target_container}`.")
        else:
            await ctx.send(f"⚠️ Unknown action `{action}`. Available actions: `restart`, `status`.")

async def setup(bot):
    await bot.add_cog(ServerManagement(bot))
