from ..__imports__ import *
from ..settings import *
from ..perks import perkdict


Discord_init_Color = 0xffbb54

class DiscordInit:
    DISCORD_BOT_TOKEN = ""
    VERSION = version
    def __init__(self, client):
        self.pre = command_prefix
        self.perks = perkdict
        if not hasattr(self, 'client'):
            self.client = client
        self.ddb = DiscordComponents(client)
        self.avatar = "https://cdn.discordapp.com/attachments/715107506187272234/850379532459573288/pacslav.png"
        self.name = self_name
        
        self.client.event(self.on_ready)
        self.client.event(self.on_message)
        self.client.event(self.on_command_error)
        
        self.db = mongo_client['PacchuSlave']
        self.init_db()

    async def on_ready(self):
        print('We have logged in as {0.user}'.format(self.client))
        if not hasattr(self,'name'):
            self.name = self.client.user.name
        if not hasattr(self, 'avatar'):
            self.avatar = "https://cdn.discordapp.com/attachments/715107506187272234/850379532459573288/pacslav.png"
        statustxt = "Questioning Insanity now" #adding loop changing statuses
        activity = discord.Game(name=statustxt)
        if(self.client):
            print("Connected to Database...")
        print(self.db.list_collection_names())
        await self.client.change_presence(status=discord.Status.online, activity=activity)
    
    async def on_message(self, message):
        global client, botcount, currentcount, http, command_prefix
        if(message.author == self.client.user or message.author.bot):
            return

        for x in message.mentions:
            if(x == self.client.user and len(message.content)==21):
                await message.channel.send(choice(self.perks['replies']['pings']))
        # try:
        qq = message.content.lower().split(' ')[0]
        if(len(qq) >= 3 and qq != None):
            query = {'search': qq} # exact match here
            try:
                match = self.MemberTaunt.find_one(query)['taunt']
                await message.channel.send(match)
                if('pacchu' in query):
                    await message.message.add_reaction('<:pac_1:858689626088275988>')
                    await message.message.add_reaction('<:pac_2:858689625794019328>')
                    await message.message.add_reaction('<:pac_3:858689626025492522>')
            except:
                pass
        await self.client.process_commands(message)
    
    async def on_command_error(self,ctx, error):
        if isinstance(error, CommandNotFound):
            await ctx.send(choice(self.perks['replies']['command_not_found_error']) + f"```{self.pre}help```")
            return 
        raise error


    def init_db(self):
        self.serverstat = self.db['serverstat']
        self.bruhs = self.db['bruh']
        self.animeSearch = self.db['animeSearch']
        self.charSearch = self.db['charSearch']
        self.animePics = self.db['animePics']
        self.mangaSearch = self.db['mangaSearch']
        self.gptDb = self.db['gptQuery']
        self.PodcastSuggest = self.db['PodSuggest']
        self.VoiceUsage = self.db['VoiceActivity']
        self.MemberTaunt = self.db['memberTaunt']
        self.MiscCollection = self.db['miscCollection']
        self.discordStickers = self.db['discordStickers']

class BaseBot(DiscordInit, commands.Cog):

    @commands.command()
    async def ping(self,ctx):
        await ctx.message.add_reaction('⌚')
        embed = discord.Embed(colour=discord.Colour(0x27ce89))
        embed.add_field(name="Latency", value=f"{round(self.client.latency,2)} ms")
        embed.add_field(name="CPU", value=f"{round(psutil.cpu_freq().current/1024,2)}Ghz -- {round(psutil.cpu_percent(interval=0.1),2)}%")
        embed.add_field(name="Memory", value=f'{round(psutil.virtual_memory().available/1024**2,2)} MB')
        embed.add_field(name="Servers", value=f"Active in {str(len(self.client.guilds))} Servers", inline=True)
        await better_send(ctx,embed=embed)
        
    
    @commands.command()
    async def invite(self, ctx):
        await ctx.message.add_reaction('♥')
        embed = discord.Embed(title="Click here", url="https://discord.com/api/oauth2/authorize?client_id=709426015759368282&permissions=8&scope=bot",
                              description="Invite link for this bot", color=Discord_init_Color)
        embed.set_thumbnail(url=self.avatar)
        await ctx.send(embed=embed, components=[
            Button(style=ButtonStyle.URL, label="Add me to your server",
                   url="https://discord.com/api/oauth2/authorize?client_id=709426015759368282&permissions=8&scope=bot")
        ])
        
    @commands.command(aliases=['gh'])
    async def github(self, ctx):
        await ctx.message.add_reaction('♥')
        await ctx.send("https://github.com/itspacchu/pacchubot",components = [
            Button(style=ButtonStyle.URL, label="Visit my Github",
                   url="https://github.com/itspacchu/pacchubot")
        ])

    # add pagination to this
    @commands.command(aliases=['h', 'halp', 'hel'])
    async def help(self, ctx):
        embed = discord.Embed(
            color=Discord_init_Color, description=f"Created by Pacchu & Leo")
        embed.set_thumbnail(url=self.avatar)
        embed.add_field(name=f"{self.pre}anime/ani",
                        value="Searches for given anime", inline=True)
        embed.add_field(name=f"{self.pre}manga/m",
                        value="Searches for give Manga", inline=True)
        embed.add_field(name=f"{self.pre}anipics/ap",
                        value="Searches for Images of given Anime Charactor", inline=True)
        embed.add_field(name=f"{self.pre}cartoonize/ic @mention/file",
                        value="Image Processing Cartoonize AI", inline=True)
        embed.add_field(name=f"{self.pre}distort/id @mention/file",
                        value="Image Processing Distort Image based on VectorField", inline=True)
        embed.add_field(name=f"{self.pre}wikipic/wpotd",
                        value="Fetches Wikipedia Picture of the Day", inline=False)
        embed.add_field(name=f"{self.pre}hubbleday/hb",
                        value="What Hubble saw on your birthday", inline=False)
        embed.add_field( name=f"{self.pre}stats", value="partially implemented **bugs**", inline=False)
        """
        embed.add_field(name=f"{self.pre}pod",
                        value="Podcast playback section", inline=False)
        embed.add_field(name=f"{self.pre}play/p  , {self.pre}lofi/pl",
                        value="Youtube Playback and Lofi music", inline=False)
        """
        embed.add_field(name=f"{self.pre}invite",
                        value="Invite link for this bot", inline=False)  
        embed.add_field(name=f"{self.pre}avatar @Pacchu / {self.pre}av @Pacchu",
                        value=f"Something of use atleast", inline=False)
        embed.add_field(name=f"{self.pre}bruh/sike [emote,link,text message]",
                        value=f"Something to be saved? idk why it an option", inline=False)
        embed.add_field(name=f"{self.pre}gpt \"Today is a wonderful..\"",
                        value="gpt neo text completion", inline=True)
        embed.add_field(name=f"{self.pre}q \"Why is chocolate beautiful?\"",
                        value="gpt neo answering", inline=True)
        embed.add_field(name=f"{self.pre}spotify @mention",
                        value="Gets the user's Spotify activity", inline=False)
        embed.add_field(name=f"{self.pre}github",
                        value="Contribute to this bot", inline=False)
        embed.add_field(name=f"{self.pre}help",
                        value="isnt it obvious :o", inline=False)
        embed.set_footer(
            text=f"{self.name} {self.VERSION}", icon_url=self.avatar)
        try:
            await ctx.reply(embed=embed)
        except AttributeError:
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(BaseBot(bot))
