import discord
from discord.ext import commands
import sqlite3

connection = sqlite3.connect("HallyuHeroes.db")
cursor = connection.cursor()

class Trade(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.allowed_users = {307595556325425174, 403661101385908225, 820035016242757653}  # Ajoutez les ID des utilisateurs autorisés ici

    def is_allowed_user(self, ctx):
        # Votre logique pour vérifier si l'utilisateur est autorisé
        return ctx.author.id in self.allowed_users

    def format_money(self, money):
        return "{:,}".format(money).replace(",", " ")

    @commands.command()
    async def gift(self, ctx, user: discord.Member = None, *code_cards: str):
        if user is None:
            user = ctx.author

        if not code_cards:
            embed = discord.Embed(description="Please provide at least one card code", color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        author_id = ctx.author.id
        given_cards = []

        for code_card in code_cards:
            cursor.execute("SELECT * FROM user_inventaire WHERE user_id = ? AND code_card = ?", (author_id, code_card))
            card_data = cursor.fetchone()

            if card_data is None:
                embed = discord.Embed(description=f"You don't have the card `{code_card}`", color=discord.Color.red())
                await ctx.send(embed=embed)
                continue

            # Vérifier si la carte est verrouillée
            if card_data[13]: 
                embed = discord.Embed(description=f"You can't gift the locked card `{code_card}`", color=discord.Color.red())
                await ctx.send(embed=embed)
                continue

            # Vérifier si la carte se trouve dans le marché
            cursor.execute("SELECT * FROM market WHERE code_card = ?", (code_card,))
            market_card_data = cursor.fetchone()

            if market_card_data is not None:
                # Retirer la carte du marché
                cursor.execute("DELETE FROM market WHERE code_card = ?", (code_card,))
                connection.commit()

            # Donner la carte à l'utilisateur mentionné
            cursor.execute("UPDATE user_inventaire SET user_id = ? where code_card = ?", (user.id, code_card))
            connection.commit()

            given_cards.append(code_card)

        if given_cards:
            cards_str = ', '.join([f"`{card}`" for card in given_cards])
            embed = discord.Embed(description=f"You gave the cards {cards_str} to {user.mention}", color=discord.Color.green())
            await ctx.send(embed=embed)

    @commands.command()
    async def bal_give(self, ctx, user: discord.Member = None, amount: int = None):
        if user is None:
            user = ctx.author

        if amount is None:
            embed = discord.Embed(description="Please enter an amount", color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        if amount < 0:
            embed = discord.Embed(description="Amount cannot be negative", color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        author_id = ctx.author.id
        cursor.execute("SELECT argent FROM user_data WHERE user_id = ?", (author_id,))
        author_money = cursor.fetchone()

        if author_money[0] < amount:
            embed = discord.Embed(description="You don't have enough money", color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        cursor.execute("UPDATE user_data SET argent = argent - ? WHERE user_id = ?", (amount, author_id))
        cursor.execute("UPDATE user_data SET argent = argent + ? WHERE user_id = ?", (amount, user.id))
        connection.commit()

        cursor.execute("SELECT argent FROM user_data WHERE user_id = ?", (str(author_id),))
        updated_amount = cursor.fetchone()[0]
        uptated_formatted_amount = self.format_money(updated_amount)

        embed = discord.Embed(description=f"You gave **{amount}** <:HCoins:1134169003657547847> to {user.mention}!\n\nNew balance : **{uptated_formatted_amount}** <:HCoins:1134169003657547847>", color=discord.Color.green())
        await ctx.send(embed=embed)
    
    @commands.command()
    async def add_money(self, ctx, user: discord.User, amount: int = 1):
        # Vérifier si l'utilisateur est autorisé
        if not self.is_allowed_user(ctx):
            embed = discord.Embed(title="Unauthorized", description="You are not authorized to use this command.", color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        # Ajouter le pack à l'inventaire de l'utilisateur spécifié
        with sqlite3.connect("HallyuHeroes.db") as connection:
            cursor = connection.cursor()
            cursor.execute(f"UPDATE user_data SET argent = argent + ? WHERE user_id = ?", (amount, user.id))
            connection.commit()

        embed = discord.Embed(title="Money Added", description=f"You gave **{amount}** <:HCoins:1134169003657547847> to {user.mention} !", color=discord.Color.green())
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Trade(bot))
