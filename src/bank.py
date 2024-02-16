import discord
from discord.ext import commands
import sqlite3

connection = sqlite3.connect("HallyuHeroes.db")
cursor = connection.cursor()

class Bank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=['tr'])
    async def transfer(self, ctx, amount: int):
        # Vérifier si l'utilisateur a suffisamment d'argent pour transférer
        author_id = ctx.author.id
        user = ctx.author
        cursor.execute("SELECT argent FROM user_data WHERE user_id = ?", (author_id,))
        author_money = cursor.fetchone()[0]
        if author_money < amount:
            embed = discord.Embed(description="You don't have enough money to transfer", color=discord.Color.red())
            await ctx.send(embed=embed)
            return
        
        # Mettre à jour l'argent de l'utilisateur et de sa banque
        cursor.execute("UPDATE user_data SET argent = argent - ? WHERE user_id = ?", (amount, author_id))
        cursor.execute("UPDATE user_data SET bank = bank + ? WHERE user_id = ?", (amount, author_id))
        connection.commit()

        embed = discord.Embed(title=f"{user.display_name}'s Bank", description=f"You transferred **{amount}** <:HCoins:1134169003657547847> to your bank", color=discord.Color.green())
        await ctx.send(embed=embed)

    @commands.command(aliases=['ext'])
    async def extract(self, ctx, amount: int):
        # Vérifier si l'utilisateur a suffisamment d'argent dans sa banque
        author_id = ctx.author.id
        user = ctx.author
        cursor.execute("SELECT bank FROM user_data WHERE user_id = ?", (author_id,))
        bank_money = cursor.fetchone()[0]
        if bank_money < amount:
            embed = discord.Embed(description="You don't have enough money in your bank to extract", color=discord.Color.red())
            await ctx.send(embed=embed)
            return
        
        # Mettre à jour l'argent de l'utilisateur et de sa banque
        cursor.execute("UPDATE user_data SET bank = bank - ? WHERE user_id = ?", (amount, author_id))
        cursor.execute("UPDATE user_data SET argent = argent + ? WHERE user_id = ?", (amount, author_id))
        connection.commit()

        embed = discord.Embed(title=f"{user.display_name}'s Bank", description=f"You extracted **{amount}** <:HCoins:1134169003657547847> from your bank", color=discord.Color.green())
        await ctx.send(embed=embed)

    @commands.command()
    async def bank(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        cursor.execute("SELECT bank FROM user_data WHERE user_id = ?", (user.id,))
        bank_money = cursor.fetchone()[0]

        embed = discord.Embed(title=f"{user.display_name}'s Bank", description=f"Bank Balance: **{bank_money}** <:HCoins:1134169003657547847>", color=discord.Color.blue())
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Bank(bot))
