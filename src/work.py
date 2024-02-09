import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
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
            await ctx.send(embed=embed)
            return False

    return commands.check(predicate)

# Fonction pour formater l'argent
def format_money(money):
    return "{:,}".format(money).replace(",", " ")

# Fonction de récompense hebdomadaire
async def weekly_reward():
    # Récupérer tous les utilisateurs
    cursor.execute("SELECT user_id, work FROM user_data")
    users = cursor.fetchall()

    # Parcourir tous les utilisateurs
    for user_id, work_count in users:
        reward = 0
        if work_count >= 300:
            reward = 100000
        elif 250 <= work_count <= 299:
            reward = 70000
        elif 200 <= work_count <= 249:
            reward = 50000
        elif 150 <= work_count <= 199:
            reward = 30000
        elif 100 <= work_count <= 149:
            reward = 20000
        elif 50 <= work_count <= 99:
            reward = 10000
        elif 10 <= work_count <= 49:
            reward = 5000

        # Mettre à jour l'argent de l'utilisateur
        cursor.execute("UPDATE user_data SET argent = argent + ? WHERE user_id = ?", (reward, user_id))

    # Réinitialiser le compteur de travail pour tous les utilisateurs
    cursor.execute("UPDATE user_data SET work = 0")
    connection.commit()

class Work(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler()
        self.scheduler.add_job(weekly_reward, trigger="cron", day_of_week="fri", hour=18, minute=00, second=0)
        self.scheduler.start()

    def cog_unload(self):
        self.scheduler.shutdown()

    @commands.command(aliases=['w'])
    @has_favorite_card()
    @commands.cooldown(1, 1200, commands.BucketType.user)
    async def work(self, ctx):
        user = ctx.author

        # Increment the 'work' column in the 'user_data' table
        cursor.execute("UPDATE user_data SET work = work + 1 WHERE user_id = ?", (str(user.id),))
        connection.commit()

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
        updated_formatted_amount = format_money(updated_amount)

        embed = discord.Embed(title=f"{user.name} - **WORK**", description=f"You have earned **{montant}** <:HCoins:1134169003657547847> from your last job!\n\nNew balance : **{updated_formatted_amount}** <:HCoins:1134169003657547847>", color=discord.Color.green())
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Work(bot))
