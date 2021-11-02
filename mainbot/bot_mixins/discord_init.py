from mainbot.core.gpt2api import mention_convo
from ..__imports__ import *
from ..settings import *
from ..perks import perkdict
from ..core.gpt2api import mention_convo

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
        # self.client.event(self.on_command_error)

        self.db = mongo_client['PacchuSlave']
        self.init_db()

    async def on_ready(self):
        print('We have logged in as {0.user}'.format(self.client))
        if not hasattr(self, 'name'):
            self.name = self.client.user.name
        if not hasattr(self, 'avatar'):
            self.avatar = "https://cdn.discordapp.com/attachments/715107506187272234/850379532459573288/pacslav.png"
        statustxt = "Pacchu is doing No Nut November seriously"
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
            if(x == self.client.user):
                if(len(message.content) > 25):
                    payload_to_send = message.content.replace(
                        "<@!709426015759368282>", "")
                else:
                    payload_to_send = choice(
                        ["Bonjour", "Weather is good", "I'm good", "Hi", "Waddup"])

                await message.channel.send(mention_convo(payload_to_send)["generated_text"] + " " + message.author.mention)
    
        await self.client.process_commands(message)

        if('pacchu' in message.content.lower() and len(message.content) > 10):
            await message.add_reaction(Emotes.PACCHU)

        qq = message.content.lower().split(' ')[0]
        if(len(qq) >= 3 and qq != None):
            query = {'search': qq}  # exact match here
            try:
                match = self.MemberTaunt.find_one(query)['taunt']
                await message.channel.send(match)
            except Exception as e:
                await asyncio.sleep(1)  # this error is on every goddamn message ffs

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
    async def ping(self, ctx):
        await ctx.message.add_reaction('⌚')
        embed = discord.Embed(colour=discord.Colour(0x27ce89))
        embed.add_field(name="Latency", value=f"> Latency {round(self.client.latency * 1000)}ms")
        embed.add_field(name="CPU Load",value=f"{round(psutil.cpu_percent(4))}% Usage")
        embed.add_field(name="Memory Load", value=f'{round(psutil.virtual_memory().available/1024**2,2)} MB / 900MB')
        embed.add_field(name="Servers", value=f"Sneaking in {str(len(self.client.guilds))} Servers", inline=True)
        await better_send(ctx, embed=embed)

    @ commands.command()
    async def invite(self, ctx):
        await ctx.message.add_reaction(Emotes.PACPILOVE)
        embed = discord.Embed(title="Click here", url="https://discord.com/api/oauth2/authorize?client_id=709426015759368282&permissions=8&scope=bot",
                              description="Invite link for this bot", color=Discord_init_Color)
        embed.set_thumbnail(url=self.avatar)
        await ctx.send(embed=embed, components=[
            Button(style=ButtonStyle.URL, label="Add me to your server",
                   url="https://discord.com/api/oauth2/authorize?client_id=709426015759368282&permissions=8&scope=bot")
        ])

    @ commands.command(aliases=['gh'])
    async def github(self, ctx):
        await ctx.message.add_reaction(Emotes.PACPILOVE)
        await ctx.send("https://github.com/itspacchu/pacchubot", components=[
            Button(style=ButtonStyle.URL, label="Visit my Github",
                   url="https://github.com/itspacchu/pacchubot")
        ])

    @ commands.command(aliases=['cstatus'])
    async def statuschange(self, ctx, *, newstatus):
        await ctx.message.add_reaction(Emotes.PACPLAY)
        if(isItPacchu(str(ctx.author.id))):
            statustxt = newstatus
            await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=statustxt))
        else:
            await ctx.send("> **SUDO COMMAND** Only my creator has the authority over that!!" + ctx.author.mention)

    @ commands.command(aliases=['asbot'])
    async def impbot(self, ctx, *, msgtosend):
        if(isItPacchu(str(ctx.author.id)) or ctx.author.guild_permissions.administrator):
            if(ctx.author.guild_permissions.administrator):
                msgtosend += " [Admin]"
            await ctx.send(msgtosend)
            await ctx.message.delete()
        else:
            await ctx.send("> **SUDO COMMAND** This is a sudo command " + ctx.author.mention)

    @ commands.command(aliases=['h', 'halp', 'hel'])
    async def help(self, ctx, pgno=0):
        embedColor = find_dominant_color(ctx.author.avatar_url_as(
            format=None, static_format='png', size=64))
        embed = discord.Embed(
            color=embedColor, description=f"Created by Pacchu & Leo {pgno+1}/2")
        embed.set_thumbnail(url=self.avatar)
        if(pgno == 0):

            embed.add_field(name=f"{self.pre}avatar @Pacchu / {self.pre}av @Pacchu",
                            value=f"Supports Cartoonizing [p.ic] , Edge Detection [p.ied] , Distorting [p.id] ", inline=False)

            embed.add_field(name=f"{self.pre}bruh/sike [emote,link,text message]",
                            value=f"Something to be saved? idk why it an option", inline=False)

            embed.add_field(name=f"{self.pre}pod",
                            value="Podcast playback section", inline=False)

            embed.add_field(name=f"{self.pre}lofi/pl [study/sleep]",
                            value="Lofi music", inline=False)

            embed.add_field(name=f"{self.pre}anime/ani",
                            value="Searches for given anime", inline=True)

            embed.add_field(name=f"{self.pre}manga/m",
                            value="Searches for give Manga", inline=True)

            embed.add_field(name=f"{self.pre}spotify @mention",
                            value="Gets the user's Spotify activity", inline=False)

        elif(pgno == 1):
            embed.add_field(name=f"{self.pre}wikipic/wpotd Date",
                            value="Fetches Wikipedia Picture of the Day", inline=False)
            embed.add_field(name=f"{self.pre}hubbleday/hb Date",
                            value="What Hubble saw on your birthday", inline=False)
            embed.add_field(name=f"{self.pre}invite",
                            value="Invite link for this bot", inline=False)
            embed.add_field(name=f"{self.pre}anipics/ap",
                            value="Searches for Images of given Anime Charactor", inline=True)
            embed.add_field(name=f"{self.pre}cartoonize/ic @mention/file",
                            value="Image Processing Cartoonize AI", inline=True)
            embed.add_field(name=f"{self.pre}distort/id @mention/file",
                            value="Image Processing Distort Image based on VectorField", inline=True)
            embed.add_field(name=f"{self.pre}sticker/st [sticker name]",
                            value="Discord Stickers NQN clone", inline=False)
            embed.add_field(name=f"{self.pre}impersonate/sayas @mention 'Deez nuzz' ",
                            value="Impersonates the person mentioned", inline=False)
            embed.add_field(name=f"{self.pre}quote",
                            value="Give a random quote", inline=True)
            embed.add_field(name=f"{self.pre}q \"Why is chocolate beautiful?\"",
                            value="gpt neo answering", inline=True)

            embed.add_field(name=f"{self.pre}github",
                            value="Contribute to this bot", inline=False)
        embed.set_footer(
            text=f"{self.name} {self.VERSION}", icon_url=self.avatar)
        del_dis = await ctx.send(embed=embed, components=[[
            Button(style=ButtonStyle.gray, label="More help"),
        ],])

        res = await self.client.wait_for("button_click", timeout=100)
        if(await ButtonProcessor(ctx, res, "More help", userCheck=True)):
            await del_dis.delete()
            del_dis = None
            if(pgno == 0):
                pgnoToGo = 1
            else:
                pgnoToGo = 0
            await ctx.invoke(self.client.get_command('help'), pgno=pgnoToGo)


def setup(bot):
    bot.add_cog(BaseBot(bot))
