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

        cursor.execute("SELECT COUNT(*) FROM user_inventaire WHERE user_id = ?", (str(user.id),))
        count = cursor.fetchone()[0]

        if count > 0:
            cursor.execute("SELECT code_card, nom, groupe, rarete FROM user_inventaire WHERE user_id = ?", (str(user.id),))
            result = cursor.fetchall()

            embed = discord.Embed(title=f"Inventaire de {user.name}", color=discord.Color.green())
            for row in result:
                code_card = row[0]
                nom = row[1]
                groupe = row[2]
                rarete = row[3]
                embed.add_field(name=f"{code_card}", value=f"Nom : {nom}\nGroupe : {groupe}\nRareté : <:C_:1107771999490686987>", inline=False) #changer le code par la rarete adéquate si C = <:C_:1107771999490686987>, U = ...

            embed.set_footer(text=f"Nombre total de cartes : {count}")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=f"Inventaire de {user.name}", description="Votre inventaire est vide.", color=discord.Color.red())
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Inventaire(bot))