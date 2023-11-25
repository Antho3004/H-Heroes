import discord
from discord.ext import commands
import sqlite3

connection = sqlite3.connect("HallyuHeroes.db")
cursor = connection.cursor()

class Balance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def format_balance(self, balance):
        return "{:,}".format(balance).replace(",", " ")  # Using format method and then replacing commas with spaces

    @commands.command()
    async def bal(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        cursor.execute("SELECT argent FROM user_data WHERE user_id = ?", (str(user.id),))
        result = cursor.fetchone()

        if result is None:
            embed = discord.Embed(title=f"Balance of {user.name}", description=f"{user.mention} doesn't have any money yet.")
            await ctx.send(embed=embed)

        money = result[0]

        formatted_balance = self.format_balance(money)

        embed = discord.Embed(title=f"Balance of {user.name}", description=f"{user.mention} has **{formatted_balance}** <:HCoins:1134169003657547847>")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Balance(bot))
