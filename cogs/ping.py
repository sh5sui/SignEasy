import discord
from discord import app_commands
from discord.ext import commands
import time

class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Check the bot's latency")
    async def ping(self, interaction: discord.Interaction):

        starttime = round(self.bot.latency * 1000)

        start = time.monotonic()
        await interaction.response.send_message("pong")
        msg = await interaction.original_response()
        end = time.monotonic()

        send = round((end - start) * 1000)

        embed = discord.Embed(color=discord.Color.dark_blue())
        embed.add_field(name="", value=f"{starttime}ms (edit: {send}ms)")

        await msg.edit(content="", embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Ping(bot))