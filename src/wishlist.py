import discord
from discord.ext import commands
import sqlite3
from dispie import Paginator

connection = sqlite3.connect("HallyuHeroes.db")
cursor = connection.cursor()

class Wishlist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def wish_add(self, ctx, *card_codes: str):
        user_id = ctx.author.id

        # Check if each card code has the correct format
        valid_card_codes = []
        invalid_card_codes = []

        for card_code in card_codes:
            card_code_prefix = card_code.split("-")[0]

            # Check if the card exists in the "cards" table based on the prefix
            cursor.execute("SELECT * FROM cards WHERE code_card LIKE ?", (f"{card_code_prefix}%",))
            card_exists = cursor.fetchone()

            if card_exists:
                valid_card_codes.append(card_code)
            else:
                invalid_card_codes.append(card_code)

        # Update the user's wishlist with valid card codes
        cursor.execute("SELECT wishlist FROM user_data WHERE user_id = ?", (user_id,))
        current_wishlist = cursor.fetchone()

        if current_wishlist and current_wishlist[0]:
            current_wishlist_set = set(current_wishlist[0].split(','))  # Split the string by commas
        else:
            current_wishlist_set = set()

        # Check if a card is already in the wishlist before adding it
        existing_cards = current_wishlist_set.intersection(valid_card_codes)
        if existing_cards:
            embed = discord.Embed(title="Existing Cards", color=discord.Color.orange())
            embed.add_field(name="Already in Wishlist", value=f"The following cards are already in your wishlist: {', '.join(existing_cards)}", inline=False)
            await ctx.send(embed=embed)
            return

        new_wishlist = ','.join(current_wishlist_set.union(valid_card_codes))  # Join the elements of the set with commas
        cursor.execute("UPDATE user_data SET wishlist = ? WHERE user_id = ?", (new_wishlist, user_id))
        connection.commit()

        if valid_card_codes:
            embed = discord.Embed(title="Cards Added to Wishlist", color=discord.Color.green())
            embed.add_field(name="Success", value=f"The following cards have been added to your wishlist: {', '.join(valid_card_codes)}", inline=False)

        if invalid_card_codes:
            embed = discord.Embed(title="Cards Added to Wishlist", color=discord.Color.red())
            embed.add_field(name="Invalid Card Codes", value=f"The following card codes are invalid or do not exist in the database: {', '.join(invalid_card_codes)}", inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def wish_remove(self, ctx, *card_codes: str):
        user_id = ctx.author.id

        # Retrieve the user's current wishlist
        cursor.execute("SELECT wishlist FROM user_data WHERE user_id = ?", (user_id,))
        current_wishlist = cursor.fetchone()

        if current_wishlist and current_wishlist[0]:
            current_wishlist_set = set(current_wishlist[0].split(','))  # Divisez la chaîne par des virgules
        else:
            current_wishlist_set = set()

        # Remove specified card codes from the wishlist
        removed_card_codes = []

        for card_code in card_codes:
            if card_code in current_wishlist_set:
                current_wishlist_set.remove(card_code)
                removed_card_codes.append(card_code)

        new_wishlist = ','.join(current_wishlist_set)  # Joignez les éléments de l'ensemble avec des virgules
        cursor.execute("UPDATE user_data SET wishlist = ? WHERE user_id = ?", (new_wishlist, user_id))
        connection.commit()

        # Send a message with the results
        embed = discord.Embed(title="Cards Removed from Wishlist", color=discord.Color.green())

        if removed_card_codes:
            embed.add_field(name="Success", value=f"The following cards have been removed from your wishlist: {', '.join(removed_card_codes)}", inline=False)
        else:
            embed.add_field(name="Failure", value=f"The following cards : {', '.join(removed_card_codes)}", inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def wishlist(self, ctx, member: discord.Member = None):
        user_id = member.id if member else ctx.author.id
        user_name = member.name if member else ctx.author.name

        # Retrieve the user's wishlist from the database
        cursor.execute("SELECT wishlist FROM user_data WHERE user_id = ?", (user_id,))
        wishlist = cursor.fetchone()

        if wishlist and wishlist[0]:
            card_codes = wishlist[0].split(",")  # Diviser la chaîne par virgule

            # Check if cards in wishlist are in the user's inventory
            cursor.execute("SELECT code_card FROM user_inventaire WHERE user_id = ? AND code_card IN ({})".format(','.join(['?']*len(card_codes))), (user_id,) + tuple(card_codes))
            owned_cards = set(card[0] for card in cursor.fetchall())

            pages = [card_codes[i:i + 15] for i in range(0, len(card_codes), 15)]

            embeds = []
            for i, page in enumerate(pages):
                embed = discord.Embed(title=f"{user_name}'s Wishlist", color=discord.Color.blue())
                for card_code in page:
                    # Add a checkmark if the card is in the user's inventory
                    checkmark = " ✅" if card_code in owned_cards else ""
                    embed.add_field(name=f"", value=f"- {card_code.strip()} {checkmark}", inline=False)

                embeds.append(embed)

            # Display pages using Paginator
            paginator = Paginator(embeds)
            await paginator.start(ctx)
        else:
            embed = discord.Embed(title=f"{user_name}'s Wishlist", color=discord.Color.blue())
            embed.add_field(name="No Cards", value=f"")
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Wishlist(bot))
