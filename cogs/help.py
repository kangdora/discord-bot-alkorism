import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="도움말", aliases=["help", "도움"])
    async def help(self, ctx):
        await ctx.send("도움말")