import discord
from discord.ext import commands
import sqlite3
import asyncio

connection = sqlite3.connect("HallyuHeroes.db")
cursor = connection.cursor()

class Inventaire(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def show_inventory(self, ctx, user, page):
        cursor.execute("SELECT COUNT(*) FROM user_inventaire WHERE user_id = ?", (str(user.id),))
        count = cursor.fetchone()[0]

        if count > 0:
            cursor.execute("SELECT code_card, nom, groupe, rarete FROM user_inventaire WHERE user_id = ? ORDER BY groupe, nom", (str(user.id),))
            result = cursor.fetchall()

            items_per_page = 9
            total_pages = (count + items_per_page - 1) // items_per_page
            page = max(1, min(page, total_pages))

            start_idx = (page - 1) * items_per_page
            end_idx = min(start_idx + items_per_page, count)

            embed = discord.Embed(title=f"{user.name}'s inventory", color=discord.Color.green())

            for i in range(start_idx, end_idx):
                row = result[i]
                code_card = row[0]
                nom = row[1]
                groupe = row[2]
                rarete = row[3]

                rarity_emojis = {
                    "C": "<:C_:1107771999490686987>",
                    "U": "<:U_:1107772008193867867>",
                    "R": "<:R_:1107772004410601553>",
                    "E": "<:E_:1107772001747222550>",
                    "L": "<:L_:1107772002690945055>"
                }

                rarity_emoji = rarity_emojis.get(rarete, "")

                embed.add_field(name=f"{code_card}", value=f"Name : {nom}\nGroup : {groupe}\nRareté : {rarity_emoji}\n", inline=True)

            embed.set_footer(text=f"Page {page}/{total_pages} - You have {count} cards")
            msg = await ctx.send(embed=embed)

            if total_pages > 1:
                await msg.add_reaction("⬅️")
                await msg.add_reaction("➡️")

                def check(reaction, user):
                    return user == ctx.author and str(reaction.emoji) in ["⬅️", "➡️"]

                while True:
                    try:
                        reaction, _ = await self.bot.wait_for("reaction_add", timeout=60.0, check=check)

                        if str(reaction.emoji) == "➡️" and page < total_pages:
                            page += 1
                        elif str(reaction.emoji) == "⬅️" and page > 1:
                            page -= 1

                        # Update the embed with new page data
                        start_idx = (page - 1) * items_per_page
                        end_idx = min(start_idx + items_per_page, count)
                        embed.clear_fields()
                        for i in range(start_idx, end_idx):
                            row = result[i]
                            code_card = row[0]
                            nom = row[1]
                            groupe = row[2]
                            rarete = row[3]
                            rarity_emoji = rarity_emojis.get(rarete, "")
                            embed.add_field(name=f"{code_card}", value=f"Name : {nom}\nGroup : {groupe}\nRareté : {rarity_emoji}\n", inline=True)
                        embed.set_footer(text=f"Page {page}/{total_pages} - You have {count} cards")
                        await msg.edit(embed=embed)

                    except asyncio.TimeoutError:
                        await msg.clear_reactions()
                        break

        else:
            embed = discord.Embed(title=f"{user.name}'s inventory", description="Your inventaire is empty.", color=discord.Color.red())
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
