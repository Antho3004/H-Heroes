import discord
from discord.ext import commands
import sqlite3
from dispie import Paginator

connection = sqlite3.connect("HallyuHeroes.db")
cursor = connection.cursor()

class MarketPlace(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def format_money(self, money):
        return "{:,}".format(money).replace(",", " ")

    @commands.command()
    async def mp(self, ctx: commands.Context, user: discord.Member = None, page: int = 1):
        if user is None:
            cursor.execute("SELECT COUNT(*) FROM market")
            count = cursor.fetchone()[0]

            if count > 0:
                cursor.execute("SELECT i.user_id, i.groupe, i.nom, i.rarete, m.code_card, m.prix , i.event FROM market m JOIN user_inventaire i ON m.code_card = i.code_card ORDER BY i.groupe, i.nom")
                result = cursor.fetchall()

                # Divisez vos données en morceaux de 9 cartes par page
                chunks = [result[i:i + 9] for i in range(0, len(result), 9)]

                embeds = []  # Initialisez la liste d'embeds en dehors de la boucle

                for chunk in chunks:
                    embed = discord.Embed(title=f"Marketplace", color=discord.Color.blue())
                    
                    for i in range(0, len(chunk), 3):
                        cards_in_line = chunk[i:i + 3]
                        for line in cards_in_line:
                            if line[6] and line[6].lower() == 'xmas 2023':
                                rarity_emojis = {
                                    "U": "<:xmas_boot:1183911398661693631>",
                                    "L": "<:xmas_hat:1183911360808112160>"
                                }
                            elif line[6] and line[6].lower() == 'new year 2024':
                                rarity_emojis = {
                                    "R": "<:NY_Confetti:1185996235551805470>",
                                    "L": "<:NY_Fireworks:1185996232477384808>"
                                }
                            elif line[6] and line[6].lower() == 'lunar 2024':
                                rarity_emojis = {
                                    "L": "<:Hongbao:1205276514443067533>"
                                }
                            elif line[6] and line[6].lower() == 'valentine 2024':
                                rarity_emojis = {
                                    "U": "<:Flowers:1207807685215391775>",
                                    "E": "<:Arc:1207807149531729971>"
                                }
                            elif line[6] and line[6].lower() == "summer 2024":
                                rarity_emojis = {
                                    "U": "<:Wave:1256760316612710400>",
                                    "E": "<:Coconut:1256760318869110856>"
                                }
                            else:
                                rarity_emojis = {
                                    "C": "<:C_:1107771999490686987>",
                                    "U": "<:U_:1107772008193867867>",
                                    "R": "<:R_:1107772004410601553>",
                                    "E": "<:E_:1107772001747222550>",
                                    "L": "<:L_:1107772002690945055>"
                                }
                            embed.add_field(
                                name=f"{line[1]} - {line[2]} {rarity_emojis.get(line[3], '')}",
                                value=f"{line[4]}\nPrice : {self.format_money(line[5])} <:HCoins:1134169003657547847>\n<@{line[0]}>",
                                inline=True
                            )
                    embed.set_footer(text=f"Total cards: {count}")
                    embeds.append(embed)

                # Créez un objet Paginator en passant la liste d'embeds
                paginator = Paginator(embeds)

                # Démarrez la pagination
                await paginator.start(ctx)

            else:
                embed = discord.Embed(title="Marketplace", description="Marketplace is empty.", color=discord.Color.red())
                await ctx.send(embed=embed)
        else:
            cursor.execute("SELECT COUNT(*) FROM market m JOIN user_inventaire i ON m.code_card = i.code_card WHERE i.user_id = ?", (user.id,))
            count = cursor.fetchone()[0]

            if count > 0:
                cursor.execute("SELECT i.user_id, i.groupe, i.nom, i.rarete, m.code_card, m.prix, i.event FROM market m JOIN user_inventaire i ON m.code_card = i.code_card WHERE i.user_id = ? ORDER BY i.groupe, i.nom", (user.id,))
                result = cursor.fetchall()

                # Divisez vos données en morceaux de 9 cartes par page
                chunks = [result[i:i + 9] for i in range(0, len(result), 9)]

                embeds = []  # Initialisez la liste d'embeds en dehors de la boucle

                for chunk in chunks:
                    embed = discord.Embed(title=f"Marketplace", color=discord.Color.blue())
                    
                    for i in range(0, len(chunk), 3):
                        cards_in_line = chunk[i:i + 3]

                        for line in cards_in_line:
                            if line[6] and line[6].lower() == 'xmas 2023':
                                rarity_emojis = {
                                    "U": "<:xmas_boot:1183911398661693631>",
                                    "L": "<:xmas_hat:1183911360808112160>"
                                }
                            elif line[6] and line[6].lower() == 'new year 2024':
                                rarity_emojis = {
                                    "R": "<:NY_Confetti:1185996235551805470>",
                                    "L": "<:NY_Fireworks:1185996232477384808>"
                                }
                            elif line[6] and line[6].lower() == 'lunar2024':
                                rarity_emojis = {
                                    "L": "<:Hongbao:1205276514443067533>"
                                }
                            elif line[6] and line[6].lower() == 'valentine 2024':
                                rarity_emojis = {
                                    "U": "<:Flowers:1207807685215391775>",
                                    "E": "<:Arc:1207807149531729971>"
                                }
                            elif line[6] and line[6].lower() == 'spring 2024':
                                rarity_emojis = {
                                    "U": "<:Marigold:1220794525094772806>",
                                    "R": "<:Sakura:1220794502944657460>"
                                }
                            elif line[6] and line[6].lower() == "april fool's day":
                                rarity_emojis = {
                                    "L": "<:JOKE:1224024439004332142>"
                                }
                            elif line[6] and line[6].lower() == "summer 2024":
                                rarity_emojis = {
                                    "U": "<:Wave:1256760316612710400>",
                                    "E": "<:Coconut:1256760318869110856>"
                                }
                            else:
                                rarity_emojis = {
                                    "C": "<:C_:1107771999490686987>",
                                    "U": "<:U_:1107772008193867867>",
                                    "R": "<:R_:1107772004410601553>",
                                    "E": "<:E_:1107772001747222550>",
                                    "L": "<:L_:1107772002690945055>"
                                }
                            embed.add_field(
                                name=f"{line[1]} - {line[2]} {rarity_emojis.get(line[3], '')}",
                                value=f"{line[4]}\nPrice : {self.format_money(line[5])} <:HCoins:1134169003657547847>\n<@{line[0]}>",
                                inline=True
                            )
                    embed.set_footer(text=f"Total cards: {count}")
                    embeds.append(embed)

                # Créez un objet Paginator en passant la liste d'embeds
                paginator = Paginator(embeds)

                # Démarrez la pagination
                await paginator.start(ctx)

            else:
                embed = discord.Embed(title="Marketplace", description="Marketplace is empty.", color=discord.Color.red())
                await ctx.send(embed=embed)

    @commands.command()
    async def sell(self, ctx, code_card, prix):
        user = ctx.author
        
        # Vérifier si le prix est un nombre valide
        try:
            prix = int(prix)
        except ValueError:
            embed = discord.Embed(
                title=f"{user.name} - **Marketplace**",
                description="Please enter a valid price.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        # Vérifier si l'utilisateur possède la carte qu'il souhaite vendre
        cursor.execute("SELECT code_card FROM user_inventaire WHERE user_id = ? AND code_card = ?", (user.id, code_card))
        sell_card = cursor.fetchone()

        # Vérifier si l'utilisateur a déjà cette carte en vente dans le marché
        cursor.execute("SELECT m.code_card FROM market m JOIN user_inventaire i ON m.code_card = i.code_card WHERE i.user_id = ? and m.code_card = ?", (user.id, code_card))
        existing_sale = cursor.fetchone()

        if sell_card is not None:
            if existing_sale:
                # Remplacer la carte déjà en vente par la nouvelle valeur
                cursor.execute("UPDATE market SET prix = ? where code_card = ?", (prix, code_card))
            else:
                # Insérer les informations de la carte dans la table "market"
                cursor.execute("INSERT INTO market (code_card, prix) VALUES (?, ?)", (code_card, prix))

            connection.commit()

            formatted_argent = self.format_money(prix)

            embed = discord.Embed(
                title=f"{user.name} - **Marketplace**",
                description=f"The card `{code_card}` is on sale for **{formatted_argent}** <:HCoins:1134169003657547847>",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title=f"{user.name} - **Marketplace**",
                description=f"You do not have the card: `{code_card}`",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

    @commands.command()
    async def buy(self, ctx, code_card):
        user = ctx.author
        # Get the price of the card from the market
        cursor.execute("SELECT m.prix, i.user_id FROM market m JOIN user_inventaire i ON m.code_card = i.code_card WHERE i.code_card = ?", (code_card,))
        result1 = cursor.fetchone()

        if result1 is not None:
            card_price = result1[0]
            seller_id = result1[1]

            # Get the buyer's current balance
            cursor.execute("SELECT argent FROM user_data WHERE user_id = ?", (user.id,))
            result2 = cursor.fetchone()

            if result2 is not None:
                user_balance = result2[0]

                if user_balance >= card_price:
                    code_card = str(code_card)
                    # Deduct the card price from the buyer's balance
                    cursor.execute("UPDATE user_data SET argent = argent - ? WHERE user_id = ?", (card_price, user.id))
                    # Add the card price to the seller's balance
                    cursor.execute("UPDATE user_data SET argent = argent + ? WHERE user_id = ?", (card_price, seller_id))
                    # Add the card to the buyer's inventory
                    cursor.execute("UPDATE user_inventaire SET user_id = ? where code_card = ?", (user.id, code_card))
                    # Remove the card from the market
                    cursor.execute("DELETE FROM market WHERE code_card = ?", (code_card,))
                    connection.commit()

                    cursor.execute("SELECT argent FROM user_data WHERE user_id = ?", (str(user.id),))
                    updated_amount = cursor.fetchone()[0]
                    uptated_formatted_amount = self.format_money(updated_amount)
                    

                    formatted_argent = self.format_money(card_price)

                    embed = discord.Embed(title=f"{user.name} - **Purchase**",
                        description=f"You have purchased the **{code_card}** for **{formatted_argent}** <:HCoins:1134169003657547847>\n\nNew balance : **{uptated_formatted_amount}** <:HCoins:1134169003657547847>", color=discord.Color.green()
                    )
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title=f"{user.name} - **Purchase**", description="Sorry, you don't have enough <:HCoins:1134169003657547847> to buy this card.",
                        color=discord.Color.red()
                    )
                    await ctx.send(embed=embed)
            else:
                # The user doesn't have a balance entry, meaning they don't have any money
                embed = discord.Embed(title=f"{user.name} - **Purchase**", description="Sorry, you don't have enough <:HCoins:1134169003657547847> to buy this card.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=f"{user.name} - **Market**",
                description="Sorry, this card is not available in this marketplace.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

    @commands.command()
    async def wd(self, ctx, code_card):
        user = ctx.author

        # Check if the user owns the card they want to withdraw from the market
        cursor.execute("SELECT i.user_id FROM market m JOIN user_inventaire i ON m.code_card = i.code_card WHERE i.code_card = ?", (code_card,))
        seller_id = cursor.fetchone()

        if seller_id[0] != user.id:
            # Remove the card from the market
            code_card = str(code_card)
            cursor.execute("DELETE FROM market WHERE code_card = ?", (code_card,))
            connection.commit()

            embed = discord.Embed(
                title="MarketPlace",
                description=f"`{code_card}` has been withdrawn from the market.",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="MarketPlace",
                description=f"You are not authorised to withdraw this card from the market because it does not belong to you.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(MarketPlace(bot))