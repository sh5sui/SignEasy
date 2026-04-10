import discord
from discord import app_commands
from discord.ext import commands
import sqlite3

class ContractView(discord.ui.View):
    def __init__(self, teamrole: discord.Role, teamroleicon, manager: discord.Member):
        super().__init__()
        self.teamrole = teamrole
        self.teamroleicon = teamroleicon
        self.manager = manager

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.green)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(color=discord.Color.green())
        embed.set_author(name=interaction.guild.name, icon_url=interaction.guild.icon.url if interaction.guild.icon else None)
        embed.set_thumbnail(url=self.teamroleicon)
        embed.add_field(name="Team Offer", value=f"You have accepted the offer to {self.teamrole.mention}", inline=False)
        embed.add_field(name="", value=f"> • Manager - {self.manager.mention} {self.manager.name}", inline=False)

        await interaction.message.edit(content=None, embed=embed, view=None)

        with sqlite3.connect("SignEasy.db") as conn:
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO signings (guildid, userid, teamid, signed) VALUES (?, ?, ?, ?)",
                (interaction.guild.id, interaction.user.id, self.teamrole.id, 1)
            )

            cursor.execute("SELECT signingchannelid FROM guild_config WHERE guildid = ?", (interaction.guild.id,))
            signingid = cursor.fetchone()
            conn.commit()

        if signingid is None:
            return

        signingchannel = await interaction.guild.fetch_channel(signingid[0])  # index the tuple

        acceptembed = discord.Embed(color=self.teamrole.color)
        acceptembed.set_author(name=interaction.guild.name, icon_url=interaction.guild.icon.url if interaction.guild.icon else None)
        acceptembed.set_thumbnail(url=self.teamroleicon)
        acceptembed.add_field(name="Offer Accepted", value=f"{interaction.user.mention} has accepted an offer from {self.teamrole.mention}", inline=False)
        acceptembed.add_field(name="", value=f"> • Manager - {self.manager.mention} {self.manager.name}", inline=False)

        await signingchannel.send(embed=acceptembed)
        await interaction.user.add_roles(self.teamrole)

    @discord.ui.button(label="Decline", style=discord.ButtonStyle.red)
    async def decline(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(color=discord.Color.red())
        embed.set_author(name=interaction.guild.name, icon_url=interaction.guild.icon.url if interaction.guild.icon else None)
        embed.set_thumbnail(url=self.teamroleicon)
        embed.add_field(name="Team Offer", value=f"You have declined the offer to {self.teamrole.mention}", inline=False)
        embed.add_field(name="", value=f"> • Manager - {self.manager.mention} {self.manager.name}", inline=False)

        await interaction.message.edit(content=None, embed=embed, view=None)


class Contract(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="contract", description="Contract someone to join your team")
    async def Contract(self, interaction: discord.Interaction, player: discord.Member):

        with sqlite3.connect("SignEasy.db") as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT setupcomplete FROM guild_config WHERE guildid = ?", (interaction.guild.id,))
            row = cursor.fetchone()
            if row is None or row[0] == 0:
                await interaction.response.send_message("Setup is not complete, please ask an admin to run /setup", ephemeral=True)
                return

            cursor.execute("SELECT manager, assistant FROM signings WHERE guildid = ? AND userid = ?",
                           (interaction.guild.id, interaction.user.id))
            check = cursor.fetchone()
            if check is None or (check[0] == 0 and check[1] == 0):
                await interaction.response.send_message("You aren't assigned as a manager or assistant and cannot run this command", ephemeral=True)
                return

            cursor.execute("SELECT signed FROM signings WHERE guildid = ? AND userid = ?",
                           (interaction.guild.id, player.id))
            signed = cursor.fetchone()
            if signed and signed[0] == 1:
                await interaction.response.send_message("That player is already signed", ephemeral=True)
                return

            cursor.execute("SELECT teamid FROM signings WHERE guildid = ? AND userid = ?",
                           (interaction.guild.id, interaction.user.id))
            role = cursor.fetchone()
            if role is None:
                await interaction.response.send_message("An error occurred: your team role cannot be found", ephemeral=True)
                return

        teamrole = interaction.guild.get_role(role[0])
        if teamrole is None:
            await interaction.response.send_message("An error occurred: team role no longer exists", ephemeral=True)
            return

        teamroleicon = teamrole.icon.url if teamrole.icon else None

        embed = discord.Embed(color=teamrole.color)
        embed.set_thumbnail(url=teamroleicon)
        embed.set_author(name=interaction.guild.name, icon_url=interaction.guild.icon.url if interaction.guild.icon else None)
        embed.add_field(name="Team Offer", value=f"You have been sent an offer by {self.teamrole.mention}", inline=False)
        embed.add_field(name="", value=f"> • Manager - {interaction.user.mention} {interaction.user.name}", inline=False)

        await player.send(embed=embed, view=ContractView(teamrole, teamroleicon, interaction.user))
        await interaction.response.send_message(f"Offer sent to {player.mention}", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Contract(bot))