import discord
from discord.ext import commands
import sqlite3
from dispie import Paginator

connection = sqlite3.connect("HallyuHeroes.db")
cursor = connection.cursor()

class Battle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rank_stats(self, ctx, member: discord.Member = None):
        user_id = member.id if member else ctx.author.id
        user_name = member.name if member else ctx.author.name

        # Récupérer les cartes de l'utilisateur depuis la base de données
        cursor.execute("SELECT nom, groupe, code_card, rarete, event, chant, dance, rap, acting, modeling FROM user_inventaire WHERE user_id = ?", (user_id,))
        user_cards = cursor.fetchall()

        # Calculer la somme des compétences pour chaque carte et les classer
        ranked_cards = sorted(user_cards, key=lambda card: sum(card[5:]), reverse=True)

        # Créer des pages pour l'affichage paginé
        chunks = [ranked_cards[i:i + 10] for i in range(0, len(ranked_cards), 10)]

        embeds = []
        for i, chunk in enumerate(chunks):
            embed = discord.Embed(title=f"Rank Stat - {user_name}", color=discord.Color.blue())
            for j, card in enumerate(chunk):
                position = i * 10 + j + 1
                total_score = sum(card[5:])
                if position == 1:
                    emoji = ":first_place:"
                elif position == 2:
                    emoji = ":second_place:"
                elif position == 3:
                    emoji = ":third_place:"
                else:
                    emoji = f"{position}."
                
                if card[4] and card[4].lower() == 'xmas 2023':
                    rarity_emojis = {
                        "U": "<:xmas_boot:1183911398661693631>",
                        "L": "<:xmas_hat:1183911360808112160>"
                    }
                elif card[4] and card[4].lower() == 'new year 2024':
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
                embed.add_field(name=f"{emoji} {card[0]} {card[1]} {rarity_emojis.get(card[3], '')}", value=f"Code: `{card[2]}` : **{total_score}**", inline=False)

            embed.set_footer(text=f"Page {i + 1}/{len(chunks)}")
            embeds.append(embed)

        # Afficher les pages avec Paginator
        paginator = Paginator(embeds)
        await paginator.start(ctx)
    
    @commands.command()
    async def rank_stats_global(self, ctx):

        # Récupérer les cartes de l'utilisateur depuis la base de données
        cursor.execute("SELECT user_id, nom, groupe, code_card, rarete, event, chant, dance, rap, acting, modeling FROM user_inventaire")
        user_cards = cursor.fetchall()

        # Calculer la somme des compétences pour chaque carte et les classer
        ranked_cards = sorted(user_cards, key=lambda card: sum(card[6:]), reverse=True)

        # Créer des pages pour l'affichage paginé
        chunks = [ranked_cards[i:i + 10] for i in range(0, len(ranked_cards), 10)]

        embeds = []
        for i, chunk in enumerate(chunks):
            embed = discord.Embed(title=f"Rank Stats Global", color=discord.Color.blue())
            for j, card in enumerate(chunk):
                position = i * 10 + j + 1
                total_score = sum(card[6:])
                if position == 1:
                    emoji = ":first_place:"
                elif position == 2:
                    emoji = ":second_place:"
                elif position == 3:
                    emoji = ":third_place:"
                else:
                    emoji = f"{position}."
                
                if card[5] and card[5].lower() == 'xmas 2023':
                    rarity_emojis = {
                        "U": "<:xmas_boot:1183911398661693631>",
                        "L": "<:xmas_hat:1183911360808112160>"
                    }
                elif card[5] and card[5].lower() == 'new year 2024':
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
                embed.add_field(name=f"{emoji} {card[1]} {card[2]} {rarity_emojis.get(card[4], '')}", value=f"Code: `{card[3]}` : **{total_score}**\nOwner : <@{card[0]}>", inline=False)

            embed.set_footer(text=f"Page {i + 1}/{len(chunks)}")
            embeds.append(embed)

        # Afficher les pages avec Paginator
        paginator = Paginator(embeds)
        await paginator.start(ctx)
    
    @commands.command()
    async def create_team(self, ctx, team_name, code_card1, code_card2, code_card3, code_card4, code_card5):
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
    async def delete_team(self, ctx, team_name):
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
    async def team(self, ctx, member: discord.Member = None):
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
    async def team_view(self, ctx, team_name):
        user_id = ctx.author.id

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
            title=f"Team {team_name}",description=f"Team owner : <@{owner_id}>",
            color=discord.Color.blue()
        )

        total_stats = 0  # Variable to store the total stats of all 5 cards
        sorted_cards = []  # List to store card information for sorting

        for code_card in team_cards:
            # Fetch card information from the 'user_inventaire' table
            cursor.execute("""
                SELECT nom, groupe, rarete, event,
                        chant + dance + rap + acting + modeling AS total_stat
                FROM user_inventaire
                WHERE user_id = ? AND code_card = ?
            """, (owner_id, code_card))

            card_info = cursor.fetchone()

            if card_info:
                total_stats += card_info[4]  # Add the stats of the current card to the total
                sorted_cards.append((code_card, card_info))

        # Sort cards based on total stats in descending order
        sorted_cards.sort(key=lambda x: x[1][4], reverse=True)

        for code_card, card_info in sorted_cards:
            # Determine the rarity emoji based on the event and rarity
            rarity_emojis = self.get_rarity_emojis(card_info[3], card_info[2])

            embed.add_field(
                name=f"{card_info[0]} ({card_info[1]}) {rarity_emojis}",
                value=f"Code : `{code_card}`\nTotal Stat: **{card_info[4]}**",
                inline=False
            )

        embed.set_footer(text=f"Total Stats for the Team: {total_stats}")
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
        else:
            return {
                "C": "<:C_:1107771999490686987>",
                "U": "<:U_:1107772008193867867>",
                "R": "<:R_:1107772004410601553>",
                "E": "<:E_:1107772001747222550>",
                "L": "<:L_:1107772002690945055>"
            }.get(rarity, "")
    
    @commands.command()
    async def rank_teams(self, ctx):
        # Récupérer les équipes depuis la base de données
        cursor.execute("SELECT user_id, team_name, code_card1, code_card2, code_card3, code_card4, code_card5 FROM team")
        teams_data = cursor.fetchall()

        # Créer un dictionnaire pour stocker les statistiques totales de chaque équipe
        teams_stats = {}

        for team_data in teams_data:
            owner_id, team_name, *team_cards = team_data
            total_stats = 0
            for code_card in team_cards:
                # Récupérer les statistiques de chaque carte depuis la table 'user_inventaire'
                cursor.execute("""
                    SELECT chant + dance + rap + acting + modeling AS total_stat
                    FROM user_inventaire
                    WHERE user_id = ? AND code_card = ?
                """, (owner_id, code_card))

                card_info = cursor.fetchone()

                if card_info:
                    total_stats += card_info[0]  # Ajouter les statistiques de la carte actuelle au total

            # Ajouter les statistiques totales de l'équipe au dictionnaire avec user_id
            teams_stats[team_name] = {"total_stats": total_stats, "user_id": owner_id}

        # Trier les équipes en fonction des statistiques totales en ordre décroissant
        sorted_teams = sorted(teams_stats.items(), key=lambda x: x[1]["total_stats"], reverse=True)

        # Créer des pages pour l'affichage paginé
        chunks = [sorted_teams[i:i + 10] for i in range(0, len(sorted_teams), 10)]
        embeds = []
        for i, chunk in enumerate(chunks):
            embed = discord.Embed(title="Rank Teams", color=discord.Color.blue())
            for j, (team_name, data) in enumerate(chunk):
                position = i * 10 + j + 1

                if position == 1:
                    emoji = ":first_place:"
                elif position == 2:
                    emoji = ":second_place:"
                elif position == 3:
                    emoji = ":third_place:"
                else:
                    emoji = f"{position}."

                embed.add_field(
                    name=f"{emoji} {team_name}",
                    value=f"\nTotal stats: **{data['total_stats']}**\nOwner : <@{data['user_id']}>",
                    inline=False
                )

            embed.set_footer(text=f"Page {i + 1}/{len(chunks)}")
            embeds.append(embed)

        # Afficher les pages avec Paginator
        paginator = Paginator(embeds)
        await paginator.start(ctx)

async def setup(bot):
    await bot.add_cog(Battle(bot))