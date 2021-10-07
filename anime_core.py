from jikanpy import Jikan
from imports import *
from utilityhandler import *

class AnimeCore(commands.Cog):
    ani = Jikan()
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['ani'])
    async def anime(self,ctx,*,animeQuery,index=0):
        try:
            try:
                await ctx.message.add_reaction('🔍')
                asrc = self.ani.search('anime', animeQuery)['results'][index]
            except:
                await ctx.message.add_reaction('🔍')
                asrc = self.ani.search('anime', animeQuery)['results'][index+1]
            mal_id = asrc['mal_id']
            more_info = self.ani.anime(mal_id)
            trailer_url = more_info['trailer_url']
            if(not trailer_url == None):
                embed = nextcord.Embed(title=more_info['title'], url=str(more_info['trailer_url']), description="Youtube", color=0xffff00)
            else:
                embed = nextcord.Embed(
                    title=more_info['title'], description="No Trailer available", color=find_dominant_color(asrc['image_url']))
            try:
                embed.set_author(name=more_info['title_japanese'])
            except:
                embed.set_author(name=asrc['title'])
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
            del_dis = await ctx.send(embed=embed)
        except KeyError:
            await ctx.message.add_reaction('😭')
            embed = nextcord.Embed(color=0xff0000)
            embed.add_field(name="Anime Not Found", value="That Anime is not found on MAL", inline=False)
            embed.set_footer(text=self.name, icon_url=self.avatar)
            await ctx.send(embed=embed)
