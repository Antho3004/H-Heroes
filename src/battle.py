import discord
from discord.ext import commands
import sqlite3
import random
from dispie import Paginator
from apscheduler.schedulers.asyncio import AsyncIOScheduler

connection = sqlite3.connect("HallyuHeroes.db")
cursor = connection.cursor()

# Fonction de récompense hebdomadaire
async def weekly_reward_ranked():
    # Récupérer tous les utilisateurs
    cursor.execute("SELECT user_id, Heroes_points FROM user_data")
    reward_users_hp = cursor.fetchall()

    # Trier la liste par ordre décroissant des Heroes Points
    users_hp_sorted = sorted(reward_users_hp, key=lambda x: x[1], reverse=True)

    # Définir les récompenses en packs training
    rewards = [30, 25, 23, 20, 18, 15, 10, 7, 5, 3]

    # Attribuer les récompenses aux 10 premiers utilisateurs
    for i in range(min(10, len(users_hp_sorted))):
        user_id, _ = users_hp_sorted[i]
        reward = rewards[i]

        cursor.execute("UPDATE user_data SET training = training + ? WHERE user_id = ?", (reward, user_id))

    # N'oublie pas de valider et de commit tes changements
    connection.commit()


class Battle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.rounds_to_win = 3
        self.user_choices = {}
        self.opponent_choices = {}
        self.user_wins = 0
        self.opponent_wins = 0
        self.scheduler = AsyncIOScheduler()
        self.scheduler.add_job(weekly_reward_ranked, trigger="cron", day_of_week="fru", hour=18, minute=00, second=0)
        self.scheduler.start()

    def cog_unload(self):
        self.scheduler.shutdown()

    @commands.command()
    @commands.cooldown(1, 1200, commands.BucketType.user)
    async def battle(self, ctx):
        user_id = ctx.author.id

        cursor.execute("SELECT team_favorite FROM user_data WHERE user_id = ?", (user_id,))
        user_team = cursor.fetchone()

        if user_team is None:
            embed = discord.Embed(title="Error", description="You don't have a team.", color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        cursor.execute("SELECT * FROM team WHERE team_name = ?", (user_team[0],))
        user_team_info = cursor.fetchone()

        cursor.execute("SELECT * FROM team WHERE team_name != ? AND user_id != ? ORDER BY RANDOM() LIMIT 1", (user_team[0], user_id))
        opponent_team_info = cursor.fetchone()

        if opponent_team_info is None:
            embed = discord.Embed(title="Error", description="There are no other teams.", color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        opponent_team_name = opponent_team_info[1]
        opponent_user_id = opponent_team_info[0]

        self.user_choices[ctx.author.id] = {"card": None, "category": None}
        self.opponent_choices[opponent_user_id] = {"card": None, "category": None}

        embed = discord.Embed(title=f"Battle - {ctx.author.display_name}", color=discord.Colour.blue())

        embed.add_field(name="My Team", value=f"{user_team[0]}\nOwner: <@{user_id}>", inline=True)
        embed.add_field(name="VS", value="", inline=True)
        embed.add_field(name=f"Opposing team", value=f"{opponent_team_name}\nOwner: <@{opponent_user_id}>", inline=True)

        user_cards_info = self.get_team_cards_info(user_team_info)
        embed.add_field(name="My Team Cards", value=user_cards_info, inline=True)

        opponent_cards_info = self.get_team_cards_info(opponent_team_info)
        embed.add_field(name="Opposing Team Cards", value=f"{opponent_cards_info}", inline=True)
        
        await ctx.send(embed=embed)

        # Initialiser le nombre de victoires de l'utilisateur
        self.user_wins = 0
        self.opponent_wins = 0

        # Créer une liste de cartes disponibles pour chaque équipe
        user_available_cards = list(user_team_info[2:])
        opponent_available_cards = list(opponent_team_info[2:])

        while self.user_wins < self.rounds_to_win and self.opponent_wins < self.rounds_to_win:
            # Choix aléatoire de la catégorie pour le round
            category = self.get_random_category()

            # Choix aléatoire des cartes pour chaque équipe dans la même catégorie
            user_card = self.get_random_card(user_available_cards)
            opponent_card = self.get_random_card(opponent_available_cards)

            self.user_choices[ctx.author.id] = {"card": user_card, "category": category}
            self.opponent_choices[opponent_user_id] = {"card": opponent_card, "category": category}

            # Comparaison des statistiques des cartes pour la catégorie choisie
            user_stat_category = user_card[6:11][self.get_category_index(category)]
            opponent_stat_category = opponent_card[6:11][self.get_category_index(category)]

            # Détermination du vainqueur du round
            if user_stat_category > opponent_stat_category:
                round_winner = ctx.author.id
                winning_card_name = user_card[3]  # Nom de la carte gagnante
                cursor.execute("UPDATE user_data SET round_win = round_win + ? WHERE user_id = ?", (1, ctx.author.id))
                cursor.execute("UPDATE user_data SET round_lose = round_lose + ? WHERE user_id = ?", (1, opponent_user_id))
                connection.commit()
            elif user_stat_category < opponent_stat_category:
                round_winner = opponent_user_id
                winning_card_name = opponent_card[3]  # Nom de la carte gagnante
                cursor.execute("UPDATE user_data SET round_lose = round_lose + ? WHERE user_id = ?", (1, ctx.author.id))
                cursor.execute("UPDATE user_data SET round_win = round_win + ? WHERE user_id = ?", (1, opponent_user_id))
                connection.commit()
            else:
                # En cas d'égalité, vous pouvez définir une logique spécifique
                round_winner = "égalité"
                winning_card_name = "Nobody"
                cursor.execute("UPDATE user_data SET round_equal = round_equal + ? WHERE user_id = ?", (1, ctx.author.id))
                cursor.execute("UPDATE user_data SET round_equal = round_equal + ? WHERE user_id = ?", (1, opponent_user_id))
                connection.commit()

            # Incrémentation du score du vainqueur
            if round_winner == ctx.author.id:
                self.user_wins += 1
            elif round_winner == opponent_user_id:
                self.opponent_wins += 1
            
            # Retirer les cartes utilisées du pool de cartes disponibles
            user_available_cards.remove(user_card[1])
            opponent_available_cards.remove(opponent_card[1])

            # Création de l'embed pour le round
            round_embed = discord.Embed(title=f"MATCH - {user_team[0]} VS {opponent_team_name}", color=discord.Colour.blue())
            round_embed.add_field(name=f"",value=f"**Round {self.user_wins + self.opponent_wins} : {category}**", inline=False)
            round_embed.add_field(name=f"{user_team[0]}", value=f"{user_card[2]} {user_card[3]}\n({user_card[1]})\nSTATS : **{user_stat_category}**", inline=True)
            round_embed.add_field(name=f"{opponent_team_name}", value=f"{opponent_card[2]} {opponent_card[3]}\n({opponent_card[1]})\nSTATS : **{opponent_stat_category}**", inline=True)

            if round_winner != "égalité":
                round_embed.add_field(name="", value=f"**Winner {winning_card_name}** - <@{round_winner}>", inline=False)
            else:
                round_embed.add_field(name="Draw", value="The round is a draw", inline=False)

            # Envoyer l'embed du round
            await ctx.send(embed=round_embed)

        # Vérification de l'équipe gagnante
        winner_id = ctx.author.id if self.user_wins == self.rounds_to_win else opponent_user_id
        loser_id = opponent_user_id if winner_id == ctx.author.id else ctx.author.id

        # Création de l'embed de résultat en fonction du vainqueur
        if winner_id == ctx.author.id:
            cursor.execute("UPDATE user_data SET battle_win = battle_win + ? WHERE user_id = ?", (1, ctx.author.id))
            connection.commit()
            cursor.execute("UPDATE user_data SET battle_lose = battle_lose + ? WHERE user_id = ?", (1, opponent_user_id))
            connection.commit()
            result_embed = self.create_winner_embed(ctx, winner_id, loser_id)
        elif loser_id == ctx.author.id:
            cursor.execute("UPDATE user_data SET battle_lose = battle_lose + ? WHERE user_id = ?", (1, ctx.author.id))
            connection.commit()
            cursor.execute("UPDATE user_data SET battle_win = battle_win + ? WHERE user_id = ?", (1, opponent_user_id))
            connection.commit()
            result_embed = self.create_loser_embed(ctx, winner_id, loser_id)
        else :
            result_embed = discord.Embed(title=f"Battle result - {ctx.author.display_name}", color=discord.Colour.green())
            result_embed.add_field(name="Draw", value=f"This battle is a draw", inline=False)

        # Envoyer l'embed de résultat
        await ctx.send(embed=result_embed)

    def get_team_cards_info(self, team_info):
        card_codes = team_info[2:]
        cards_info = ""

        for code in card_codes:
            cursor.execute("SELECT * FROM user_inventaire WHERE code_card = ?", (code,))
            card_info = cursor.fetchone()

            if card_info:
                total_stats = sum(card_info[6:11])
                cards_info += f"**{card_info[3]} ({card_info[2]})**\nCode : `{card_info[1]}`\nTotal Stats: **{total_stats}**\n\n"

        return cards_info
    
    def get_random_card(self, available_cards):
        random_card_code = random.choice(available_cards)
        cursor.execute("SELECT * FROM user_inventaire WHERE code_card = ?", (random_card_code,))
        return cursor.fetchone()

    def get_random_category(self):
        categories = ["dance", "sing", "rap", "acting", "modeling"]
        return random.choice(categories)

    def get_category_index(self, category):
        # Retourne l'index de la catégorie dans la liste des catégories
        return ["dance", "sing", "rap", "acting", "modeling"].index(category)

    def create_winner_embed(self, ctx, winner_id, loser_id):
        winner_embed = discord.Embed(title=f"Battle result - {ctx.author.display_name}", color=discord.Colour.green())
        winner_embed.add_field(name="Victory !", value=f"Congratulations <@{winner_id}> you won {self.user_wins} - {self.opponent_wins} against <@{loser_id}>", inline=False)

        hp_win = random.randint(25, 30)
        cursor.execute("UPDATE user_data SET Heroes_points = Heroes_points + ? WHERE user_id = ?", (hp_win, winner_id))
        connection.commit()

        # Réduire les points de héros en cas de défaite
        hp_loss = random.randint(20, 25)  # Vous pouvez ajuster ces valeurs selon vos besoins
        cursor.execute("UPDATE user_data SET Heroes_points = MAX(0, Heroes_points - ?) WHERE user_id = ?", (hp_loss, loser_id))
        connection.commit()

        # Ajouter des informations sur la récompense gagnée
        reward_type = None
        reward_amount = None

        # Chances pour les récompenses
        argent_chance = 0.5
        training_chance = 0.5

        # Choisir une récompense en fonction des probabilités
        rand_num = random.random()

        if rand_num < argent_chance:
            reward_type = "Money"
            reward_amount = random.randint(3000, 5000)
        elif rand_num < (argent_chance + training_chance):
            reward_type = "Packs Training"
            reward_amount = 10

        # Appliquer la récompense
        if reward_type and reward_amount is not None:
            if reward_type == "Money":
                cursor.execute("UPDATE user_data SET argent = argent + ? WHERE user_id = ?", (reward_amount, winner_id))
            elif reward_type == "Packs Training":
                cursor.execute("UPDATE user_data SET training = training + ? WHERE user_id = ?", (reward_amount, winner_id))

            connection.commit()

            # Ajouter la récompense à l'embed
            winner_embed.add_field(name="Reward earned", value=f"{reward_type} : **{reward_amount}** and you won **{hp_win}** Heroes Points\nYou made your opponent lose **{hp_loss}** Heroes Points", inline=False)

        return winner_embed

    def create_loser_embed(self, ctx, winner_id, loser_id):

        # Réduire les points de héros en cas de défaite
        hp_loss = random.randint(20, 25)  # Vous pouvez ajuster ces valeurs selon vos besoins
        cursor.execute("UPDATE user_data SET Heroes_points = MAX(0, Heroes_points - ?) WHERE user_id = ?", (hp_loss, loser_id))
        connection.commit()

        # Ajouter les points de héros à l'adversaire
        hp_win = random.randint(20, 30)  # Vous pouvez ajuster ces valeurs selon vos besoins
        cursor.execute("UPDATE user_data SET Heroes_points = Heroes_points + ? WHERE user_id = ?", (hp_loss, winner_id))
        connection.commit()
        
        loser_embed = discord.Embed(title=f"Battle result - {ctx.author.display_name}", color=discord.Colour.red())
        loser_embed.add_field(name="Defeat...", value=f"Sad <@{loser_id}> you lost {self.user_wins} - {self.opponent_wins} against <@{winner_id}>", inline=False)
        loser_embed.add_field(name="Lost awards", value=f"You lost **{hp_loss}** Heroes Points\nYou have won your opponent **{hp_win}** points", inline=False)
        return loser_embed
    
    @commands.command()
    async def battle_stats(self, ctx, member: discord.Member = None):
        if member is None:
            user_id = ctx.author.id
            user_display_name = ctx.author.display_name
        else:
            user_id = member.id
            user_display_name = member.display_name

        # Récupérer les statistiques de l'utilisateur
        cursor.execute("SELECT round_win, round_lose, round_equal, battle_win, battle_lose, Heroes_points FROM user_data WHERE user_id = ?", (user_id,))
        user_stats = cursor.fetchone()

        if user_stats is None:
            await ctx.send(f"No statistics found for {user_display_name}.")
            return

        if user_stats[5] == 0:
            ranked = "unranked"
        elif user_stats[5] > 1 and user_stats[5] <= 1000:
            ranked = "Bronze"
        elif user_stats[5] > 1000 and user_stats[5] <= 2000:
            ranked = "Silver"
        elif user_stats[5] > 2000 and user_stats[5] <= 3000:
            ranked = "Gold"
        elif user_stats[5] > 3000 and user_stats[5] <=4000:
            ranked = "Platinum"
        elif user_stats[5] > 4000 and user_stats[5] <=5000:
            ranked = "Diamond"
        elif user_stats[5] > 5000:
            ranked = "Heroes"

        # Créer l'embed avec les statistiques
        stats_embed = discord.Embed(title=f"Battle statistics - {user_display_name}", color=discord.Colour.blue())
        stats_embed.add_field(name="Stats : ", value=f"- Rounds win : **{user_stats[0]}**\n- Rounds lose : **{user_stats[1]}**\n- Rounds equal : **{user_stats[2]}**\n- Battle win : **{user_stats[3]}**\n- Battle lose : **{user_stats[4]}**\n- Heroes Point : **{user_stats[5]}** ({ranked})", inline=True)

        await ctx.send(embed=stats_embed)
    
    @commands.command()
    async def battle_stats_global(self, ctx):

        # Récupérer les cartes de l'utilisateur depuis la base de données
        cursor.execute("SELECT user_id, battle_win, battle_lose FROM user_data")
        user_stats = cursor.fetchall()

        # Calculer le winrate pour chaque utilisateur et les classer du plus haut au plus bas
        ranked_battle = sorted(user_stats, key=lambda x: (0 if (x[1] + x[2]) == 0 else (x[1] / (x[1] + x[2])) * 100, x[1]), reverse=True)

        # Créer des pages pour l'affichage paginé
        chunks = [ranked_battle[i:i + 10] for i in range(0, len(ranked_battle), 10)]
        embeds = []

        for i, chunk in enumerate(chunks):
            embed = discord.Embed(title=f"Rank Stats Global", color=discord.Color.blue())
            for j, user in enumerate(chunk):
                position = i * 10 + j + 1
                if position == 1:
                    emoji = ":first_place:"
                elif position == 2:
                    emoji = ":second_place:"
                elif position == 3:
                    emoji = ":third_place:"
                else:
                    emoji = f"{position}."

                win_rate = 0 if (user[1] + user[2]) == 0 else (user[1] / (user[1] + user[2])) * 100

                embed.add_field(name=f"", value=f"{emoji} <@{user[0]}>\nVictory : **{user[1]}** - Lose : **{user[2]}**\nWinrate : **{win_rate:.2f}%**", inline=False)

            embed.set_footer(text=f"Page {i + 1}/{len(chunks)}")
            embeds.append(embed)

        # Afficher les pages avec Paginator
        paginator = Paginator(embeds)
        await paginator.start(ctx)
    
    @commands.command()
    async def ranked(self, ctx):
        # Récupérer les cartes de l'utilisateur depuis la base de données
        cursor.execute("SELECT user_id, Heroes_points FROM user_data")
        user_hp = cursor.fetchall()

        # Trier la liste par ordre décroissant des Heroes Points
        user_hp_sorted = sorted(user_hp, key=lambda x: x[1], reverse=True)

        # Créer des pages pour l'affichage paginé
        chunks = [user_hp_sorted[i:i + 10] for i in range(0, len(user_hp_sorted), 10)]
        embeds = []

        for i, chunk in enumerate(chunks):
            embed = discord.Embed(title=f"Rank Stats Global", color=discord.Color.blue())
            for j, user in enumerate(chunk):
                position = i * 10 + j + 1

                if user[1] == 0:
                    ranked = "unranked"
                elif user[1] > 0 and user[1] <= 1000:
                    ranked = "Bronze"
                elif user[1] > 1000 and user[1] <= 2000:
                    ranked = "Silver"
                elif user[1] > 2000 and user[1] <= 3000:
                    ranked = "Gold"
                elif user[1] > 3000 and user[1] <= 4000:
                    ranked = "Platinum"
                elif user[1] > 4000 and user[1] <= 5000:
                    ranked = "Diamond"
                elif user[1] > 5000:
                    ranked = "Heroes"

                if position == 1:
                    emoji = ":first_place:"
                elif position == 2:
                    emoji = ":second_place:"
                elif position == 3:
                    emoji = ":third_place:"
                else:
                    emoji = f"{position}."

                embed.add_field(name=f"", value=f"{emoji} <@{user[0]}>\nHeroes Points : **{user[1]}** ({ranked})", inline=False)

            embed.set_footer(text=f"Page {i + 1}/{len(chunks)}")
            embeds.append(embed)

        # Afficher les pages avec Paginator
        paginator = Paginator(embeds)
        await paginator.start(ctx)

async def setup(bot):
    await bot.add_cog(Battle(bot))
