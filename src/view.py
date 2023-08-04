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
            embed = discord.Embed(title="", color=discord.Color.red())
            embed.add_field(name="You don't have this card", value="")
            await ctx.send(embed=embed)
            return

        # Extraire les informations de la carte
        user_id, card_code, groupe, nom, rarete, version, chant, dance, rap, acting, modeling, image_url, event = card_data

        # Créer l'embed pour afficher les détails de la carte
        embed = discord.Embed(title="CARD'S DETAILS", description=f"**CODE** : {code_card}\n**NAME** : {nom}\n**GROUP** : {groupe}\n**VERSION** : {version}\n" ,color=discord.Color.blue())
        embed.add_field(name="STATS", value=f":musical_note: **SING** : {chant}\n:dancer: **DANCE** : {dance}\n:microphone: **RAP** : {rap}\n:projector: **ACTING** : {acting}\n:kimono: **MODELING** : {modeling}", inline=True)

        # Vérifier si l'événement existe et l'ajouter à l'embed si c'est le cas
        if event:
            embed.add_field(name="", value=f"**EVENT** : {event}", inline=False)
        
        # Ajouter l'image à l'embed
        embed.set_image(url=image_url)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(View(bot))
