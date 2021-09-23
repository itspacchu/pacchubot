from discord_components import component
from ..__imports__ import *
from ..settings import *
from ..perks import perkdict
from random import randint
from .discord_init import DiscordInit
import requests


class DeprecatedCommandsMixin(DiscordInit, commands.Cog):
    @commands.command()
    async def ecchi(self, ctx):
        try:
            webhook = await ctx.channel.create_webhook(name="pacchu_webhook")
            await webhook.send("That no longer exists :( rip ecchichan 2020-2020", username="ecchichan", avatar_url="https://i.redd.it/5xkpkqjoz9g11.jpg")
            await ctx.channel.webhooks()
            await webhook.delete()
        except:
            ctx.send("That no longer exists :( rip ecchichan 2020-2020")

    @commands.command()
    async def quote(self, ctx):
        try:
            webhook = await ctx.channel.create_webhook(name="pacchu_webhook")
            SOMESTUFF = requests.get(
                "https://api.quotable.io/random").json()
            await webhook.send(SOMESTUFF['content'], username=SOMESTUFF['author'], avatar_url="https://i.imgur.com/vWgiDHR.png")
            await ctx.channel.webhooks()
            await webhook.delete()
        except:
            ctx.send("That no longer exists :( rip ecchichan 2020-2020")

    @commands.command(aliases=['pappu', 'lundi', 'seggs', 'sex', '69'])
    async def fuck(self, ctx):
        await ctx.send(choice(self.perks['links']['erotic_perv']))
        await ctx.send("well about that discord might be looking at you bud")

    @commands.command()
    async def pp(self, ctx):
        await ctx.send("your thing might be large but this command doesnt exist anymore :(")

    @commands.command()
    async def sigma(self, ctx):
        await ctx.message.add_reaction("♎")
        await ctx.send("Calculating chance you having a partner")
        progbar = await ctx.send("```[>          ]```")
        for i in range(5):
            await progbar.edit(content="```[" + "="*i*2 + ">" + " "*(11-(i*2)) + "]```")
            await asyncio.sleep(1.3)
        await progbar.edit(content="```[===========]```")
        await asyncio.sleep(1.3)
        await progbar.delete()
        await ctx.send(f"> You have a {randint(0,950)/10}% of finding a partner partner")

    @commands.command(aliases=['seski'])
    async def simp(self, ctx):
        try:
            webhook = await ctx.channel.create_webhook(name="pacchu_webhook")
            await webhook.send(choice(["Oh Dadddyio", "Oniichan :3", "( ͡° ͜ʖ ͡°) :3", "Hey Daddy", "Aw Daddy"]) + " " + ctx.author.mention, username="Waifuchan", avatar_url="https://i.imgur.com/T3fp9AL.png")
            await ctx.channel.webhooks()
            await webhook.delete()
        except:
            ctx.send("> Webhook permission not available")


def setup(bot):
    bot.add_cog(DeprecatedCommandsMixin(bot))
