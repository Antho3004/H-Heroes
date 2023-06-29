import discord
from discord.ext import commands
import sqlite3
import random

connection = sqlite3.connect("HallyuHeroes.db")
cursor = connection.cursor()

class Drop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def drop(self, ctx):
        user_id = ctx.author.id
        # Requête pour obtenir une carte aléatoire
        cursor.execute("SELECT code_card, nom, groupe, rarete, version, chant, dance, rap, acting, modeling, image_url FROM cards ORDER BY RANDOM() LIMIT 1")
        result = cursor.fetchone()

        if not result:
            await ctx.send("Aucune carte n'est disponible.")
            return

        code_card, card_name, groupe, rarete, version, chant, dance, rap, acting, modeling, url_image = result

        # Incrémenter le numéro après le tiret
        code_card_parts = code_card.split("-")
        if len(code_card_parts) == 2:
            try:
                card_num = int(code_card_parts[1]) + 1
                code_card = f"{code_card_parts[0]}-{card_num:04d}"
            except ValueError:
                pass

        # Vérifier si le code_card existe déjà dans la table user_inventaire
        existing_card = cursor.execute("SELECT code_card FROM user_inventaire WHERE code_card = ?", (code_card,)).fetchone()
        while existing_card:
            # Incrémenter le numéro après le tiret
            code_card_parts = code_card.split("-")
            if len(code_card_parts) == 2:
                try:
                    card_num = int(code_card_parts[1]) + 1
                    code_card = f"{code_card_parts[0]}-{card_num:04d}"
                    existing_card = cursor.execute("SELECT code_card FROM user_inventaire WHERE code_card = ?", (code_card,)).fetchone()
                except ValueError:
                    pass

        # Modifier les colonnes chant, dance, rap, acting et modeling avec des valeurs aléatoires entre 1 et 100
        chant = random.randint(1, 100)
        dance = random.randint(1, 100)
        rap = random.randint(1, 100)
        acting = random.randint(1, 100)
        modeling = random.randint(1, 100)

        # Vérifier si la carte existe déjà dans la table user_inventaire
        existing_card = cursor.execute("SELECT code_card FROM user_inventaire WHERE code_card = ?", (code_card,)).fetchone()
        if existing_card:
            # Si la carte existe, rajouter un +1 et ne rien faire d'autre
            pass
        else:
            # Si la carte n'existe pas, l'ajouter à l'inventaire avec user_id à None
            cursor.execute(
                "INSERT INTO user_inventaire (code_card, user_id, groupe, nom, rarete, version, chant, dance, rap, acting, modeling) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (code_card, user_id, groupe, card_name, rarete, version, chant, dance, rap, acting, modeling)
            )
            connection.commit()

        # Crée le titre de l'embed avec le nom de la carte, le groupe et la rareté
        title = f"{card_name} [{groupe}] - Rareté : {rarete}"

        # Crée l'embed Discord avec le titre, l'image et les autres informations
        embed = discord.Embed(title=title)
        embed.set_image(url=url_image)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Drop(bot))
