from discord import member
from mainbot.core.injectPayload import distortImage, downloadFileFromUrl
from ..__imports__ import *
from ..settings import *
from .discord_init import DiscordInit
import time
from bs4 import BeautifulSoup
from random import choice

class ImageProcessingMixin(DiscordInit, commands.Cog):
    @commands.command(aliases=['ic', 'cartoon'])
    async def cartoonize(self,ctx, member: discord.Member = None):
        filname = str(round(time.time()))
        await ctx.message.add_reaction('🖌')
        try:
            attachment_url = ctx.message.attachments[0].url
            await ctx.message.add_reaction('⏬')
            await better_send(ctx, "Processing will take few seconds..")
        except:
            try:
                hgp = member
                await ctx.message.add_reaction('🎭')
                if(ctx.message.author == hgp or hgp == None):
                    attachment_url = ctx.message.author.avatar_url
                else:
                    attachment_url = hgp.avatar_url
                await better_send(ctx, "Getting User's avatar")
            except:
                await better_send(ctx, "I think something went wrong!")
                return None

        downloadFileFromUrl(attachment_url, filname)
        s = requests.Session()
        url = "https://cartoonize-lkqov62dia-de.a.run.app/cartoonize"
        with open(str(filname + '.png'), 'rb') as f:
            r = s.post(url, files={'image': f})
        soup = BeautifulSoup(r.text, 'html.parser')
        dlink = soup.find_all('a')[0]['href']
        
        downloadFileFromUrl(dlink, filname)
        s.close()
        file = discord.File(filname + '.png',filename="cartoonized_img.png")
        embed = discord.Embed(color=find_dominant_color(dlink))
        embed.set_image(url="attachment://cartoonized_img.png")
        try:
            await ctx.send(file=file,embed=embed)
            await asyncio.sleep(1)
        except:
            pass
        os.remove(filname + '.png')

    @commands.command(aliases=['idh', 'distort-help'])
    async def distortion_help(self,ctx):
        embed = discord.Embed(title="Image Distortion", colour=discord.Colour(0xff7e2e), description=f"```{self.pre}id @mention/file``` attach an image or @mention someone to get their dp")
        embed.set_image(url="https://raw.githubusercontent.com/itspacchu/pacchubot/master/images/cartoonizehelp.png")
        await ctx.send(embed=embed)
    
    @commands.command(aliases=['ich', 'cartoonize-help'])
    async def cartoonize_help(self,ctx):
        embed = discord.Embed(title="Image Cartoonization", colour=discord.Colour(0xff67aa), description="```{self.pre}.ic @mention/file``` attach an image or @mention someone to get their dp")
        embed.set_image(url="https://raw.githubusercontent.com/itspacchu/pacchubot/master/images/helper.png")
        await ctx.send(embed=embed)

    @commands.command(aliases=['id', 'distort'])
    async def distortion(self,ctx,member:discord.Member==None,choix):
        if(choix == None):
            choix = choice(distortionTypes)
        else:
            choix = int(choix,10)
        try:
            if(member == None):
                ctx.message.author
            filname = str(round(time.time()))
            await ctx.message.add_reaction('🔨')
            try:
                attachment_url = ctx.message.attachments[0].url
                await ctx.message.add_reaction('⏬')
                await better_send(ctx, "Processing will take few seconds..")
            except:
                try:
                    hgp = member
                    await ctx.message.add_reaction('🎭')
                    if(ctx.message.author == hgp or hgp == None):
                        attachment_url = ctx.message.author.avatar_url
                    else:
                        attachment_url = hgp.avatar_url
                    await better_send(ctx, "Getting User's avatar")
                except:
                    await better_send(ctx, "I think something went wrong!")
                    return None

            downloadFileFromUrl(attachment_url, filname)
            img2distort = Image.open(filname + '.png')
            dimg = distortImage(img2distort,int(choix))
            dimg[0].save(filname + '.png')
            file = discord.File(filname + '.png', filename="distortedImage.png")
            embed = discord.Embed(color=find_dominant_color(filname + '.png',local=True))
            embed.set_image(url="attachment://distortedImage.png")
            if(dimg[1] != None):
                embed.set_footer(text=dimg[1])
            try:
                await ctx.send(file=file, embed=embed)
                await asyncio.sleep(1)
            except:
                pass
            os.remove(filname + '.png')
        except IndexError:
            await ctx.send(f"Something seemed to be wrong \n use help```{self.pre}idh```")
        
        


def setup(bot):
    bot.add_cog(ImageProcessingMixin(bot))
