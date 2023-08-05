import discord
from discord.ext import commands
import sqlite3

connection = sqlite3.connect("HallyuHeroes.db")
cursor = connection.cursor()

class Fuse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def fuse(self, ctx, *codes):  # Pass the card codes as arguments
        
        rarity_order = {'C': 1, 'U': 2, 'R': 3, 'E': 4, 'L': 5}
        
        if len(codes) != 10:
            await ctx.send("You need to provide exactly 10 card codes.")
            return
        
        cards_obtenue = []
        cards_to_fuse = []
        rarities = set()
        
        for code in codes:
            # Fetch card information from database based on code
            cursor.execute("SELECT rarete FROM user_inventaire WHERE code_card=?", (code,))
            result = cursor.fetchone()
            if result:
                rarity = result[0]
                cards_to_fuse.append((code, rarity))
                cards_obtenue.append(code)
                rarities.add(rarity)
            else:
                await ctx.send(f"Card with code `{code}` not found.")
                return
        
        if len(rarities) != 1:
            await ctx.send("All cards must have the same rarity.")
            return
        
        current_rarity = rarity_order[cards_to_fuse[0][1]]
        next_rarity = current_rarity + 1
        next_rarity_symbol = None
        
        for symbol, rarity_value in rarity_order.items():
            if rarity_value == next_rarity:
                next_rarity_symbol = symbol
                break
        
        if not next_rarity_symbol:
            await ctx.send("Can't fuse to a higher rarity.")
            return
        
        # Check if the user has enough cards to fuse
        # Implement your logic here to remove cards from user_inventaire and market
        for code_card in codes:
            code_card = str(code_card)
            cursor.execute("DELETE FROM user_inventaire WHERE user_id = ? AND code_card = ?", (ctx.author.id, (code_card)))
        
        # Remove cards from the market
        #for code in codes:
            #cursor.execute("DELETE FROM market WHERE card_code=?", (code,))
        
        # Insert the new fused card into user's inventory
        
        await ctx.send(f"You have successfully fused your cards into a {next_rarity_symbol}-rarity card!")

async def setup(bot):
    await bot.add_cog(Fuse(bot))
