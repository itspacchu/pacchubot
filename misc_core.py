from imports import *
import requests
from random import randint,choice

class MiscCommandsCore(commands.Cog):
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
    async def sigma(self, ctx):
        await ctx.message.add_reaction("♎")
        kek = await ctx.send("Calculating chance you having a partner")
        progbar = await ctx.send("```[>          ]```")
        for i in range(5):
            await progbar.edit(content="```[" + "="*i*2 + ">" + " "*(11-(i*2)) + "]```")
            await asyncio.sleep(1.3)
        await progbar.edit(content="```[===========]```")
        await asyncio.sleep(1.3)
        await progbar.delete()
        await kek.edit(f"> You have a {randint(0,950)/10}% of finding a partner partner {ctx.author.mention}")
    
    @commands.command()
    async def echodetails(self, ctx):
        if(1):
            pass
        else:
            await ctx.send("> THIS IS A SUDO COMMAND !!! Only Bot Developers can run this command")
            return
        try:
            await ctx.send(f"```USER : {ctx.author.name}#{ctx.author.discriminator}\n> {ctx.message.content}\n```")
            try:
                await ctx.send(f"```FILES FOUND : {ctx.attachments[0].url}```")
            except:
                pass
        except:
            await ctx.send("> Wat dis should work all the time some bug")
    
    @commands.command(aliases=['impersonate', 'sayas'])
    async def impersonator(self, ctx, member: nextcord.Member, *, message=None):
        text = message
        try:
            webhook = await ctx.channel.create_webhook(name=f"{ctx.author.id}")
            await webhook.send(str(message), username=member.display_name+"*", avatar_url=member.avatar.url)
            webhooks = await ctx.channel.webhooks()
            for webhook in webhooks:
                try:
                    await webhook.delete()
                except:
                    pass
            try:
                await ctx.message.delete()
            except nextcord.ext.commands.errors.CommandInvokeError as e:
                await ctx.message.add_reaction(Emotes.PACEXCLAIM)
        except:
            await ctx.send("> Webhook permission not available")
