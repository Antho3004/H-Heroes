import discord
from discord.ext import commands
import sqlite3

connection = sqlite3.connect("HallyuHeroes.db")
cursor = connection.cursor()

class Preview(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def preview(self, ctx, code_card: str):
        user = ctx.author

        cursor.execute("SELECT * FROM cards WHERE code_card = ?", (code_card,))
        card_data = cursor.fetchone()

        # Extraire les informations de la carte
        card_code, groupe, nom, rarete, version, chant, dance, rap, acting, modeling, image_url, event = card_data

        # Créer l'embed pour afficher les détails de la carte
        embed = discord.Embed(title="PREVIEW CARD", description=f"**NAME** : {nom}\n**GROUP** : {groupe}\n**VERSION** : {version}" ,color=discord.Color.blue())

        # Vérifier si l'événement existe et l'ajouter à l'embed si c'est le cas
        if event:
            embed.add_field(name="", value=f"**EVENT** : {event}", inline=False)
        
        # Ajouter l'image à l'embed
        embed.set_image(url=image_url)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Preview(bot))
