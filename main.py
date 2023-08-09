#Rax Bot developed by: DkillGames#4592
#V.1.1.2

import os
import re
import random
import discord
import requests
from dotenv import load_dotenv
from discord import app_commands
from functions.music import MusicCore
from discord.ext import tasks, commands
from functions.embeds import SuperEmbeds
from commands.music import MusicCommands
from functions.robloxAPI import robloxAPI

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
last_video_uploaded = None
music_commands = MusicCommands(client, music_core)

async def get_last_video():
    html = requests.get(os.getenv('YOUTUBE_CHANNEL_ID') + "/videos").text
    return "https://www.youtube.com/watch?v=" + re.search('(?<="videoId":").*?(?=")', html).group()

@client.event
async def on_ready():
    
    global last_video_uploaded
    default_channel = client.get_channel(int(os.getenv('DEFAULT_CHANNEL_ID')))

    await default_channel.send(embed=SuperEmbeds().bot_ready())
    print('--------------------------------------------------')
    print(f'Bot logueado como: {client.user} (ID: {client.user.id})')
    print('--------------------------------------------------')

    last_video_uploaded = await get_last_video()

@tasks.loop(minutes=5)
async def status_task():
    """
    Setup the game status task of the bot.
    """
    statuses = ["Suscrebete a Rax!", "Jugando con Rax!", "256k subs!"]
    await client.change_presence(activity=discord.Game(random.choice(statuses)))

@tasks.loop(minutes=1)
async def new_video():
    """
    Check if Rax upload a new video
    """
    global last_video_uploaded
    tmp_video = await get_last_video()
    if tmp_video != last_video_uploaded:
        await client.get_channel(int(os.getenv("NEW_VIDEO_CHANNEL_ID"))).send(f'@everyone **Rax ha subido un nuevo video!**\n{last_video_uploaded}')

#======> General <======

@client.command()
async def ad(command: commands.Context, *args):
    if not command.author.get_role(int(os.getenv("STAFF_ROLE"))):
        return await command.reply('***:no_entry: No perteneces al staff para usar este comando***', ephemeral=True)

    await client.get_channel(int(os.getenv("ANNOUNCE_CHANNEL_ID"))).send(embed=SuperEmbeds().announce(" ".join(str(arg) for arg in args)))

@client.command()
async def game(command: commands.Context, *args):

    target_id: int = 0

    if re.fullmatch(r'https?://www\.roblox\.com/games/\d+/[A-Za-z0-9-]+', args[0]):
        target_id = re.findall(r'/games/(\d+)/', args[0])[0]

    elif re.fullmatch(r'\d+', args[0]):
        target_id = args[0]

    elif re.fullmatch(r'^[A-Za-z0-9\s\W]+$', " ".join(args)):
        
        game = robloxAPI().get_game_info(name="+".join(args))

        embed = SuperEmbeds().refer_game(game)
        return await command.reply(embed=embed)

    game = robloxAPI().get_game_info(id=int(target_id))
    embed = SuperEmbeds().refer_game(game)
    return await command.reply(embed=embed)
    


@client.tree.command()
async def help(interaction: discord.Interaction):
    await interaction.response.send_message(embed=SuperEmbeds().bot_commands())

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