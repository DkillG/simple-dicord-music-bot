import discord
from functions.music import MusicCore

class MusicCommands():
    client: discord.Client = None
    music_controller: MusicCore = None

    def __init__(self, client: discord.Client, music_controller: MusicCore):
        self.client = client
        self.music_controller = music_controller

    async def no_bot_message(self, interaction: discord.Interaction):
        if not self.client.voice_clients:
            await interaction.response.send_message('***:no_entry: No me encuentro reproduciendo musica ahora***', ephemeral=True)
            return True

        return False
        
    async def play(self, interaction: discord.Interaction, song_name: str):
        if interaction.user.voice is None:
            return await interaction.response.send_message('***:no_entry: Por favor ingresa primero a un canal de voz***', ephemeral=True)

        await self.music_controller.connect_bot(self.client, interaction)
        await self.music_controller.play_get_music(song_name, interaction)

    async def stop(self, interaction: discord.Interaction):
        if await self.no_bot_message(interaction): return

        await self.music_controller.stop_music()
        await interaction.response.send_message('***Gracias por escuchar musica conmigo ;)***')

    async def resume(self, interaction: discord.Interaction):
        if await self.no_bot_message(interaction): return

        self.music_controller.resume_music()
        await interaction.response.send_message('***:arrow_forward: La musica esta continuando***')

    async def pause(self, interaction: discord.Interaction):
        if await self.no_bot_message(interaction): return

        self.music_controller.pause_music()
        await interaction.response.send_message('***:pause_button: La musica fue detenida***')

    async def next(self, interaction: discord.Interaction):
        if await self.no_bot_message(interaction): return

        await self.music_controller.next_music(interaction)

    async def loop(self, interaction: discord.Interaction):
        if await self.no_bot_message(interaction): return

        await self.music_controller.set_loop(interaction)