from ..__imports__ import *
from ..settings import *
from ..perks import perkdict

from .discord_init import DiscordInit

class DeprecatedCommandsMixin(DiscordInit, commands.Cog):
    @commands.command()
    async def ecchi(self,ctx):
        await ctx.reply("That was removed due to licensing issues :( rip ecchichan 2020-2020")
    
    @commands.command()
    async def fuck(self,ctx):
        await ctx.send(choice(self.perks['links']['erotic_perv']))
        await ctx.send("well about that discord might be looking at you bud")
        
    @commands.command()
    async def pp(self,ctx):
        await ctx.send("it might be large but this command doesnt exist anymore :(")
    
    @commands.command()
    async def simp(self,ctx):
        await ctx.send("No")
    
    

def setup(bot):
    bot.add_cog(DeprecatedCommandsMixin(bot))
