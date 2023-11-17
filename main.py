#Rax Bot developed by: DkillGames#4592
#V.1.1.2

import os
import discord
from dotenv import load_dotenv
from discord import app_commands
from functions.music import MusicCore
from discord.ext import commands
from commands.music import MusicCommands

load_dotenv()

#======> General <======

class Bot(commands.Bot):
    def __init__(self, *, command_prefix: str, intents: discord.Intents):
        super().__init__(command_prefix=command_prefix, intents=intents)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=discord.Object(id=os.getenv("GROUP_ID")))
        await self.tree.sync(guild=discord.Object(id=os.getenv("GROUP_ID")))

intents = discord.Intents.default()

intents.members = True
intents.presences = True
intents.message_content = True
client = Bot(command_prefix="!", intents=intents)

music_core = MusicCore()
music_commands = MusicCommands(client, music_core)


@client.event
async def on_ready():

    print('--------------------------------------------------')
    print(f'Bot logueado como: {client.user} (ID: {client.user.id})')
    print('--------------------------------------------------')

#======> Music <======
@client.tree.command()
@app_commands.rename(song_name='text')
@app_commands.describe(song_name='Nombre de la cancion que quieres escuchar')
async def play(interaction: discord.Interaction, song_name: str):
    await music_commands.play(interaction, song_name)

@client.tree.command()
async def stop(interaction: discord.Interaction):
    await music_commands.stop(interaction)

@client.tree.command()
async def resume(interaction: discord.Interaction):
    await music_commands.resume(interaction)

@client.tree.command()
async def pause(interaction: discord.Interaction):
    await music_commands.pause(interaction)

@client.tree.command()
async def next(interaction: discord.Interaction):
    await music_commands.next(interaction)

@client.tree.command()
async def loop(interaction: discord.Interaction):
    await music_commands.loop(interaction)


#======> Bot conection <======
client.run(os.getenv('TOKEN'))