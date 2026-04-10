import discord
from discord.ext import commands
import os
import sys
from dotenv import load_dotenv
import sqlite3

load_dotenv()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

bot = commands.Bot(command_prefix=";", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"logged in as {bot.user.name}")
    conn = sqlite3.connect("SignEasy.db")
    cursor = conn.cursor()

    cursor.execute (
        """
        CREATE TABLE IF NOT EXISTS guild_config (
            guildid INTEGER PRIMARY KEY,
            signingchannelid INTEGER,
            releaseschannelid INTEGER,
            managerroleid INTEGER,
            assistantroleid INTEGER,
            resultschannel INTEGER,
            sanctionchannel INTEGER,
            setupcomplete BOOLEAN DEFAULT 0
        )
        """
    )
    
    cursor.execute (
        """
        CREATE TABLE IF NOT EXISTS signings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guildid INTEGER NOT NULL,
            userid INTEGER,
            teamid INTEGER,
            signed BOOLEAN DEFAULT 0,
            manager BOOLEAN DEFAULT 0,
            assistant BOOLEAN DEFAULT 0,
            teamcap INTEGER DEFAULT 16,
            FOREIGN KEY (guildid) REFERENCES guild_config(guildid)
        )
        """
    )
    
    conn.commit()
    conn.close()

async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and not filename.startswith("_"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

@bot.event
async def setup_hook():
    await load()
    await bot.tree.sync()
    
@bot.event
async def on_message_delete(message):
    
    if message.author.bot:
        return
    
    if message.raw_mentions:
        
        gping = bot.get_emoji(1492216605365502205)
        
        musers = ", ".join(user.mention for user in message.mentions)
        
        embed = discord.Embed(title=f"{gping} Ghost ping detected", color=discord.Color.dark_blue())
        embed.timestamp = discord.utils.utcnow()
        embed.add_field(name="Author", value=message.author.mention, inline=False)
        embed.add_field(name="Mentions", value=musers, inline=False)
        embed.add_field(name="Content", value=message.content or "Unable to fetch content", inline=False)
        
        await message.channel.send(embed=embed)

token = os.getenv("token")
bot.run(token)