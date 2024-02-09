import discord
from discord.ext import commands
import sqlite3
import random

connection = sqlite3.connect("HallyuHeroes.db")
cursor = connection.cursor()

class Daily(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
        self.cartes_preferees = {
            307595556325425174: [("Kim Lip", "LOONA"), ("Kim Lip", "ARTMS"), ("Nana", "EL7Z UP"), ("Nana", "Woo!ah!"), ("B.I", "SOLOISTS")],  #Antho
            403661101385908225: [("Lisa", "BLACKPINK"), ("Lisa", "SOLOISTS"), ("Minnie", "(G)I-DLE"), ("Jackson", "GOT7"), ("Jackson Wang", "SOLOISTS")], #Royal
            820035016242757653: [("Chanyeol", "EXO"), ("Chanyeol", "SOLOISTS"), ("Suho", "EXO"), ("Suho", "SOLOISTS"), ("Woosung", "The Rose"), ("Woosung", "SOLOISTS")],#Kelly
            154322614515531776: [("Yena", "IZ*ONE"), ("Yena", "SOLOISTS"), ("Chungha", "SOLOISTS"), ("Momo", "TWICE"), ("Momo", "MISAMO")], # Zmix
            757723242763911300: [("Kazuha", "Le sserafim"), ("Julie", "Kiss of life"), ("Xiaoting", "Kep1er")], # Koro
            297758951230144513: [("Chaewon", "Le sserafim"), ("Chaewon", "IZ*ONE"), ("Bae", "NMIXX"), ("Haerin", "Newjeans")], # Vision
            396221256715862026: [("Gahyeon", "Dreamcatcher"), ("Suzy", "MissA"), ("Suzy", "SOLOISTS"), ("Suzy", "SOLOIST"), ("Bona", "WJSN"), ("Bona", "WJSN The Black")], #Rayleigh
            906220412919246898: [("Sana", "Twice"), ("Sana", "MISAMO"), ("Sumin", "STAYC"), ("Jihyo", "TWICE")], # Roswel
            304193355141873666: [("Hani", "EXID"), ("Siwon", "Super Junior"), ("Max Changmin", "TVXQ"), ("Max Changmin", "SOLOISTS")], # Walpole
            929379626558586910: [("Hui", "Pentagon"), ("Mingi", "Ateez"), ("Yeosang", "Ateez")], # Unnilie
            254635682184560641: [("Winter", "aespa"), ("Winter", "GIRLS ON TOP"), ("Ryujin", "Itzy"), ("Taemin", "Shinee"), ("Taemin", "SOLOISTS")], # Osi
            629238375509000192: [("Yeojun", "TXT"), ("Junho", "2PM"), ("L","INFINITE")], # Lululionne
            559414465288863745: [("Lisa", "BLACKPINK"), ("Lisa", "SOLOISTS"), ("JIMIN", "BTS"), ("JIMIN", "SOLOISTS"), ("Hyunjin", "Stray kids")], # Akira
            374658090693427202: [("Dahyun", "TWICE"), ("SOOBIN", "TXT"), ("Felix", "Stray kids")], # Faeclyn
            } 
    
    def format_money(self, money):
        return "{:,}".format(money).replace(",", " ")

    @commands.command()
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daily(self, ctx):
        user_id = ctx.author.id

        # Générer un nombre aléatoire pour choisir entre carte (1) ou argent (2)
        reward_choice = random.randint(1, 2)

        if reward_choice == 1:
            # Récompense de carte
            # Définir les pourcentages de drop en fonction de la rareté
            rarity_drop_rates = {
                "C": 30,   # 30% pour les cartes communes (Common)
                "U": 25,   # 25% pour les cartes peu communes (Uncommon)
                "R": 20,   # 20% pour les cartes rares (Rare)
                "E": 15,   # 15% pour les cartes épiques (Epic)
                "L": 10    # 10% pour les cartes légendaires (Legendary)
            }

            # Calculer le pourcentage total de drop (100%)
            total_drop_rate = sum(rarity_drop_rates.values())

            # Obtenir un nombre aléatoire entre 1 et 100 pour déterminer la rareté
            drop_chance = random.randint(1, total_drop_rate)

            # Déterminer la rareté de la carte en fonction du nombre aléatoire obtenu
            rarity = None
            cumulative_chance = 0
            for rarete, drop_rate in rarity_drop_rates.items():
                cumulative_chance += drop_rate
                if drop_chance <= cumulative_chance:
                    rarity = rarete
                    break

            if not rarity:
                await ctx.send("La rareté n'est pas disponible.")
                return

            # Requête pour obtenir une carte aléatoire de la rareté déterminée
            cursor.execute("SELECT code_card, nom, groupe, version, image_url, event FROM cards WHERE rarete = ? ORDER BY RANDOM() LIMIT 1", (rarity,))
            result = cursor.fetchone()

            if not result:
                await ctx.send("Aucune carte n'est disponible.")
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
                chant += random.randint(100, 150)
                dance += random.randint(100, 150)
                rap += random.randint(100, 150)
                acting += random.randint(100, 150)
                modeling += random.randint(100, 150)
            elif rarity == "R":
                chant += random.randint(150, 200)
                dance += random.randint(150, 200)
                rap += random.randint(150, 200)
                acting += random.randint(150, 200)
                modeling += random.randint(150, 200)
            elif rarity == "E":
                chant += random.randint(200, 250)
                dance += random.randint(200, 250)
                rap += random.randint(200, 250)
                acting += random.randint(200, 250)
                modeling += random.randint(200, 250)
            elif rarity == "L":
                chant += random.randint(250, 300)
                dance += random.randint(250, 300)
                rap += random.randint(250, 300)
                acting += random.randint(250, 300)
                modeling += random.randint(250, 300)

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

            # Get the corresponding rarity emoji
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
            elif event and event.lower() == 'lunar2024':
                rarity_emojis = {
                    "L": "<:Hongbao:1205276514443067533>"
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
            title = f"**DAILY REWARD - DROP**"

            # Crée le message à envoyer après avoir dropé la carte
            drop_message = f"Congratulations {ctx.author.mention}\nYou have dropped: [{groupe} {card_name} - {rarity_emoji} ] n° {code_card.split('-')[1]}\nCode : `{code_card}`"

            # Crée l'embed Discord avec le titre, le message et l'image de la carte
            embed = discord.Embed(title=title, description=drop_message)
            embed.set_image(url=url_image)

            # Envoie l'embed
            await ctx.send(embed=embed)

            # Vérifier si la carte dropée est la carte préférée d'un joueur
            players_with_favorite_card = []
            bonus_amount = 1000
            for player_id, favorite_cards in self.cartes_preferees.items():
                for fav_name, fav_group in favorite_cards:
                    if card_name.lower() == fav_name.lower() and groupe.lower() == fav_group.lower():
                        players_with_favorite_card.append(player_id)
                        # Donner le bonus d'argent au joueur qui a dropé la carte préférée
                        cursor.execute("UPDATE user_data SET argent = argent + ? WHERE user_id = ?", (bonus_amount, user_id))
                        connection.commit()
                        break 

            # Envoyer un message au joueur qui a dropé la carte préférée
            if players_with_favorite_card:
                players_mentions = ", ".join([f"<@{player_id}>" for player_id in players_with_favorite_card])
                embed_bonus = discord.Embed(
                    title="**Bonus**",
                    description=f"Congratulations {ctx.author.mention}\nYou received a bonus of **{bonus_amount}** <:HCoins:1134169003657547847> for dropping the favorite card of {players_mentions}.",
                    color=discord.Color.gold()
                )
                await ctx.send(embed=embed_bonus)

        else:
            # Récompense en argent
            montant = random.randint(500, 1000)
            cursor.execute("SELECT * FROM user_data WHERE user_id = ?", (str(user_id),))
            result = cursor.fetchone()

            if result is not None:
                cursor.execute("UPDATE user_data SET argent = argent + ? WHERE user_id = ?", (montant, str(user_id)))
            else:
                cursor.execute("INSERT INTO user_data VALUES (?, ?, ?, ?, ?)", (str(user_id), "", montant, 0, ""))

            connection.commit()

            cursor.execute("SELECT argent FROM user_data WHERE user_id = ?", (str(user_id),))
            updated_amount = cursor.fetchone()[0]
            uptated_formatted_amount = self.format_money(updated_amount)

            # Crée le titre de l'embed
            title = f"**DAILY REWARD - WORK**"

            # Crée le message à envoyer après avoir gagné de l'argent
            drop_message = f"Congratulations {ctx.author.mention}\nYou have received a daily reward of {montant} <:HCoins:1134169003657547847>!\n\nNew balance : **{uptated_formatted_amount}** <:HCoins:1134169003657547847>"

            # Crée l'embed Discord avec le titre et le message
            embed = discord.Embed(title=title, description=drop_message, color=discord.Color.green())

            # Envoie l'embed
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Daily(bot))