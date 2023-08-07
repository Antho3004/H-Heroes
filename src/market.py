import discord
from discord.ext import commands
import sqlite3
import asyncio

connection = sqlite3.connect("HallyuHeroes.db")
cursor = connection.cursor()

class MarketPlace(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def format_money(self, money):
        return "{:,}".format(money).replace(",", " ")

    @commands.command()
    async def mp(self, ctx, user: discord.Member = None, page: int = 1):
        if user is None:
            cursor.execute("SELECT COUNT(*) FROM market")
            count = cursor.fetchone()[0]

            if count > 0:
                cursor.execute("SELECT i.user_id, i.groupe, i.nom, i.rarete, m.code_card, m.prix FROM market m JOIN user_inventaire i ON m.code_card = i.code_card ORDER BY i.groupe, i.nom")
                result = cursor.fetchall()

                items_per_page = 9
                total_pages = (count + items_per_page - 1) // items_per_page
                page = max(1, min(page, total_pages))

                start_idx = (page - 1) * items_per_page
                end_idx = min(start_idx + items_per_page, count)

                embed = discord.Embed(title=f"Marketplace", color=discord.Color.blue())

                rarity_emojis = {
                    "C": "<:C_:1107771999490686987>",
                    "U": "<:U_:1107772008193867867>",
                    "R": "<:R_:1107772004410601553>",
                    "E": "<:E_:1107772001747222550>",
                    "L": "<:L_:1107772002690945055>"
                }

                for i in range(start_idx, end_idx):
                    row = result[i]
                    user_id = row[0]
                    groupe = row[1]
                    nom = row[2]
                    rarete = row[3]
                    code_card = row[4]
                    prix = row[5]

                    formatted_argent = self.format_money(prix)

                    rarity_emoji = rarity_emojis.get(rarete, "")

                    embed.add_field(name=f"**{groupe}** **{nom}** {rarity_emoji}", value=f"{code_card}\nPrice : {formatted_argent} <:HCoins:1134169003657547847>\n<@{user_id}>",inline=True)
                embed.set_footer(text=f"Page {page}/{total_pages} - Total cards in the marketplace: {count}")
                msg = await ctx.send(embed=embed)

                if total_pages > 1:
                    await msg.add_reaction("⬅️")
                    await msg.add_reaction("➡️")

                    def check(reaction, user):
                        return user == ctx.author and str(reaction.emoji) in ["⬅️", "➡️"]

                    while True:
                        try:
                            reaction, _ = await self.bot.wait_for("reaction_add", timeout=180.0, check=check)

                            if str(reaction.emoji) == "➡️" and page < total_pages:
                                page += 1
                            elif str(reaction.emoji) == "⬅️" and page > 1:
                                page -= 1
                            
                            start_idx = (page - 1) * items_per_page
                            end_idx = min(start_idx + items_per_page, count)
                            embed.clear_fields()
                            for i in range(start_idx, end_idx):
                                row = result[i]
                                user_id = row[0]
                                groupe = row[1]
                                nom = row[2]
                                rarete = row[3]
                                code_card = row[4]
                                prix = row[5]

                                rarity_emoji = rarity_emojis.get(rarete, "")

                                embed.add_field(name=f"**{groupe}** **{nom}** {rarity_emoji}", value=f"{code_card}\nPrice : {prix} <:HCoins:1134169003657547847>\n<@{user_id}>",inline=True)
                            embed.set_footer(text=f"Page {page}/{total_pages} - Total cards in the marketplace: {count}")
                            await msg.edit(embed=embed)

                            # Reset reaction count to 1
                            await reaction.remove(ctx.author)

                        except asyncio.TimeoutError:
                            await msg.clear_reactions()
                            break

            else:
                embed = discord.Embed(title="Marketplace", description="Marketplace is empty.", color=discord.Color.red())
                await ctx.send(embed=embed)
        
        else:
            cursor.execute("SELECT COUNT(*) FROM market m JOIN user_inventaire i ON m.code_card = i.code_card WHERE i.user_id = ?", (user.id,))
            count = cursor.fetchone()[0]

            if count > 0:
                cursor.execute("SELECT i.user_id, i.groupe, i.nom, i.rarete, m.code_card, m.prix FROM market m JOIN user_inventaire i ON m.code_card = i.code_card WHERE i.user_id = ? ORDER BY i.groupe, i.nom", (user.id,))
                result = cursor.fetchall()

                items_per_page = 9
                total_pages = (count + items_per_page - 1) // items_per_page
                page = max(1, min(page, total_pages))

                start_idx = (page - 1) * items_per_page
                end_idx = min(start_idx + items_per_page, count)

                embed = discord.Embed(title=f"Marketplace", color=discord.Color.blue())

                rarity_emojis = {
                    "C": "<:C_:1107771999490686987>",
                    "U": "<:U_:1107772008193867867>",
                    "R": "<:R_:1107772004410601553>",
                    "E": "<:E_:1107772001747222550>",
                    "L": "<:L_:1107772002690945055>"
                }

                for i in range(start_idx, end_idx):
                    row = result[i]
                    user_id = row[0]
                    groupe = row[1]
                    nom = row[2]
                    rarete = row[3]
                    code_card = row[4]
                    prix = row[5]

                    formatted_argent = self.format_money(prix)

                    rarity_emoji = rarity_emojis.get(rarete, "")

                    embed.add_field(name=f"**{groupe}** **{nom}** {rarity_emoji}", value=f"{code_card}\nPrice : {formatted_argent} <:HCoins:1134169003657547847>\n<@{user_id}>",inline=True)
                embed.set_footer(text=f"Page {page}/{total_pages} - Total cards in the marketplace: {count}")
                msg = await ctx.send(embed=embed)

                if total_pages > 1:
                    await msg.add_reaction("⬅️")
                    await msg.add_reaction("➡️")

                    def check(reaction, user):
                        return user == ctx.author and str(reaction.emoji) in ["⬅️", "➡️"]

                    while True:
                        try:
                            reaction, _ = await self.bot.wait_for("reaction_add", timeout=180.0, check=check)

                            if str(reaction.emoji) == "➡️" and page < total_pages:
                                page += 1
                            elif str(reaction.emoji) == "⬅️" and page > 1:
                                page -= 1
                            
                            start_idx = (page - 1) * items_per_page
                            end_idx = min(start_idx + items_per_page, count)
                            embed.clear_fields()
                            for i in range(start_idx, end_idx):
                                row = result[i]
                                user_id = row[0]
                                groupe = row[1]
                                nom = row[2]
                                rarete = row[3]
                                code_card = row[4]
                                prix = row[5]

                                rarity_emoji = rarity_emojis.get(rarete, "")

                                embed.add_field(name=f"**{groupe}** **{nom}** {rarity_emoji}", value=f"{code_card}\nPrice : {prix} <:HCoins:1134169003657547847>\n<@{user_id}>",inline=True)
                            embed.set_footer(text=f"Page {page}/{total_pages} - Total cards in the marketplace: {count}")
                            await msg.edit(embed=embed)

                            # Reset reaction count to 1
                            await reaction.remove(ctx.author)

                        except asyncio.TimeoutError:
                            await msg.clear_reactions()
                            break

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
                title="Marketplace",
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
                title="Marketplace",
                description=f"The card `{code_card}` is on sale for **{formatted_argent}** <:HCoins:1134169003657547847>",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Vente",
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

                    formatted_argent = self.format_money(card_price)

                    embed = discord.Embed(
                        description=f"You have purchased the **{code_card}** for **{formatted_argent}** <:HCoins:1134169003657547847>", color=discord.Color.green()
                    )
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(description="Sorry, you don't have enough <:HCoins:1134169003657547847> to buy this card.",
                        color=discord.Color.red()
                    )
                    await ctx.send(embed=embed)
            else:
                # The user doesn't have a balance entry, meaning they don't have any money
                embed = discord.Embed(description="Sorry, you don't have enough <:HCoins:1134169003657547847> to buy this card.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
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