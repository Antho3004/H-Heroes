import discord
from discord.ext import commands
import sqlite3
from dispie import Paginator

connection = sqlite3.connect("HallyuHeroes.db")
cursor = connection.cursor()

class Inventaire(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def show_inventory(self, ctx, user, filter_type, filter_value):
        # Convertir la valeur du filtre en minuscules
        filter_value = filter_value.lower() if filter_value else None

        if filter_type == "name":
            # Filtrer par nom de carte
            cursor.execute(f"SELECT COUNT(*) FROM user_inventaire WHERE user_id = ? AND LOWER(nom) = ?", (str(user.id), filter_value))
        elif filter_type == "group":
            # Filtrer par groupe
            cursor.execute(f"SELECT COUNT(*) FROM user_inventaire WHERE user_id = ? AND LOWER(groupe) = ?", (str(user.id), filter_value))
        elif filter_type == "rarity":
            # Filtrer par groupe
            cursor.execute(f"SELECT COUNT(*) FROM user_inventaire WHERE user_id = ? AND LOWER(rarete) = ?", (str(user.id), filter_value))
        elif filter_type == "event":
            # Filtrer par event
            cursor.execute(f"SELECT COUNT(*) FROM user_inventaire WHERE user_id = ? AND LOWER(event) = ?", (str(user.id), filter_value))
        else:
            # Pas de filtre, afficher tous les éléments
            cursor.execute(f"SELECT COUNT(*) FROM user_inventaire WHERE user_id = ?", (str(user.id),))

        count = cursor.fetchone()[0]

        if count > 0:
            if filter_type:
                if filter_type == "name":
                    cursor.execute(f"SELECT code_card, nom, groupe, rarete, event FROM user_inventaire WHERE user_id = ? AND LOWER(nom) = ? ORDER BY groupe, nom, rarete, CAST(SUBSTR(code_card, INSTR(code_card, '-') + 1) AS INTEGER)", (str(user.id), filter_value))
                elif filter_type == "group":
                    cursor.execute(f"SELECT code_card, nom, groupe, rarete, event FROM user_inventaire WHERE user_id = ? AND LOWER(groupe) = ? ORDER BY groupe, nom, rarete, CAST(SUBSTR(code_card, INSTR(code_card, '-') + 1) AS INTEGER)", (str(user.id), filter_value))
                elif filter_type == "rarity":
                    cursor.execute(f"SELECT code_card, nom, groupe, rarete, event FROM user_inventaire WHERE user_id = ? AND LOWER(rarete) = ? ORDER BY groupe, nom, rarete, CAST(SUBSTR(code_card, INSTR(code_card, '-') + 1) AS INTEGER)", (str(user.id), filter_value))
                elif filter_type == "event":
                    cursor.execute(f"SELECT code_card, nom, groupe, rarete, event FROM user_inventaire WHERE user_id = ? AND LOWER(event) = ? ORDER BY groupe, nom, rarete, CAST(SUBSTR(code_card, INSTR(code_card, '-') + 1) AS INTEGER)", (str(user.id), filter_value))
            else:
                cursor.execute(f"SELECT code_card, nom, groupe, rarete, event FROM user_inventaire WHERE user_id = ? ORDER BY groupe, nom, rarete, CAST(SUBSTR(code_card, INSTR(code_card, '-') + 1) AS INTEGER)", (str(user.id),))

            result = cursor.fetchall()

            if not result:
                # Aucun résultat trouvé avec le filtre spécifié
                embed = discord.Embed(title=f"{user.name}'s inventory", description=f"No cards found in the inventory with the specified filter.", color=discord.Color.red())
                await ctx.send(embed=embed)
                return

            chunks = [result[i:i + 9] for i in range(0, len(result), 9)]

            embeds = []

            for chunk in chunks:
                embed = discord.Embed(title=f"{user.name}'s inventory", color=discord.Color.green())

                for line in chunk:
                        if line[4] and line[4].lower() == 'xmas 2023':
                            rarity_emojis = {
                                "U": "<:xmas_boot:1183911398661693631>",
                                "L": "<:xmas_hat:1183911360808112160>"
                            }
                        elif line[4] and line[4].lower() == 'new year 2024':
                            rarity_emojis = {
                                "R": "<:NY_Confetti:1185996235551805470>",
                                "L": "<:NY_Fireworks:1185996232477384808>"
                            }
                        elif line[4] and line[4].lower() == 'lunar 2024':
                            rarity_emojis = {
                                "L": "<:Hongbao:1205276514443067533>"
                            }
                        else:
                            rarity_emojis = {
                                "C": "<:C_:1107771999490686987>",
                                "U": "<:U_:1107772008193867867>",
                                "R": "<:R_:1107772004410601553>",
                                "E": "<:E_:1107772001747222550>",
                                "L": "<:L_:1107772002690945055>"
                            }

                        card_name = f"{line[0]}"
                        card_info = ""

                        # Check if the event is present and not NULL
                        if line[4] is not None:
                            card_info += f"Event: {line[4]}\n"

                        card_info += f"Name: {line[1]}\nGroup: {line[2]}\n"
                        card_info += f"Rarity: {rarity_emojis.get(line[3], '')}\n"

                        embed.add_field(name=card_name, value=card_info, inline=True)

                embed.set_footer(text=f"Total cards: {count}")
                embeds.append(embed)

            paginator = Paginator(embeds)
            await paginator.start(ctx)

        else:
            embed = discord.Embed(title=f"{user.name}'s inventory", description="The inventory is empty.", color=discord.Color.red())
            await ctx.send(embed=embed)

    @commands.command()
    async def inventory(self, ctx, user: discord.Member = None, *, filter_arg=None):
        if user is None:
            user = ctx.author
        else:
            # Correction pour obtenir l'utilisateur mentionné
            user = ctx.guild.get_member(int(user.id))

        if filter_arg:
            # Utiliser split("=") une seule fois pour séparer le type de filtre et la valeur du filtre
            filter_parts = filter_arg.split("=")

            # Le type de filtre est la première partie
            filter_type = filter_parts[0].lower()

            # La valeur du filtre est le reste de la chaîne, y compris les espaces
            filter_value = "=".join(filter_parts[1:])

            await self.show_inventory(ctx, user, filter_type, filter_value)
        else:
            await self.show_inventory(ctx, user, None, None)

    @commands.command(name='inv')
    async def shortcut_inventory(self, ctx, user: discord.Member = None, *, filter_arg=None):
        if user is None:
            user = ctx.author
        else:
            # Correction pour obtenir l'utilisateur mentionné
            user = ctx.guild.get_member(int(user.id))

        if filter_arg:
            # Utiliser split("=") une seule fois pour séparer le type de filtre et la valeur du filtre
            filter_parts = filter_arg.split("=")

            # Le type de filtre est la première partie
            filter_type = filter_parts[0].lower()

            # La valeur du filtre est le reste de la chaîne, y compris les espaces
            filter_value = "=".join(filter_parts[1:])

            await self.show_inventory(ctx, user, filter_type, filter_value)
        else:
            await self.show_inventory(ctx, user, None, None)

async def setup(bot):
    await bot.add_cog(Inventaire(bot))
