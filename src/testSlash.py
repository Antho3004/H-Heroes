import discord
from discord.ext import commands
from discord_slash import SlashCommand
import sqlite3

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx):

async def setup(bot):
    await bot.add_cog(Test(bot))
