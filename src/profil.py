import discord
from discord.ext import commands
import sqlite3

connection = sqlite3.connect("HallyuHeroes.db")
cursor = connection.cursor()

class Profil(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def format_money(self, money):
        return "{:,}".format(money).replace(",", " ")

    @commands.command()
    async def profile(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        cursor.execute("SELECT * FROM user_data WHERE user_id = ?", (str(user.id),))
        result = cursor.fetchone()

        if result is not None:
            description = result[1]
            argent = result[2]
            formatted_argent = self.format_money(argent)

            cursor.execute("SELECT COUNT(*) FROM user_inventaire WHERE user_id = ?", (str(user.id),))
            nombre_de_cartes = cursor.fetchone()[0]

            cursor.execute("SELECT COALESCE(bronze, 0) FROM user_data WHERE user_id = ?", (str(user.id),))
            packs_bronze = cursor.fetchone()[0]

            cursor.execute("SELECT COALESCE(silver, 0) FROM user_data WHERE user_id = ?", (str(user.id),))
            packs_silver = cursor.fetchone()[0]

            cursor.execute("SELECT COALESCE(gold, 0) FROM user_data WHERE user_id = ?", (str(user.id),))
            packs_gold = cursor.fetchone()[0]

            cursor.execute("SELECT COALESCE(legendary, 0) FROM user_data WHERE user_id = ?", (str(user.id),))
            packs_legendaire = cursor.fetchone()[0]

            # Get the favorite card from the user_data table
            cursor.execute("SELECT carte_favori FROM user_data WHERE user_id = ?", (str(user.id),))
            carte_favori = cursor.fetchone()[0]

            # Check if the favorite card is still in the user's inventory
            cursor.execute("SELECT code_card FROM user_inventaire WHERE user_id = ? AND code_card = ?", (user.id, carte_favori))
            favorite_card_available = cursor.fetchone() is not None

            if not favorite_card_available:
                # If the favorite card is not in the user's inventory, set it to None
                carte_favori = "None"

        else:
            description = "Welcome on my profile!"
            argent = 0
            formatted_argent = self.format_money(argent)
            nombre_de_cartes = 0
            carte_favori = "None"
            packs_bronze = 0
            packs_silver = 0
            packs_gold = 0
            packs_legendaire = 0

        embed = discord.Embed(title=f"{user.name}'s profile", description=description, color=discord.Color.blue())
        embed.add_field(name="", value=f":moneybag: **Wallet** : {formatted_argent} <:HCoins:1134169003657547847>", inline=False)
        embed.add_field(name="", value=f":flower_playing_cards: **Inventory** : {nombre_de_cartes}", inline=False)
        embed.add_field(name="", value=f":heart: **Favorite card** : {carte_favori}\n\n", inline=False)
        embed.add_field(name="PACKS", value=f"<:Bronze:1136312536665440387> **Bronze** : {packs_bronze}\n<:Argent:1136312524900401213>  **Silver** : {packs_silver}\n<:Gold:1136312506957189131> **Gold** : {packs_gold}\n<:Legendary:1136312609449193544> **Legendary** : {packs_legendaire}", inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def description(self, ctx, *, new_description):
        user = ctx.author

        cursor.execute("SELECT * FROM user_data WHERE user_id = ?", (str(user.id),))
        result = cursor.fetchone()

        if result is not None:
            cursor.execute("UPDATE user_data SET description = ? WHERE user_id = ?", (new_description, str(user.id)))
        else:
            cursor.execute("INSERT INTO user_data VALUES (?, ?, ?, ?, ?)", (str(user.id), new_description, 0, 0, ""))

        connection.commit()

        # Create an embed for the updated description response
        updated_embed = discord.Embed(title="**UPDATED DESCRIPTION**", description=new_description, color=discord.Color.green())
        await ctx.send(embed=updated_embed)

async def setup(bot):
    await bot.add_cog(Profil(bot))
