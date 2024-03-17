import discord
from discord.ext import commands
from discord import Embed
import sqlite3
from dispie import Paginator

connection = sqlite3.connect("HallyuHeroes.db")
cursor = connection.cursor()

class Lock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def lock(self, ctx, *, arg: str):
        user_id = ctx.author.id
        successful_locks = []
        unsuccessful_locks = []
        already_locked = []
        issue_number = None  # Initialiser la variable issue_number à None
        cards_to_lock = []  # Initialiser une liste pour stocker les codes des cartes à verrouiller

        if arg.startswith("group="):
            # Extraire le nom du groupe spécifié par l'utilisateur
            group_name = arg.split("=")[1]
            cursor.execute("SELECT code_card FROM user_inventaire WHERE user_id = ? AND LOWER(groupe) = ?", (user_id, group_name.lower()))
            cards_to_lock = [row[0] for row in cursor.fetchall()]
        elif arg.startswith("name="):
            # Extraire le nom spécifié par l'utilisateur
            name = arg.split("=")[1]
            cursor.execute("SELECT code_card FROM user_inventaire WHERE user_id = ? AND LOWER(nom) = ?", (user_id, name.lower()))
            cards_to_lock = [row[0] for row in cursor.fetchall()]
        elif arg.startswith("event="):
            # Extraire l'event spécifié par l'utilisateur
            event = arg.split("=")[1]
            cursor.execute("SELECT code_card FROM user_inventaire WHERE user_id = ? AND LOWER(event) = ?", (user_id, event.lower()))
            cards_to_lock = [row[0] for row in cursor.fetchall()]
        elif arg.startswith("issue="):  # Vérifier si l'argument spécifie une issue
            issue_number = arg.split("=")[1]  # Extraire le numéro de l'issue
            cursor.execute("SELECT code_card FROM user_inventaire WHERE user_id = ? AND SUBSTR(code_card, INSTR(code_card, '-') + 1) = ?", (user_id, issue_number))
            cards_to_lock = [row[0] for row in cursor.fetchall()]
        else:
            # Si l'argument ne commence ni par "group=", ni par "name=", ni par "issue=", supposons que ce sont des codes de carte
            cards_to_lock = arg.split()

        for code_card in cards_to_lock:
            cursor.execute("SELECT * FROM user_inventaire WHERE code_card = ? and user_id = ?", (code_card, user_id))
            card_data = cursor.fetchone()

            if card_data:
                # Vérifiez si la carte n'est pas déjà verrouillée
                if not card_data[13]: 
                    # Mettez à jour la colonne lock à True
                    cursor.execute("UPDATE user_inventaire SET lock = ? WHERE code_card = ? and user_id = ?", (True, code_card, user_id))
                    connection.commit()
                    successful_locks.append(code_card)
                else:
                    already_locked.append(code_card)
            else:
                unsuccessful_locks.append(code_card)

        # Nombre de cartes verrouillées
        num_successful_locks = len(successful_locks)

        if num_successful_locks > 0:
            success_message = f"**{num_successful_locks}** card(s) successfully locked : `{', '.join(successful_locks)}`"
            embed_success = Embed(title="Locked card", description=success_message, color=discord.Color.green())
            await ctx.send(embed=embed_success)

        if already_locked:
            already_locked_message = f"Cards already locked : `{', '.join(already_locked)}`"
            embed_already_locked = Embed(title="Locked card", description=already_locked_message, color=discord.Color.orange())
            await ctx.send(embed=embed_already_locked)

        if unsuccessful_locks:
            num_unsuccessful_locks = len(unsuccessful_locks)
            fail_message = f"{num_unsuccessful_locks} card(s) not found : `{', '.join(unsuccessful_locks)}`"
            embed_fail = Embed(title="Locked card", description=fail_message, color=discord.Color.red())
            await ctx.send(embed=embed_fail)

    @commands.command()
    async def unlock(self, ctx, *, arg: str):
        user_id = ctx.author.id
        successful_unlocks = []
        unsuccessful_unlocks = []
        already_unlocked = []
        issue_number = None  # Initialiser la variable issue_number à None
        cards_to_unlock = []  # Initialiser une liste pour stocker les codes des cartes à déverrouiller

        if arg.startswith("group="):
            # Extraire le nom du groupe spécifié par l'utilisateur
            group_name = arg.split("=")[1]
            cursor.execute("SELECT code_card FROM user_inventaire WHERE user_id = ? AND LOWER(groupe) = ?", (user_id, group_name.lower()))
            cards_to_unlock = [row[0] for row in cursor.fetchall()]
        elif arg.startswith("name="):
            # Extraire le nom spécifié par l'utilisateur
            name = arg.split("=")[1]
            cursor.execute("SELECT code_card FROM user_inventaire WHERE user_id = ? AND LOWER(nom) = ?", (user_id, name.lower()))
            cards_to_unlock = [row[0] for row in cursor.fetchall()]
        elif arg.startswith("event="):
            # Extraire l'event spécifié par l'utilisateur
            event = arg.split("=")[1]
            cursor.execute("SELECT code_card FROM user_inventaire WHERE user_id = ? AND LOWER(event) = ?", (user_id, event.lower()))
            cards_to_unlock = [row[0] for row in cursor.fetchall()]
        elif arg.startswith("issue="):  
            issue_number = arg.split("=")[1]  # Extraire le numéro de l'issue
            cursor.execute("SELECT code_card FROM user_inventaire WHERE user_id = ? AND SUBSTR(code_card, INSTR(code_card, '-') + 1) = ?", (user_id, issue_number))
            cards_to_unlock = [row[0] for row in cursor.fetchall()]
        else:
            # Si l'argument ne commence ni par "group=", ni par "name=", ni par "issue=", supposons que ce sont des codes de carte
            cards_to_unlock = arg.split()

        for code_card in cards_to_unlock:
            cursor.execute("SELECT * FROM user_inventaire WHERE code_card = ? and user_id = ?", (code_card, user_id))
            card_data = cursor.fetchone()

            if card_data:
                # Vérifiez si la carte est verrouillée
                if card_data[13]:
                    # Mettez à jour la colonne lock à False
                    cursor.execute("UPDATE user_inventaire SET lock = ? WHERE code_card = ? and user_id = ?", (False, code_card, user_id))
                    connection.commit()
                    successful_unlocks.append(code_card)
                else:
                    already_unlocked.append(code_card)
            else:
                unsuccessful_unlocks.append(code_card)

        # Nombre de cartes déverrouillées
        num_successful_unlocks = len(successful_unlocks)

        if num_successful_unlocks > 0:
            success_message = f"**{num_successful_unlocks}** card(s) successfully unlocked : `{', '.join(successful_unlocks)}`"
            embed_success = Embed(title="Unlocked card", description=success_message, color=discord.Color.green())
            await ctx.send(embed=embed_success)

        if already_unlocked:
            already_unlocked_message = f"Cards already unlocked : `{', '.join(already_unlocked)}`"
            embed_already_unlocked = Embed(title="Unlocked card", description=already_unlocked_message, color=discord.Color.orange())
            await ctx.send(embed=embed_already_unlocked)

        if unsuccessful_unlocks:
            num_unsuccessful_unlocks = len(unsuccessful_unlocks)
            fail_message = f"{num_unsuccessful_unlocks} card(s) not found : `{', '.join(unsuccessful_unlocks)}`"
            embed_fail = Embed(title="Unlocked card", description=fail_message, color=discord.Color.red())
            await ctx.send(embed=embed_fail)

    @commands.command()
    async def locklist(self, ctx, member: discord.Member = None):  # Ajout du paramètre "member"
        if member is None:
            member = ctx.author  # Utilisateur par défaut : l'auteur du message

        cursor.execute("SELECT * FROM user_inventaire WHERE lock = ? AND user_id = ? ORDER BY groupe, nom, rarete, CAST(SUBSTR(code_card, INSTR(code_card, '-') + 1) AS INTEGER)", (True, member.id))
        locked_cards_data = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) FROM user_inventaire WHERE lock = ? AND user_id = ?", (True, member.id))
        count = cursor.fetchone()[0]

        if locked_cards_data:
            chunks = [locked_cards_data[i:i + 15] for i in range(0, len(locked_cards_data), 15)]
            locked_cards_list = []
            for chunk in chunks:
                embed = discord.Embed(title=f"Locked cards", color=discord.Color.green())

                for line in chunk:
                    if line[12] and line[12].lower() == 'xmas 2023':
                        rarity_emojis = {
                            "U": "<:xmas_boot:1183911398661693631>",
                            "L": "<:xmas_hat:1183911360808112160>"
                        }
                    elif line[12] and line[12].lower() == 'new year 2024':
                        rarity_emojis = {
                            "R": "<:NY_Confetti:1185996235551805470>",
                            "L": "<:NY_Fireworks:1185996232477384808>"
                        }
                    elif line[12] and line[12].lower() == 'lunar2024':
                        rarity_emojis = {
                            "L": "<:Hongbao:1205276514443067533>"
                        }
                    elif line[12] and line[12].lower() == 'valentine 2024':
                        rarity_emojis = {
                            "U": "<:Flowers:1207807685215391775>",
                            "E": "<:Arc:1207807149531729971>"
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
                    card_name = f"- {line[2]} {line[3]} {rarity_emojis.get(line[4], '')} : `{line[1]}`"
                    embed.add_field(name="", value=card_name, inline=False)
                
                embed.set_footer(text=f"Total cards: {count}")
                locked_cards_list.append(embed)

            paginator = Paginator(locked_cards_list)
            await paginator.start(ctx)
        else:
            embed_no_locked_cards = Embed(title="Locked cards", description="No card is currently locked.", color=discord.Color.blue())
            await ctx.send(embed=embed_no_locked_cards)

async def setup(bot):
    await bot.add_cog(Lock(bot))
