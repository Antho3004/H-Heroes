import discord
from discord.ext import commands

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def shop(self, ctx):
        # Créez un embed pour afficher les packs
        embed = discord.Embed(title="SHOP", description="", color=discord.Color.blue())

        embed.add_field(name="", value=f"<:Bronze:1136312536665440387> **Bronze** : 1000 <:HCoins:1134169003657547847>", inline=False)
        embed.add_field(name="", value=f"<:Argent:1136312524900401213> **Silver** : 5000 <:HCoins:1134169003657547847>", inline=False)
        embed.add_field(name="", value=f"<:Gold:1136312506957189131> **Gold** : 10000 <:HCoins:1134169003657547847>", inline=False)
        embed.add_field(name="", value=f"<:Legendary:1136312609449193544> **Legendary** : 20000 <:HCoins:1134169003657547847>", inline=False)

        # Envoyez l'embed
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Shop(bot))
