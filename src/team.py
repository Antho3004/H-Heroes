import discord
from discord.ext import commands
import sqlite3
from dispie import Paginator

connection = sqlite3.connect("HallyuHeroes.db")
cursor = connection.cursor()

class Team(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def make_team(self, ctx, team_name, code_card1, code_card2, code_card3, code_card4, code_card5):
        user_id = ctx.author.id

        # Check if the user provided exactly 5 unique cards
        if len(set([team_name, code_card1, code_card2, code_card3, code_card4, code_card5])) != 6:
            embed = discord.Embed(title="Team Creation Failed",
                                description="To create a team, please follow this format: teamName + codeCarte + codeCarte + codeCarte + codeCarte + codeCarte",
                                color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        # Check if the user entered exactly 5 cards after the team name
        if not all([code_card1, code_card2, code_card3, code_card4, code_card5]):
            embed = discord.Embed(title="Team Creation Failed",
                                description="To create a team, please follow this format: teamName + codeCarte + codeCarte + codeCarte + codeCarte + codeCarte",
                                color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        # Check if the user owns the specified cards in their inventory
        cursor.execute("SELECT code_card FROM user_inventaire WHERE user_id = ? AND code_card IN (?, ?, ?, ?, ?)",
                    (user_id, code_card1, code_card2, code_card3, code_card4, code_card5))
        valid_cards = cursor.fetchall()

        # Check if the team name is already taken
        cursor.execute("SELECT team_name FROM team WHERE user_id = ? AND team_name = ?", (user_id, team_name))
        existing_team = cursor.fetchone()

        if existing_team:
            embed = discord.Embed(title="Team Creation Failed",
                                description=f"The team name **{team_name}** is already taken. Please choose a different name.",
                                color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        if len(valid_cards) == 5:
            # Update the 'team' table with the cards and team name
            cursor.execute("INSERT INTO team (user_id, team_name, code_card1, code_card2, code_card3, code_card4, code_card5) "
                        "VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (user_id, team_name, code_card1, code_card2, code_card3, code_card4, code_card5))
            connection.commit()

            embed = discord.Embed(title="Team Created",
                                description=f"Your team **{team_name}** has been successfully created!",
                                color=discord.Color.green())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Team Creation Failed",
                                description="You must own all 5 specified cards in your inventory.",
                                color=discord.Color.red())
            await ctx.send(embed=embed)

    @commands.command()
    async def remove_team(self, ctx, team_name):
        user_id = ctx.author.id

        # Check if the specified team name exists for the user
        cursor.execute("SELECT * FROM team WHERE user_id = ? AND team_name = ?", (user_id, team_name))
        team_data = cursor.fetchone()

        if team_data:
            # Delete the team from the 'team' table
            cursor.execute("DELETE FROM team WHERE user_id = ? AND team_name = ?", (user_id, team_name))
            connection.commit()

            embed = discord.Embed(title="Team Deleted",
                                description=f"Your team **{team_name}** has been successfully deleted !",
                                color=discord.Color.green())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Team Deletion Failed",
                                description=f"The team **{team_name}** does not exist.",
                                color=discord.Color.red())
            await ctx.send(embed=embed)
    
    @commands.command()
    async def change(self, ctx, team_name, current_card, new_card):
        user_id = ctx.author.id

        # Check if the current card is in the user's team
        cursor.execute("SELECT * FROM team WHERE user_id = ? AND team_name = ? AND (code_card1 = ? OR code_card2 = ? OR code_card3 = ? OR code_card4 = ? OR code_card5 = ?)",
                    (user_id, team_name, current_card, current_card, current_card, current_card, current_card))
        team_data = cursor.fetchone()

        if not team_data:
            embed = discord.Embed(title="Card Change Failed",
                                description=f"The specified current card is not in your team **{team_name}**",
                                color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        # Check if the new card is in the user's inventory
        cursor.execute("SELECT code_card FROM user_inventaire WHERE user_id = ? AND code_card = ?", (user_id, new_card))
        new_card_in_inventory = cursor.fetchone()

        if not new_card_in_inventory:
            embed = discord.Embed(title="Card Change Failed",
                                description=f"The card `{new_card}` is not in your inventory.",
                                color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        # Update the user's team with the new card
        cursor.execute(f"UPDATE team SET code_card{team_data.index(current_card) - 1} = ? WHERE user_id = ? AND team_name = ?",
                    (new_card, user_id, team_name))
        connection.commit()

        embed = discord.Embed(title="Card Changed",
                            description=f"Successfully changed your card from `{current_card}` to `{new_card}` in your team **{team_name}**",
                            color=discord.Color.green())
        await ctx.send(embed=embed)

    @commands.command()
    async def teams(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        user_id = member.id

        # Fetch teams for the specified user from the 'team' table
        cursor.execute("SELECT team_name, code_card1, code_card2, code_card3, code_card4, code_card5 FROM team WHERE user_id = ?", (user_id,))
        user_teams = cursor.fetchall()

        if not user_teams:
            embed = discord.Embed(title=f"No Teams Found for {member.display_name}",
                                description=f"{member.display_name} doesn't have any teams.",
                                color=discord.Color.blue())
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(title=f"{member.display_name}'s Teams", color=discord.Color.blue())

        for i, team in enumerate(user_teams, 1):
            total_stats = 0  # Variable to store the total stats of all 5 cards

            for code_card in team[1:]:
                # Fetch card information from the 'user_inventaire' table
                cursor.execute("""
                    SELECT chant + dance + rap + acting + modeling AS total_stat
                    FROM user_inventaire
                    WHERE user_id = ? AND code_card = ?
                """, (user_id, code_card))

                card_info = cursor.fetchone()

                if card_info:
                    total_stats += card_info[0]  # Add the stats of the current card to the total

            embed.add_field(
                name=f"Team {i} : {team[0]}",
                value=f"Total stats : **{total_stats}**",
                inline=False
            )

        await ctx.send(embed=embed)

    @commands.command()
    async def team_stats(self, ctx, team_name):
        
        # Fetch user information from the 'team' table
        cursor.execute("""
            SELECT user_id, team_name, code_card1, code_card2, code_card3, code_card4, code_card5
            FROM team
            WHERE team_name = ?
        """, (team_name,))

        team_data = cursor.fetchone()

        if not team_data:
            embed = discord.Embed(title=f"No Team Found",
                                description=f"There is no team with the name **{team_name}**.",
                                color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        owner_id, team_name, *team_cards = team_data

        embed = discord.Embed(
            title=f"Team {team_name}", description=f"Team owner : <@{owner_id}>",
            color=discord.Color.blue()
        )

        category_totals = {
            "Sing": 0,
            "Dance": 0,
            "Rap": 0,
            "Acting": 0,
            "Modeling": 0
        }

        for code_card in team_cards:
            # Fetch card information from the 'user_inventaire' table
            cursor.execute("""
                SELECT nom, groupe, rarete, event,
                        chant, dance, rap, acting, modeling,
                        chant + dance + rap + acting + modeling AS total_stat
                FROM user_inventaire
                WHERE user_id = ? AND code_card = ?
            """, (owner_id, code_card))

            card_info = cursor.fetchone()

            if card_info:
                for i, category in enumerate(["Sing", "Dance", "Rap", "Acting", "Modeling"]):
                    category_totals[category] += card_info[4 + i]  # Add the stat of the current card to the category total

                # Add a field for each category
                embed.add_field(
                    name=f"{card_info[0]} ({card_info[1]})",
                    value=f"Code : `{code_card}`\nTotal Stat: **{card_info[9]}**",
                    inline=False
                )
        
        # Add a line of separation
        embed.add_field(name="\u200b", value="**Total Stats by Category :**", inline=False)

        # Add category totals to the embed
        for category, total in category_totals.items():
            embed.add_field(name=f"{category}", value=f"Total: **{total}**", inline=False)

        embed.set_footer(text=f"Total Stats for the Team: {sum(category_totals.values())}")
        await ctx.send(embed=embed)
        
    def get_rarity_emojis(self, event, rarity):
        if event and event.lower() == 'xmas 2023':
            return {
                "U": "<:xmas_boot:1183911398661693631>",
                "L": "<:xmas_hat:1183911360808112160>"
            }.get(rarity, "")
        elif event and event.lower() == 'new year 2024':
            return {
                "R": "<:NY_Confetti:1185996235551805470>",
                "L": "<:NY_Fireworks:1185996232477384808>"
            }.get(rarity, "")
        elif event and event.lower() == 'lunar 2024':
            return {
                "L": "<:Hongbao:1205276514443067533>"
            }.get(rarity, "")
        else:
            return {
                "C": "<:C_:1107771999490686987>",
                "U": "<:U_:1107772008193867867>",
                "R": "<:R_:1107772004410601553>",
                "E": "<:E_:1107772001747222550>",
                "L": "<:L_:1107772002690945055>"
            }.get(rarity, "")
    

async def setup(bot):
    await bot.add_cog(Team(bot))