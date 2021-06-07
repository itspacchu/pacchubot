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
        embed = discord.Embed(title="Image Cartoonization", colour=discord.Colour(0xff67aa), description=f"```{self.pre}.ic @mention/file``` attach an image or @mention someone to get their dp")
        
        embed.set_image(url="https://raw.githubusercontent.com/itspacchu/pacchubot/master/images/cartoonizehelp.png")
        await ctx.send(embed=embed)

    @commands.command(aliases=['id', 'distort'])
    async def distortion(self,ctx,member:discord.Member=None):
        choix = choice(range(len(distortionTypes)))
        try:
            if(member == None):
                member = ctx.message.author
            filname = str(round(time.time()))
            await ctx.message.add_reaction('🔨')
            try:
                attachment_url = ctx.message.attachments[0].url
                await ctx.message.add_reaction('⏬')
                await better_send(ctx, "> Processing will take few seconds..")
            except:
                try:
                    hgp = member
                    await ctx.message.add_reaction('🎭')
                    if(ctx.message.author == hgp or hgp == None):
                        attachment_url = ctx.message.author.avatar_url
                    else:
                        attachment_url = hgp.avatar_url
                    await better_send(ctx, "> Getting User's avatar")
                except:
                    await better_send(ctx, "I think something went wrong!")
                    return None

            downloadFileFromUrl(attachment_url, filname)
            img2distort = Image.open(filname + '.png')
            dimg = distortImage(img2distort,distortionTypes[choix])
            dimg[0].save(filname + '.png')
            file = discord.File(filname + '.png', filename="distortedImage.png")
            embed = discord.Embed(color=find_dominant_color(filname + '.png',local=True))
            embed.set_image(url="attachment://distortedImage.png")
            if(dimg[1] != None):
                embed.set_footer(text=dimg[1])
            else:
                embed.set_footer(text=" ")
            try:
                await ctx.send(file=file, embed=embed)
                await asyncio.sleep(1)
            except:
                pass
            os.remove(filname + '.png')
            self.MiscCollection.find_one_and_update({'_id': ObjectId("60be497c826104950c8ea5d6")}, {'$inc': {'images_distorted': 1}})
        except IndexError:
            await ctx.send(f"Something seemed to be wrong \n use help```{self.pre}idh```")
            
        
        


def setup(bot):
    bot.add_cog(ImageProcessingMixin(bot))
