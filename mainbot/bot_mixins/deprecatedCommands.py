from discord_components import component
from ..__imports__ import *
from ..settings import *
from ..perks import perkdict

from .discord_init import DiscordInit

class DeprecatedCommandsMixin(DiscordInit, commands.Cog):
    @commands.command()
    async def ecchi(self,ctx):
        try:
            webhook = await ctx.channel.create_webhook(name="pacchu_webhook")
            await webhook.send("That no longer exists :( rip ecchichan 2020-2020", username="ecchichan", avatar_url="https://i.redd.it/5xkpkqjoz9g11.jpg")
            await ctx.channel.webhooks()
            await webhook.delete()
        except:
            ctx.send("That no longer exists :( rip ecchichan 2020-2020")
    
    @commands.command(aliases=['pappu','lundi','seggs','sex','69'])
    async def fuck(self,ctx):
        await ctx.send(choice(self.perks['links']['erotic_perv']))
        await ctx.send("well about that discord might be looking at you bud")
        
    @commands.command()
    async def pp(self,ctx):
        await ctx.send("it might be large but this command doesnt exist anymore :(")
    
    @commands.command()
    async def simp(self,ctx):
        try:
            webhook = await ctx.channel.create_webhook(name="pacchu_webhook")
            await webhook.send(choice(perkdict['replies']['slutty']), username="Waifuchan", avatar_url="https://i.imgur.com/T3fp9AL.png")
            await ctx.channel.webhooks()
            await webhook.delete()
        except:
            ctx.send("> Webhook permission not available")
        
    

def setup(bot):
    bot.add_cog(DeprecatedCommandsMixin(bot))
