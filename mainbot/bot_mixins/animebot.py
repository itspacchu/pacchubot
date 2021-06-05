from discord.utils import find
from ..__imports__ import *
from ..settings import *

from .discord_init import DiscordInit

Anime_Embed_color = 0x54a7ff

class AnimeMixin(DiscordInit, commands.Cog):
    @commands.command(aliases=['achar', 'ac'])
    async def anichar(self, ctx, *Query):
        global ani
        animeQuery = queryToName(Query)
        try:
            await ctx.message.add_reaction('🔍')
            asrc = ani.character(ani.search('character', str(animeQuery))['results'][0]['mal_id'])
            if(len(asrc['about']) < 200):
                embed = discord.Embed(title=f"**{asrc['name']}**", colour=discord.Colour(Anime_Embed_color), url=asrc['url'], description=asrc['about'].strip().replace(r'\n', '')+'...')
            else:
                embed = discord.Embed(title=f"**{asrc['name']}**", colour=discord.Colour(Anime_Embed_color), url=asrc['url'], description=asrc['about'][200].strip().replace(r'\n', '')+'...')
            embed.set_footer(text=f"Not the correct Character ... Try spelling their full name", icon_url=self.client.user.avatar_url)
            embed.add_field(name="Waifu Meter", value=f"{asrc['member_favorites']} have liked them", inline=False)
            try:
                await ctx.reply(embed=embed)
            except AttributeError:
                await ctx.send(embed=embed)
            try:
                dbStore = {
                    "charname": animeQuery,
                    "username": ctx.message.author.name,
                }
            except:
                pass
            self.charSearch.insert_one(dbStore)
        except:
            await ctx.message.add_reaction('😞')
            embed = discord.Embed(color=Anime_Embed_color)
            embed.add_field(name="Character Not Found",value="That Character is not found", inline=False)
            embed.set_footer(text=f" {self.name} {version}", icon_url=self.avatar)
            try:
                await ctx.reply(embed=embed)
            except AttributeError:
                await ctx.send(embed=embed)

    @commands.command(aliases=['ap', 'anip', 'anishow'])
    async def anipics(self, ctx, *Query):
        global ani, http
        charQuery = queryToName(Query)
        try:
            
            await ctx.message.add_reaction('🔍')
            charid = ani.search('character', charQuery)['results'][0]
            url = f"https://api.jikan.moe/v3/character/{charid['mal_id']}/pictures"
            picdat = json.loads(http.request('GET', url).data.decode())['pictures']
            color = find_dominant_color(choice(picdat)['large'])
            embed = discord.Embed(title=f"_{charid['name']}_", colour=color, url=charid['url'])
            embed.set_image(url=choice(picdat)['large'])
            embed.set_footer(text=f"Search for full title for more accurate results",icon_url=self.client.user.avatar_url)
            await ctx.reply(embed=embed)
        except:
            await ctx.message.add_reaction('😞')
            embed = discord.Embed(color=0xff0000)
            embed.add_field(name="Images Not Found",value=" Coudn't find any images on given Query ", inline=False)
            embed.set_footer(
                text=f" {self.name} {version}", icon_url=self.avatar)
            await ctx.reply(embed=embed)

    @commands.command(aliases=['ani', 'anim'])
    async def anime(self,ctx, *Query):
        global  ani
        animeQuery = queryToName(Query).strip()
        dbStore = {
            "charname": animeQuery,
            "username": ctx.message.author.name,
        }
        self.animeSearch.insert_one(dbStore)
        try:
            try:
                await ctx.message.add_reaction('🔍')
                asrc = ani.search('anime', animeQuery)['results'][0]
            except:
                await ctx.message.add_reaction('🔍')
                asrc = ani.search('anime', animeQuery)['results'][1]
            mal_id = asrc['mal_id']
            more_info = ani.anime(mal_id)
            trailer_url = more_info['trailer_url']
            if(not trailer_url == None):
                embed = discord.Embed(title=more_info['title'], url=str(more_info['trailer_url']), description="Youtube", color=Anime_Embed_color)
            else:
                embed = discord.Embed(
                    title=more_info['title'], description="No Trailer available", color=find_dominant_color(asrc['image_url']))
            try:
                embed.set_author(name=more_info['title_japanese'], url=asrc['url'])
            except:
                embed.set_author(name=asrc['title'], url=asrc['url'])
            try:
                embed.set_image(url=asrc['image_url'])
            except:
                pass
            try:
                embed.add_field(name="Studio", value=str(more_info['studios'][0]['name']) + " ", inline=True)
            except:
                pass
            try:
                embed.add_field(name="Started Airing",value=f"{asrc['start_date'][:10]} ", inline=True)
            except:
                pass
            try:
                embed.add_field(name="Rating", value=f"{asrc['score']}/10 ", inline=True)
            except:
                pass
            try:
                embed.add_field(name="Synopsis", value=str(more_info['synopsis'][:512])+'...', inline=False)
            except:
                pass
            try:
                embed.add_field(name="Episodes", value=str(
                    asrc['episodes']) + " ", inline=False)
            except:
                pass
            try:
                embed.add_field(name="Views", value=str(
                    asrc['members']) + " ", inline=True)
            except:
                pass
            try:
                embed.add_field(name="Rated", value=str(
                    asrc['rated']) + " ", inline=True)
            except:
                pass
            try:
                if(more_info['opening_themes']):
                    embed.add_field(name="Openings", value=list_to_string(more_info['opening_themes'], 4) + " ", inline=False)
            except:
                pass
            try:
                if(more_info['ending_themes']):
                    embed.add_field(name="Endings", value=list_to_string(more_info['ending_themes'], 4) + " ", inline=False)
            except:
                pass
            embed.set_footer(text=f"Search for full title for more accurate results", icon_url=self.avatar)
            await ctx.send(embed=embed)
        except KeyError:
            await ctx.message.add_reaction('😭')
            embed = discord.Embed(color=0xff0000)
            embed.add_field(name="Anime Not Found", value="That Anime is not found on MAL", inline=False)
            embed.set_footer(text=self.name, icon_url=self.avatar)
            await ctx.send(embed=embed)


    @commands.command(aliases=['man', 'm'])
    async def manga(self, ctx, *Query):
        global  ani
        mangaQuery = queryToName(Query)
        dbStore = {
            "charname": mangaQuery,
            "username": ctx.message.author.name,
        }
        self.mangaSearch.insert_one(dbStore)
        try:
            await ctx.message.add_reaction('🔍')
            asrc = ani.search('manga', mangaQuery)['results'][0]
            try:
                color = find_dominant_color(asrc['image_url'])
            except:
                color = Anime_Embed_color
            embed = discord.Embed(title="Manga Search result", description=asrc['mal_id'], color=Anime_Embed_color)
            embed.set_author(name=asrc['title'], url=asrc['url'])
            embed.add_field(name="Publishing",value=f"{asrc['start_date'][:10]}", inline=False)
            embed.add_field(name="Rating", value=f"{int(asrc['score'])}/10", inline=False)
            embed.add_field(name="Summary", value=asrc['synopsis'], inline=False)
            embed.add_field(name="Volumes", value=asrc['volumes'], inline=True)
            embed.add_field(name="Chapters", value=asrc['chapters'], inline=True)
            embed.add_field(name="Members Watched",value=asrc['members'], inline=True)
            try:
                embed.set_image(url=asrc['image_url'])
            except:
                pass
            embed.set_footer(text=f"Search for full title for more accurate results", icon_url=self.client.user.avatar_url)
            await ctx.reply(embed=embed)
        except:
            await ctx.message.add_reaction('😿')
            embed = discord.Embed(color=0xff0000)
            embed.add_field(name="Manga Not Found", value="Manga Query not found on MAL", inline=False)
            await ctx.reply(embed=embed)
        return

def setup(bot):
    bot.add_cog(AnimeMixin(bot))
