import discord
from discord.ext import commands
import sqlite3
from dispie import Paginator

connection = sqlite3.connect("HallyuHeroes.db")
cursor = connection.cursor()

class Rank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rank_cards(self, ctx, member: discord.Member = None):
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
                elif card[4] and card[4].lower() == 'lunar2024':
                    rarity_emojis = {
                        "L": "<:Hongbao:1205276514443067533>"
                    }
                elif card[4] and card[4].lower() == 'valentine 2024':
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
                embed.add_field(name=f"{emoji} {card[0]} {card[1]} {rarity_emojis.get(card[3], '')}", value=f"Code: `{card[2]}` : **{total_score}**", inline=False)

            embed.set_footer(text=f"Page {i + 1}/{len(chunks)}")
            embeds.append(embed)

        # Afficher les pages avec Paginator
        paginator = Paginator(embeds)
        await paginator.start(ctx)
    
    @commands.command()
    async def lb_cards(self, ctx):

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
                elif card[5] and card[5].lower() == 'lunar2024':
                    rarity_emojis = {
                        "L": "<:Hongbao:1205276514443067533>"
                    }
                elif card[5] and card[5].lower() == 'valentine 2024':
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
                embed.add_field(name=f"{emoji} {card[1]} {card[2]} {rarity_emojis.get(card[4], '')}", value=f"Code: `{card[3]}` : **{total_score}**\nOwner : <@{card[0]}>", inline=False)

            embed.set_footer(text=f"Page {i + 1}/{len(chunks)}")
            embeds.append(embed)

        # Afficher les pages avec Paginator
        paginator = Paginator(embeds)
        await paginator.start(ctx)
        
    @commands.command()
    async def team_rank(self, ctx):
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
    await bot.add_cog(Rank(bot))