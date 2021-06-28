from ..__imports__ import *
from ..settings import *
from .discord_init import DiscordInit

#webhooks stuff goes here
class stickerHandler(DiscordInit, commands.Cog):
    @commands.command(aliases=['st','sendsticker','sends'])
    async def sticker(self, ctx, stickername="onmyway"):
        try:
            query = {'search': stickername}  # exact match here
            try:
                match = self.discordStickers.find_one(query)['stickerurl']
                webhook = await ctx.channel.create_webhook(name=ctx.author.name)
                await webhook.send(match, username=ctx.author.name, avatar_url=ctx.author.avatar_url)
                await ctx.channel.webhooks()
                await ctx.message.delete()
            except:
                pass  
        except Exception as e:
            await ctx.channel.send(e)

    @commands.command(aliases=['impersonate'])
    async def impersonator(self, ctx, whom:discord.Member,*text):
            text = queryToName(text)
            try:
                webhook = await ctx.channel.create_webhook(name=whom.name)
                await webhook.send(text, username=whom.name + '*' , avatar_url=whom.avatar_url)
                await ctx.channel.webhooks()
                await ctx.message.delete()
            except Exception as e:
                await ctx.message.add_reaction('<:pacDoubleExclaim:858677949775872010>')
                
    
#discordStickers
def setup(bot):
    bot.add_cog(stickerHandler(bot))
