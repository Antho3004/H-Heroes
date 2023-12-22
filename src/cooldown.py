import discord
from discord.ext import commands

class Cooldown(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cd(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
        
        drop_cooldown = self.bot.get_command("drop").get_cooldown_retry_after(ctx)
        work_cooldown = self.bot.get_command("work").get_cooldown_retry_after(ctx)
        daily_cooldown = self.bot.get_command("daily").get_cooldown_retry_after(ctx)

        drop_time = self.format_cooldown_time(drop_cooldown)
        work_time = self.format_cooldown_time(work_cooldown)
        daily_time = self.format_cooldown_time(daily_cooldown)

        embed = discord.Embed(title=f"{user.name} - **Cooldown**", color=discord.Color.blue())
        embed.add_field(name="", value=f"<:hclock2:1136747860478664765> **Drop** : {'✅' if drop_cooldown == 0 else drop_time}", inline=False)
        embed.add_field(name="", value=f"<:hclock2:1136747860478664765> **Work** : {'✅' if work_cooldown == 0 else work_time}", inline=False)
        embed.add_field(name="", value=f"<:hclock2:1136747860478664765> **Daily** : {'✅' if daily_cooldown == 0 else daily_time}", inline=False)
        embed.add_field(name="", value=f"<:hclock2:1136747860478664765> **Battle** : Soon", inline=False)

        await ctx.send(embed=embed)

    @staticmethod
    def format_cooldown_time(cooldown_seconds):
        minutes, seconds = divmod(cooldown_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return f"{int(hours)}h {int(minutes)}m {int(seconds)}s" if hours else f"{int(minutes)}m {int(seconds)}s"

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cooldown_time = error.retry_after
            time_remaining = self.format_cooldown_time(cooldown_time)
            message = f"Please wait **{time_remaining}** before using this command again."
            
            embed = discord.Embed(title="Cooldown", description=message, color=discord.Color.red())
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Cooldown(bot))
