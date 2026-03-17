import discord
from discord.ext import commands
from discord import app_commands
import requests
import time
import json
import os

if not os.path.exists("env.json"):
    with open("env.json", "w") as f:
        json.dump({
            "token": "YOUR_DISCORD_BOT_TOKEN_HERE",
            "user_id": 123456789012345678,
            "channel_id": 123456789012345678
        })
    input("Please set up your env.json file with your bot token, user ID, and channel ID.")
    exit()

with open("env.json", "r", encoding="utf-8") as f:
    env = json.load(f)

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default()) # we dont need everything
youruserid = env["user_id"]
timeoffset = 0 # just in case ur computer's time is screwed and not synced with real utc
ctime = time.time() + timeoffset
rating = "0" # this can be chaned with the /setrating command.
playing = False

async def send_buttons():
    class MainControlPannel(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None) # we dont want the buttons to disappear after 180 seconds, so we set timeout to None
        @discord.ui.button(label="Start RPC", style=discord.ButtonStyle.green)
        async def start_rpc(self, interaction: discord.Interaction, button: discord.ui.Button):
            if not interaction.user.id == youruserid:
                await interaction.response.send_message("You are not authorized to use this command.", ephemeral=True)
                return
            global ctime
            ctime = time.time() + timeoffset
            requests.post("http://127.0.0.1:6767/start_rpc", json={
                "user_id": youruserid,
                "rating": rating,
                "ctime": ctime
            })
            await interaction.response.send_message("Welcome to maimai!", ephemeral=True)
        
        @discord.ui.button(label="Stop RPC", style=discord.ButtonStyle.red)
        async def stop_rpc(self, interaction: discord.Interaction, button: discord.ui.Button):
            global playing
            if not interaction.user.id == youruserid:
                await interaction.response.send_message("You are not authorized to use this command.", ephemeral=True)
                return
            playing = False
            requests.post("http://127.0.0.1:6767/stop_rpc", json={
                "user_id": youruserid
            })
            await interaction.response.send_message("Goodbye! (Don't leave your belongings behind!)", ephemeral=True)
        
        @discord.ui.button(label="In Queue", style=discord.ButtonStyle.blurple)
        async def inqueue(self, interaction: discord.Interaction, button: discord.ui.Button):
            if not interaction.user.id == youruserid:
                await interaction.response.send_message("You are not authorized to use this command.", ephemeral=True)
                return
            global ctime
            ctime = time.time() + timeoffset
            global playing
            playing = False
            requests.post("http://127.0.0.1:6767/inqueue", json={
                "user_id": youruserid,
                "rating": rating,
                "ctime": ctime,
            })
            await interaction.response.send_message("Status set to in queue.", ephemeral=True)

        @discord.ui.button(label="Playing", style=discord.ButtonStyle.gray)
        async def playing(self, interaction: discord.Interaction, button: discord.ui.Button):
            if not interaction.user.id == youruserid:
                await interaction.response.send_message("You are not authorized to use this command.", ephemeral=True)
                return
            global playing
            if not playing:
                global ctime
                ctime = time.time() + timeoffset
                playing = True
            requests.post("http://127.0.0.1:6767/playing", json={
                "user_id": youruserid,
                "rating": rating,
                "ctime": ctime
            })
            await interaction.response.send_message("Status set to playing maimai.", ephemeral=True)

    channel = bot.get_channel(env["channel_id"])
    await channel.send("Maimai RPC Control Panel:", view=MainControlPannel())

@bot.event
async def on_ready():
    await bot.tree.sync()
    await send_buttons()

# if you don't like buttons you can also use slash commands. the setrating function is only a command.
@bot.tree.command(name="start-rpc", description="Welcome to maimai!")
async def start_rpc(interaction: discord.Interaction):
    if not interaction.user.id == youruserid:
        await interaction.response.send_message("You are not authorized to use this command.", ephemeral=True)
        return
    global ctime
    ctime = time.time() + timeoffset
    requests.post("http://127.0.0.1:6767/start_rpc", json={
        "user_id": youruserid,
        "rating": rating,
        "ctime": ctime
    })
    await interaction.response.send_message("Welcome to maimai!", ephemeral=True)

@bot.tree.command(name="inqueue", description="Set your status to in queue.")
async def inqueue(interaction: discord.Interaction):
    if not interaction.user.id == youruserid:
        await interaction.response.send_message("You are not authorized to use this command.", ephemeral=True)
        return
    global ctime
    ctime = time.time() + timeoffset
    global playing
    playing = False
    requests.post("http://127.0.0.1:6767/inqueue", json={
        "user_id": youruserid,
        "rating": rating,
        "ctime": ctime
    })
    await interaction.response.send_message("Status set to in queue.", ephemeral=True)

@bot.tree.command(name="playing", description="Set your status to playing maimai.")
async def playing(interaction: discord.Interaction):
    if not interaction.user.id == youruserid:
        await interaction.response.send_message("You are not authorized to use this command.", ephemeral=True)
        return
    global playing
    if not playing:
        global ctime
        ctime = time.time() + timeoffset
        playing = True
    requests.post("http://127.0.0.1:6767/playing", json={
        "user_id": youruserid,
        "rating": rating,
        "ctime": ctime
    })
    await interaction.response.send_message("Status set to playing maimai.", ephemeral=True)

@bot.tree.command(name="setrating", description="Set your maimai rating.")
@app_commands.describe(newrating="Your new maimai rating.")
async def setrating(interaction: discord.Interaction, newrating: str):
    if not interaction.user.id == youruserid:
        await interaction.response.send_message("You are not authorized to use this command.", ephemeral=True)
        return
    global rating
    rating = newrating
    await interaction.response.send_message(f"Rating updated to {rating}.", ephemeral=True)

@bot.tree.command(name="stop", description="See you! (Don't leave your belongings behind!)")
async def stoppresence(interaction: discord.Interaction):
    if not interaction.user.id == youruserid:
        await interaction.response.send_message("You are not authorized to use this command.", ephemeral=True)
        return
    requests.post("http://127.0.0.1:6767/stop_rpc", json={
        "user_id": youruserid
    })
    await interaction.response.send_message("Goodbye! (Don't leave your belongings behind!)", ephemeral=True)

bot.run(env["token"])