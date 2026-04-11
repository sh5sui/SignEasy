import discord
from discord import app_commands
from discord.ext import commands
import time
import sqlite3

class Sack(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="sack", description="Remove someone as manager or assistant manager of a team")
    async def Sack(self, interaction: discord.Interaction, member: discord.Member):
        
        if not interaction.user.guild_permissions.administrator:
            interaction.response.send_message("Only admins can sack managers", ephemeral=True)
            return

        conn = sqlite3.connect("SignEasy.db")
        cursor = conn.cursor()

        cursor.execute("SELECT setupcomplete FROM guild_config WHERE guildid = ?", (interaction.guild.id,))
        row = cursor.fetchone()

        if row is None or row[0] == 0:
            await interaction.response.send_message("You haven't completed the setup so your unable to use this command, please get an admin to do /setup to unlock all features of the bot")
            conn.close()
            return
        
        cursor.execute("SELECT manager, assistant FROM signings WHERE guildid = ? AND userid = ?",
                       (interaction.guild.id, member.id))
        row = cursor.fetchone()

        if row and (row[0] == 1 or row[1] == 1):
            cursor.execute("UPDATE signings SET teamid = NULL, signed = 0, manager = 0, assistant = 0 WHERE guildid = ? AND userid = ?",
                           (interaction.guild.id, member.id))
            conn.commit()
            conn.close()
            await interaction.response.send_message(f"Successfully removed {member.mention} as manager or assistant of any team")
        else:
            await interaction.response.send_message(f"{member.mention} is not a manager or assistant of any team")
            conn.close()
            return
        
        await interaction.response.send_message(f"{member.mention} has been sacked")

async def setup(bot: commands.Bot):
    await bot.add_cog(Sack(bot))