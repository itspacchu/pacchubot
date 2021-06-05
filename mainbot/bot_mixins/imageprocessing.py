from mainbot.core.injectPayload import downloadFileFromUrl
from ..__imports__ import *
from ..settings import *
from .discord_init import DiscordInit
import time
from bs4 import BeautifulSoup

class ImageProcessingMixin(DiscordInit, commands.Cog):
    @commands.command(aliases=['ic', 'cartoon'])
    async def cartoonize(self,ctx, member: discord.Member = None):
        filname = str(round(time.time()))
        await ctx.message.add_reaction('🖌')
        try:
            attachment_url = ctx.message.attachments[0].url
            await ctx.message.add_reaction('⏬')
            await better_send(ctx, "Processing take few seconds..")
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

def setup(bot):
    bot.add_cog(ImageProcessingMixin(bot))
