from discord import channel
from discord.utils import find
from ..__imports__ import *
from ..settings import *

from .discord_init import DiscordInit

Anime_Embed_color = 0x54a7ff

class AnimeMixin(DiscordInit, commands.Cog):
    @commands.command(aliases=['ap','anichar', 'anic'])
    async def anipics(self, ctx, *Query,index=0):
        global ani, http
        del_dis =None
        charQuery = queryToName(Query)
        try:
            await ctx.message.add_reaction('🔍')
            try:
                malID = int(charQuery)
                url = f"https://api.jikan.moe/v3/character/{malID}/pictures"
                name = f"https://api.jikan.moe/v3/character/{malID}"
            except ValueError:
                charid = ani.search('character', charQuery)['results'][index]
                url = f"https://api.jikan.moe/v3/character/{charid['mal_id']}/pictures"
                name = f"https://api.jikan.moe/v3/character/{charid['mal_id']}"
                
            chardetail = json.loads(http.request('GET', name).data.decode())
            namedat = chardetail['name']
            picdat = json.loads(http.request('GET', url).data.decode())['pictures']
            color = find_dominant_color(choice(picdat)['large'])
            embed = discord.Embed(title=f"{namedat}",url = chardetail['url'] ,colour=color)
            try:
                embed.add_field(
                    name="from Anime/Manga", value=chardetail['animeography'][index]['name'], inline=True)
            except:   
                try:
                    embed.add_field(
                        name="from Manga", value=chardetail['mangaography'][index]['name'], inline=True)
                except:
                    pass
            embed.set_image(url=choice(picdat)['large'])
            del_dis = await ctx.send(embed=embed,components=[[
                Button(style=ButtonStyle.green, label="Next Picture"),
                Button(style=ButtonStyle.URL, label="Anime",
                       url=chardetail['animeography'][index]['url']),
                Button(style=ButtonStyle.URL, label="Manga",
                       url=chardetail['mangaography'][index]['url']),
            ],])
        except IndexError as e:
            await ctx.message.add_reaction('😞')
            embed = discord.Embed(color=0xff0000)
            embed.add_field(name="Images Not Found",value=" Coudn't find any images on given Query try charID? ", inline=False)
            embed.set_footer(
                text=f" {self.name} {version}", icon_url=self.avatar)
            await ctx.send(embed=embed)
            await report_errors_to_channel(self.client, e)
        
        while True:
            res = await self.client.wait_for("button_click")
            if(await ButtonProcessor(ctx, res, "Next Picture")):
                await del_dis.delete()
                del_dis = None
                await ctx.invoke(self.client.get_command('anipics'), charQuery, index=index+1)
        
        
            

    @commands.command(aliases=['ani', 'anim'])
    async def anime(self,ctx, *Query,index=0):
        del_dis = None
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
                asrc = ani.search('anime', animeQuery)['results'][index]
            except:
                await ctx.message.add_reaction('🔍')
                asrc = ani.search('anime', animeQuery)['results'][index+1]
            mal_id = asrc['mal_id']
            more_info = ani.anime(mal_id)
            trailer_url = more_info['trailer_url']
            if(not trailer_url == None):
                embed = discord.Embed(title=more_info['title'], url=str(more_info['trailer_url']), description="Youtube", color=Anime_Embed_color)
            else:
                embed = discord.Embed(
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
            del_dis = await ctx.send(embed=embed,components=[
                Button(style=ButtonStyle.green, label="Next Anime"),
                Button(style=ButtonStyle.URL, label="MAL", url=asrc['url'])
            ])
        except KeyError:
            await ctx.message.add_reaction('😭')
            embed = discord.Embed(color=0xff0000)
            embed.add_field(name="Anime Not Found", value="That Anime is not found on MAL", inline=False)
            embed.set_footer(text=self.name, icon_url=self.avatar)
            await ctx.send(embed=embed)
        while True:
            res = await self.client.wait_for("button_click")
            if(await ButtonProcessor(ctx,res,"Next Anime")):
                await del_dis.delete()
                del_dis = None
                await ctx.invoke(self.client.get_command('anime'), animeQuery , index=index+1)
        


    @commands.command(aliases=['man', 'm'])
    async def manga(self, ctx, *Query,index=0):
        global  ani
        del_dis = None
        mangaQuery = queryToName(Query)
        dbStore = {
            "charname": mangaQuery,
            "username": ctx.message.author.name,
        }
        self.mangaSearch.insert_one(dbStore)
        try:
            await ctx.message.add_reaction('🔍')
            asrc = ani.search('manga', mangaQuery)['results'][index]
            try:
                color = find_dominant_color(asrc['image_url'])
            except:
                color = Anime_Embed_color
            embed = discord.Embed(title="Manga Search result", description=asrc['mal_id'], color=Anime_Embed_color)
            embed.set_author(name=asrc['title'])
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
            del_dis = await ctx.send(embed=embed,components=[
                Button(style=ButtonStyle.green, label="Next Manga"),
                Button(style=ButtonStyle.URL, label="Visit MAL", url=asrc['url'])
            ])
        except Exception as e:
            await ctx.message.add_reaction('😿')
            embed = discord.Embed(color=0xff0000)
            embed.add_field(name="Manga Not Found", value="Manga Query not found on MAL", inline=False)
            await ctx.send(embed=embed)
            await report_errors_to_channel(self.client, e)
        while True:
            res = await self.client.wait_for("button_click",timeout=500)
            if(await ButtonProcessor(ctx, res, "Next Manga")):
                await del_dis.delete()
                del_dis = None
                await ctx.invoke(self.client.get_command('anime'), mangaQuery, index=index+1)

def setup(bot):
    bot.add_cog(AnimeMixin(bot))
