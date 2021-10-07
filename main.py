#python3
import imports
from on_message_core import OnMessageHandler,CoreCommands
from anime_core import AnimeCore
from image_core import ImageHandler
from music_core import MusicCore
from ctypes.util import find_library
from misc_core import MiscCommandsCore
from database_core import DatabaseHandler
from apihandler import bot_token
client = imports.commands.Bot(command_prefix=["~",">>"], intents=imports.nextcord.Intents.all())
client.remove_command("help")

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    imports.nextcord.opus.load_opus(find_library('opus'))
    
client.add_cog(OnMessageHandler(client))
client.add_cog(AnimeCore(client))
client.add_cog(ImageHandler(client))
client.add_cog(CoreCommands(client))
client.add_cog(MusicCore(client))
client.add_cog(MiscCommandsCore(client))
client.add_cog(DatabaseHandler(client))
client.run(bot_token)