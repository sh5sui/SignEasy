import discord
from discord import app_commands
from discord.ext import commands
import time
import sqlite3

class Results(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
class MatchResultModal(discord.ui.Modal, title="Match Results"):
    def __init__(self, team1: str, team2: str, team1score: str, team2score: str):
        super().__init__()
        self.team1 = team1
        self.team2 = team2
        self.team1score = team1score
        self.team2score = team2score

    team1_scorers = discord.ui.TextInput(
        label="Team 1 Scorers",
        placeholder="PlayerA, PlayerB, PlayerC",
        required=False
    )
    team1_assisters = discord.ui.TextInput(
        label="Team 1 Assisters",
        placeholder="PlayerD, PlayerE",
        required=False
    )
    team2_scorers = discord.ui.TextInput(
        label="Team 2 Scorers",
        placeholder="PlayerF, PlayerG",
        required=False
    )
    team2_assisters = discord.ui.TextInput(
        label="Team 2 Assisters",
        placeholder="PlayerH",
        required=False
    )
    
    async def onsubmit(self, interaction: discord.Interaction):
        team1_scorers = [s.strip() for s in self.team1_scorers.value.split(",") if s.strip()]
        team1_assisters = [s.strip() for s in self.team1_assisters.value.split(",") if s.strip()]
        team2_scorers = [s.strip() for s in self.team2_scorers.value.split(",") if s.strip()]
        team2_assisters = [s.strip() for s in self.team2_assisters.value.split(",") if s.strip()]
        
        embed = discord.Embed(title=f"Match results for")

    @app_commands.command(name="results", description="Send the results of a match in the results channel")
    async def Results(self, interaction: discord.Interaction, team1: str, team2: str, team1score: str, team2score: str, ):
        
        if not interaction.user.guild_permissions.administrator:
            interaction.response.send_message("Only admins can send results", ephemeral=True)
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

async def setup(bot: commands.Bot):
    await bot.add_cog(Results(bot))