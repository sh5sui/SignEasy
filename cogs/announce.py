import discord
from discord import app_commands
from discord.ext import commands
import time
import sqlite3

class Announce(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="announce", description="Make an announcement with the bot")
    async def Announce(self, interaction: discord.Interaction, msgchannel: discord.TextChannel, message: str, timestamp: bool, title: str = "", thumburl: str = ""):
        
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You need administrator permissions to run this command", ephemeral=True)
            return

        conn = sqlite3.connect("SignEasy.db")
        cursor = conn.cursor()

        cursor.execute("SELECT setupcomplete FROM guild_config WHERE guildid = ?", (interaction.guild.id,))
        row = cursor.fetchone()

        if row is None or row[0] == 0:
            await interaction.response.send_message("You haven't completed the setup so your unable to use this command, please get an admin to do /setup to unlock all features of the bot")
            return
        
        embed = discord.Embed(title=title, color=discord.Color.blue())
        embed.set_thumbnail(url=thumburl)
        embed.add_field(name="", value=message)

        await msgchannel.send(embed=embed)

        conn.commit()
        conn.close()

async def setup(bot: commands.Bot):
    await bot.add_cog(Announce(bot))