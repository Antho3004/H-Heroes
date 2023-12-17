import discord
from discord.ext import commands
import sqlite3
import random
import datetime

connection = sqlite3.connect("HallyuHeroes.db")
cursor = connection.cursor()

# Custom check function to determine if the user has a favorite card
def has_favorite_card():
    async def predicate(ctx):
        user = ctx.author
        cursor.execute("SELECT i.rarete FROM user_data AS u JOIN user_inventaire AS i ON u.carte_favori = i.code_card WHERE u.user_id = ?", (str(user.id),))
        result = cursor.fetchone()

        if result is not None:
            return True
        else:
            embed = discord.Embed(title=f"{user.name} - **WORK**", description="You don't have a favorite card. Please choose one using the command `$fav or $favorite`", color=discord.Color.red())
            await ctx.send(embed=embed)  # Await the send() function here
            return False

    return commands.check(predicate)

class Work(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def format_money(self, money):
        return "{:,}".format(money).replace(",", " ")

    @commands.command()
    @has_favorite_card()  # Apply the custom check decorator
    @commands.cooldown(1, 1800, commands.BucketType.user)
    async def work(self, ctx):
        user = ctx.author

        cursor.execute("SELECT i.rarete FROM user_data AS u JOIN user_inventaire AS i ON u.carte_favori = i.code_card WHERE u.user_id = ?", (str(user.id),))
        result = cursor.fetchone()

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

        # Update user's money in the database
        cursor.execute("UPDATE user_data SET argent = argent + ? WHERE user_id = ?", (montant, str(user.id)))
        connection.commit()

        # Fetch the updated amount after the update
        cursor.execute("SELECT argent FROM user_data WHERE user_id = ?", (str(user.id),))
        updated_amount = cursor.fetchone()[0]
        uptated_formatted_amount = self.format_money(updated_amount)

        embed = discord.Embed(title=f"{user.name} - **WORK**", description=f"You have earned **{montant}** <:HCoins:1134169003657547847> from your last job!\n\nTotal balance : **{uptated_formatted_amount}** <:HCoins:1134169003657547847>", color=discord.Color.green())
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Work(bot))
