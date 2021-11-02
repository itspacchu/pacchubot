
from datetime import datetime as dt
from datetime import date

from discord_components import button
#from typing_extensions import Unpack
from mainbot.core import wikipedia_api, nasabirthday_api
from ..__imports__ import *
from ..settings import *
from .discord_init import DiscordInit

class AdditionalFeatureMixin(DiscordInit, commands.Cog):
    @commands.command(aliases=['g'])
    async def gpt(self, ctx, *lquery):
        await ctx.message.add_reaction('💡')
        query = queryToName(lquery)
        reply = g2a.gptquery(query)
        await ctx.reply(g2a.sanitize(reply))

    @commands.command(aliases=['wpotd', 'potd', 'wikipic'])
    async def wikipediapotd(self, ctx, *qdate):
        try:
            qdate = queryToName(qdate)
            if(qdate):
                qdate = list(map(int, qdate.split('-')))  # DD-MM-YY
                today_date = dt(qdate[2], qdate[1], qdate[0])
            else:
                today_date = dt.today()
            try:
                await ctx.message.add_reaction('☀')
                response = wikipedia_api.fetch_potd(today_date)
                color = find_dominant_color(response['image_src'])
                embed = discord.Embed(title="Wikipedia Picture of the Day",
                                      colour=color, description=response['filename'][6:])
                embed.set_image(url=response['image_src'])
            except:
                embed = discord.Embed(title="No Image Found", colour=discord.Colour(
                    0x6a5651), description=f"Wikipedia Doesn't have an image of the day on {qdate[0]} - {qdate[1]} - {qdate[2]}")

            embed.set_author(name=self.name, icon_url=bot_avatar_url)
            embed.set_footer(
                text="Wikipedia", icon_url="https://upload.wikimedia.org/wikipedia/en/thumb/8/80/Wikipedia-logo-v2.svg/220px-Wikipedia-logo-v2.svg.png")
            await ctx.send(embed=embed, components=[
                Button(style=ButtonStyle.URL, label="Visit wiki",
                       url=response['image_page_url']),
            ])
        except:
            await ctx.message.add_reaction('‼')
            await ctx.reply("> Something went wrong processing the image or is the date in proper format? [DD-MM-YYYY]")

    @commands.command(aliases=['hb', 'hubbleday'])
    async def hubblebirthday(self, ctx, *date_ish):
        await ctx.message.add_reaction('🔭')
        if(len(date_ish) != 0):
            date_ish = queryToName(date_ish)
            try:
                month, day = date_ish.split('-')
                img = nasabirthday_api.get_birthday_image(
                    month[1:].lower(), day)
            except:
                await ctx.message.add_reaction('‼')
                await ctx.reply("Is the date in proper format? ```\n>> September-15```")
                return None
        else:
            month, day = date.today().strftime("%B %d").lower().split(' ')
            img = nasabirthday_api.get_birthday_image(month, day)
        color = find_dominant_color(img["image-url"])
        embed = discord.Embed(colour=color)
        embed.set_image(url=img["image-url"])
        embed.set_author(name=self.name, icon_url=bot_avatar_url)
        embed.set_footer(
            text="NASA", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/NASA_logo.svg/300px-NASA_logo.svg.png")
        await ctx.send(embed=embed, components=[
            Button(style=ButtonStyle.URL, label="Visit Source",
                   url=img["hubble-url"]),
        ])

    @commands.command(pass_context=True, aliases=['que'])
    async def question(self, ctx, *lquery):
        await ctx.message.add_reaction('🔎')
        query = queryToName(lquery)
        reply = g2a.questionreply(query)
        await ctx.reply(reply)

    @commands.command()
    async def spotify(self, ctx, user: discord.Member = None):
        wait = None
        song_url_if_exists = ""
        le_url = "https://open.spotify.com/track/"
        await ctx.message.add_reaction('🎵')
        flag = 0
        if user == None:
            user = ctx.message.author
        if user.activities:
            for activity in user.activities:
                if isinstance(activity, discord.Spotify):
                    flag = 1
                    embed = discord.Embed(title=f"{user.name}'s Spotify", description="Listening to {}".format(
                        activity.title), color=find_dominant_color(activity.album_cover_url))
                    embed.set_thumbnail(url=activity.album_cover_url)
                    embed.add_field(name="Artist", value=activity.artist)
                    song_url_if_exists = le_url+activity.track_id
                    allbuttons = [
                        Button(style=ButtonStyle.URL, label="Open in Spotify",
                               url=le_url + activity.track_id)
                    ]
                    voice_state = ctx.author.voice
                    if(voice_state != None and ctx.guild.id == voice_state.channel.guild.id):
                        allbuttons.append(
                            Button(style=ButtonStyle.green, label="Spotify",
                               url=song_url_if_exists),
                        )
                    wait = await ctx.send(embed=embed, components=allbuttons)
        if(flag == 0):
            embed = discord.Embed(
                title=f"{user.name}'s Spotify",
                description="Not Listening to anything",
                color=0x1DB954)
            await ctx.send(embed=embed, delete_after=20)

        if(voice_state != None and ctx.channel.guild.id == voice_state.channel.guild.id):
            while True:
                res = await self.client.wait_for("button_click", timeout=300)
                await ctx.invoke(self.client.get_command('play'), url=song_url_if_exists)
                await res.respond(type=InteractionType.ChannelMessageWithSource, content="Connecting to Voice channel ...")
        

    @commands.command(aliases=['linkify', 'li'])
    async def linkit(self, ctx, *, url):
        try:
            response = requests.get(url)
            try:
                soup = BeautifulSoup(response.text, 'html.parser')
                title = soup.find("meta", property="og:title")
                imageurl = soup.find("meta", property="og:image")
                titleval = title["content"] if title else domain_finder(url)
                webhook = await ctx.channel.create_webhook(name=ctx.author.name)
                embed = discord.Embed(
                    title=titleval, colour=discord.Colour(0x90ca1f), url=url)
                if(imageurl):
                    embed.set_thumbnail(url=imageurl["content"])
                await webhook.send(embed=embed, username=ctx.author.name, avatar_url=ctx.author.avatar_url)
                webhooks = await ctx.channel.webhooks()
                for webhook in webhooks:
                    try:
                        await webhook.delete()
                    except:
                        pass
                await ctx.message.delete()
            except Exception as e:
                await ctx.message.add_reaction(Emotes.PACEXCLAIM)
                print(e)
        except requests.ConnectionError as exception:
            pass
            
def setup(bot):
    bot.add_cog(AdditionalFeatureMixin(bot))
