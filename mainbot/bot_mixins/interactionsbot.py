from ..__imports__ import *
from ..settings import *
from .discord_init import DiscordInit

class InteractionsMixin(DiscordInit, commands.Cog):
    @commands.command()
    async def hug(self,ctx, member: discord.Member):
        hgp = member
        await ctx.message.add_reaction('🤗')
        if(ctx.message.author == hgp or hgp == None):
            embed = discord.Embed(title=f"{ctx.message.author.mention} hugs themselves",description=f"Don't worry {ctx.message.author.mention}.. {choice(self.perks['replies']['sadhugs'])}", colour=discord.Colour(0x00ffb7))
            embed.set_image(url=choice(self.perks['links']['sadhugs']))
        else:
            embed = discord.Embed(title=" ", description=f"{ctx.message.author.mention} hugs {hgp.mention}", colour=discord.Colour(0x00ffb7))
            embed.set_image(url=choice(self.perks['links']['hugs']))
        embed.set_author(name=hgp.name, icon_url=hgp.avatar_url)
        embed.set_footer(text=f"{self.name}", icon_url=self.avatar)
        await ctx.reply(embed=embed)


    @commands.command()
    async def kiss(self, ctx, member: discord.Member):
        hgp = member
        await ctx.message.add_reaction('👄')
        if(ctx.message.author == hgp or hgp == None):
            embed = discord.Embed(
                title=" ", description=f"{ctx.message.author.mention} kisses themselves..HOW!!!?", colour=discord.Colour(0x00ffb7))
            embed.set_image(url=choice(self.perks['links']['erotic_perv']))
        else:
            embed = discord.Embed(
                title="💋", description=f"{ctx.message.author.mention} kisses {hgp.mention}", colour=discord.Colour(0x00ffb7))
            embed.set_image(url=choice(self.perks['links']['kiss']))
        embed.set_author(name=hgp.name, icon_url=hgp.avatar_url)
        embed.set_footer(text=f"{self.client.user.name}",
                        icon_url=self.client.user.avatar_url)
        await ctx.reply(embed=embed)

    @commands.command()
    async def kill(self, ctx, member: discord.Member):
        hgp = member
        await ctx.message.add_reaction('🔪')
        if(ctx.message.author == hgp or hgp == None):
            embed = discord.Embed(title=" ", description=f"{ctx.message.author.mention} you know there are better ways for than .. than to ask me", colour=discord.Colour(0x00ffb7))
            embed.set_image(url="https://i.pinimg.com/originals/53/4d/f2/534df2eed76c2b48bc9f892086f1e749.jpg")
        else:
            embed = discord.Embed(title=" ", description=f"{ctx.message.author.mention} kills {hgp.mention}", colour=discord.Colour(0x00ffb7))
            embed.set_image(url=choice(self.perks['links']['kill']))
        embed.set_author(name=hgp.name, icon_url=hgp.avatar_url)
        embed.set_footer(text=f"{self.client.user.name}",icon_url=self.client.user.avatar_url)
        await ctx.reply(embed=embed)


    @commands.command()
    async def pat(self, ctx, member: discord.Member):
        hgp = member
        await ctx.message.add_reaction('👋')
        print(hgp)
        if(ctx.message.author == hgp or hgp == None):
            embed = discord.Embed(title=" ", description=f"{ctx.message.author.mention} pats themselves", colour=discord.Colour(0x00ffb7))
            embed.add_field(name="👋", value=f"{ctx.message.author.mention}.. i'll pat you :3")
            embed.set_image(url=choice(self.perks['links']['pats']))
        else:
            embed = discord.Embed(title=" ", description=f"{ctx.message.author.mention} pats {hgp.mention}", colour=discord.Colour(0x00ffb7))
            embed.set_image(url=choice(self.perks['links']['pats']))
        embed.set_author(name=hgp.name, icon_url=hgp.avatar_url)
        embed.set_footer(text=f"{self.client.user.name}",
                        icon_url=self.client.user.avatar_url)
        await ctx.reply(embed=embed)


    @commands.command()
    async def sike(self, ctx, *qlink):
        try:
            link = ctx.message.attachments[0].url
        except:
            link = queryToName(qlink)
        if(ctx.message.guild == None):
            await ctx.reply("This is a dm tho? try it in a server m8")
        else:
            if(link == ""):
                try:
                    await ctx.reply(str(self.bruhs.find_one({"guild": ctx.message.author.id})['link']))
                except:
                    embed = discord.Embed(color=0x00ff00)
                    embed.add_field(name="No Sike! found",
                                    value=f"add sike {command_prefix}sike <value> ; Value can be Link , Text  ...", inline=False)
                    embed.set_footer(text=f" {self_name} {version}", icon_url=self_avatar)
                    await ctx.message.channel.send(embed=embed)
            else:
                if(self.bruhs.find_one({"guild": ctx.message.author.id}) == None):
                    dbStore = {
                        "guild": ctx.message.author.id,
                        "link": link
                    }
                    self.bruhs.insert_one({"guild": ctx.message.author.id}, dbStore)
                else:
                    dbStore = {
                        "guild": ctx.message.author.id,
                        "link": link
                    }
                    self.bruhs.replace_one({"guild": ctx.message.author.id}, dbStore)
                if(self.bruhs.find_one({"guild": ctx.message.author.id}) == None):
                    dbStore = {
                        "guild": ctx.message.author.id,
                        "link": link
                    }
                    self.bruhs.insert_one({"guild": ctx.message.author.id}, dbStore)
                else:
                    dbStore = {
                        "guild": ctx.message.author.id,
                        "link": link
                    }
                    self.bruhs.replace_one({"guild": ctx.message.author.id}, dbStore)
                embed = discord.Embed(color=0x00ff00)
                embed.add_field(name="Sike! Updated",
                                value="Sike! has been sucessfully updated", inline=False)
                embed.set_footer(text=f" {self_name} {version}", icon_url=self_avatar)
                await ctx.message.channel.send(embed=embed)  
    
    @commands.command()
    async def bruh(self,ctx, *qlink):
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
                    embed.set_footer(text=f" {self_name} {version}", icon_url=self_avatar)
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
                embed.set_footer(text=f" {self_name} {version}", icon_url=self_avatar)
                await ctx.message.channel.send(embed=embed)

        
    
def setup(bot):
    bot.add_cog(InteractionsMixin(bot))
