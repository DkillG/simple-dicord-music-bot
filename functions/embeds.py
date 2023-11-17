import os
import discord

class SuperEmbeds:

    def get_default_color(self):
        return discord.Colour.from_str(os.getenv("DEFAULT_COLOR"))

    def create_embed(self, name: str, author: str, duration: str, by: str, url: str | None, index: int, image: str, playlist: list) -> discord.Embed:
        embed = discord.Embed(title=name, colour=self.get_default_color())

        if url: embed.url = url
        embed.set_thumbnail(url=image)
        embed.add_field(name='Autor', value=author)
        embed.add_field(name='Pedida por', value=by)
        embed.add_field(name=' ', value=' ', inline=False)
        embed.add_field(name='Duracion', value=duration)
        embed.add_field(name='Posicion', value=index)
        embed.add_field(name=' ', value=' ', inline=False)
        
        for i, song in enumerate(playlist):
            embed.add_field(name=f"#{i + 1} - {song['music'].title} {song['music'].author}", value='', inline=False)

        return embed
    
    def playing_music(self, name: str, author: str, duration: str, by: str, url: str, image: str, playlist: list) -> discord.Embed:
        return self.create_embed(name, author, duration, by, url, 1, image, playlist)
    
    def added_music(self, name: str, author: str, duration: str, by: str, index: int, image: str, playlist: list) -> discord.Embed:
        return self.create_embed(f"Se agrego {name} a la lista", author, duration, by, None, index, image, playlist)
    
    def bot_ready(self):
        return discord.Embed(title=f"Hola! soy {os.getenv('BOT_NAME')} (^.^)/", colour=self.get_default_color(),
            description="""Cuento con una amplia de comandos y estoy aqui para ayudarlos en todo lo que necesiten ^^\n
            Estare dando noticias muy importante sobre el mundo de Roblox y leaks cada dia!\n
            Quieres escuchar musica? Unete a un canal y comienza a reproducir canciones con el comando `/play`\n
            Puedes ver la lista completa de comandos utilizando `/help`""")

    def announce(self, description: str):
        return discord.Embed(title="Anuncio importante!", description=description, colour=self.get_default_color())
    
    def new_video(self):
        embed = discord.Embed(title=f"Rax ha subido un nuevo video!", url='https://www.youtube.com/embed/TxIAGoqmW3s', colour=self.get_default_color())
        return embed

    def bot_commands(self):
        return discord.Embed(title=f"Comandos de {os.getenv('BOT_NAME')}", colour=self.get_default_color(),
            description="""**Comandos generales**\n
            - __/help__: Te permite ver todos los comandos del bot\n\n
            **Comandos de Musica**\n
            - __/play:__ Te permite escuchar una cancion en los canales de voz\n
            - __/stop:__ Te permite detener/sacar al bot de los canales de voz\n
            - __/pause:__ Te permite pausar una cancion indefinidamente\n
            - __/resume:__ Te permite continuar una cancion pausada\n
            - __/next:__ Te permite saltar a la siguiente cancion\n
            - __/loop:__ Te permite reproducir una cancion en bucle\n""")