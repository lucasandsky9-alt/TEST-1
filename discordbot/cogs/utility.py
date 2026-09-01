import time
import asyncio
import platform
import discord
from discord.ext import commands
import datetime

class Utility(commands.Cog):
    """General utility and information commands."""

    def __init__(self, bot):
        self.bot = bot
        self.reminders = {}

    @commands.hybrid_command(description="Check the bot's latency.")
    async def ping(self, ctx):
        await ctx.send(f"🏓 Pong! `{round(self.bot.latency * 1000)}ms`")

    @commands.hybrid_command(description="Show info about a user.")
    async def userinfo(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(title=f"{member}", color=discord.Color.blurple())
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="ID", value=member.id)
        embed.add_field(name="Joined server", value=discord.utils.format_dt(member.joined_at) if member.joined_at else "Unknown")
        embed.add_field(name="Account created", value=discord.utils.format_dt(member.created_at))
        embed.add_field(name="Top role", value=member.top_role.mention if hasattr(member, "top_role") else "N/A")
        embed.add_field(name="Bot?", value=str(member.bot))
        await ctx.send(embed=embed)

    @commands.hybrid_command(description="Show info about this server.")
    @commands.guild_only()
    async def serverinfo(self, ctx):
        g = ctx.guild
        embed = discord.Embed(title=g.name, color=discord.Color.green())
        if g.icon:
            embed.set_thumbnail(url=g.icon.url)
        embed.add_field(name="Owner", value=str(g.owner))
        embed.add_field(name="Members", value=g.member_count)
        embed.add_field(name="Created", value=discord.utils.format_dt(g.created_at))
        embed.add_field(name="Channels", value=len(g.channels))
        embed.add_field(name="Roles", value=len(g.roles))
        embed.add_field(name="Boosts", value=g.premium_subscription_count)
        await ctx.send(embed=embed)

    @commands.hybrid_command(description="Get a user's avatar.")
    async def avatar(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(title=f"{member}'s avatar", color=discord.Color.blurple())
        embed.set_image(url=member.display_avatar.url)
        await ctx.send(embed=embed)

    @commands.hybrid_command(description="Show info about a role.")
    @commands.guild_only()
    async def roleinfo(self, ctx, *, role: discord.Role):
        embed = discord.Embed(title=role.name, color=role.color)
        embed.add_field(name="ID", value=role.id)
        embed.add_field(name="Members", value=len(role.members))
        embed.add_field(name="Position", value=role.position)
        embed.add_field(name="Mentionable", value=role.mentionable)
        embed.add_field(name="Hoisted", value=role.hoist)
        await ctx.send(embed=embed)

    @commands.hybrid_command(description="Show info about a channel.")
    @commands.guild_only()
    async def channelinfo(self, ctx, channel: discord.abc.GuildChannel = None):
        channel = channel or ctx.channel
        embed = discord.Embed(title=f"#{channel.name}", color=discord.Color.blurple())
        embed.add_field(name="ID", value=channel.id)
        embed.add_field(name="Type", value=str(channel.type))
        embed.add_field(name="Created", value=discord.utils.format_dt(channel.created_at))
        await ctx.send(embed=embed)

    @commands.hybrid_command(description="Get the bot's invite link.")
    async def invite(self, ctx):
        perms = discord.Permissions(permissions=8)
        url = discord.utils.oauth_url(self.bot.user.id, permissions=perms)
        await ctx.send(f"Invite me: <{url}>")

    @commands.hybrid_command(description="Show how long the bot has been running.")
    async def uptime(self, ctx):
        delta = datetime.datetime.utcnow() - self.bot.start_time
        hours, rem = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(rem, 60)
        await ctx.send(f"⏱️ Uptime: `{hours}h {minutes}m {seconds}s`")

    @commands.hybrid_command(description="Start a simple yes/no poll.")
    async def poll(self, ctx, *, question: str):
        embed = discord.Embed(title="📊 Poll", description=question, color=discord.Color.orange())
        embed.set_footer(text=f"Asked by {ctx.author}")
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")

    @commands.hybrid_command(description="Set a reminder (in minutes).")
    async def remindme(self, ctx, minutes: float, *, reminder: str):
        await ctx.send(f"⏰ Okay {ctx.author.mention}, I'll remind you in {minutes} minute(s).")

        async def send_reminder():
            await asyncio.sleep(minutes * 60)
            try:
                await ctx.author.send(f"⏰ Reminder: {reminder}")
            except discord.Forbidden:
                await ctx.send(f"{ctx.author.mention} ⏰ Reminder: {reminder}")

        self.bot.loop.create_task(send_reminder())

    @commands.hybrid_command(description="Evaluate a basic math expression.")
    async def calc(self, ctx, *, expression: str):
        allowed = set("0123456789+-*/(). ")
        if not set(expression) <= allowed:
            await ctx.send("Only numbers and + - * / ( ) are allowed.")
            return
        try:
            result = eval(expression, {"__builtins__": {}})
            await ctx.send(f"🧮 `{expression}` = **{result}**")
        except Exception:
            await ctx.send("Couldn't evaluate that expression.")

    @commands.hybrid_command(description="Show a simple dictionary-style definition (placeholder).")
    async def define(self, ctx, *, word: str):
        await ctx.send(f"📖 Hook this up to a dictionary API (e.g. dictionaryapi.dev) to define **{word}**.")

    @commands.hybrid_command(description="Show current weather for a location (placeholder).")
    async def weather(self, ctx, *, location: str):
        await ctx.send(f"🌦️ Hook this up to a weather API (e.g. OpenWeatherMap) to show weather for **{location}**.")

    @commands.hybrid_command(description="Translate text (placeholder).")
    async def translate(self, ctx, lang: str, *, text: str):
        await ctx.send(f"🌐 Hook this up to a translation API to translate to **{lang}**: {text}")

    @commands.hybrid_command(description="Show bot and system stats.")
    async def stats(self, ctx):
        embed = discord.Embed(title="Bot Stats", color=discord.Color.blurple())
        embed.add_field(name="Servers", value=len(self.bot.guilds))
        embed.add_field(name="Users", value=sum(g.member_count for g in self.bot.guilds))
        embed.add_field(name="Commands", value=len(set(self.bot.commands)))
        embed.add_field(name="Python", value=platform.python_version())
        embed.add_field(name="discord.py", value=discord.__version__)
        embed.add_field(name="Latency", value=f"{round(self.bot.latency * 1000)}ms")
        await ctx.send(embed=embed)

    @commands.hybrid_command(description="Shorten a URL (placeholder).")
    async def shorten(self, ctx, url: str):
        await ctx.send(f"🔗 Hook this up to a URL-shortener API to shorten: {url}")

    @commands.hybrid_command(description="Show the raw content of a message by ID.")
    @commands.guild_only()
    async def rawmessage(self, ctx, message_id: int):
        try:
            msg = await ctx.channel.fetch_message(message_id)
        except discord.NotFound:
            await ctx.send("Message not found in this channel.")
            return
        await ctx.send(f"```{discord.utils.escape_markdown(msg.content)[:1900]}```")

    @commands.hybrid_command(description="Show the current server's emoji list.")
    @commands.guild_only()
    async def emojis(self, ctx):
        if not ctx.guild.emojis:
            await ctx.send("This server has no custom emojis.")
            return
        await ctx.send(" ".join(str(e) for e in ctx.guild.emojis[:50]))

    @commands.hybrid_command(description="Show the number of members in each role.")
    @commands.guild_only()
    async def rolecounts(self, ctx):
        lines = [f"{r.name}: {len(r.members)}" for r in sorted(ctx.guild.roles, key=lambda r: -len(r.members))[:15]]
        await ctx.send("\n".join(lines))

    @commands.hybrid_command(description="Convert a value between simple units (km/mi, kg/lb, c/f).")
    async def convert(self, ctx, value: float, from_unit: str, to_unit: str):
        conversions = {
            ("km", "mi"): lambda v: v * 0.621371,
            ("mi", "km"): lambda v: v / 0.621371,
            ("kg", "lb"): lambda v: v * 2.20462,
            ("lb", "kg"): lambda v: v / 2.20462,
            ("c", "f"): lambda v: v * 9 / 5 + 32,
            ("f", "c"): lambda v: (v - 32) * 5 / 9,
        }
        key = (from_unit.lower(), to_unit.lower())
        if key not in conversions:
            await ctx.send("Supported: km<->mi, kg<->lb, c<->f")
            return
        result = conversions[key](value)
        await ctx.send(f"{value}{from_unit} = **{result:.2f}{to_unit}**")

    @commands.hybrid_command(description="Show the current timestamp in Discord's timestamp format.")
    async def timestamp(self, ctx):
        now = discord.utils.utcnow()
        await ctx.send(f"{discord.utils.format_dt(now, 'F')} (`{int(now.timestamp())}`)")

async def setup(bot):
    bot.start_time = getattr(bot, "start_time", __import__("datetime").datetime.utcnow())
    await bot.add_cog(Utility(bot))
