import discord
from discord.ext import commands
import sqlite3

connection = sqlite3.connect("HallyuHeroes.db")
cursor = connection.cursor()

class Start(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def start(self, ctx):
        # Vérifier si l'utilisateur a déjà un compte
        user_id = ctx.author.id
        cursor.execute("SELECT * FROM user_data WHERE user_id = ?", (user_id,))
        existing_account = cursor.fetchone()

        if existing_account:
            # Si l'utilisateur a déjà un compte, envoie un message d'erreur
            embed = discord.Embed(title="Account", description="You already have an account!", color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            # Si l'utilisateur n'a pas de compte, insère les données dans la base de données
            cursor.execute("INSERT INTO user_data (user_id, description, argent, nombre_de_cartes, carte_favori, bronze, silver, gold, Legendary) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",(user_id, "Welcome on my profile !", 0, 0, "NULL", 0, 0, 0, 0))
            connection.commit()
            
            # Envoie un message dans un embed pour indiquer que le compte a été créé
            embed = discord.Embed(title="Account", description="Your account has been created.", color=discord.Color.green())
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Start(bot))
