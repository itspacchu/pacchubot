from ..__imports__ import *
from ..settings import *
from .discord_init import DiscordInit
from discord.ext import commands

Discord_init_Color = 0xffbb54


class InteractionsMixin(DiscordInit, commands.Cog):

    @commands.command(aliases=['av', 'pic', 'dp'])
    async def avatar(self, ctx, member: discord.Member = None):
        hgp = member
        url_link = None
        await ctx.message.add_reaction(Emotes.PACTICK)
        if(ctx.message.author == hgp or hgp == None):
            embed = discord.Embed(
                title="OwO", description=f"{ctx.message.author.mention} steals ...wait thats your OWN", colour=find_dominant_color(ctx.message.author.avatar_url))
            embed.set_image(url=ctx.message.author.avatar_url)
            url_link = ctx.message.author.avatar_url
        else:
            embed = discord.Embed(
                title="Swong..!", description=f"{ctx.message.author.mention} yeets {hgp.mention}'s profile pic 👀'", colour=find_dominant_color(hgp.avatar_url))
            embed.set_image(url=hgp.avatar_url)
            url_link = hgp.avatar_url
        try:
            embed.set_author(name=hgp.name, icon_url=hgp.avatar_url)
        except:
            embed.set_author(name=ctx.message.author.name,
                             icon_url=ctx.message.author.avatar_url)
        embed.set_footer(text=f"{self.client.user.name}",
                         icon_url=self.client.user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(aliases=['sk'])
    async def sike(self, ctx, *qlink):
        try:
            link = ctx.message.attachments[0].url
        except:
            link = queryToName(qlink)

        if(link == ""):
            try:
                await ctx.reply(str(self.bruhs.find_one({"guild": ctx.message.author.id})['link']))
            except:
                embed = discord.Embed(color=0x00ff00)
                embed.add_field(name="No Sike! found",
                                value=f"add sike {command_prefix}sike <value> ; Value can be Link , Text  ...", inline=False)
                embed.set_footer(
                    text=f" {self_name} {version}", icon_url=self_avatar)
                await ctx.message.channel.send(embed=embed)
        else:
            if(self.bruhs.find_one({"guild": ctx.message.author.id}) == None):
                dbStore = {
                    "guild": ctx.message.author.id,
                    "link": link
                }
                self.bruhs.insert_one(
                    {"guild": ctx.message.author.id}, dbStore)
            else:
                dbStore = {
                    "guild": ctx.message.author.id,
                    "link": link
                }
                self.bruhs.replace_one(
                    {"guild": ctx.message.author.id}, dbStore)
            if(self.bruhs.find_one({"guild": ctx.message.author.id}) == None):
                dbStore = {
                    "guild": ctx.message.author.id,
                    "link": link
                }
                self.bruhs.insert_one(
                    {"guild": ctx.message.author.id}, dbStore)
            else:
                dbStore = {
                    "guild": ctx.message.author.id,
                    "link": link
                }
                self.bruhs.replace_one(
                    {"guild": ctx.message.author.id}, dbStore)
            embed = discord.Embed(color=0x00ff00)
            embed.add_field(name="Sike! Updated",
                            value="Sike! has been sucessfully updated", inline=False)
            embed.set_footer(
                text=f" {self_name} {version}", icon_url=self_avatar)
            await ctx.message.channel.send(embed=embed)

    @commands.command(aliases=['br'])
    async def bruh(self, ctx, *qlink):
        try:
            link = ctx.message.attachments[0].url
        except:
            link = queryToName(qlink)

        if(ctx.message.guild == None):
            await ctx.reply("This is a dm tho? try it in a server m8")
        else:
            if(link == ""):
                try:
                    await ctx.reply(str(self.bruhs.find_one({"guild": ctx.message.guild.id})['link']))
                except:
                    embed = discord.Embed(color=0x00ff00)
                    embed.add_field(name="No Bruh found",
                                    value=f"Consider adding Bruh using {command_prefix}Bruh <value> ; Value can be Link , Text  ...", inline=False)
                    embed.set_footer(
                        text=f" {self_name} {version}", icon_url=self_avatar)
                    await ctx.message.channel.send(embed=embed)
            else:
                if(self.bruhs.find_one({"guild": ctx.message.guild.id}) == None):
                    dbStore = {
                        "guild": ctx.message.guild.id,
                        "link": link
                    }
                    self.bruhs.insert_one(
                        {"guild": ctx.message.guild.id}, dbStore)
                else:
                    dbStore = {
                        "guild": ctx.message.guild.id,
                        "link": link
                    }
                    self.bruhs.replace_one(
                        {"guild": ctx.message.guild.id}, dbStore)
                if(self.bruhs.find_one({"guild": ctx.message.guild.id}) == None):
                    dbStore = {
                        "guild": ctx.message.guild.id,
                        "link": link
                    }
                    self.bruhs.insert_one(
                        {"guild": ctx.message.guild.id}, dbStore)
                else:
                    dbStore = {
                        "guild": ctx.message.guild.id,
                        "link": link
                    }
                    self.bruhs.replace_one(
                        {"guild": ctx.message.guild.id}, dbStore)
                embed = discord.Embed(color=0x00ff00)
                embed.add_field(name="Bruh Updated",
                                value="Bruh has been sucessfully updated", inline=False)
                embed.set_footer(
                    text=f" {self_name} {version}", icon_url=self_avatar)
                await ctx.message.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(InteractionsMixin(bot))
