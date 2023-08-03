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
    #@commands.cooldown(1, 1800, commands.BucketType.user)
    async def work(self, ctx):
        user = ctx.author

        cursor.execute("SELECT i.rarete FROM user_data AS u JOIN user_inventaire AS i ON u.carte_favori = i.code_card WHERE u.user_id = ?", (str(user.id),))
        result = cursor.fetchone()

        if result is not None:
            carte_rarete = result[0]
            if carte_rarete == "C":
                montant = random.randint(10, 100)
            elif carte_rarete == "U":
                montant = random.randint(100, 200)
            elif carte_rarete == "R":
                montant = random.randint(200, 300)
            elif carte_rarete == "E":
                montant = random.randint(300, 400)
            elif carte_rarete == "L":
                montant = random.randint(400, 500)
            else:
                embed = discord.Embed(title="**WORK**", description="You must choose a favourite card using the command `$fav or $favorite`", color=discord.Color.red())
                await ctx.send(embed=embed)
                return

            cursor.execute("UPDATE user_data SET argent = argent + ? WHERE user_id = ?", (montant, str(user.id)))
        else:
            embed = discord.Embed(title="**WORK**", description="You don't have a favorite card. Please choose one using the command `$fav or $favorite`", color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        connection.commit()

        embed = discord.Embed(title=f"**WORK**", description=f"You have earned **{montant}** <:HCoins:1134169003657547847> from your last job!", color=discord.Color.green())
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
