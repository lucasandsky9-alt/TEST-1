import discord
from discord.ext import commands

class Info(commands.Cog):
    """Help, bot info, and misc commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(description="Show all commands, grouped by category.")
    async def help(self, ctx, command_name: str = None):
        if command_name:
            cmd = self.bot.get_command(command_name)
            if not cmd:
                await ctx.send(f"No command called `{command_name}` found.")
                return
            embed = discord.Embed(title=f"!{cmd.name}", description=cmd.description or "No description.", color=discord.Color.blurple())
            if cmd.aliases:
                embed.add_field(name="Aliases", value=", ".join(cmd.aliases))
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(
            title="📖 Command List",
            description=f"Use `!help <command>` for details on a specific command.\nTotal commands: **{len(set(self.bot.commands))}**",
            color=discord.Color.blurple(),
        )
        for cog_name, cog in sorted(self.bot.cogs.items()):
            cmds = sorted(set(cog.get_commands()), key=lambda c: c.name)
            if not cmds:
                continue
            names = ", ".join(f"`{c.name}`" for c in cmds)
            embed.add_field(name=f"{cog_name} ({len(cmds)})", value=names, inline=False)
        await ctx.send(embed=embed)

    @commands.hybrid_command(description="Show info about the bot.")
    async def botinfo(self, ctx):
        embed = discord.Embed(title=f"About {self.bot.user.name}", color=discord.Color.blurple())
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.add_field(name="Servers", value=len(self.bot.guilds))
        embed.add_field(name="Commands", value=len(set(self.bot.commands)))
        embed.add_field(name="Library", value=f"discord.py {discord.__version__}")
        embed.set_footer(text="Built with discord.py — organized into cogs by category.")
        await ctx.send(embed=embed)

    @commands.hybrid_command(description="See the bot's changelog (placeholder).")
    async def changelog(self, ctx):
        await ctx.send("📝 v1.0.0 — Initial release with 100+ commands across Utility, Fun, Moderation, Economy, and Games.")

    @commands.hybrid_command(description="Suggest a feature for the bot.")
    async def suggest(self, ctx, *, suggestion: str):
        await ctx.send(f"💡 Thanks for the suggestion, {ctx.author.mention}! (Hook this up to a suggestions channel/log.)")

    @commands.hybrid_command(description="Report a bug.")
    async def report(self, ctx, *, bug: str):
        await ctx.send(f"🐛 Bug report received, {ctx.author.mention}. (Hook this up to a bug-tracking channel/log.)")

    @commands.hybrid_command(description="Send feedback about the bot.")
    async def feedback(self, ctx, *, message: str):
        await ctx.send(f"📬 Thanks for the feedback, {ctx.author.mention}!")

    @commands.hybrid_command(description="Show useful links.")
    async def links(self, ctx):
        embed = discord.Embed(title="🔗 Links", color=discord.Color.blurple())
        embed.add_field(name="discord.py docs", value="https://discordpy.readthedocs.io/", inline=False)
        embed.add_field(name="Discord Developer Portal", value="https://discord.com/developers/applications", inline=False)
        await ctx.send(embed=embed)

    @commands.hybrid_command(description="Show bot credits.")
    async def credits(self, ctx):
        await ctx.send("🙌 Built with discord.py. Customize this with your own credits!")

    @commands.hybrid_command(description="Vote for the bot (placeholder for top.gg link).")
    async def vote(self, ctx):
        await ctx.send("🗳️ Add your top.gg (or similar) vote link here!")

    @commands.hybrid_command(description="Show the bot's privacy policy (placeholder).")
    async def privacy(self, ctx):
        await ctx.send("🔒 Add a link to your privacy policy here.")

    @commands.hybrid_command(description="Show the bot's terms of service (placeholder).")
    async def terms(self, ctx):
        await ctx.send("📜 Add a link to your terms of service here.")

async def setup(bot):
    await bot.add_cog(Info(bot))
