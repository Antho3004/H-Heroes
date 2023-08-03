import discord
from discord.ext import commands
import sqlite3

connection = sqlite3.connect("HallyuHeroes.db")
cursor = connection.cursor()

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def shop(self, ctx):
        packs = ["Bronze", "Silver", "Gold", "Legendary"]
        # ... (existing code for the shop command)

    @commands.command()
    async def buy_pack(self, ctx, pack_name: str):
        packs = {
            "bronze": 3000,
            "silver": 7000,
            "gold": 15000,
            "legendary": 25000
        }

        pack_name_lower = pack_name.lower()
        if pack_name_lower not in packs:
            embed = discord.Embed(title="**SHOP**", description="This pack does not exist. Available packs: **bronze**/**silver**/**gold**/**legendary**", color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        price = packs[pack_name_lower]

        # Vérifier si l'utilisateur a assez d'argent
        user_id = ctx.author.id
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

async def setup(bot):
    await bot.add_cog(Shop(bot))
