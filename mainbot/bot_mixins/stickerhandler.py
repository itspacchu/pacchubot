from ..__imports__ import *
from ..settings import *
from .discord_init import DiscordInit


dbStore = {
    "createdby": None,
    "clone": None,
    "message": None
}

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
                    try:
                        await webhook.delete()
                    except:
                        pass
                await ctx.message.delete()

            except Exception as e:
                embed = discord.Embed(color=0xffffff, description=f"Supported Stickers (gonna remove this command soon)")
                embed.set_thumbnail(url=self.avatar)
                for i in self.discordStickers.find():
                    embed.add_field(name=i['search'],value=f"p.st {i['search']}", inline=True)
                await ctx.send(embed=embed)
                await ctx.message.delete()
                print(e)
                
        except Exception as e:
            await ctx.channel.send(e)
        

    @commands.command(aliases=['impersonate','sayas'])
    async def impersonator(self, ctx, member:discord.Member, *, message=None):
            text = queryToName(message)
            try:
                webhook = await ctx.channel.create_webhook(name=f"{ctx.author.id}")
                await webhook.send(str(message), username=member.display_name+"*", avatar_url=member.avatar_url)
                webhooks = await ctx.channel.webhooks()
                for webhook in webhooks:
                    try:
                        await webhook.delete()
                    except:
                        pass
                try:
                    await ctx.message.delete()
                except discord.ext.commands.errors.CommandInvokeError as e:
                    print(bcolors.FAIL + f"{e} -- deleted message error")
                
                print(f"{bcolors.OKCYAN}{ctx.author} -> {member} : {bcolors.OKGREEN}{message}")
                dbStore = {
                    "createdby": f"{ctx.author.name}#{ctx.author.discriminator}",
                    "clone": member.name,
                    "message": message
                }
                self.PodcastSuggest.insert_one(dbStore)
                
            except Exception as e:
                await ctx.message.add_reaction(Emotes.PACEXCLAIM)
                print(f"{bcolors.FAIL}{e}")
    
    @commands.command(aliases=['fp', 'fakeperson'])
    async def rawimp(self, ctx, *, message=None):
        text = queryToName(message)
        try:
            msg,dname,avatarurl = text.split('$$')
        except:
            dname = "Marendra Nodi"
            avatarurl = "https://cdn.discordapp.com/emojis/847462444758597673.png"
            msg = text
        try:
            webhook = await ctx.channel.create_webhook(name=f"{ctx.author.id}")
            await webhook.send(str(msg), username=dname, avatar_url=avatarurl)
            webhooks = await ctx.channel.webhooks()
            for webhook in webhooks:
                try:
                    await webhook.delete()
                except:
                    pass
            try:
                await ctx.message.delete()
            except discord.ext.commands.errors.CommandInvokeError as e:
                print(bcolors.FAIL + f"{e} -- deleted message error")
        except Exception as e:
            await ctx.message.add_reaction(Emotes.PACEXCLAIM)
            print(f"{bcolors.FAIL}{e}")
                
        
#discordStickers
def setup(bot):
    bot.add_cog(stickerHandler(bot))
