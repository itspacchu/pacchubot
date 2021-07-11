from ..__imports__ import *
from ..settings import *
from .discord_init import DiscordInit

Discord_init_Color = 0xffbb54

class InteractionsMixin(DiscordInit, commands.Cog):
    
    @commands.command(aliases=['av', 'pic', 'dp'])
    async def avatar(self, ctx, member: discord.Member = None):
        """

        """
        hgp = member
        url_link = None
        await ctx.message.add_reaction('🙄')
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
        
        await ctx.send(embed=embed, components=[[
            Button(style=ButtonStyle.green, label="Cartoonize"),
            Button(style=ButtonStyle.blue, label="Distort"),
        ],])
        while True:
            res = await self.client.wait_for("button_click", timeout=100)
            if(res.channel == ctx.channel):
                if(await ButtonProcessor(ctx,res,"Cartoonize")):
                    await ctx.invoke(self.client.get_command('cartoonize'), attachedImg=url_link)
                elif(await ButtonProcessor(ctx, res, "Distort")):
                    await ctx.invoke(self.client.get_command('distortion'), attachedImg=url_link)
        
    @commands.command(aliases=['gb'])
    async def guild_banner(self, ctx, member: discord.Member = None):
        """

        """
        hgp = member
        await ctx.message.add_reaction(Emotes.PACEXCLAIM)
        try:
            embed = discord.Embed(title="", colour=find_dominant_color(ctx.message.guild.banner_url))
            embed.set_image(url=ctx.message.guild.banner_url)
        except:
            embed = discord.Embed(title="Server Doesn't have a banner", colour=0xff2020)
        await better_send(ctx, embed=embed)
    
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
        await ctx.send(embed=embed)


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
        await ctx.send(embed=embed)

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
        await ctx.send(embed=embed)


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
        await ctx.send(embed=embed)


    @commands.command(aliases=['sk'])
    async def sike(self, ctx, *qlink):
        try:
            link = ctx.message.attachments[0].url
        except:
            link = queryToName(qlink)
        if(False):
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
    
    @commands.command(aliases=['br'])
    async def bruh(self,ctx, *qlink):
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
        self.MiscCollection.find_one_and_update({'_id': ObjectId(
            "60be497c826104950c8ea5d6")}, {'$inc': {'bruhs_delivered': 1}})
    
    @commands.command(aliases=['vs','vemb'])
    async def vidembed(self, ctx, *qlink):
        try:
            if(len(qlink) <= 1):
                raise IndexError("There should be a string url")
            await ctx.message.add_reaction('🎥')
            link_encoded_safe = quote(queryToName(qlink[:1]), safe='')
            try:
                title = quote(queryToName(qlink[1:]), safe='')
            except:
                title = f"Video by {ctx.message.author.mention}"
            full_url = "http://api.itspacchu.tk/vidembed?vsrc="+link_encoded_safe + "&title=" + title
            await ctx.message.channel.send(full_url)
        except IndexError:
            await ctx.message.add_reaction(Emotes.PACEXCLAIM)
            embed = discord.Embed(title="Video URL to Discord Embed", colour=discord.Colour(
                0x365eff), description=f"```{self.pre}vs [link to .mp4/.webm video]``` send an embed with .mp4 or .webm videos unrestricted \n Want to upload video > 8MB use the buttons below (FOSS)")
            await ctx.send(embed=embed, components=[[
                Button(style=ButtonStyle.URL,label="Transfer.sh", url="https://transfer.sh/"),
            ],])
        
 
def setup(bot):
    bot.add_cog(InteractionsMixin(bot))
