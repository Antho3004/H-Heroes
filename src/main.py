import discord
from discord.ext import commands
import os
import dotenv
import database

class Bot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix="$", intents=discord.Intents.all())

    async def setup_hook(self) -> None:
        await self.load_extension("profil")
        await self.load_extension("balance")
        await self.load_extension("work")
        await self.load_extension("inventaire")
        await self.load_extension("drop")
        await self.load_extension("view")
        await self.load_extension("favorite")
        await self.load_extension("market")
        await self.load_extension("shop")
        await self.load_extension("daily")
        #await self.load_extension("cooldown")
        await self.tree.sync()
        database.table_users()

    async def on_ready(self) -> None:
        print("Le bot est en ligne")

def main () -> None:
    dotenv.load_dotenv()

    TOKEN = os.getenv("TOKEN")

    if TOKEN is None:
        raise ValueError("Le token n'est pas défini")
    
    bot = Bot()
    bot.run(token=TOKEN)

if __name__ == "__main__":
    main()