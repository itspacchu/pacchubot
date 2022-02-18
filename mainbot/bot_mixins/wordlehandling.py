from ast import alias
from ..__imports__ import *
from ..settings import *
from .discord_init import DiscordInit
from datetime import datetime

class WordleInstance():
    word = ""
    count = 0
    MAX_PLAYABLE = 5
    last_played:datetime = None

    def __init__(self,word,MAX_PLAYABLE=5,last_played=None,count=0):
        self.word = word
        self.MAX_PLAYABLE = MAX_PLAYABLE
        self.last_played = datetime.now()

    def playable(self):
        return self.count <= (self.MAX_PLAYABLE)

    def reset(self):
        self.count = 0

    def process_guess(self,guess):
        if(self.count <= self.MAX_PLAYABLE):
            if(len(guess) == len(self.word)):
                self.count += 1
                retStr = list("⬛"*len(self.word))
                inner_matcher = list(self.word)
                #perfect matches
                for i,char in enumerate(zip(guess,self.word)):
                    if(char[0] == char[1]):
                        retStr[i] = "🟩"
                        inner_matcher[i] = "$"
                        continue
                
                #yellow matches
                for i,char in enumerate(zip(guess,self.word)):
                    if(retStr[i] == "🟩"):
                        continue
                    elif((char[0] in inner_matcher)):
                        retStr[i] = "🟨"
                        inner_matcher[inner_matcher.index(char[0])] = "$"
                return "".join(retStr)
            else:
                return f"Not a valid guess. Word is {len(self.word)} letters long"
        else:
            return "You're outta guesses buddy"
        


class OnWordleHandler(DiscordInit, commands.Cog):
    client = None
    players = {}
    WORDLE_WORD = None
    WORDLE_MAX_PLAYABLE = 5

    def __init__(self, client):
        self.client = client
        super().__init__(client=client)

    @commands.command(alias=['wordleset'])
    async def setword(self, ctx, *, word):
        if(isItPacchu(str(ctx.author.id)) or ctx.author.guild_permissions.administrator):
            word = word.lower()
            try:
                self.wordleData.update_one({'server': str(ctx.guild.id)}, {'$set': {'word': word ,'count': 5}}, upsert=True)
                await ctx.send(f"> Wordle for **{ctx.guild.name}** updated on database")
                self.WORDLE_WORD = self.wordleData.find_one({"server": str(ctx.guild.id)})['word']
                self.WORDLE_MAX_PLAYABLE = self.wordleData.find_one({"server": str(ctx.guild.id)})['count']
            except:
                self.wordleData.insert_one({'server': str(ctx.guild.id), 'word': word , 'count': 5})
                await ctx.send(f"> Wordle for **{ctx.guild.name}** created on database")
        else:
            await ctx.send("SUDO* command")

    @commands.command(name="w", aliases=["wordle"])
    async def wordleHandlerFunction(self, ctx, *, word):
        word = word.lower()
        self.WORDLE_WORD = self.wordleData.find_one({"server": str(ctx.guild.id)})['word']
        self.WORDLE_MAX_PLAYABLE = self.wordleData.find_one({"server": str(ctx.guild.id)})['count']

        if(ctx.author.id not in self.players):
            self.players[ctx.author.id] = WordleInstance(self.WORDLE_WORD,self.WORDLE_MAX_PLAYABLE)
s

        if(self.players[ctx.author.id].playable()):
            await ctx.reply(f"|| {self.players[ctx.author.id].process_guess(word)} [{self.players[ctx.author.id].count}/{self.WORDLE_MAX_PLAYABLE}]||")
        else:
            await ctx.send(f"{ctx.author.mention} you're outta guesses buddy")
            self.players[ctx.author.id].reset()

def setup(bot):
    bot.add_cog(OnWordleHandler(bot))