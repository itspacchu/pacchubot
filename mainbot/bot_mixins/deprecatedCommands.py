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
            await webhook.send("That was removed due to licensing issues :( rip ecchichan 2020-2020", username="ecchichan", avatar_url="https://i.redd.it/5xkpkqjoz9g11.jpg")
            await ctx.channel.webhooks()
            await webhook.delete()
        except:
            ctx.send("That was removed due to licensing issues :( rip ecchichan 2020-2020")
    
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
        
    
    @commands.command()
    async def buttons(self,ctx):
        await ctx.send("WUT DA FOOK BOOTANS",components=[
            [Button(style=ButtonStyle.red,label="DIS BUTTON EXISTS WOAOWI"),
            Button(style=ButtonStyle.URL, label="I LOV THIS ANIME",
                   url="https://4anime.to/anime/violet-evergarden"),
            Button(style=ButtonStyle.URL, label="ANOTHER BOOTON",
                   url="bit.ly/IqT6zt")],
            [Button(style=ButtonStyle.URL, label="I LOV THIS WEBTOON",
                    url="https://www.webtoons.com/en/comedy/everywhere-and-nowhere/list?title_no=1598&page=1"),
             Button(style=ButtonStyle.URL, label="DOX PACCHU",
                    url="https://www.youtube.com/user/bandinancandy")]
        ])
        
        res = await self.client.wait_for("button_click")
        if(res.channel == ctx.message.channel):
            await res.respond(
                type = InteractionType.ChannelMessageWithSource,
                content = "YOU CLICKED A BUTTTTOOONNNNNNNNNNNNNNNNN"
            )
            
        
    

def setup(bot):
    bot.add_cog(DeprecatedCommandsMixin(bot))
