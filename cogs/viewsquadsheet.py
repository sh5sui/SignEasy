import discord
from discord import app_commands
from discord.ext import commands
import time
import sqlite3

class ViewSS(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="viewss", description="View a teams squadsheet")
    async def ViewSS(self, interaction: discord.Interaction, role: discord.Role):

        conn = sqlite3.connect("SignEasy.db")
        cursor = conn.cursor()

        cursor.execute("SELECT setupcomplete FROM guild_config WHERE guildid = ?", (interaction.guild.id,))
        row = cursor.fetchone()

        if row is None or row[0] == 0:
            await interaction.response.send_message("You haven't completed the setup so your unable to use this command, please get an admin to do /setup to unlock all features of the bot")
            return
        
        embed = discord.Embed(title=f"Squadsheet for {role.name}", color=discord.Color.dark_blue())
        embed.add_field(name="", value="\n".join(member.mention for member in role.members))
        embed.add_field(name="", value="\n".join(str(member.id) for member in role.members))

        await interaction.response.send_message(embed=embed)

        conn.commit()
        conn.close()

async def setup(bot: commands.Bot):
    await bot.add_cog(ViewSS(bot))