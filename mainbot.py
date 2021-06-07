from mainbot.utils import bcolors
from discord.ext.commands.errors import NoEntryPointError
from mainbot import *
from mainbot.__imports__ import *
from mainbot import settings

class BotStore(DiscordInit):
    def __init__(self):
        self.client = commands.Bot(command_prefix=settings.command_prefix_use, intents=discord.Intents.all())
        
        self.client.remove_command('help')
        super().__init__(self)
        self.add_cogs()

    def add_cogs(self):
        directory = os.listdir('./mainbot/bot_mixins')
        ignore_files = ["__init__.py","musicbot.py"]
        filtered_directory = [x for x in directory if x not in ignore_files]
        for filename in filtered_directory:
            if filename.endswith('.py'):
                try:
                    self.client.load_extension(f"mainbot.bot_mixins.{filename[:-3]}")
                    print(f"{bcolors.OKCYAN}{filename} Cog imported")
                except NoEntryPointError:
                    print(f'{bcolors.WARNING}no entry point in {filename}')
        print(bcolors.CWHITE2)

    def __call__(self):
        self.client.run(self.db['discordToken'].find_one(
            {"botname": "pacchuslave"})['token'])

if __name__ == '__main__':
    Bot = BotStore()
    Bot()
