from imports import *

class OnMessageHandler(commands.Cog):
    client = None
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        if message.content.startswith("hello"):
            await message.channel.send("Hello!")

class CoreCommands(commands.Cog):
    client = None
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"> Latency {round(self.client.latency * 1000)}ms")
    
    

    