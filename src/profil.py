import discord
from discord.ext import commands
import sqlite3

connection = sqlite3.connect("HallyuHeroes.db")
cursor = connection.cursor()

class Profil(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def profil(self, ctx):
        user = ctx.author

        cursor.execute("SELECT * FROM user_data WHERE user_id = ?", (str(user.id),))
        result = cursor.fetchone()

        if result is not None:
            description = result[1]
            argent = result[2]
            nombre_de_cartes = result[3]
            carte_favori = result[4]
        else:
            description = "Bienvenue sur mon profil !"
            argent = 0
            nombre_de_cartes = 0
            carte_favori = ""

        embed = discord.Embed(title=f"Profil de {user.name}", description=description, color=discord.Color.blue())
        embed.add_field(name="Argent", value=str(argent), inline=False)
        embed.add_field(name="Nombre de cartes", value=str(nombre_de_cartes), inline=False)
        embed.add_field(name="Carte favorite", value=carte_favori, inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def description(self, ctx, *, new_description):
        user = ctx.author

        cursor.execute("SELECT * FROM user_data WHERE user_id = ?", (str(user.id),))
        result = cursor.fetchone()

        if result is not None:
            cursor.execute("UPDATE user_data SET description = ? WHERE user_id = ?", (new_description, str(user.id)))
        else:
            cursor.execute("INSERT INTO user_data VALUES (?, ?, ?, ?, ?)", (str(user.id), new_description, 0, 0, ""))

        connection.commit()

        await ctx.send("**La description a été mise à jour avec succès !**")

async def setup(bot):
    await bot.add_cog(Profil(bot))
