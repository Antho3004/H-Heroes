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
    
    def format_money(self, money):
        return "{:,}".format(money).replace(",", " ")

    @commands.command()
    async def burn(self, ctx, *, arg: str):
        user_id = ctx.author.id
        total_money_reward = 0  # Variable pour stocker la somme totale d'argent gagnée
        card_burn = 0 # Variable pour stocker le nombre de carte bruler
        error_occurred = False  # Indicateur d'erreur

        # Vérifiez si l'argument commence par "issue=" pour déterminer si l'utilisateur veut brûler par l'issue ou par le code de la carte
        if arg.startswith("issue="):
            # Extraire la plage d'issues spécifiée par l'utilisateur
            issue_range = arg.split("=")[1]
            start_issue, end_issue = map(int, issue_range.split('-'))
            # Mettre en œuvre la logique pour brûler les cartes dans la plage d'issues spécifiée
            cursor.execute("SELECT code_card FROM user_inventaire WHERE user_id = ? AND CAST(SUBSTR(code_card, INSTR(code_card, '-') + 1) AS INTEGER) BETWEEN ? AND ?", (user_id, start_issue, end_issue))
            codes_cards = [row[0] for row in cursor.fetchall()]
        else:
            codes_cards = arg.split()  # Si l'argument ne commence pas par "issue=", supposons que ce sont des codes de carte

        locked_cards = []  # Liste pour stocker les cartes lockées
        burned_cards = []  # Liste pour stocker les cartes déjà brûlées

        for code_card in codes_cards:
            # Check if the user has the card in their inventory
            cursor.execute("SELECT * FROM user_inventaire WHERE user_id = ? AND code_card = ?", (user_id, code_card))
            existing_card = cursor.fetchone()

            if not existing_card:
                burned_cards.append(code_card)  # Ajouter la carte déjà brûlée à la liste
                continue

            # Check if the card is in the market
            cursor.execute("SELECT * FROM market WHERE code_card = ?", (code_card,))
            card_in_market = cursor.fetchone()

            if card_in_market:
                embed = Embed(title="Card Burning Error", description=f"You must remove the card `{code_card}` from the marketplace before burning it", color=discord.Color.red())
                await ctx.send(embed=embed)
                error_occurred = True  # Une erreur s'est produite
                continue  # Move to the next card in case of error

            # Check if the card is in the user_inventaire with lock "True"
            cursor.execute("SELECT * FROM user_inventaire WHERE code_card = ?", (code_card,))
            lock = cursor.fetchone()

            if lock[13] == True:
                locked_cards.append(code_card)  # Ajouter la carte lockée à la liste
                continue  # Move to the next card

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
            card_burn += 1


        connection.commit()

        cursor.execute("SELECT argent FROM user_data WHERE user_id = ?", (str(user_id),))
        updated_amount = cursor.fetchone()[0]
        updated_formatted_amount = self.format_money(updated_amount)

        if burned_cards:
            # Construire le message avec les cartes déjà brûlées
            burned_cards_str = ", ".join(burned_cards)
            embed = Embed(title="Warning Card Burning", description=f"You burned **{card_burn}** cards and gained a total of **{total_money_reward}** <:HCoins:1134169003657547847>\n\nNew balance : **{updated_formatted_amount}** <:HCoins:1134169003657547847>\n\nPlease note that `{burned_cards_str}` are already burned.", color=discord.Color.orange())
            await ctx.send(embed=embed)
            error_occurred = True

        if locked_cards:
            # Construire le message avec les cartes lockées
            locked_cards_str = ", ".join(locked_cards)
            embed = Embed(title="Warning Card Burning", description=f"You burned **{card_burn}** cards and gained a total of **{total_money_reward}** <:HCoins:1134169003657547847>\n\nNew balance : **{updated_formatted_amount}** <:HCoins:1134169003657547847>\n\nPlease note that `{locked_cards_str}` cards are blocked. If you want to burn them, unlock them first.", color=discord.Color.orange())
            await ctx.send(embed=embed)
            error_occurred = True

        if not error_occurred:  # Exécuter seulement si aucune erreur ne s'est produite
            # Confirmation message in an embed with the total money reward
            embed = Embed(title="Cards Burned Successfully", description=f"You burned **{card_burn}** cards and gained a total of **{total_money_reward}** <:HCoins:1134169003657547847>\n\nNew balance : **{updated_formatted_amount}** <:HCoins:1134169003657547847>", color=discord.Color.green())
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Burn(bot))


