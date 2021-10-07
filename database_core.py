from imports import *
from pymongo import MongoClient

# All Database Required Functions are here

mongo_url = f"mongodb+srv://{os.environ['MONGO_INITDB_ROOT_USERNAME']}:{os.environ['MONGO_INITDB_ROOT_PASSWORD']}@{os.environ['MONGO_HOST']}"
mongo_client = MongoClient(mongo_url)
db = mongo_client['PacchuSlave']


class DatabaseHandler(commands.Cog):
    client = None
    bruhs = db['bruh']
    MemberTaunt = db['memberTaunt']
    def __init__(self, client):
        self.client = client  
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        qq = message.content.lower().split(' ')[0]
        try:
            query = {'search': qq}
            match = self.MemberTaunt.find_one(query)['taunt']
            await message.channel.send(match)
        except:
            pass
    
    @commands.command(aliases=['br'])
    async def bruh(self, ctx, * ,link=None):
        try:
            link = ctx.message.attachments[0].url
        except:
            pass

        if(ctx.message.guild == None):
            await ctx.reply("> This is Direct Message m8")
        else:
            if(link == None):
                try:
                    await ctx.reply(str(self.bruhs.find_one({"guild": ctx.message.guild.id})['link']))
                except:
                    embed = nextcord.Embed(color=0x00ff00)
                    embed.add_field(name="No Bruh found",value=f"Consider adding Bruh using {command_prefix}Bruh <value> ; Value can be Link , Text  ...", inline=False)
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
                embed = nextcord.Embed(color=0x00ff00)
                embed.add_field(name="Database Updated", value="Bruh has been sucessfully updated", inline=False)
                await ctx.message.channel.send(embed=embed)