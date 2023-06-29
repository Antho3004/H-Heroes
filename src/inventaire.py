import discord
from discord.ext import commands
import sqlite3

connection = sqlite3.connect("HallyuHeroes.db")
cursor = connection.cursor()

class Inventaire(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def inventaire(self, ctx):
        user = ctx.author

        cursor.execute("SELECT * FROM user_inventaire WHERE user_id = ?", (str(user.id),))
        result = cursor.fetchone()

        if result is not None:
            nombre_de_cartes = result[3]
            cartes = result[4].split(", ") if result[4] else []
        else:
            nombre_de_cartes = 0
            cartes = []

        if nombre_de_cartes == 0:
            await ctx.send("Votre inventaire est vide.")
        else:
            embed = discord.Embed(title=f"Inventaire de {user.name}", color=discord.Color.green())
            embed.add_field(name="Nombre de cartes", value=str(nombre_de_cartes), inline=False)
            embed.add_field(name="Cartes", value=", ".join(cartes), inline=False)

            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Inventaire(bot))
