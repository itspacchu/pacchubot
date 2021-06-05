from datetime import datetime as dt
from datetime import date
#from typing_extensions import Unpack
from mainbot.core import wikipedia_api,nasabirthday_api
from ..__imports__ import *
from ..settings import *
from .discord_init import DiscordInit

class AdditionalFeatureMixin(DiscordInit, commands.Cog):
    @commands.command(aliases=['g'])
    async def gpt(self, ctx, *lquery):
        await ctx.message.add_reaction('💡')
        query = queryToName(lquery)
        reply = g2a.gptquery(query)
        await ctx.reply(reply)
        dbStore = {
            "query": query,
            "username": ctx.message.author.name,
            "reply": reply
        }
        self.gptDb.insert_one(dbStore)
        
    @commands.command(aliases=['wpotd', 'potd','wikipic'])
    async def wikipediapotd(self, ctx , *qdate):
        try:
            qdate = queryToName(qdate)
            if(qdate):
                qdate = list(map(int,qdate.split('-'))) ## DD-MM-YY
                today_date = dt(qdate[2],qdate[1],qdate[0])
            else:
                today_date = dt.today()
            try:
                await ctx.message.add_reaction('☀')
                response = wikipedia_api.fetch_potd(today_date)
                color = find_dominant_color(response['image_src'])
                embed = discord.Embed(title="Wikipedia Picture of the Day", colour=color, url=response['image_page_url'], description=response['filename'][6:])
                embed.set_image(url=response['image_src'])
            except:
                embed = discord.Embed(title="No Image Found", colour=discord.Colour(
                    0x6a5651), description=f"Wikipedia Doesn't have an image of the day on {qdate[0]} - {qdate[1]} - {qdate[2]}")
            
            embed.set_author(name=self.name, icon_url=bot_avatar_url)
            embed.set_footer(
                text="Wikipedia", icon_url="https://upload.wikimedia.org/wikipedia/en/thumb/8/80/Wikipedia-logo-v2.svg/220px-Wikipedia-logo-v2.svg.png")
            await ctx.send(embed=embed)
        except ValueError:
            await ctx.message.add_reaction('‼')
            await ctx.reply("Is the date in proper format? ```DD-MM-YYYY \n>> 15-09-2001```")

    @commands.command(aliases=['hb', 'hubbleday'])
    async def hubblebirthday(self, ctx , *date_ish):
        await ctx.message.add_reaction('🔭')
        if(len(date_ish) != 0):
            date_ish = queryToName(date_ish)
            try:
                month,day = date_ish.split('-')
                img = nasabirthday_api.get_birthday_image(month[1:].lower(), day)
            except:
                await ctx.message.add_reaction('‼')
                await ctx.reply("Is the date in proper format? ```\n>> September-15```")
                return None
        else:
            month, day = date.today().strftime("%B %d").lower().split(' ')
            img = nasabirthday_api.get_birthday_image(month,day)
        color = find_dominant_color(img["image-url"])
        embed = discord.Embed(colour=color)
        embed.set_image(url=img["image-url"])
        embed.set_author(name=self.name, icon_url=bot_avatar_url)
        embed.set_footer(
            text="NASA", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/NASA_logo.svg/300px-NASA_logo.svg.png")
        await ctx.send(embed=embed)



    @commands.command(pass_context=True, aliases=['q', 'que'])
    async def question(self, ctx, *lquery):
        await ctx.message.add_reaction('🔎')
        query = queryToName(lquery)
        reply = g2a.questionreply(query)
        await ctx.reply(reply)
        dbStore = {
            "query": query,
            "username": ctx.message.author.name,
            "reply": reply
        }
        self.gptDb.insert_one(dbStore)

    @commands.command()
    async def stats(self, ctx):
        embed = discord.Embed(color=0xf3d599)
        embed.set_author(name=self.client.user.name,
                         icon_url=self.client.user.avatar_url)
        try:
            embed.add_field(name="Pacchu's Slave stat counter",
                            value="shows all the statistics of the bot", inline=False)
            embed.add_field(name="Weebo Anime searches", value=str(
                self.animeSearch.count_documents({"guild": ctx.message.guild.id})), inline=True)
            embed.add_field(name="Weebo Manga searches", value=str(
                self.mangaSearch.count_documents({"guild": ctx.message.guild.id})), inline=True)
            embed.add_field(name="Anime images delivered for simps", value=str(
                self.animePics.count_documents({"guild": ctx.message.guild.id})), inline=True)
            embed.set_footer(
                text=f"MongoDB Connection Active 🟢", icon_url=self.avatar)
            await ctx.send(embed=embed)
        except KeyError:
            embed.add_field(name="Database API cannot be reachable 🔴",
                            value="404?", inline=True)
            embed.set_footer(
                text=f"Facebook doesnt sponser this btw", icon_url=self.avatar)
            await ctx.send(embed=embed)

    @commands.command()
    async def spotify(ctx, user: discord.Member = None):
        await ctx.message.add_reaction('🎵')
        if user == None:
            user = ctx.author
            pass
        if user.activities:
            for activity in user.activities:
                if isinstance(activity, discord.Spotify):
                    embed = discord.Embed(title=f"{user.name}'s Spotify", description="Listening to {}".format(
                        activity.title), color=find_dominant_color(activity.album_cover_url))
                    embed.set_thumbnail(url=activity.album_cover_url)
                    embed.add_field(name="Artist", value=activity.artist)
                    await ctx.reply(embed=embed)
                else:
                    embed = discord.Embed(
                        title=f"{user.name}'s Spotify",
                        description="Not Listening to anything",
                        color=0x1DB954)
                    await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(AdditionalFeatureMixin(bot))

