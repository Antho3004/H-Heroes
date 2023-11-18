import discord
from discord.ext import commands
import sqlite3
from dispie import Paginator

connection = sqlite3.connect("HallyuHeroes.db")
cursor = connection.cursor()

class Inventaire(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def show_inventory(self, ctx: commands.Context, user, page):
        cursor.execute("SELECT COUNT(*) FROM user_inventaire WHERE user_id = ?", (str(user.id),))
        count = cursor.fetchone()[0]

        if count > 0:
            cursor.execute("SELECT code_card, nom, groupe, rarete FROM user_inventaire WHERE user_id = ? ORDER BY groupe, nom, rarete, CAST(SUBSTR(code_card, INSTR(code_card, '-') + 1) AS INTEGER)", (str(user.id),))

            result = cursor.fetchall()

            rarity_emojis = {
                "C": "<:C_:1107771999490686987>",
                "U": "<:U_:1107772008193867867>",
                "R": "<:R_:1107772004410601553>",
                "E": "<:E_:1107772001747222550>",
                "L": "<:L_:1107772002690945055>"
            }

            # Divisez vos données en morceaux de 9 cartes par page
            chunks = [result[i:i + 9] for i in range(0, len(result), 9)]

            embeds = []

            for chunk in chunks:
                embed = discord.Embed(title=f"{user.name}'s inventory", color=discord.Color.green())

                for line in chunk:
                    embed.add_field(
                        name=f"{line[0]}", value=f"Name: {line[1]}\nGroup: {line[2]}\nRarity: {rarity_emojis.get(line[3], '')}\n", inline=True)

                # Ajoutez le nombre de cartes au pied de l'embed
                embed.set_footer(text=f"Total cards: {count}")
                embeds.append(embed)

            # Créez un objet Paginator en passant la liste d'embeds
            paginator = Paginator(embeds)

            # Démarrez la pagination
            await paginator.start(ctx)

        else:
            embed = discord.Embed(title=f"{user.name}'s inventory", description="Your inventory is empty.", color=discord.Color.red())
            await ctx.send(embed=embed)

    @commands.command()
    async def inventory(self, ctx, user: discord.Member = None, page: int = 1):
        if user is None:
            user = ctx.author

        await self.show_inventory(ctx, user, page)

    @commands.command(name='inv')
    async def shortcut_inventory(self, ctx, user: discord.Member = None, page: int = 1):
        if user is None:
            user = ctx.author

        await self.show_inventory(ctx, user, page)

async def setup(bot):
    await bot.add_cog(Inventaire(bot))
