import discord
from discord.ext import commands
import sqlite3

connection = sqlite3.connect("HallyuHeroes.db")
cursor = connection.cursor()

class View(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def view(self, ctx, code_card: str):
        user = ctx.author

        # Vérifier si l'utilisateur possède la carte
        cursor.execute("SELECT * FROM user_inventaire WHERE user_id = ? AND code_card = ?", (user.id, code_card))
        card_data = cursor.fetchone()
        
        if not card_data:
            await ctx.send("Vous ne possédez pas cette carte.")
            return

        # Extraire les informations de la carte
        card_code, nom, groupe, version, chant, dance, rap, acting, modeling = card_data

        # Créer l'embed pour afficher les détails de la carte
        embed = discord.Embed(title="Détails de la carte", color=discord.Color.blue())
        embed.add_field(name="Code", value=card_code, inline=True)
        embed.add_field(name="Nom", value=nom, inline=True)
        embed.add_field(name="Groupe", value=groupe, inline=True)
        embed.add_field(name="Version", value=version, inline=True)
        embed.add_field(name="Chant", value=chant, inline=True)
        embed.add_field(name="Danse", value=dance, inline=True)
        embed.add_field(name="Rap", value=rap, inline=True)
        embed.add_field(name="Acting", value=acting, inline=True)
        embed.add_field(name="Modeling", value=modeling, inline=True)

        await ctx.send(embed=embed)

    @commands.command()
    async def card(self, ctx, code_card: str):
        await self.view(ctx, code_card)  # Appeler la méthode 'view' pour afficher les détails de la carte


async def setup(bot):
    await bot.add_cog(View(bot))
