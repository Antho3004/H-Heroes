import discord
from discord.ext import commands
import sqlite3

connection = sqlite3.connect("HallyuHeroes.db")
cursor = connection.cursor()

class Trade(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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

        embed = discord.Embed(description=f"You gave **{amount}** <:HCoins:1134169003657547847> to {user.mention}!", color=discord.Color.green())
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Trade(bot))
