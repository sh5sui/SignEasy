import discord
from discord import app_commands
from discord.ext import commands
import time
import requests
import sqlite3

class Sanction(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="sanction", description="Sanction a user")
    async def Sanction(self, interaction: discord.Interaction, user: discord.Member, robloxuser: str, duration: str, bail: str, reason: str = None):
        
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You need administrator to run this command")
            return
        
        cursor.execute (
            "SELECT setupcomplete FROM guild_config WHERE guildid = ?",
            (interaction.guild.id,)
        ) 
        row = cursor.fetchone ()
        if row is None or row[0] == 0:
            await interaction.response.send_message("Setup is not complete, please ask an admin to run /setup", ephemeral=True)
            conn.close()
            return
        
        uri = "https://users.roblox.com/v1/usernames/users"
        data = {
            "usernames": robloxuser,
            "excludeBannedUsers": False
        }
        
        res = requests.post(url=uri, json=data)
        
        userid = res["data"][0]["id"]
        
        embed = discord.Embed(title=f"{interaction.guild.name} Sanction", color=discord.Color.red())
        embed.add_field(name="User", value=user.mention, inline=False)
        embed.add_field(name="UserID", value=user.id, inline=False)
        embed.add_field(name="Roblox", value=f"{robloxuser} \n https://roblox.com/users{userid}/profile", inline=False)
        embed.add_field(name="Length", value=duration, inline=False)
        embed.add_field(name="Bail", value=bail, inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.timestamp = discord.utils.utcnow()
        
        conn = sqlite3.connect("SignEasy.db")
        cursor = conn.cursor()
        
        cursor.execute (
            "SELECT sanctionchannel FROM guild_config WHERE guildid = ?",
            (interaction.guild.id)
        ) 
        row = cursor.fetchone ()
        
        sanctionchannel = interaction.guild.get_channel(row[0])
        
        aaaa = await sanctionchannel.send(embed=embed)
        
        await interaction.response.send_message(f"{user.mention} has been sanctioned {aaaa.jump_url}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Sanction(bot))