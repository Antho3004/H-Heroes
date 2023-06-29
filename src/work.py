import discord
from discord.ext import commands
import sqlite3
import random

connection = sqlite3.connect("HallyuHeroes.db")
cursor = connection.cursor()

class Work(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
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

        await ctx.send(f"**Tu as gagné {montant} d'argent !**")

async def setup(bot):
    await bot.add_cog(Work(bot))
