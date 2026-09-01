import discord
from discord.ext import commands
import datetime

class Moderation(commands.Cog):
    """Server moderation commands. Require appropriate permissions."""

    def __init__(self, bot):
        self.bot = bot
        self.warning_data = {}  # {guild_id: {user_id: [reasons]}}

    @commands.hybrid_command(description="Kick a member.")
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    @commands.guild_only()
    async def kick(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        await member.kick(reason=reason)
        await ctx.send(f"👢 Kicked {member} — {reason}")

    @commands.hybrid_command(description="Ban a member.")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.guild_only()
    async def ban(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        await member.ban(reason=reason)
        await ctx.send(f"🔨 Banned {member} — {reason}")

    @commands.hybrid_command(description="Unban a user by ID.")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.guild_only()
    async def unban(self, ctx, user_id: int):
        user = await self.bot.fetch_user(user_id)
        await ctx.guild.unban(user)
        await ctx.send(f"✅ Unbanned {user}")

    @commands.hybrid_command(description="Softban a member (ban + unban to clear messages).")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.guild_only()
    async def softban(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        await member.ban(reason=reason, delete_message_days=1)
        await ctx.guild.unban(member)
        await ctx.send(f"🔨 Softbanned {member} — {reason}")

    @commands.hybrid_command(description="Timeout a member for N minutes.")
    @commands.has_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    @commands.guild_only()
    async def timeout(self, ctx, member: discord.Member, minutes: int, *, reason: str = "No reason provided"):
        until = discord.utils.utcnow() + datetime.timedelta(minutes=minutes)
        await member.timeout(until, reason=reason)
        await ctx.send(f"🔇 Timed out {member} for {minutes} minute(s) — {reason}")

    @commands.hybrid_command(description="Remove a member's timeout.")
    @commands.has_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    @commands.guild_only()
    async def untimeout(self, ctx, member: discord.Member):
        await member.timeout(None)
        await ctx.send(f"🔊 Removed timeout for {member}")

    @commands.hybrid_command(description="Warn a member.")
    @commands.has_permissions(moderate_members=True)
    @commands.guild_only()
    async def warn(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        g = self.warning_data.setdefault(ctx.guild.id, {})
        u = g.setdefault(member.id, [])
        u.append(reason)
        await ctx.send(f"⚠️ Warned {member} — {reason} (Total warnings: {len(u)})")

    @commands.hybrid_command(description="Show a member's warnings.")
    @commands.has_permissions(moderate_members=True)
    @commands.guild_only()
    async def warnings(self, ctx, member: discord.Member):
        reasons = self.warning_data.get(ctx.guild.id, {}).get(member.id, [])
        if not reasons:
            await ctx.send(f"{member} has no warnings.")
            return
        listing = "\n".join(f"{i+1}. {r}" for i, r in enumerate(reasons))
        await ctx.send(f"⚠️ Warnings for {member}:\n{listing}")

    @commands.hybrid_command(description="Clear a member's warnings.")
    @commands.has_permissions(moderate_members=True)
    @commands.guild_only()
    async def clearwarnings(self, ctx, member: discord.Member):
        self.warning_data.get(ctx.guild.id, {}).pop(member.id, None)
        await ctx.send(f"✅ Cleared warnings for {member}")

    @commands.hybrid_command(description="Delete N messages from this channel.")
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    @commands.guild_only()
    async def purge(self, ctx, amount: int):
        amount = max(1, min(amount, 100))
        deleted = await ctx.channel.purge(limit=amount + 1)
        msg = await ctx.send(f"🧹 Deleted {len(deleted) - 1} messages.")
        await msg.delete(delay=3)

    @commands.hybrid_command(description="Set slowmode for this channel (seconds).")
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    @commands.guild_only()
    async def slowmode(self, ctx, seconds: int):
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"🐌 Slowmode set to {seconds}s")

    @commands.hybrid_command(description="Lock this channel (deny @everyone send messages).")
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    @commands.guild_only()
    async def lock(self, ctx):
        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send("🔒 Channel locked.")

    @commands.hybrid_command(description="Unlock this channel.")
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    @commands.guild_only()
    async def unlock(self, ctx):
        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = None
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send("🔓 Channel unlocked.")

    @commands.hybrid_command(description="Change a member's nickname.")
    @commands.has_permissions(manage_nicknames=True)
    @commands.bot_has_permissions(manage_nicknames=True)
    @commands.guild_only()
    async def nick(self, ctx, member: discord.Member, *, nickname: str = None):
        await member.edit(nick=nickname)
        await ctx.send(f"✏️ Changed {member}'s nickname to {nickname or 'default'}")

    @commands.hybrid_command(description="Add a role to a member.")
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    @commands.guild_only()
    async def addrole(self, ctx, member: discord.Member, *, role: discord.Role):
        await member.add_roles(role)
        await ctx.send(f"✅ Added {role.name} to {member}")

    @commands.hybrid_command(description="Remove a role from a member.")
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    @commands.guild_only()
    async def removerole(self, ctx, member: discord.Member, *, role: discord.Role):
        await member.remove_roles(role)
        await ctx.send(f"✅ Removed {role.name} from {member}")

async def setup(bot):
    await bot.add_cog(Moderation(bot))
