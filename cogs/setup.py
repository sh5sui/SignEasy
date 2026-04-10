import discord
from discord import app_commands
from discord.ext import commands
import time
import sqlite3
import asyncio

conn = sqlite3.connect("SignEasy.db")
cursor = conn.cursor()

class Continue(discord.ui.View):
    def __init__(self, authorid: int):
        super().__init__()
        self.authorid = authorid
    @discord.ui.button(label="Continue", style=discord.ButtonStyle.green)
    async def callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        if interaction.user.id != self.authorid:
            await interaction.response.send_message("Only the author can continue", ephemeral=True)
            return
        
        await interaction.message.delete()
        
        embed = discord.Embed(title="EasySign setup", color=discord.Color.dark_blue())
        embed.add_field(name="Manager Role", value="Mention your manager role")

        await interaction.response.send_message(embed=embed)

        def check(message: discord.Message):
            return (
                message.author.id == self.authorid and
                message.channel == interaction.channel
            )
        
        try:
            message = await interaction.client.wait_for("message", timeout=60.0, check=check)
        except:
            await interaction.followup.send("Setup command timed out")
            return
        
        if message.role_mentions:
            role = message.role_mentions[0]
            await interaction.followup.send(f"Set manager role to {role.mention}")
        else:
            await interaction.followup.send("Setup command failed as you didn't mention a valid role, please retry")
            return

        await asyncio.sleep(3)
        
        await message.delete()

        todel = []

        async for message in interaction.channel.history(limit=100):
            if message.author == interaction.client.user:
                todel.append(message)

        if todel:
            await interaction.channel.delete_messages(todel)

        embed = discord.Embed(title="EasySign setup", color=discord.Color.dark_blue())
        embed.add_field(name="Assistant Manager Role", value="Mention your assistant manager role")

        await interaction.followup.send(embed=embed)

        try:
            assistantmessage = await interaction.client.wait_for("message", timeout=60.0, check=check)
        except:
            await interaction.followup.send("Setup command timed out")
            return
        
        if assistantmessage.role_mentions:
            assistantrole = assistantmessage.role_mentions[0]
            await interaction.followup.send(f"Set assistant manager role to {assistantrole.mention}")
        else:
            await interaction.followup.send("Setup command failed as you didn't mention a valid role, please retry")
            return
        
        await asyncio.sleep(3)

        await assistantmessage.delete()

        dele = []

        async for message in interaction.channel.history(limit=100):
            if message.author == interaction.client.user:
                dele.append(message)

        if dele:
            await interaction.channel.delete_messages(dele)

        embedchan = discord.Embed(title="EasySign setup", color=discord.Color.dark_blue())
        embedchan.add_field(name="Signing channel", value="Mention your signing channel")

        embedrel = discord.Embed(title="EasySign setup", color=discord.Color.dark_blue())
        embedrel.add_field(name="Release channel", value="Mention your Release channel")

        await interaction.followup.send(embed=embedchan)

        try:
            chan = await interaction.client.wait_for("message", timeout=60.0, check=check)
        except:
            await interaction.followup.send("Setup command timed out")
            return
        
        if chan.channel_mentions:
            signchannel = chan.channel_mentions[0]
            await interaction.followup.send(f"Set signing channel to {signchannel.mention}")
        else:
            await interaction.followup.send("Setup command failed as you didn't mention a valid channel, please retry")
            return
        
        await asyncio.sleep(3)

        await chan.delete()

        delet = []

        async for message in interaction.channel.history(limit=100):
            if message.author == interaction.client.user:
                delet.append(message)

        if delet:
            await interaction.channel.delete_messages(delet)

        await interaction.followup.send(embed=embedrel)

        try:
            rel = await interaction.client.wait_for("message", timeout=60.0, check=check)
        except:
            await interaction.followup.send("Setup command timed out")
            return
        
        if rel.channel_mentions:
            releasechannel = rel.channel_mentions[0]
            await interaction.followup.send(f"Set release channel to {releasechannel.mention}")
        else:
            await interaction.followup.send("Setup command failed as you didn't mention a valid channel, please retry")
            return
        
        await asyncio.sleep(3)

        await rel.delete()

        delete = []

        async for message in interaction.channel.history(limit=100):
            if message.author == interaction.client.user:
                delete.append(message)

        if delete:
            await interaction.channel.delete_messages(delete)

        cursor.execute("""
            INSERT OR REPLACE INTO guild_config
            (guildid, signingchannelid, releaseschannelid, managerroleid, assistantroleid, setupcomplete)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                interaction.guild.id,
                signchannel.id,
                releasechannel.id,
                role.id,
                assistantrole.id,
                1
            )
        )

        conn.commit()
        conn.close()
        
class Setup(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="setup", description="Setup the bot for signing")
    async def setup(self, interaction: discord.Interaction):

        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You cannot run this command as your not an administrator in this server", ephemeral=True)
            return
        
        embed = discord.Embed(title="EasySign setup", color=discord.Color.dark_blue())
        embed.add_field(name="Welcome", value="Welcome to the EasySign setup for your league")
        embed.add_field(name="Information", value="Before you start, please ensure you have a signing channel, manager role and assistant manager role. Also it is optional to have a releases channel but it is not required as you can just use your signing channel again.", inline=False)
        embed.set_footer(text="Press the button to continue")

        await interaction.response.send_message(embed=embed, view=Continue(interaction.user.id))

async def setup(bot: commands.Bot):
    await bot.add_cog(Setup(bot))