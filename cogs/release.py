import discord
from discord import app_commands
from discord.ext import commands
import sqlite3

class Release(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="release", description="Release someone from your team")
    async def Release(self, interaction: discord.Interaction, player: discord.Member):

        with sqlite3.connect("SignEasy.db") as conn:
            cursor = conn.cursor()

            cursor.execute (
                "SELECT setupcomplete FROM guild_config WHERE guildid = ?",
                (interaction.guild.id,)
            ) 
            row = cursor.fetchone ()
            if row is None or row[0] == 0:
                await interaction.response.send_message("Setup is not complete, please ask an admin to run /setup", ephemeral=True)
                conn.close()
                return

            cursor.execute (
                "SELECT manager, assistant FROM signings WHERE guildid = ? AND userid = ?",
                (interaction.guild.id, interaction.user.id)
            )
            check = cursor.fetchone()
            if check is None or (check[0] == 0 and check[1] == 0):
                await interaction.response.send_message("You aren't assigned as a manager or assistant and cannot run this command", ephemeral=True)
                conn.close()
                return
            cursor.execute (
                "SELECT signed FROM signings WHERE guildid = ? AND userid = ?",
                (interaction.guild.id, player.id)
            ) 
            signed = cursor.fetchone ()
            if signed and signed[0] == 0:
                await interaction.response.send_message("That player is not signed", ephemeral=True)
                conn.close()
                return

            cursor.execute (
                "SELECT teamid FROM signings WHERE guildid = ? AND userid = ?",
                (interaction.guild.id, interaction.user.id)
            )
            role = cursor.fetchone()
            if role is None:
                await interaction.response.send_message("An error occurred: your team role cannot be found", ephemeral=True)
                conn.close()
                return

        teamrole = interaction.guild.get_role(role[0])
        if teamrole is None:
            await interaction.response.send_message("An error occurred: team role no longer exists", ephemeral=True)
            return
        
        cursor.execute("SELECT signingchannelid FROM guild_config WHERE guildid = ?", (interaction.guild.id,))
        signingid = cursor.fetchone()
        conn.commit()

        if signingid is None:
            conn.close()
            return

        signingchannel = await interaction.guild.fetch_channel(signingid[0])
        
        teamroleicon = teamrole.icon.url if teamrole.icon else None
        
        embed = discord.Embed(color=discord.Color.red())
        embed.set_thumbnail(url=teamroleicon)
        embed.set_author(name=interaction.guild.name, icon_url=interaction.guild.icon.url if interaction.guild.icon else None)
        embed.add_field(name="Team Release", value=f"{player.mention} has been released by {self.teamrole.mention}", inline=False)
        embed.add_field(name="", value=f"> • Manager - {interaction.user.mention} {interaction.user.name}", inline=False)
        
        await signingchannel.send(embed=embed)
        
        conn.close()
        
async def setup(bot: commands.Bot):
    await bot.add_cog(Release(bot))