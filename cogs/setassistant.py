import discord
from discord import app_commands
from discord.ext import commands
import time
import sqlite3

class SetAssistant(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="setassistant", description="Assign someone as the assistant manager of a team")
    async def SetAssistant(self, interaction: discord.Interaction, member: discord.Member, team: discord.Role):

        conn = sqlite3.connect("SignEasy.db")
        cursor = conn.cursor()

        cursor.execute("SELECT setupcomplete FROM guild_config WHERE guildid = ?", (interaction.guild.id,))
        row = cursor.fetchone()

        if row is None or row[0] == 0:
            await interaction.response.send_message("You haven't completed the setup so your unable to use this command, please get an admin to do /setup to unlock all features of the bot")
            conn.close()
            return
        
        cursor.execute("SELECT id FROM signings WHERE guildid = ? AND userid = ? AND teamid = ?",
                      (interaction.guild.id, member.id, team.id))
        if cursor.fetchone():
            await interaction.response.send_message(f"{member.mention} is already assigned to that team")
            conn.close()
            return
        
        cursor.execute("SELECT manager, assistant FROM signings WHERE guildid = ? AND userid = ?",
                       (interaction.guild.id, member.id))
        row = cursor.fetchone()

        if row and (row[0] == 1 or row[1] == 1):
            await interaction.response.send_message(f"{member.mention} is already assigned as the manager or assistant manager of another team")
            return
        
        cursor.execute(
            """
            INSERT INTO signings (guildid, userid, teamid, assistant, signed)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                interaction.guild.id,
                member.id,
                team.id,
                1,
                1
            )
        )
        conn.commit()
        conn.close()

        await interaction.response.send_message(f"{member.mention} has been assigned as the assistant manager of {team.mention}")

async def setup(bot: commands.Bot):
    await bot.add_cog(SetAssistant(bot))