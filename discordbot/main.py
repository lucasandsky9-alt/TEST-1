import os
import asyncio
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = os.getenv("BOT_PREFIX", "!")

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
log = logging.getLogger("bot")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or(PREFIX), intents=intents, help_command=None)

    async def setup_hook(self):
        cogs_dir = os.path.join(os.path.dirname(__file__), "cogs")
        for filename in os.listdir(cogs_dir):
            if filename.endswith(".py") and not filename.startswith("_"):
                extension = f"cogs.{filename[:-3]}"
                try:
                    await self.load_extension(extension)
                    log.info(f"Loaded extension: {extension}")
                except Exception as e:
                    log.exception(f"Failed to load extension {extension}: {e}")

        # Sync slash commands (optional, hybrid commands support both prefix and slash)
        try:
            synced = await self.tree.sync()
            log.info(f"Synced {len(synced)} slash commands.")
        except Exception as e:
            log.exception(f"Failed to sync slash commands: {e}")

    async def on_ready(self):
        total_commands = len(set(self.commands))
        log.info(f"Logged in as {self.user} (ID: {self.user.id})")
        log.info(f"Loaded {total_commands} commands across {len(self.cogs)} cogs.")
        activity = discord.Activity(type=discord.ActivityType.watching, name=f"{PREFIX}help | {total_commands}+ commands")
        await self.change_presence(activity=activity)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Missing argument: `{error.param.name}`. Use `{PREFIX}help {ctx.command}` for usage.")
            return
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to do that.")
            return
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.send("I don't have the permissions needed to do that.")
            return
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"That command is on cooldown. Try again in {error.retry_after:.1f}s.")
            return
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("That command can't be used in DMs.")
            return
        log.exception("Unhandled command error", exc_info=error)
        await ctx.send(f"Something went wrong running that command: `{error}`")

bot = MyBot()

async def main():
    if not TOKEN:
        raise SystemExit("No DISCORD_TOKEN found. Copy .env.example to .env and fill in your bot token.")
    async with bot:
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
