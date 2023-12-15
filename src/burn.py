import discord
from discord.ext import commands
from discord import Embed
import sqlite3
import random

connection = sqlite3.connect("HallyuHeroes.db")
cursor = connection.cursor()

class Burn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def burn(self, ctx, *codes_cards: str):
        user_id = ctx.author.id
        total_money_reward = 0  # Variable pour stocker la somme totale d'argent gagnée

        for code_card in codes_cards:
            # Check if the user has the card in their inventory
            cursor.execute("SELECT * FROM user_inventaire WHERE user_id = ? AND code_card = ?", (user_id, code_card))
            existing_card = cursor.fetchone()

            if not existing_card:
                embed = Embed(title="Card Burning Error", description=f"You do not have the card `{code_card}` in your inventory", color=discord.Color.red())
                await ctx.send(embed=embed)
                continue  # Move to the next card in case of error

            # Get the amount of money to add (for example, 50 to illustrate, you can adjust this)
            carte_rarete = existing_card[4]
            if carte_rarete == "C":
                money_reward = random.randint(10, 100)
            elif carte_rarete == "U":
                money_reward = random.randint(100, 200)
            elif carte_rarete == "R":
                money_reward = random.randint(200, 300)
            elif carte_rarete == "E":
                money_reward = random.randint(300, 400)
            elif carte_rarete == "L":
                money_reward = random.randint(400, 500)

            # Add money to the user
            cursor.execute("UPDATE user_data SET argent = argent + ? WHERE user_id = ?", (money_reward, user_id))
            total_money_reward += money_reward  # Ajouter la récompense à la somme totale

            # Remove the card from the user's inventory
            cursor.execute("DELETE FROM user_inventaire WHERE user_id = ? AND code_card = ?", (user_id, code_card))

        connection.commit()

        # Confirmation message in an embed with the total money reward
        embed = Embed(title="Cards Burned Successfully", description=f"You burned **{len(codes_cards)}** cards and gained a total of **{total_money_reward}** <:HCoins:1134169003657547847>", color=discord.Color.green())
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Burn(bot))
