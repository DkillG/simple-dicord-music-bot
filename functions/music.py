import os
import pytube
import discord
import asyncio
from datetime import timedelta
from functions.embeds import SuperEmbeds

class MusicCore():
    player: discord.VoiceClient = None
    music_playing: dict[pytube.YouTube, str]
    channel_command: discord.TextChannel = None
    music_playlist: list[dict[pytube.YouTube, str]] = []

    music_configuration = {
        'repeat': False,
        'paused': False,
    }

    def get_music_id(self, name: str) -> int:
        return pytube.Search(name).results[0].video_id

    def get_music_metadata(self, id: int) -> pytube.YouTube:
        return pytube.YouTube(f'https://youtube.com/watch?v={id}')

    def get_musicfiles_downloaded(self):
        files = [archivo for archivo in os.listdir(f"{os.getcwd()}\\music") if os.path.isfile(os.path.join(f"{os.getcwd()}\\music", archivo))]
        return files

    def get_music_file(self, id: int):
        path = os.path.abspath(f'{os.getcwd()}\\music\\{id}.mp3')
        exist = os.path.isfile(path)

        if exist:
            return path
        else:
            files = self.get_musicfiles_downloaded()

            if len(files) >= int(os.getenv("MUSIC_LIMIT")):
                sorted_files = sorted(files, key=lambda archivo: os.path.getmtime(os.path.join(f"{os.getcwd()}\\music", archivo)))

                for file in sorted_files[:6]:
                    os.remove(os.path.join(f"{os.getcwd()}\\music", file))

            return self.donwload_music_file(id)

    def donwload_music_file(self, id: int) -> str:
        return self.get_music_metadata(id).streams.get_audio_only().download(f'{os.getcwd()}\\music', id + '.mp3')

    async def add_music_playlist(self, music: pytube.YouTube, file: str, interaction: discord.Interaction):
        
        if interaction:
            self.channel_command = interaction.channel
        
        self.music_playing = { 'music': music, 'file': file, 'by': interaction.user }
        self.music_playlist.append({ 'music': music, 'file': file, 'by': interaction.user })

        if len(self.music_playlist) < 2:
            await self.play_music()
        else:
            embed = SuperEmbeds().added_music(music.title, music.author, str(timedelta(seconds=music.length)), self.music_playlist[0]['by'], len(self.music_playlist), music.thumbnail_url, self.music_playlist)
            await self.channel_command.send(embed=embed)

    async def connect_bot(self, client: discord.Client, interaction: discord.Interaction):
        if client.voice_clients: return
        self.player = await interaction.user.voice.channel.connect()

    async def play_get_music(self, name: str, interaction: discord.Interaction):
        await interaction.response.send_message(f":mag: Searching for `{name}` in YouTube ")

        id = self.get_music_id(name)
        await self.add_music_playlist(self.get_music_metadata(id), self.get_music_file(id), interaction)

    async def play_music(self):
        if not self.player: return

        music: pytube.YouTube = self.music_playlist[0]['music']
        embed = SuperEmbeds().playing_music(music.title, music.author, str(timedelta(seconds=music.length)), self.music_playlist[0]['by'], music.watch_url, music.thumbnail_url, self.music_playlist)

        await self.channel_command.send(embed=embed)
        self.player.play(discord.FFmpegPCMAudio(executable="ffmpeg/bin/ffmpeg.exe", source=self.music_playlist[0]['file'], options={'options': '-vn'}), after=lambda x: (await self.player_error(x) for _ in '_').__anext__())

        while self.player and self.player.is_playing() or self.music_configuration['paused']:
            await asyncio.sleep(1)

        await self.music_controller()
    
    async def set_loop(self, interaction: discord.Interaction):
        self.music_configuration['repeat'] = not self.music_configuration['repeat']

        if self.music_configuration['repeat']:
            await interaction.response.send_message(f"**:repeat: Bucle activado**")
        else:
            await interaction.response.send_message(f"**:repeat: Bucle desactivado**")

    def pause_music(self):
        if self.music_configuration['paused']: return

        self.music_configuration['paused'] = True
        self.player.pause()

    def resume_music(self):
        if not self.music_configuration['paused']: return

        self.music_configuration['paused'] = False
        self.player.resume()

    async def stop_music(self):
        self.player.stop()

        await self.player.disconnect()
        self.channel_command = None
        self.music_playing = None
        self.music_playlist = []
        self.player = None

    async def next_music(self, interaction: discord.Interaction):
        if not self.player: return

        if len(self.music_playlist) > 1:
            self.player.stop()
            
            await interaction.response.send_message("**:track_next: Musica salteada**")
        else:
            await interaction.response.send_message("**:no_entry: No hay mas canciones para reproducir**")


    async def player_error(self, error: Exception | None):
        print(f"[Error]: {error}")
        await self.stop_music()
    
    async def music_controller(self):
        if not self.player: return

        if self.music_configuration['repeat']:
            return await self.play_music()

        if len(self.music_playlist) > 1:
            
            self.music_playlist.pop(0)
            await self.play_music()

        else:
            await self.stop_music()