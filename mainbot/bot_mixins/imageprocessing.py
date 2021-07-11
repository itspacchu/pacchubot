from discord import member
from mainbot.core.injectPayload import downloadFileFromUrl,distortion_new
from ..__imports__ import *
from ..settings import *
from .discord_init import DiscordInit
import time
from bs4 import BeautifulSoup
from random import choice

class ImageProcessingMixin(DiscordInit, commands.Cog):
    @commands.command(aliases=['ic', 'cartoon'])
    async def cartoonize(self,ctx, member: discord.Member = None,attachedImg=None):
        filname = str(round(time.time()))
        attachment_url = await unified_imagefetcher(ctx=ctx,member=member,attachedImg=attachedImg)
        downloadFileFromUrl(attachment_url, filname)
        s = requests.Session()
        url = "https://cartoonize-lkqov62dia-de.a.run.app/cartoonize"
        with open(str(filname + '.png'), 'rb') as f:
            r = s.post(url, files={'image': f})
        soup = BeautifulSoup(r.text, 'html.parser')
        dlink = soup.find_all('a')[0]['href']
        downloadFileFromUrl(dlink, filname)
        s.close()
        file = discord.File(filname + '.png', filename="cartoonize.png")
        embed = discord.Embed(color=find_dominant_color(filname + '.png',local=True))
        embed.set_image(url="attachment://cartoonize.png")
        embed.set_footer(text=" ")
        try:
            await ctx.send(file=file, embed=embed)
            await asyncio.sleep(1)
        except:
            pass
        await asyncio.sleep(1)
        os.remove(filname + '.png')
        self.MiscCollection.find_one_and_update({'_id': ObjectId("60be497c826104950c8ea5d6")}, {'$inc': {'images_cartoonized': 1}})

    @commands.command(aliases=['idh', 'distort-help'])
    async def distortion_help(self,ctx):
        embed = discord.Embed(title="Image Distortion", colour=discord.Colour(0xff7e2e), description=f"```{self.pre}id @mention/file``` attach an image or @mention someone to get their dp")
        embed.set_image(
            url="https://raw.githubusercontent.com/itspacchu/pacchubot/master/images/helper.png")
        await ctx.send(embed=embed)
    
    @commands.command(aliases=['ich', 'cartoonize-help'])
    async def cartoonize_help(self,ctx):
        embed = discord.Embed(title="Image Cartoonization", colour=discord.Colour(0xff67aa), description=f"```{self.pre}ic @mention/file``` attach an image or @mention someone to get their dp")
        
        embed.set_image(url="https://raw.githubusercontent.com/itspacchu/pacchubot/master/images/cartoonizehelp.png")
        await ctx.send(embed=embed)

    @commands.command(aliases=['id', 'distort'])
    async def distortion(self,ctx,member:discord.Member=None,attachedImg=None):
        choix = choice(range(len(distortionTypes)))
        try:
            filname = str(round(time.time()))
            attachment_url = await unified_imagefetcher(ctx=ctx, member=member, attachedImg=attachedImg)
            async with ctx.typing():
                downloadFileFromUrl(attachment_url, filname)
                Image.fromarray(distortion_new(filname + '.png', choice(distortionTypes))).convert('RGB').save(filname + '.png')
                file = discord.File(filname + '.png', filename="distortedImage.png")
                embed = discord.Embed(color=find_dominant_color(filname + '.png',local=True))
                embed.set_image(url="attachment://distortedImage.png")
            try:
                await ctx.send(file=file, embed=embed)
                await asyncio.sleep(1)
            except:
                pass
            os.remove(filname + '.png')
            self.MiscCollection.find_one_and_update({'_id': ObjectId("60be497c826104950c8ea5d6")}, {'$inc': {'images_distorted': 1}})
        except Exception as e:
            await ctx.send(f"GIFs aren't working ;-;```{self.pre}idh\n{e}```")
            return
            
        
        


def setup(bot):
    bot.add_cog(ImageProcessingMixin(bot))
