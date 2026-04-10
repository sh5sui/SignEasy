import discord
from discord import app_commands
from discord.ext import commands
import time

class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="help", description="Show all of the bots command")
    async def Help(self, interaction: discord.Interaction):
        
        embed = discord.Embed(title="SignEasy help", color=discord.Color.dark_blue())
        embed.set_author(name=self.bot.user.name)
        embed.add_field(name="/help", value="Display this embed", inline=False)
        embed.add_field(name="/setup", value="Setup the bot for this server", inline=False)
        embed.add_field(name="/setmanager", value="Assign someone as the manager for a team", inline=False)
        embed.add_field(name="/setassistant", value="Assign someone as the assistant manager for the team", inline=False)
        embed.add_field(name="/contract", value="Send a contract to a player", inline=False)
        embed.add_field(name="/release", value="Release a player from your team", inline=False)
        embed.add_field(name="/sack", value="Remove a manager or assistant manager from his position", inline=False)
        embed.add_field(name="/viewsquadsheet", value="View the squadsheet of a team", inline=False)
        embed.add_field(name="/motm", value="Send the man of the match and mentions in the results channel", inline=False)
        embed.add_field(name="/ping", value="Display the bots latency", inline=False)
        embed.timestamp = discord.utils.utcnow()
        
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))