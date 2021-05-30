from datetime import datetime
from mainbot.core import wikipedia_api
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

    @commands.command()
    async def cartoonize(self, ctx):
        attachment_url = ctx.message.attachments[0].url
        filname = await cartoonize(attachment_url)
        await ctx.send(file=discord.File(f'{filname}.png'))
        
    @commands.command(aliases=['wpotd', 'potd'])
    async def wikipediapotd(self, ctx):
        today_date = datetime.today()
        print(today_date)
        response = await wikipedia_api.fetch_potd(today_date)
        embed = discord.Embed(title="Wikipedia Picture of the Day", colour=discord.Colour(0x6a5651), url=response['image_page'], description=response['filename'][6:])
        embed.set_image(url=response['image_src'])
        embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
        embed.set_author(name=self.name, icon_url=self.avatar)
        embed.set_footer(text="Wikipedia API", icon_url="https://upload.wikimedia.org/wikipedia/en/thumb/8/80/Wikipedia-logo-v2.svg/220px-Wikipedia-logo-v2.svg.png")
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
                        activity.title), color=0x1DB954)
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

