import discord
from discord.ext import commands
from dispie import Paginator  # Assurez-vous que le module dispie est correctement importé

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        command_list = [
            "**Basic**",
            "- `$start` : Allows you to create an account.",
            "- `$drop or $dr` : Gives you a random card every 2 minutes.",
            "- `$favorite or $fav [code card]` : Adds a favorite card",
            "- `$cd` : Display cooldown",
            "- `$work` : Earn money every 20 minutes",
            "- `$burn [code card]` : Burn a card",
            "- `$atlas` : Allows you to see all the cards available in the game",
            "- `$show [code card]` : allows you to preview a card",
            "- `$view [code card]` : Displays information, statistics, and the current card",
            "- `$daily`: Grants money or a card once every 24 hours",
            "- `$profile or $pr` : Shows your profile.",
            "- `$description or $desc [text]` : Changes your profile description.",
            "- `$bal` : Displays the currency in your account.",
            "- `$inventory or $inv` : Shows your card inventory. Display can be filtered based on chosen criteria (group, idol, version, rarity, event).",
            "- `$gift [@player] [code card]` : Allows you to give away a card to a player",
            "- `$gift_packs [@player] [rarity pack]` : Allows you to give packs to a player",
            "- `$pay [@player] [amount]` : Allows you to give money to another user.",
            "\n**Market/Shop**",
            "- `$mp` : Displays the card market. Display can be filtered based on chosen criteria (group, idol, version, rarity, event).",
            "- `$buy [code card]` : Allows you to buy a card from the market.",
            "- `$sell [code card]` : Allows you to sell a card.",
            "- `$wd [code card]` : Allows you to remove a card from the market",
            "- `$shop` : Display the shop",
            "- `$buy_pack [rarity pack]` : Buy a pack",
            "- `$open_pack [rarity pack]` : Open a pack",
            "\n**Battle**",
            "- `$battle` : Start a battle against another team",
            "- `$make_team [team name] [5 code card]` : Build a team",
            "- `$remove_team [team name]` : Delete a team",
            "- `$change [team name] [Old card] [New Card]` : Replace a card from your team with a new card",
            "- `$training [code card]` : Allows you to train a card",
            "- `favorite_team [team name]` : Add your team in favorite for battles",
            "- `$lb_cards` : Displays card rankings based on stats of all players",
            "- `$rank_cards` : Displays card rankings based on stats",
            "- `$teams` : Display all your teams",
            "- `$team_stats [team name]` : Displays team with 5 cards and stats",
            "- `$team_rank` : Displays a ranking of all teams",
            "- `$stats` : Display your battle stats",
            "- `$gstats` : Display battle stats for all players",
            "- `$leaderboard or $lb` : Displays a ranking based on Heroes Points",
            "\n**Wishlist**",
            "- `$wish_add [code card]` : Add a card to your wishlist",
            "- `$wish_remove [code card]` : Remove a card to you wishlist",
            "- `$wish_list` : Display your wishlist",
            "\n**Lock card**",
            "- `$lock [code card]` : Allows you to block a card",
            "- `$unlock [code card]` : Allows you to unlock a card",
            "- `$lock_list` : Display your blocked cards",
            "\n**Bank**",
            "- `$bank` : Display your bank account",
            "- `$tranfer or $tr [amount]` : Add money to the bank",
            "- `$extract or $ext [amount]` : Extract money from the bank"
        ]

        embed_pages = []
        current_page = 1
        commands_per_page = 15

        for i in range(0, len(command_list), commands_per_page):
            commands_chunk = command_list[i:i + commands_per_page]
            embed = discord.Embed(title=f"HELP - Page {current_page}", color=discord.Color.orange())
            embed.add_field(name="COMMAND LIST", value="\n".join(commands_chunk), inline=False)
            embed_pages.append(embed)
            current_page += 1

        paginator = Paginator(embed_pages)

        await paginator.start(ctx)

async def setup(bot):
    await bot.add_cog(Help(bot))
