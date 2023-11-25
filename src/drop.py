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
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def drop(self, ctx):
        user_id = ctx.author.id

        # Définir les pourcentages de drop en fonction de la rareté
        rarity_drop_rates = {
            "C": 70,   # 40% pour les cartes communes (Common)
            "U": 30   # 30% pour les cartes peu communes (Uncommon)
            #"R": 15,   # 15% pour les cartes rares (Rare)
            #"E": 10,   # 10% pour les cartes épiques (Epic)
            #"L": 5     # 5% pour les cartes légendaires (Legendary)
        }

        # Calculer le pourcentage total de drop (100%)
        total_drop_rate = sum(rarity_drop_rates.values())
        
        # Obtenir un nombre aléatoire entre 1 et 100 pour déterminer la rareté
        drop_chance = random.randint(1, total_drop_rate + 1)
        

        # Déterminer la rareté de la carte en fonction du nombre aléatoire obtenu
        rarity = None
        for rarete, drop_rate in rarity_drop_rates.items():
            if drop_chance <= drop_rate:
                rarity = rarete
                break
            drop_chance -= drop_rate
        
        if not rarity:
            await ctx.send(rarity)
            return

        # Requête pour vérifier s'il y a des cartes disponibles de la rareté déterminée
        cursor.execute("SELECT code_card FROM cards WHERE rarete = ?", (rarity))
        available_cards = cursor.fetchall()

        if not available_cards:
            await ctx.send("Si vous voyez ce message ça veut dire que c'est pas normal")
            return

        # Requête pour obtenir une carte aléatoire de la rareté déterminée
        cursor.execute("SELECT code_card, nom, groupe, version, image_url FROM cards WHERE rarete = ? ORDER BY RANDOM() LIMIT 1", (rarity,))
        result = cursor.fetchone()

        if not result:
            await ctx.send("erreur 3.")
            return

        code_card, card_name, groupe, version, url_image = result

        # Incrémenter le numéro après le tiret
        code_card_parts = code_card.split("-")
        if len(code_card_parts) == 2:
            try:
                card_num = int(code_card_parts[1]) + 1
                code_card = f"{code_card_parts[0]}-{card_num}"
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
                    code_card = f"{code_card_parts[0]}-{card_num}"
                    existing_card = cursor.execute("SELECT code_card FROM user_inventaire WHERE code_card = ?", (code_card,)).fetchone()
                except ValueError:
                    pass

        # Modifier les colonnes chant, dance, rap, acting et modeling avec des valeurs aléatoires en fonction de la rareté
        chant = random.randint(0, 100)
        dance = random.randint(0, 100)
        rap = random.randint(0, 100)
        acting = random.randint(0, 100)
        modeling = random.randint(0, 100)

        if rarity == "U":
            chant = random.randint(100, 150)
            dance = random.randint(100, 150)
            rap = random.randint(100, 150)
            acting = random.randint(100, 150)
            modeling = random.randint(100, 150)
        elif rarity == "R":
            chant = random.randint(150, 200)
            dance = random.randint(150, 200)
            rap = random.randint(150, 200)
            acting = random.randint(150, 200)
            modeling = random.randint(150, 200)
        elif rarity == "E":
            chant = random.randint(200, 250)
            dance = random.randint(200, 250)
            rap = random.randint(200, 250)
            acting = random.randint(200, 250)
            modeling = random.randint(200, 250)
        elif rarity == "L":
            chant = random.randint(250, 300)
            dance = random.randint(250, 300)
            rap = random.randint(250, 300)
            acting = random.randint(250, 300)
            modeling = random.randint(250, 300)

        # Vérifier si la carte existe déjà dans la table user_inventaire
        existing_card = cursor.execute("SELECT code_card FROM user_inventaire WHERE code_card = ?", (code_card,)).fetchone()
        if existing_card:
            # Si la carte existe, rajouter un +1 et ne rien faire d'autre
            pass
        else:
            # Si la carte n'existe pas, l'ajouter à l'inventaire avec user_id à None
            cursor.execute(
                "INSERT INTO user_inventaire (code_card, user_id, groupe, nom, rarete, version, chant, dance, rap, acting, modeling, image_url) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (code_card, user_id, groupe, card_name, rarity, version, chant, dance, rap, acting, modeling, url_image)
            )
            connection.commit()

        # Get the corresponding rarity emoji
        rarity_emojis = {
            "C": "<:C_:1107771999490686987>",
            "U": "<:U_:1107772008193867867>",
            "R": "<:R_:1107772004410601553>",
            "E": "<:E_:1107772001747222550>",
            "L": "<:L_:1107772002690945055>"
        }

        rarity_emoji = rarity_emojis.get(rarity, "")  # Get the emoji for the corresponding rarity or an empty string if not found

        # Crée le titre de l'embed avec le nom de la carte, le groupe et la rareté
        title = f"**DROP**"

        # Crée le message à envoyer après avoir dropé la carte
        drop_message = f"Congratulations {ctx.author.mention}\nYou have dropped: [{groupe} {card_name} - {rarity_emoji} ] n° {code_card.split('-')[1]}\nCode : `{code_card}`"

        # Crée l'embed Discord avec le titre, le message et l'image de la carte
        embed = discord.Embed(title=title, description=drop_message)
        embed.set_image(url=url_image)

        # Envoie l'embed
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Drop(bot))