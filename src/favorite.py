import discord
from discord.ext import commands
import sqlite3

connection = sqlite3.connect("HallyuHeroes.db")
cursor = connection.cursor()

class Favorite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def favorite(self, ctx, code_card: str):
        user = ctx.author

        cursor.execute("SELECT code_card FROM user_inventaire WHERE user_id = ? AND code_card = ?", (user.id, code_card))
        card_favorite = cursor.fetchone()

        if card_favorite is not None:
            # Card found in user's inventory, update favorite card in user_data table
            cursor.execute("UPDATE user_data SET carte_favori = ? WHERE user_id = ?", (code_card, user.id))
            connection.commit()

            embed = discord.Embed(
                title="Carte favorite mise à jour",
                description=f"La carte **{code_card}** a été ajoutée comme carte favorite.",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        else:
            # Card not found in user's inventory
            embed = discord.Embed(
                title="Erreur",
                description="Vous ne possédez pas cette carte.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Favorite(bot))
