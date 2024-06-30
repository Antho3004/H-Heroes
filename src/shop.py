import discord
from discord.ext import commands
import sqlite3
import random

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.allowed_users = {307595556325425174, 403661101385908225, 820035016242757653}  # Ajoutez les ID des utilisateurs autorisés ici

    def is_allowed_user(self, ctx):
        # Votre logique pour vérifier si l'utilisateur est autorisé
        return ctx.author.id in self.allowed_users
    
    def format_money(self, money):
        return "{:,}".format(money).replace(",", " ")

    @commands.command()
    async def shop(self, ctx):
        # Créez un embed pour afficher les packs
        embed = discord.Embed(title="SHOP", description="", color=discord.Color.blue())

        embed.add_field(name="", value=f"<:Bronze:1136312536665440387> **Bronze** (5 cards C/U/R): **3000** <:HCoins:1134169003657547847>", inline=False)
        embed.add_field(name="", value=f"<:Argent:1136312524900401213> **Silver** (5 cards U/R/E): **7000** <:HCoins:1134169003657547847>", inline=False)
        embed.add_field(name="", value=f"<:Gold:1136312506957189131> **Gold** (5 cards R/E/L) : **20000** <:HCoins:1134169003657547847>", inline=False)
        embed.add_field(name="", value=f"<:Legendary:1136312609449193544> **Legendary** (5 cards L): **50000** <:HCoins:1134169003657547847>", inline=False)
        embed.add_field(name="", value=f":person_lifting_weights: **Training** : **2500** <:HCoins:1134169003657547847>", inline=False)

        # Envoyez l'embed
        await ctx.send(embed=embed)

    @commands.command()
    async def buy_pack(self, ctx, pack_name: str, montant: int = 1):
        packs = {
            "bronze": 3000,
            "silver": 7000,
            "gold": 20000,
            "legendary": 50000,
            "training": 2500
        }

        pack_name_lower = pack_name.lower()
        if pack_name_lower not in packs:
            embed = discord.Embed(title="**SHOP**", description="This pack does not exist. Available packs: **bronze**/**silver**/**gold**/**legendary**/**training**", color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        price = packs[pack_name_lower] * montant

        # Vérifier si l'utilisateur a assez d'argent
        user_id = ctx.author.id
        with sqlite3.connect("HallyuHeroes.db") as connection:
            cursor = connection.cursor()

            cursor.execute("SELECT argent, bronze, silver, gold, legendary, training FROM user_data WHERE user_id = ?", (user_id,))
            result = cursor.fetchone()

            if result:
                user_money, bronze_packs, silver_packs, gold_packs, legendary_packs, training_packs = result

                # Handle NULL values and set to 0
                bronze_packs = bronze_packs or 0
                silver_packs = silver_packs or 0
                gold_packs = gold_packs or 0
                legendary_packs = legendary_packs or 0
                training_packs = training_packs or 0

                if user_money >= price:
                    # Déduire le prix du pack de l'argent de l'utilisateur
                    new_money = user_money - price

                    # Ajouter le pack à l'inventaire de l'utilisateur
                    if pack_name_lower == "bronze":
                        bronze_packs += montant
                    elif pack_name_lower == "silver":
                        silver_packs += montant
                    elif pack_name_lower == "gold":
                        gold_packs += montant
                    elif pack_name_lower == "legendary":
                        legendary_packs += montant
                    elif pack_name_lower == "training":
                        training_packs += montant

                    cursor.execute("UPDATE user_data SET argent = ?, bronze = ?, silver = ?, gold = ?, legendary = ?, training = ? WHERE user_id = ?", (new_money, bronze_packs, silver_packs, gold_packs, legendary_packs, training_packs, user_id))
                    connection.commit()

                    cursor.execute("SELECT argent FROM user_data WHERE user_id = ?", (str(user_id),))
                    updated_amount = cursor.fetchone()[0]
                    uptated_formatted_amount = self.format_money(updated_amount)

                    embed = discord.Embed(title="Purchase Successful", description=f"You have purchased **{montant}** pack **{pack_name}** !\n\nNew balance : **{uptated_formatted_amount}** <:HCoins:1134169003657547847>", color=discord.Color.green())
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title="Insufficient Funds", description="You don't have enough money to buy this pack.", color=discord.Color.red())
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="**Error**", description="You are not registered in the database.", color=discord.Color.red())
                await ctx.send(embed=embed)
    
    
    def get_rarity_emoji(self, rarity, event):
        if event is not None:
            event_lower = str(event).lower()
            if event_lower == 'xmas 2023':
                rarity_emojis = {
                    "U": "<:xmas_boot:1183911398661693631>",
                    "L": "<:xmas_hat:1183911360808112160>"
                }
            elif event_lower == 'new year 2024':
                rarity_emojis = {
                    "R": "<:NY_Confetti:1185996235551805470>",
                    "L": "<:NY_Fireworks:1185996232477384808>"
                }
            elif event_lower == 'lunar2024':
                rarity_emojis = {
                    "L": "<:Hongbao:1205276514443067533>"
                }
            elif event_lower == 'valentine 2024':
                rarity_emojis = {
                    "U": "<:Flowers:1207807685215391775>",
                    "E": "<:Arc:1207807149531729971>"
                }
            elif event_lower == 'spring 2024':
                rarity_emojis = {
                    "U": "<:Marigold:1220794525094772806>",
                    "R": "<:Sakura:1220794502944657460>"
                }
            elif event.lower() == "april fool's day":
                rarity_emojis = {
                    "L": "<:JOKE:1224024439004332142>"
                }
            elif event.lower() == "summer 2024":
                rarity_emojis = {
                    "U": "<:Wave:1256760316612710400>",
                    "E": "<:Coconut:1256760318869110856>"
                }
            elif event_lower == 'k-drama':
                rarity_emojis = {
                    "C": "<:C_:1107771999490686987>",
                    "U": "<:U_:1107772008193867867>",
                    "R": "<:R_:1107772004410601553>",
                    "E": "<:E_:1107772001747222550>",
                    "L": "<:L_:1107772002690945055>"
                }
        else:
            # Aucun événement, utilisez les emojis génériques
            rarity_emojis = {
                "C": "<:C_:1107771999490686987>",
                "U": "<:U_:1107772008193867867>",
                "R": "<:R_:1107772004410601553>",
                "E": "<:E_:1107772001747222550>",
                "L": "<:L_:1107772002690945055>"
            }

        return rarity_emojis.get(rarity, "")


    @commands.command()
    async def open_pack(self, ctx, pack_name: str):
        pack_name_lower = pack_name.lower()
        pack_inventory_column = f"{pack_name_lower}"

        # Vérifier si le pack demandé existe
        if pack_name_lower not in ["bronze", "silver", "gold", "legendary"]:
            embed = discord.Embed(title="Invalid Pack", description="Invalid pack name. Available packs: bronze, silver, gold, legendary", color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        # Vérifier si l'utilisateur a le pack demandé dans son inventaire
        user_id = ctx.author.id
        with sqlite3.connect("HallyuHeroes.db") as connection:
            cursor = connection.cursor()

            cursor.execute(f"SELECT {pack_inventory_column} FROM user_data WHERE user_id = ?", (user_id,))
            pack_count = cursor.fetchone()

            if not pack_count or pack_count[0] <= 0:
                embed = discord.Embed(title="No Packs", description=f"You don't have any {pack_name} packs in your inventory.", color=discord.Color.red())
                await ctx.send(embed=embed)
                return

            # Décrémenter le nombre de packs dans l'inventaire de l'utilisateur
            cursor.execute(f"UPDATE user_data SET {pack_inventory_column} = {pack_inventory_column} - 1 WHERE user_id = ?", (user_id,))
            connection.commit()

            # Définir les pourcentages de drop en fonction de la rareté pour chaque type de pack
            rarity_drop_rates = {}
            if pack_name_lower == "bronze":
                rarity_drop_rates = {
                    "C": 50,
                    "U": 40,
                    "R": 10
                }
            elif pack_name_lower == "silver":
                rarity_drop_rates = {
                    "U": 50,
                    "R": 30,
                    "E": 20
                }
            elif pack_name_lower == "gold":
                rarity_drop_rates = {
                    "R": 50,
                    "E": 30,
                    "L": 20
                }
            elif pack_name_lower == "legendary":
                rarity_drop_rates = {
                    "L": 100
                }

            # Déterminer le montant de la compensation en fonction de la rareté du pack
            compensation_rates = {
                "bronze": 3000,
                "silver": 7000,
                "gold": 20000,
                "legendary": 50000
            }

            compensation_amount = compensation_rates.get(pack_name_lower, 0)

            # Générer 5 cartes aléatoires comme dans la fonction drop
            cards = []
            cards_generated = 0  # Ajout de la variable pour suivre le nombre de cartes générées

            for _ in range(5):
                total_drop_rate = sum(rarity_drop_rates.values())
                drop_chance = random.randint(1, total_drop_rate + 1)

                rarity = None
                for rarete, drop_rate in rarity_drop_rates.items():
                    if drop_chance <= drop_rate:
                        rarity = rarete
                        break
                    drop_chance -= drop_rate

                if not rarity:
                    await ctx.send(rarity)
                    return
                else:
                    cards_generated += 1  # Incrémenter le nombre de cartes générées

                cursor.execute("SELECT code_card, nom, groupe, version, image_url, event FROM cards WHERE rarete = ? ORDER BY RANDOM() LIMIT 1", (rarity,))
                result = cursor.fetchone()

                if not result:
                    await ctx.send("Erreur car il n'y a pas la rareté dispo dans le jeu")
                    return

                code_card, card_name, groupe, version, url_image, event = result

                code_card_parts = code_card.split("-")
                if len(code_card_parts) == 2:
                    try:
                        card_num = int(code_card_parts[1]) + 1
                        code_card = f"{code_card_parts[0]}-{card_num}"
                    except ValueError:
                        pass

                existing_card = cursor.execute("SELECT code_card FROM user_inventaire WHERE code_card = ?", (code_card,)).fetchone()
                while existing_card:
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

                existing_card = cursor.execute("SELECT code_card FROM user_inventaire WHERE code_card = ?", (code_card,)).fetchone()
                if existing_card:
                    pass
                else:
                    cursor.execute(
                        "INSERT INTO user_inventaire (code_card, user_id, groupe, nom, rarete, version, chant, dance, rap, acting, modeling, image_url, event) "
                        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (code_card, user_id, groupe, card_name, rarity, version, chant, dance, rap, acting, modeling, url_image, event)
                    )
                    connection.commit()

                cards.append({
                    "code_card": code_card,
                    "rarity": rarity,
                    "card_name": card_name,
                    "groupe": groupe,
                    "version": version,
                    "url_image": url_image,
                    "event" : event
                })

            # Vérifier si le nombre de cartes générées est inférieur à 5 et ajouter une compensation en argent
            if cards_generated < 5:
                cursor.execute("UPDATE user_data SET argent = argent + ? WHERE user_id = ?", (compensation_amount, user_id))
                connection.commit()
                await ctx.send(f"Due to a bug, you have been compensated with **{compensation_amount}** <:HCoins:1134169003657547847>")

            # Afficher les cartes obtenues dans le message
            card_list_messages = []
            for card in cards:
                rarity_emoji = self.get_rarity_emoji(card['rarity'], card['event'])
                card_list_messages.append(
                    f"- {card['groupe']} {card['card_name']} {rarity_emoji} n° {card['code_card'].split('-')[1]} `{card['code_card']}`"
                )

            card_list_message = "\n".join(card_list_messages)

            # Créer l'embed Discord
            embed = discord.Embed(title="Opened Pack", description=f"Congratulations {ctx.author.mention}\nYou have opened a {pack_name} pack and obtained the following cards:\n{card_list_message}", color=discord.Color.green())

            # Envoyer l'embed
            await ctx.send(embed=embed)

    @commands.command()
    async def training(self, ctx, code_card: str, number_of_trainings: int=1):
        # Vérifier si l'utilisateur possède des packs_training
        user_id = ctx.author.id
        with sqlite3.connect("HallyuHeroes.db") as connection:
            cursor = connection.cursor()

            cursor.execute("SELECT training FROM user_data WHERE user_id = ?", (user_id,))
            training_packs = cursor.fetchone()[0] or 0

            if training_packs >= number_of_trainings:
                # L'utilisateur a suffisamment de packs_training, procéder à l'amélioration des stats
                cursor.execute("SELECT rarete, chant, dance, rap, acting, modeling FROM user_inventaire WHERE user_id = ? AND code_card = ?", (user_id, code_card))
                card_data = cursor.fetchone()

                if card_data:
                    rarity, chant, dance, rap, acting, modeling = card_data

                    # Définir les limites de stats en fonction de la rareté
                    stat_limits = {
                        "C": 300,
                        "U": 350,
                        "R": 400,
                        "E": 450,
                        "L": 500
                    }

                    # Vérifier la rareté de la carte et mettre à jour les stats si possible
                    if rarity in stat_limits:
                        stat_limit = stat_limits[rarity]

                        # Liste des statistiques disponibles
                        available_stats = ["chant", "dance", "rap", "acting", "modeling"]

                        stats_summary = {}  # Résumé des statistiques améliorées

                        nombre_training = 0

                        for _ in range(number_of_trainings):
                            # Choisir une statistique à améliorer
                            stat_to_improve = random.choice(available_stats)
                            cursor.execute(f"SELECT {stat_to_improve} FROM user_inventaire WHERE user_id = ? and code_card = ?", (user_id, code_card)) 
                            current_stat_value = cursor.fetchone()[0]

                            # Vérifier si la statistique a déjà dépassé la limite
                            while current_stat_value >= stat_limit:
                                # Si la statistique a déjà dépassé la limite, choisir une autre statistique
                                available_stats.remove(stat_to_improve)
                                
                                if not available_stats:
                                    embed = discord.Embed(title=f"All Stats at Limit - {ctx.author.display_name}", description=f"All stats for this card are already at the maximum limit for its rarity ({rarity}).", color=discord.Color.red())
                                    await ctx.send(embed=embed)
                                    break
                                
                                # on choisi une autre statistics
                                stat_to_improve = random.choice(available_stats)
                                cursor.execute(f"SELECT {stat_to_improve} FROM user_inventaire WHERE user_id = ? and code_card = ?", (user_id, code_card)) 
                                current_stat_value = cursor.fetchone()[0]

                            if current_stat_value >= stat_limit:
                                    # Sortir de la boucle for si toutes les statistiques ont atteint la limite
                                    break
                            
                            # Améliorer la statistique
                            upgrade = random.randint(1, 50)
                            improved_stat_value = current_stat_value + upgrade

                            # Mettre à jour la base de données avec la nouvelle valeur de la statistique
                            cursor.execute(f"UPDATE user_inventaire SET {stat_to_improve} = ? WHERE user_id = ? AND code_card = ?", (improved_stat_value, user_id, code_card))
                            cursor.execute("UPDATE user_data SET training = training - 1 WHERE user_id = ?", (user_id,)) 
                            connection.commit()

                            nombre_training += 1

                            # Ajouter la statistique améliorée au résumé
                            stat_name = "sing" if stat_to_improve == "chant" else stat_to_improve
                            stats_summary[stat_name] = stats_summary.get(stat_name, 0) + upgrade
                            
                            # Si la statistique a atteint la limite, la retirer des statistiques disponibles
                            if improved_stat_value >= stat_limit:
                                available_stats.remove(stat_to_improve)
                        

                        # Construction de l'embed final avec le résumé des statistiques améliorées
                        embed = discord.Embed(title=f"{ctx.author.display_name}'s Training Result", description=f"Stats successfully increased **{nombre_training}** times for the card `{code_card}`", color=discord.Color.green())
                        for stat, value in stats_summary.items():
                            embed.add_field(name="", value=f"{stat.capitalize()} : + **{value}**\n", inline=False)
                        await ctx.send(embed=embed)
                        
                    else:
                        embed = discord.Embed(title=f"Invalid Rarity - {ctx.author.display_name}", description=f"Invalid rarity ({rarity}) for the card `{code_card}`", color=discord.Color.red())
                        await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title=f"Card Not Found - {ctx.author.display_name}", description=f"Card with code `{code_card}` not found in your inventory.", color=discord.Color.red())
                    await ctx.send(embed=embed)
            else:
                # Message indiquant que l'utilisateur n'a pas assez de packs
                embed = discord.Embed(title=f"Not Enough Training Packs - {ctx.author.display_name}", description=f"You don't have enough training packs in your inventory. You need at least {number_of_trainings} training packs.", color=discord.Color.red())
                await ctx.send(embed=embed)


    @commands.command()
    async def add_pack(self, ctx, user: discord.User, pack_rarity: str, amount: int = 1):
        # Vérifier si l'utilisateur est autorisé
        if not self.is_allowed_user(ctx):
            embed = discord.Embed(title="Unauthorized", description="You are not authorized to use this command.", color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        # Vérifier si la rareté du pack est valide
        if pack_rarity.lower() not in ["bronze", "silver", "gold", "legendary", "training"]:
            embed = discord.Embed(title="Invalid Rarity", description="Invalid pack rarity. Available rarities: bronze, silver, gold, legendary, training", color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        # Ajouter le pack à l'inventaire de l'utilisateur spécifié
        with sqlite3.connect("HallyuHeroes.db") as connection:
            cursor = connection.cursor()
            cursor.execute(f"UPDATE user_data SET {pack_rarity.lower()} = {pack_rarity.lower()} + ? WHERE user_id = ?", (amount, user.id))
            connection.commit()

        embed = discord.Embed(title="Pack Added", description=f"**{amount} {pack_rarity}** pack{'s' if amount > 1 else ''} has been added to {user.mention}'s inventory.", color=discord.Color.green())
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Shop(bot))
