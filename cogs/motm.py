import discord
from discord import app_commands
from discord.ext import commands
import time
import sqlite3

class Motm(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="motm", description="Send who was the man of the match in the results channel")
    async def MOTM(self, interaction: discord.Interaction, team1: str, team2: str, motm: discord.Member, firstmention: discord.Member = None, secondmention: discord.Member = None, thirdmention: discord.Member = None):
        
        if not interaction.user.guild_permissions.administrator:
            interaction.response.send_message("Only admins can send MOTM notices", ephemeral=True)
            return
        
        conn = sqlite3.connect("SignEasy.db")
        cursor = conn.cursor()
        
        cursor.execute (
            "SELECT setupcomplete FROM guild_config WHERE guildid = ?",
            (interaction.guild.id,)
        ) 
        row = cursor.fetchone ()
        if row is None or row[0] == 0:
            await interaction.response.send_message("Setup is not complete, please ask an admin to run /setup", ephemeral=True)
            return
        
        cursor.execute (
            "SELECT resultschannel FROM guild_config WHERE guildid = ?",
            (interaction.guild.id)
        )
        row = cursor.fetchone()
        
        resultschannel = interaction.guild.get_channel(row[0])
        
        embed = discord.Embed(title=f"{team1} VS {team2} MOTM", color=discord.Color.dark_blue())
        embed.add_field(name="Man Of The Match", value=motm, inline=False)
        if firstmention is not None:
            embed.add_field(name="1st Mention", value=firstmention, inline=False)
        else:
            pass
        if firstmention is not None:
            embed.add_field(name="2nd Mention", value=secondmention, inline=False)
        else:
            pass
        if firstmention is not None:
            embed.add_field(name="3rd Mention", value=thirdmention, inline=False)
        else:
            pass
        
        await resultschannel.send(embed=embed)
        
        conn.close()

async def setup(bot: commands.Bot):
    await bot.add_cog(Motm(bot))