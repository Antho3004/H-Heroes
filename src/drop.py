import discord
from discord.ext import commands
import sqlite3
import random

connection = sqlite3.connect("HallyuHeroes.db")
cursor = connection.cursor()

class Drop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
        self.cartes_preferees = {
            307595556325425174: ["Kim Lip", "Nana", "B.I"],  # Antho
            403661101385908225: ["Lisa", "Minnie", "Jackson Wang", "Jackson"],  # Royal
            820035016242757653: ["Chanyeol", "Suho", "Woosung"],  # Kelly
            154322614515531776: ["Yena", "ChungHa", "Momo"],  # Zmix
            757723242763911300: ["Kazuha", "Julie", "Xiaoting"],  # Koro
            297758951230144513: ["Chaewon", "Winter", "Haerin"],  # Vision
            396221256715862026: ["Gahyeon", "Suzy", "Bona"],  # Rayleigh
            906220412919246898: ["Sana", "Sumin", "Jihyo"],  # Roswel
            304193355141873666: ["Hani", "Siwon", "Max Changmin"],  # Walpole
            929379626558586910: ["Hui", "Mingi", "Yeosang"],  # Unnilie
            254635682184560641: ["Ryujin", "Winter", "Taemin"] # Osi
            }  

    @commands.command()
    #@commands.cooldown(1, 300, commands.BucketType.user)
    async def drop(self, ctx):
        user_id = ctx.author.id

        # Définir les pourcentages de drop en fonction de la rareté
        rarity_drop_rates = {
            "C": 40,   # 40% pour les cartes communes (Common)
            "U": 30,   # 30% pour les cartes peu communes (Uncommon)
            "R": 15,   # 15% pour les cartes rares (Rare)
            "E": 10,   # 10% pour les cartes épiques (Epic)
            "L": 5     # 5% pour les cartes légendaires (Legendary)
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
            cursor.execute("UPDATE user_data SET argent = argent + ? WHERE user_id = ?", (500, str(user_id)))
            connection.commit()

            embed = discord.Embed(title=f"**Compensation**", description=f"Sorry {ctx.author.mention}\nAs I do not understand the bug you received **{500}** <:HCoins:1134169003657547847> !", color=discord.Color.green())

            await ctx.send(embed=embed)

        # Requête pour vérifier s'il y a des cartes disponibles de la rareté déterminée
        cursor.execute("SELECT code_card FROM cards WHERE rarete = ?", (rarity))
        available_cards = cursor.fetchall()

        if not available_cards:
            await ctx.send("Si vous voyez ce message ça veut dire que c'est pas normal")
            return

        # Requête pour obtenir une carte aléatoire de la rareté déterminée
        cursor.execute("SELECT code_card, nom, groupe, version, image_url, event FROM cards WHERE rarete = ? ORDER BY RANDOM() LIMIT 1", (rarity,))
        result = cursor.fetchone()

        if not result:
            await ctx.send("erreur 3.")
            return

        code_card, card_name, groupe, version, url_image, event = result

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
                "INSERT INTO user_inventaire (code_card, user_id, groupe, nom, rarete, version, chant, dance, rap, acting, modeling, image_url, event) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (code_card, user_id, groupe, card_name, rarity, version, chant, dance, rap, acting, modeling, url_image, event)
            )
            connection.commit()

            # Get the corresponding rarity emoji based on the event
            if event and event.lower() == 'xmas 2023':
                rarity_emojis = {
                    "U": "<:xmas_boot:1183911398661693631>",
                    "L": "<:xmas_hat:1183911360808112160>"
                }
            elif event and event.lower() == 'new year 2024':
                rarity_emojis = {
                    "R": "<:NY_Confetti:1185996235551805470>",
                    "L": "<:NY_Fireworks:1185996232477384808>"
                }
            else:
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

            # Vérifier si la carte dropée est la carte préférée d'un joueur
            players_with_favorite_card = []
            bonus_amount = 5000
            for player_id, favorite_cards in self.cartes_preferees.items():
                if card_name.lower() in favorite_cards.lower():
                    players_with_favorite_card.append(player_id)
                    # Donner le bonus d'argent au joueur qui a dropé la carte préférée
                    print(player_id)
                    cursor.execute("UPDATE user_data SET argent = argent + ? WHERE user_id = ?", (bonus_amount, user_id))
                    connection.commit()

            # Envoyer un message au joueur qui a dropé la carte préférée
            if players_with_favorite_card:
                players_mentions = ", ".join([f"<@{player_id}>" for player_id in players_with_favorite_card])
                embed_bonus = discord.Embed(
                    title="**Bonus**",
                    description=f"Congratulations {ctx.author.mention}\nYou received a bonus of **{bonus_amount}** <:HCoins:1134169003657547847> for dropping the UB of {players_mentions}.",
                    color=discord.Color.gold()
                )
                await ctx.send(embed=embed_bonus)

async def setup(bot):
    await bot.add_cog(Drop(bot))