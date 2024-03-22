import discord
from discord.ext import commands
import sqlite3
from dispie import Paginator

connection = sqlite3.connect("HallyuHeroes.db")
cursor = connection.cursor()

class Atlas(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def show_atlas(self, ctx, filter_type, filter_value):
        # Convertir la valeur du filtre en minuscules
        filter_value = filter_value.lower() if filter_value else None

        if filter_type == "name":
            # Filtrer par nom de carte
            cursor.execute(f"SELECT COUNT(*) FROM cards WHERE LOWER(nom) = ?", (filter_value,))
        elif filter_type == "group":
            # Filtrer par groupe
            cursor.execute(f"SELECT COUNT(*) FROM cards WHERE LOWER(groupe) = ?", (filter_value,))
        elif filter_type == "rarity":
            # Filtrer par groupe
            cursor.execute(f"SELECT COUNT(*) FROM cards WHERE LOWER(rarete) = ?", (filter_value,))
        elif filter_type == "event":
            # Filtrer par event
            cursor.execute(f"SELECT COUNT(*) FROM cards WHERE LOWER(event) = ?", (filter_value,))
        else:
            # Pas de filtre, afficher tous les éléments
            cursor.execute(f"SELECT COUNT(*) FROM cards")

        count = cursor.fetchone()[0]

        if count > 0:
            if filter_type:
                if filter_type == "name":
                    cursor.execute(f"SELECT code_card, nom, groupe, rarete, event FROM cards WHERE LOWER(nom) = ? ORDER BY groupe, nom, rarete, CAST(SUBSTR(code_card, INSTR(code_card, '-') + 1) AS INTEGER)", (filter_value,))
                elif filter_type == "group":
                    cursor.execute(f"SELECT code_card, nom, groupe, rarete, event FROM cards WHERE LOWER(groupe) = ? ORDER BY groupe, nom, rarete, CAST(SUBSTR(code_card, INSTR(code_card, '-') + 1) AS INTEGER)", (filter_value,))
                elif filter_type == "rarity":
                    cursor.execute(f"SELECT code_card, nom, groupe, rarete, event FROM cards WHERE LOWER(rarete) = ? ORDER BY groupe, nom, rarete, CAST(SUBSTR(code_card, INSTR(code_card, '-') + 1) AS INTEGER)", (filter_value,))
                elif filter_type == "event":
                    cursor.execute(f"SELECT code_card, nom, groupe, rarete, event FROM cards WHERE LOWER(event) = ? ORDER BY groupe, nom, rarete, CAST(SUBSTR(code_card, INSTR(code_card, '-') + 1) AS INTEGER)", (filter_value,))
            else:
                cursor.execute(f"SELECT code_card, nom, groupe, rarete, event FROM cards ORDER BY groupe, nom, rarete, CAST(SUBSTR(code_card, INSTR(code_card, '-') + 1) AS INTEGER)")

            result = cursor.fetchall()

            if not result:
                # Aucun résultat trouvé avec le filtre spécifié
                embed = discord.Embed(title=f"Atlas", description=f"Atlas is empty.", color=discord.Color.red())
                await ctx.send(embed=embed)
                return

            chunks = [result[i:i + 15] for i in range(0, len(result), 15)]

            embeds = []

            for chunk in chunks:
                embed = discord.Embed(title=f"Atlas", color=discord.Color.green())

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
                    elif line[4] and line[4].lower() == 'lunar2024':
                        rarity_emojis = {
                            "L": "<:Hongbao:1205276514443067533>"
                        }
                    elif line[4] and line[4].lower() == 'valentine 2024':
                        rarity_emojis = {
                            "U": "<:Flowers:1207807685215391775>",
                            "E": "<:Arc:1207807149531729971>"
                    }
                    elif line[4] and line[4].lower() == 'spring 2024':
                        rarity_emojis = {
                            "U": "<:Marigold:1220794525094772806>",
                            "R": "<:Sakura:1220794502944657460>"
                    }
                    else:
                        rarity_emojis = {
                            "C": "<:C_:1107771999490686987>",
                            "U": "<:U_:1107772008193867867>",
                            "R": "<:R_:1107772004410601553>",
                            "E": "<:E_:1107772001747222550>",
                            "L": "<:L_:1107772002690945055>"
                        }

                    card_name = f"- {line[2]} {line[1]} {rarity_emojis.get(line[3], '')} : `{line[0]}`"
                    embed.add_field(name="", value=card_name, inline=False)

                embed.set_footer(text=f"Total cards: {count}")
                embeds.append(embed)

            paginator = Paginator(embeds)
            await paginator.start(ctx)

        else:
            embed = discord.Embed(title=f"Atlas", description="Atlas is empty.", color=discord.Color.red())
            await ctx.send(embed=embed)

    @commands.command()
    async def atlas(self, ctx, *, filter_arg=None):

        if filter_arg:
            # Utiliser split("=") une seule fois pour séparer le type de filtre et la valeur du filtre
            filter_parts = filter_arg.split("=")

            # Le type de filtre est la première partie
            filter_type = filter_parts[0].lower()

            # La valeur du filtre est le reste de la chaîne, y compris les espaces
            filter_value = "=".join(filter_parts[1:])

            await self.show_atlas(ctx, filter_type, filter_value)
        else:
            await self.show_atlas(ctx, None, None)

async def setup(bot):
    await bot.add_cog(Atlas(bot))
