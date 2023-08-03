import discord
from discord.ext import commands
import sqlite3
import random
import datetime

connection = sqlite3.connect("HallyuHeroes.db")
cursor = connection.cursor()

class Work(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 1800, commands.BucketType.user)
    async def work(self, ctx):
        user = ctx.author

        cursor.execute("SELECT * FROM user_data WHERE user_id = ?", (str(user.id),))
        result = cursor.fetchone()

        montant = random.randint(10, 200)

        if result is not None:
            cursor.execute("UPDATE user_data SET argent = argent + ? WHERE user_id = ?", (montant, str(user.id)))
        else:
            cursor.execute("INSERT INTO user_data VALUES (?, ?, ?, ?, ?)", (str(user.id), "", montant, 0, ""))

        connection.commit()

        embed = discord.Embed(title=f"**WORK**", description=f"You have earned {montant} <:HCoins:1134169003657547847> from your last job!", color=discord.Color.green())
        await ctx.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            seconds = error.retry_after
            minutes, seconds = divmod(seconds, 60)
            hours, minutes = divmod(minutes, 60)
            message = f"Please wait **{int(hours)} hours, {int(minutes)} minutes, and {int(seconds)} seconds**"
            
            embed = discord.Embed(title="Cooldown", description=message, color=discord.Color.red())
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Work(bot))
