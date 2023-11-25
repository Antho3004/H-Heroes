import discord
from discord.ext import commands
import sqlite3
import random

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def shop(self, ctx):
        # Créez un embed pour afficher les packs
        embed = discord.Embed(title="SHOP", description="", color=discord.Color.blue())

        embed.add_field(name="", value=f"<:Bronze:1136312536665440387> **Bronze** (5 cards C/U/R): **3000** <:HCoins:1134169003657547847>", inline=False)
        embed.add_field(name="", value=f"<:Argent:1136312524900401213> **Silver** (5 cards U/R/E): **7000** <:HCoins:1134169003657547847>", inline=False)
        embed.add_field(name="", value=f"<:Gold:1136312506957189131> **Gold** (5 cards R/E/L) : **20000** <:HCoins:1134169003657547847>", inline=False)
        embed.add_field(name="", value=f"<:Legendary:1136312609449193544> **Legendary** (5 cards L): **50000** <:HCoins:1134169003657547847>", inline=False)

        # Envoyez l'embed
        await ctx.send(embed=embed)

    @commands.command()
    async def buy_pack(self, ctx, pack_name: str):
        packs = {
            "bronze": 3000,
            "silver": 7000,
            "gold": 20000,
            "legendary": 50000
        }

        pack_name_lower = pack_name.lower()
        if pack_name_lower not in packs:
            embed = discord.Embed(title="**SHOP**", description="This pack does not exist. Available packs: **bronze**/**silver**/**gold**/**legendary**", color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        price = packs[pack_name_lower]

        # Vérifier si l'utilisateur a assez d'argent
        user_id = ctx.author.id
        with sqlite3.connect("HallyuHeroes.db") as connection:
            cursor = connection.cursor()

            cursor.execute("SELECT argent, bronze, silver, gold, legendary FROM user_data WHERE user_id = ?", (user_id,))
            result = cursor.fetchone()

            if result:
                user_money, bronze_packs, silver_packs, gold_packs, legendary_packs = result

                # Handle NULL values and set to 0
                bronze_packs = bronze_packs or 0
                silver_packs = silver_packs or 0
                gold_packs = gold_packs or 0
                legendary_packs = legendary_packs or 0

                if user_money >= price:
                    # Déduire le prix du pack de l'argent de l'utilisateur
                    new_money = user_money - price

                    # Ajouter le pack à l'inventaire de l'utilisateur
                    if pack_name_lower == "bronze":
                        bronze_packs += 1
                    elif pack_name_lower == "silver":
                        silver_packs += 1
                    elif pack_name_lower == "gold":
                        gold_packs += 1
                    elif pack_name_lower == "legendary":
                        legendary_packs += 1

                    cursor.execute("UPDATE user_data SET argent = ?, bronze = ?, silver = ?, gold = ?, legendary = ? WHERE user_id = ?", (new_money, bronze_packs, silver_packs, gold_packs, legendary_packs, user_id))
                    connection.commit()

                    embed = discord.Embed(title="Purchase Successful", description=f"You have purchased the pack {pack_name}!", color=discord.Color.green())
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title="Insufficient Funds", description="You don't have enough money to buy this pack.", color=discord.Color.red())
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="**Error**", description="You are not registered in the database.", color=discord.Color.red())
                await ctx.send(embed=embed)
    
    
    def get_rarity_emoji(self, rarity):
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
                    "U": 50,
                    "R": 20
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

            # Générer 5 cartes aléatoires comme dans la fonction drop
            cards = []
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

                cursor.execute("SELECT code_card, nom, groupe, version, image_url FROM cards WHERE rarete = ? ORDER BY RANDOM() LIMIT 1", (rarity,))
                result = cursor.fetchone()

                if not result:
                    await ctx.send("Erreur car il n'y a pas la rarete dispo dans le jeu")
                    return

                code_card, card_name, groupe, version, url_image = result

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

                existing_card = cursor.execute("SELECT code_card FROM user_inventaire WHERE code_card = ?", (code_card,)).fetchone()
                if existing_card:
                    pass
                else:
                    cursor.execute(
                        "INSERT INTO user_inventaire (code_card, user_id, groupe, nom, rarete, version, chant, dance, rap, acting, modeling, image_url) "
                        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (code_card, user_id, groupe, card_name, rarity, version, chant, dance, rap, acting, modeling, url_image)
                    )
                    connection.commit()

                cards.append({
                    "code_card": code_card,
                    "rarity": rarity,
                    "card_name": card_name,
                    "groupe": groupe,
                    "version": version,
                    "url_image": url_image
                })

            # Afficher les cartes obtenues dans le message
            card_list_message = "\n".join([f"- {card['groupe']} {card['card_name']} {self.get_rarity_emoji(card['rarity'])} n° {card['code_card'].split('-')[1]} `{code_card}`" for card in cards])

            # Créer l'embed Discord
            embed = discord.Embed(title="Opened Pack", description=f"Congratulations {ctx.author.mention}\nYou have opened a {pack_name} pack and obtained the following cards:\n{card_list_message}", color=discord.Color.green())

            # Envoyer l'embed
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Shop(bot))
