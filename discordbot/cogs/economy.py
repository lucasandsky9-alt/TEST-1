import json
import os
import random
import time
import discord
from discord.ext import commands

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "economy.json")

SHOP_ITEMS = {
    "fishing_rod": {"price": 100, "desc": "Lets you fish for coins."},
    "pickaxe": {"price": 150, "desc": "Lets you dig for coins."},
    "lucky_charm": {"price": 300, "desc": "Slightly better gambling odds."},
    "trophy": {"price": 1000, "desc": "Just for bragging rights."},
}

def load_data():
    if not os.path.exists(DATA_PATH):
        return {}
    with open(DATA_PATH, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_data(data):
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=2)


class Economy(commands.Cog):
    """A simple virtual-currency economy system, stored in a local JSON file."""

    def __init__(self, bot):
        self.bot = bot
        self.data = load_data()

    def get_user(self, user_id):
        uid = str(user_id)
        if uid not in self.data:
            self.data[uid] = {"balance": 100, "bank": 0, "inventory": [], "last_daily": 0, "last_work": 0, "last_crime": 0, "last_beg": 0}
        return self.data[uid]

    def save(self):
        save_data(self.data)

    @commands.hybrid_command(description="Check your (or someone's) balance.")
    async def balance(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        u = self.get_user(member.id)
        await ctx.send(f"💰 {member.display_name}: **{u['balance']}** coins (bank: {u['bank']})")

    @commands.hybrid_command(description="Claim your daily coins.")
    async def daily(self, ctx):
        u = self.get_user(ctx.author.id)
        now = time.time()
        if now - u["last_daily"] < 86400:
            remaining = 86400 - (now - u["last_daily"])
            await ctx.send(f"⏳ Already claimed. Try again in {int(remaining // 3600)}h.")
            return
        amount = random.randint(100, 300)
        u["balance"] += amount
        u["last_daily"] = now
        self.save()
        await ctx.send(f"🎁 You claimed your daily reward of **{amount}** coins!")

    @commands.hybrid_command(description="Work for some coins.")
    async def work(self, ctx):
        u = self.get_user(ctx.author.id)
        now = time.time()
        if now - u["last_work"] < 1800:
            remaining = 1800 - (now - u["last_work"])
            await ctx.send(f"⏳ You're tired. Rest for {int(remaining // 60)}m.")
            return
        jobs = ["delivered pizzas", "coded a website", "walked dogs", "washed cars", "mowed lawns"]
        amount = random.randint(50, 150)
        u["balance"] += amount
        u["last_work"] = now
        self.save()
        await ctx.send(f"💼 You {random.choice(jobs)} and earned **{amount}** coins!")

    @commands.hybrid_command(description="Attempt a risky crime for coins.")
    async def crime(self, ctx):
        u = self.get_user(ctx.author.id)
        now = time.time()
        if now - u["last_crime"] < 3600:
            remaining = 3600 - (now - u["last_crime"])
            await ctx.send(f"⏳ Lay low for {int(remaining // 60)}m before trying again.")
            return
        u["last_crime"] = now
        if random.random() < 0.5:
            amount = random.randint(100, 400)
            u["balance"] += amount
            msg = f"🕵️ Success! You pulled off a heist and got **{amount}** coins!"
        else:
            amount = min(u["balance"], random.randint(50, 200))
            u["balance"] -= amount
            msg = f"🚔 Busted! You paid **{amount}** coins in fines."
        self.save()
        await ctx.send(msg)

    @commands.hybrid_command(description="Beg for some spare coins.")
    async def beg(self, ctx):
        u = self.get_user(ctx.author.id)
        now = time.time()
        if now - u["last_beg"] < 600:
            remaining = 600 - (now - u["last_beg"])
            await ctx.send(f"⏳ Wait {int(remaining // 60)}m before begging again.")
            return
        amount = random.randint(0, 50)
        u["balance"] += amount
        u["last_beg"] = now
        self.save()
        await ctx.send(f"🙏 A stranger gave you **{amount}** coins." if amount else "🙏 No one gave you anything this time.")

    @commands.hybrid_command(description="Go fishing (requires a fishing rod).")
    async def fish(self, ctx):
        u = self.get_user(ctx.author.id)
        if "fishing_rod" not in u["inventory"]:
            await ctx.send("🎣 You need a fishing rod! Buy one with `!buy fishing_rod`.")
            return
        amount = random.randint(20, 100)
        u["balance"] += amount
        self.save()
        await ctx.send(f"🎣 You caught a fish and sold it for **{amount}** coins!")

    @commands.hybrid_command(description="Go digging (requires a pickaxe).")
    async def dig(self, ctx):
        u = self.get_user(ctx.author.id)
        if "pickaxe" not in u["inventory"]:
            await ctx.send("⛏️ You need a pickaxe! Buy one with `!buy pickaxe`.")
            return
        amount = random.randint(20, 120)
        u["balance"] += amount
        self.save()
        await ctx.send(f"⛏️ You dug up treasure worth **{amount}** coins!")

    @commands.hybrid_command(description="Rob another user (risky!).")
    async def rob(self, ctx, member: discord.Member):
        if member.id == ctx.author.id:
            await ctx.send("You can't rob yourself.")
            return
        thief = self.get_user(ctx.author.id)
        target = self.get_user(member.id)
        if target["balance"] < 50:
            await ctx.send(f"{member.display_name} is too poor to rob.")
            return
        if random.random() < 0.4:
            amount = random.randint(10, min(200, target["balance"]))
            target["balance"] -= amount
            thief["balance"] += amount
            self.save()
            await ctx.send(f"🦹 You robbed **{amount}** coins from {member.display_name}!")
        else:
            fine = min(thief["balance"], random.randint(20, 100))
            thief["balance"] -= fine
            self.save()
            await ctx.send(f"🚨 You got caught and paid a **{fine}** coin fine!")

    @commands.hybrid_command(description="Gamble your coins (50/50 double or nothing).")
    async def gamble(self, ctx, amount: int):
        u = self.get_user(ctx.author.id)
        if amount <= 0 or amount > u["balance"]:
            await ctx.send("Invalid amount.")
            return
        if random.random() < 0.5:
            u["balance"] += amount
            msg = f"🎉 You won! +{amount} coins."
        else:
            u["balance"] -= amount
            msg = f"💸 You lost {amount} coins."
        self.save()
        await ctx.send(msg)

    @commands.hybrid_command(description="Play the slot machine.")
    async def slots(self, ctx, amount: int):
        u = self.get_user(ctx.author.id)
        if amount <= 0 or amount > u["balance"]:
            await ctx.send("Invalid amount.")
            return
        symbols = ["🍒", "🍋", "🍇", "💎", "7️⃣"]
        roll = [random.choice(symbols) for _ in range(3)]
        display = " ".join(roll)
        if roll[0] == roll[1] == roll[2]:
            winnings = amount * 5
            u["balance"] += winnings
            msg = f"{display}\n🎰 JACKPOT! You won **{winnings}** coins!"
        elif len(set(roll)) == 2:
            winnings = amount
            u["balance"] += winnings
            msg = f"{display}\n🎰 Small win! You won **{winnings}** coins!"
        else:
            u["balance"] -= amount
            msg = f"{display}\n🎰 No match. You lost **{amount}** coins."
        self.save()
        await ctx.send(msg)

    @commands.hybrid_command(description="Pay another user some coins.")
    async def pay(self, ctx, member: discord.Member, amount: int):
        if amount <= 0:
            await ctx.send("Amount must be positive.")
            return
        sender = self.get_user(ctx.author.id)
        if sender["balance"] < amount:
            await ctx.send("You don't have enough coins.")
            return
        receiver = self.get_user(member.id)
        sender["balance"] -= amount
        receiver["balance"] += amount
        self.save()
        await ctx.send(f"💸 {ctx.author.display_name} paid {member.display_name} **{amount}** coins.")

    @commands.hybrid_command(description="Deposit coins into your bank.")
    async def deposit(self, ctx, amount: int):
        u = self.get_user(ctx.author.id)
        if amount <= 0 or amount > u["balance"]:
            await ctx.send("Invalid amount.")
            return
        u["balance"] -= amount
        u["bank"] += amount
        self.save()
        await ctx.send(f"🏦 Deposited **{amount}** coins.")

    @commands.hybrid_command(description="Withdraw coins from your bank.")
    async def withdraw(self, ctx, amount: int):
        u = self.get_user(ctx.author.id)
        if amount <= 0 or amount > u["bank"]:
            await ctx.send("Invalid amount.")
            return
        u["bank"] -= amount
        u["balance"] += amount
        self.save()
        await ctx.send(f"🏦 Withdrew **{amount}** coins.")

    @commands.hybrid_command(description="View the shop.")
    async def shop(self, ctx):
        embed = discord.Embed(title="🛒 Shop", color=discord.Color.gold())
        for name, item in SHOP_ITEMS.items():
            embed.add_field(name=f"{name} — {item['price']} coins", value=item["desc"], inline=False)
        await ctx.send(embed=embed)

    @commands.hybrid_command(description="Buy an item from the shop.")
    async def buy(self, ctx, item: str):
        item = item.lower()
        if item not in SHOP_ITEMS:
            await ctx.send("That item doesn't exist. Check `!shop`.")
            return
        u = self.get_user(ctx.author.id)
        price = SHOP_ITEMS[item]["price"]
        if u["balance"] < price:
            await ctx.send("You can't afford that.")
            return
        u["balance"] -= price
        u["inventory"].append(item)
        self.save()
        await ctx.send(f"✅ Bought **{item}** for {price} coins!")

    @commands.hybrid_command(description="Sell an item from your inventory.")
    async def sell(self, ctx, item: str):
        item = item.lower()
        u = self.get_user(ctx.author.id)
        if item not in u["inventory"]:
            await ctx.send("You don't own that item.")
            return
        u["inventory"].remove(item)
        refund = SHOP_ITEMS.get(item, {}).get("price", 0) // 2
        u["balance"] += refund
        self.save()
        await ctx.send(f"💰 Sold **{item}** for {refund} coins.")

    @commands.hybrid_command(description="View your inventory.")
    async def inventory(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        u = self.get_user(member.id)
        if not u["inventory"]:
            await ctx.send(f"{member.display_name}'s inventory is empty.")
            return
        await ctx.send(f"🎒 {member.display_name}'s inventory: {', '.join(u['inventory'])}")

    @commands.hybrid_command(description="Show the richest users leaderboard.")
    @commands.guild_only()
    async def leaderboard(self, ctx):
        entries = []
        for uid, u in self.data.items():
            member = ctx.guild.get_member(int(uid))
            if member:
                entries.append((member.display_name, u["balance"] + u["bank"]))
        entries.sort(key=lambda x: x[1], reverse=True)
        top = entries[:10]
        if not top:
            await ctx.send("No data yet.")
            return
        lines = [f"{i+1}. {name} — {bal} coins" for i, (name, bal) in enumerate(top)]
        await ctx.send("🏆 **Leaderboard**\n" + "\n".join(lines))

async def setup(bot):
    await bot.add_cog(Economy(bot))
