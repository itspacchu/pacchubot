from imports import *
from utilityhandler import *

class ImageHandler(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['av','dp'])
    async def avatar(self, ctx, member: nextcord.Member = None):
        hgp = member
        url_link = None
        await ctx.message.add_reaction('🙄')
        if(ctx.message.author == hgp or hgp == None):
            embed = nextcord.Embed(
                title="OwO", description=f"{ctx.message.author.mention} steals ...wait thats your OWN", colour=find_dominant_color(ctx.message.author.avatar.url))
            embed.set_image(url=ctx.message.author.avatar.url)
            url_link = ctx.message.author.avatar.url
        else:
            embed = nextcord.Embed(
                title="Swong..!", description=f"{ctx.message.author.mention} yeets {hgp.mention}'s profile pic 👀'", colour=find_dominant_color(hgp.avatar.url))
            embed.set_image(url=hgp.avatar.url)
            url_link = hgp.avatar.url
        try:
            embed.set_author(name=hgp.name, icon_url=hgp.avatar.url)
        except:
            embed.set_author(name=ctx.message.author.name,
                             icon_url=ctx.message.author.avatar.url)
        embed.set_footer(text=f"{self.client.user.name}",
                         icon_url=self.client.user.avatar.url)
        await ctx.send(embed=embed)
        

    @commands.command(aliases=['ic', 'cartoon'])
    async def cartoonize(self,ctx, member: nextcord.Member = None,attachedImg=None):
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
        file = nextcord.File(filname + '.png', filename="cartoonize.png")
        embed = nextcord.Embed(color=find_dominant_color(filname + '.png',local=True))
        embed.set_image(url="attachment://cartoonize.png")
        embed.set_footer(text=" ")
        try:
            await ctx.send(file=file, embed=embed)
            await asyncio.sleep(1)
        except:
            pass
        await asyncio.sleep(1)
        os.remove(filname + '.png')