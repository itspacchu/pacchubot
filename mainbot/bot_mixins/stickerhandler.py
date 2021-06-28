from ..__imports__ import *
from ..settings import *
from .discord_init import DiscordInit

#webhooks stuff goes here
class stickerHandler(DiscordInit, commands.Cog):
    @commands.command(aliases=['st','sendsticker','sends'])
    async def sticker(self,ctx,stickername=None):
        try:
            query = {'search': stickername}
            member = ctx.author# exact match here
            try:
                match = self.discordStickers.find_one(query)['stickerurl']
                webhook = await ctx.channel.create_webhook(name=member.name)
                await webhook.send(str(match), username=member.name, avatar_url=member.avatar_url)
                webhooks = await ctx.channel.webhooks()
                for webhook in webhooks:
                    await webhook.delete()
                await ctx.message.delete()

            except Exception as e:
                embed = discord.Embed(color=0xffffff, description=f"Supported Stickers (more adding soon)")
                embed.set_thumbnail(url=self.avatar)
                for i in self.discordStickers.find():
                    embed.add_field(name=i['search'],value=f"p.st {i['search']}", inline=True)
                await ctx.send(embed=embed)
                await ctx.message.delete()
                await report_errors_to_channel(self.client, e)
                
        except Exception as e:
            await ctx.channel.send(e)
            await report_errors_to_channel(self.client, e)
        

    @commands.command(aliases=['impersonate','sayas'])
    async def impersonator(self, ctx, member: discord.Member, *, message=None):
            text = queryToName(message)
            try:
                webhook = await ctx.channel.create_webhook(name=member.name)
                await webhook.send(str(message), username=member.name+"*", avatar_url=member.avatar_url)
                webhooks = await ctx.channel.webhooks()
                for webhook in webhooks:
                        await webhook.delete()
                await ctx.message.delete()
            except Exception as e:
                await ctx.message.add_reaction('<:pacDoubleExclaim:858677949775872010>')
                await report_errors_to_channel(self.client, e)
            

            
#discordStickers
def setup(bot):
    bot.add_cog(stickerHandler(bot))
