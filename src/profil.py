import discord
from discord.ext import commands, tasks
import sqlite3


connection = sqlite3.connect("HallyuHeroes.db")
cursor = connection.cursor()

class Profil(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def format_money(self, money):
        return "{:,}".format(money).replace(",", " ")

    async def show_profile(self, ctx, user):
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

            cursor.execute("SELECT COALESCE(training, 0) FROM user_data WHERE user_id = ?", (str(user.id),))
            packs_training = cursor.fetchone()[0]

            cursor.execute("SELECT COALESCE(work, 0) FROM user_data WHERE user_id = ?", (str(user.id),))
            number_work = cursor.fetchone()[0]

            cursor.execute("SELECT carte_favori FROM user_data WHERE user_id = ?", (str(user.id),))
            carte_favori = cursor.fetchone()[0]

            cursor.execute("SELECT team_favorite FROM user_data WHERE user_id = ?", (str(user.id),))
            team_favorite = cursor.fetchone()[0]

            cursor.execute("SELECT battle_win, battle_lose FROM user_data WHERE user_id = ?", (str(user.id),))
            battle_stat = cursor.fetchone()

            win_rate = 0 if (battle_stat[0] + battle_stat[1]) == 0 else (battle_stat[0] / (battle_stat[0] +battle_stat[1])) * 100

            cursor.execute("select user_inventaire.image_url from user_data join user_inventaire on user_data.carte_favori = user_inventaire.code_card WHERE user_inventaire.user_id = ?", (str(user.id),))
            img_fav = cursor.fetchone()

            cursor.execute("SELECT code_card FROM user_inventaire WHERE user_id = ? AND code_card = ?", (user.id, carte_favori))
            favorite_card_available = cursor.fetchone() is not None

            cursor.execute("SELECT team_name FROM team WHERE user_id = ? AND team_name = ?", (user.id, team_favorite))
            favorite_team_available = cursor.fetchone() is not None

            if not favorite_card_available:
                carte_favori = "None"
            
            if not favorite_team_available:
                team_favorite = "None"

            if img_fav is not None:
                img_fav = img_fav[0]

        else:
            embed = discord.Embed(title="**Profile Not Found**", description="You don't have an account, use `$start` to create one.", color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(title=f"{user.name}'s profile", description=description, color=discord.Color.blue())
        embed.add_field(name="", value=f":moneybag: **Wallet** : {formatted_argent} <:HCoins:1134169003657547847>\n:flower_playing_cards: **Inventory** : {nombre_de_cartes}\n:heart: **Favorite card** : {carte_favori}\n<:team:1190045726139494440> **Favorite team** : {team_favorite}\n:crossed_swords: **Battle Winrate : {win_rate:.2f}%**\n:hammer_pick: **Works** : {number_work}", inline=False)
        embed.add_field(name="PACKS", value=f"<:Bronze:1136312536665440387> **Bronze** : {packs_bronze}\n<:Argent:1136312524900401213> **Silver** : {packs_silver}\n<:Gold:1136312506957189131> **Gold** : {packs_gold}\n<:Legendary:1136312609449193544> **Legendary** : {packs_legendaire}\n:person_lifting_weights: **Training** : {packs_training}", inline=False)
        embed.add_field(name="ACHIEVEMENT", value=f"Soon\n", inline=False)

        embed.set_image(url=img_fav)

        await ctx.send(embed=embed)

    @commands.command()
    async def profile(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        await self.show_profile(ctx, user)

    @commands.command(name='pr')
    async def shortcut_profile(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        await self.show_profile(ctx, user)

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

        updated_embed = discord.Embed(title="**UPDATED DESCRIPTION**", description=new_description, color=discord.Color.green())
        await ctx.send(embed=updated_embed)

async def setup(bot):
    await bot.add_cog(Profil(bot))
