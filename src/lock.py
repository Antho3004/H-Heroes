import discord
from discord.ext import commands
from discord import Embed
import sqlite3

connection = sqlite3.connect("HallyuHeroes.db")
cursor = connection.cursor()

class Lock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def lock(self, ctx, *code_cards):
        successful_locks = []
        unsuccessful_locks = []
        already_locked = []

        for code_card in code_cards:
            cursor.execute("SELECT * FROM user_inventaire WHERE code_card = ?", (code_card,))
            card_data = cursor.fetchone()

            if card_data:
                # Vérifiez si la carte n'est pas déjà verrouillée
                if not card_data[13]: 
                    # Mettez à jour la colonne lock à True
                    cursor.execute("UPDATE user_inventaire SET lock = ? WHERE code_card = ?", (True, code_card))
                    connection.commit()
                    successful_locks.append(code_card)
                else:
                    already_locked.append(code_card)
            else:
                unsuccessful_locks.append(code_card)

        if successful_locks:
            success_message = f"Cards successfully locked : `{', '.join(successful_locks)}`"
            embed_success = Embed(title="Locked card", description=success_message, color=discord.Color.green())
            await ctx.send(embed=embed_success)

        if already_locked:
            already_locked_message = f"Cards already locked : `{', '.join(already_locked)}`"
            embed_already_locked = Embed(title="Locked card", description=already_locked_message, color=discord.Color.orange())
            await ctx.send(embed=embed_already_locked)

        if unsuccessful_locks:
            fail_message = f"Cartes non trouvées : `{', '.join(unsuccessful_locks)}`"
            embed_fail = Embed(title="Locked card", description=fail_message, color=discord.Color.red())
            await ctx.send(embed=embed_fail)

    @commands.command()
    async def unlock(self, ctx, *code_cards):
        successful_unlocks = []
        unsuccessful_unlocks = []
        already_unlocked = []

        for code_card in code_cards:
            cursor.execute("SELECT * FROM user_inventaire WHERE code_card = ?", (code_card,))
            card_data = cursor.fetchone()

            if card_data:
                # Vérifiez si la carte est verrouillée
                if card_data[13]:
                    # Mettez à jour la colonne lock à False
                    cursor.execute("UPDATE user_inventaire SET lock = ? WHERE code_card = ?", ("NULL", code_card))
                    connection.commit()
                    successful_unlocks.append(code_card)
                else:
                    already_unlocked.append(code_card)
            else:
                unsuccessful_unlocks.append(code_card)

        if successful_unlocks:
            success_message = f"Cards successfully unlocked : `{', '.join(successful_unlocks)}`"
            embed_success = Embed(title="Locked card", description=success_message, color=discord.Color.green())
            await ctx.send(embed=embed_success)

        if already_unlocked:
            already_unlocked_message = f"Cards already unlocked : `{', '.join(already_unlocked)}`"
            embed_already_unlocked = Embed(title="Locked card", description=already_unlocked_message, color=discord.Color.orange())
            await ctx.send(embed=embed_already_unlocked)

        if unsuccessful_unlocks:
            fail_message = f"Cards not found : `{', '.join(unsuccessful_unlocks)}`"
            embed_fail = Embed(title="Locked card", description=fail_message, color=discord.Color.red())
            await ctx.send(embed=embed_fail)

    @commands.command()
    async def lock_view(self, ctx):
        cursor.execute("SELECT * FROM user_inventaire WHERE lock = ? AND user_id = ? ORDER BY groupe, nom, rarete", (True, ctx.author.id))
        locked_cards_data = cursor.fetchall()

        if locked_cards_data:
            locked_cards_list = []
            for card in locked_cards_data:
                card_code = card[1]
                card_name = card[3]
                card_group = card[2] 
                if card[12] and card[12].lower() == 'xmas 2023':
                    rarity_emojis = {
                        "U": "<:xmas_boot:1183911398661693631>",
                        "L": "<:xmas_hat:1183911360808112160>"
                    }
                elif card[12] and card[12].lower() == 'new year 2024':
                    rarity_emojis = {
                        "R": "<:NY_Confetti:1185996235551805470>",
                        "L": "<:NY_Fireworks:1185996232477384808>"
                    }
                else:
                    rarity_emojis = {
                        "C": "<:C_:1107771999490686987>",
                        "U": "<:U_:1107772008193867867>",
                        "R": "<:R_:1107772004410601553>",
                        "E": "<:E_:1107772001747222550>",
                        "L": "<:L_:1107772002690945055>"
                    }

                # Accéder à la clé correcte du dictionnaire pour obtenir l'emoji de rareté
                rarity_emoji = rarity_emojis.get(card[4])

                locked_cards_list.append(f"- {card_group} {card_name} {rarity_emoji} : `{card_code}`")

            locked_cards_message = "\n".join(locked_cards_list)
            embed_locked_cards = Embed(title="Locked cards", description=locked_cards_message, color=discord.Color.blue())
            await ctx.send(embed=embed_locked_cards)
        else:
            embed_no_locked_cards = Embed(title="Locked cards", description="No card is currently locked.", color=discord.Color.blue())
            await ctx.send(embed=embed_no_locked_cards)



async def setup(bot):
    await bot.add_cog(Lock(bot))