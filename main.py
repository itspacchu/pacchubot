import nextcord
from nextcord.ext import commands
from botmixins.music import MusicCog  # Import the music cog

intents = nextcord.Intents.default()
intents.message_content = True
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='p.', intents=intents)

# Load the music cog
bot.add_cog(MusicCog(bot))

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

bot.run('')
