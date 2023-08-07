import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        
        embed = discord.Embed(title="HELP", color=discord.Color.orange())
        embed.add_field(name="COMMAND LIST", value=f"`$start` : Allows you to create an account.\n`$drop` : Gives you a random card every 10 minutes.\n\
                        `$work` : Earn money every 30 minutes.\n`$view` : Displays information, statistics, and the current card.\n\
                        `$daily`: Grants money or a card once every 24 hours.\n`$profile or $pr` : Shows your profile.\n\
                        `$description` : Changes your profile description.\n`$bal` : Displays the currency in your account.\n\
                        `$inventory or $inv` : Shows your card inventory. Display can be filtered based on chosen criteria (group, idol, version, rarity, event).\n\
                        `$mp` : Displays the card market. Display can be filtered based on chosen criteria (group, idol, version, rarity, event).\n\
                        `$buy` : Allows you to buy a card from the market.\n`$sell` : Allows you to sell a card.\n`$gift` : Allows you to give away a card.\n\
                        `$bal_give` : Allows you to give money to another user.",
                        inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))
