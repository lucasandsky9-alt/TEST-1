import random
import discord
from discord.ext import commands

JOKES = [
    "Why don't scientists trust atoms? Because they make up everything.",
    "I told my computer I needed a break, and it froze.",
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "I would tell you a UDP joke, but you might not get it.",
    "There are 10 types of people: those who understand binary and those who don't.",
]

FACTS = [
    "Honey never spoils.",
    "Bananas are berries, but strawberries aren't.",
    "Octopuses have three hearts.",
    "A day on Venus is longer than its year.",
    "Sharks existed before trees.",
]

QUOTES = [
    "The only way to do great work is to love what you do.",
    "Success is not final, failure is not fatal.",
    "In the middle of difficulty lies opportunity.",
    "Do what you can, with what you have, where you are.",
]

EIGHTBALL = [
    "Yes.", "No.", "Maybe.", "Ask again later.", "Definitely!", "Absolutely not.",
    "It is certain.", "Very doubtful.", "Signs point to yes.", "Cannot predict now.",
]

WYR = [
    "Would you rather be able to fly or be invisible?",
    "Would you rather have unlimited money or unlimited time?",
    "Would you rather live without music or without TV?",
    "Would you rather explore space or the ocean?",
]


class Fun(commands.Cog):
    """Fun and entertainment commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(description="Tell a random joke.")
    async def joke(self, ctx):
        await ctx.send(random.choice(JOKES))

    @commands.hybrid_command(description="Get a random meme (placeholder for meme API).")
    async def meme(self, ctx):
        await ctx.send("😂 Hook this up to a meme API (e.g. meme-api.com) for random memes.")

    @commands.hybrid_command(name="8ball", description="Ask the magic 8-ball a question.")
    async def eightball(self, ctx, *, question: str):
        await ctx.send(f"🎱 {random.choice(EIGHTBALL)}")

    @commands.hybrid_command(description="Flip a coin.")
    async def coinflip(self, ctx):
        await ctx.send(f"🪙 {random.choice(['Heads', 'Tails'])}!")

    @commands.hybrid_command(description="Roll a dice (default d6, or specify sides).")
    async def dice(self, ctx, sides: int = 6):
        if sides < 2:
            await ctx.send("Need at least 2 sides.")
            return
        await ctx.send(f"🎲 You rolled a **{random.randint(1, sides)}** (d{sides})")

    @commands.hybrid_command(description="Play rock-paper-scissors.")
    async def rps(self, ctx, choice: str):
        choice = choice.lower()
        options = ["rock", "paper", "scissors"]
        if choice not in options:
            await ctx.send("Choose rock, paper, or scissors.")
            return
        bot_choice = random.choice(options)
        if choice == bot_choice:
            result = "It's a tie!"
        elif (choice, bot_choice) in [("rock", "scissors"), ("paper", "rock"), ("scissors", "paper")]:
            result = "You win!"
        else:
            result = "I win!"
        await ctx.send(f"You chose **{choice}**, I chose **{bot_choice}**. {result}")

    @commands.hybrid_command(description="Give someone a friendly compliment.")
    async def compliment(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        compliments = [
            "is an amazing person!", "lights up the room!", "has great taste!",
            "is incredibly talented!", "makes everything better!",
        ]
        await ctx.send(f"{member.mention} {random.choice(compliments)}")

    @commands.hybrid_command(description="Ship two users together.")
    async def ship(self, ctx, user1: discord.Member, user2: discord.Member = None):
        user2 = user2 or ctx.author
        score = random.randint(0, 100)
        bar = "█" * (score // 10) + "░" * (10 - score // 10)
        await ctx.send(f"💘 {user1.mention} + {user2.mention} = **{score}%**\n`{bar}`")

    @commands.hybrid_command(description="Give someone a hug.")
    async def hug(self, ctx, member: discord.Member):
        await ctx.send(f"🤗 {ctx.author.mention} hugs {member.mention}!")

    @commands.hybrid_command(description="Give someone a pat.")
    async def pat(self, ctx, member: discord.Member):
        await ctx.send(f"🖐️ {ctx.author.mention} pats {member.mention} on the head!")

    @commands.hybrid_command(description="High five someone.")
    async def highfive(self, ctx, member: discord.Member):
        await ctx.send(f"🙌 {ctx.author.mention} high-fives {member.mention}!")

    @commands.hybrid_command(description="Poke someone.")
    async def poke(self, ctx, member: discord.Member):
        await ctx.send(f"👉 {ctx.author.mention} pokes {member.mention}!")

    @commands.hybrid_command(description="Get a random fun fact.")
    async def fact(self, ctx):
        await ctx.send(f"📚 Did you know? {random.choice(FACTS)}")

    @commands.hybrid_command(description="Get an inspirational quote.")
    async def quote(self, ctx):
        await ctx.send(f"💬 \"{random.choice(QUOTES)}\"")

    @commands.hybrid_command(description="Reverse some text.")
    async def reverse(self, ctx, *, text: str):
        await ctx.send(text[::-1])

    @commands.hybrid_command(description="mOcK tHe TeXt LiKe ThIs.")
    async def mock(self, ctx, *, text: str):
        mocked = "".join(c.upper() if i % 2 else c.lower() for i, c in enumerate(text))
        await ctx.send(mocked)

    @commands.hybrid_command(description="Have the bot choose between options.")
    async def choose(self, ctx, *, options: str):
        choices = [o.strip() for o in options.split(",") if o.strip()]
        if len(choices) < 2:
            await ctx.send("Give me at least two options separated by commas.")
            return
        await ctx.send(f"🤔 I choose: **{random.choice(choices)}**")

    @commands.hybrid_command(description="Get a 'would you rather' question.")
    async def wyr(self, ctx):
        await ctx.send(f"🤔 {random.choice(WYR)}")

    @commands.hybrid_command(description="Turn text into ascii-style spaced letters.")
    async def ascii(self, ctx, *, text: str):
        await ctx.send(" ".join(text.upper()))

    @commands.hybrid_command(description="Roll a percentage for something silly.")
    async def rate(self, ctx, *, thing: str):
        await ctx.send(f"📈 I'd rate **{thing}** a **{random.randint(0, 100)}/100**")

    @commands.hybrid_command(description="Get a random cat picture (placeholder for cat API).")
    async def cat(self, ctx):
        await ctx.send("🐱 Hook this up to an API like thecatapi.com for random cat pics.")

    @commands.hybrid_command(description="Get a random dog picture (placeholder for dog API).")
    async def dog(self, ctx):
        await ctx.send("🐶 Hook this up to an API like dog.ceo for random dog pics.")

    @commands.hybrid_command(description="Say something as a fake announcement.")
    async def announce(self, ctx, *, message: str):
        embed = discord.Embed(title="📢 Announcement", description=message, color=discord.Color.red())
        await ctx.send(embed=embed)

    @commands.hybrid_command(description="Generate a random number between two values.")
    async def random_number(self, ctx, low: int = 1, high: int = 100):
        if low > high:
            low, high = high, low
        await ctx.send(f"🔢 {random.randint(low, high)}")

    @commands.hybrid_command(description="Flip a virtual coin multiple times.")
    async def multiflip(self, ctx, times: int = 5):
        times = max(1, min(times, 50))
        results = [random.choice(["H", "T"]) for _ in range(times)]
        await ctx.send(" ".join(results))

    @commands.hybrid_command(description="Generate a random password.")
    async def genpassword(self, ctx, length: int = 12):
        import string
        length = max(4, min(length, 64))
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        pw = "".join(random.choice(chars) for _ in range(length))
        try:
            await ctx.author.send(f"🔐 Your generated password: `{pw}`")
            await ctx.send("Sent you a DM with your password!")
        except discord.Forbidden:
            await ctx.send(f"🔐 `{pw}` (enable DMs next time for privacy)")

    @commands.hybrid_command(description="Get a random inspirational-sounding fake movie title.")
    async def moviename(self, ctx):
        adjectives = ["The Last", "Rise of the", "Legend of the", "Curse of the", "Chronicles of the"]
        nouns = ["Shadow Wolf", "Iron Phoenix", "Silent Storm", "Lost Kingdom", "Crimson Tide"]
        await ctx.send(f"🎬 *{random.choice(adjectives)} {random.choice(nouns)}*")

    @commands.hybrid_command(description="Generate a random band name.")
    async def bandname(self, ctx):
        words1 = ["Electric", "Velvet", "Broken", "Neon", "Midnight"]
        words2 = ["Wolves", "Sirens", "Echoes", "Drifters", "Kingdom"]
        await ctx.send(f"🎸 {random.choice(words1)} {random.choice(words2)}")

    @commands.hybrid_command(description="Roast someone playfully (all in good fun).")
    async def roast(self, ctx, member: discord.Member):
        roasts = [
            "you're the reason the gene pool needs a lifeguard.",
            "you bring everyone so much joy... when you leave the room.",
            "I'd explain it to you, but I don't have crayons.",
        ]
        await ctx.send(f"{member.mention}, {random.choice(roasts)}")

async def setup(bot):
    await bot.add_cog(Fun(bot))
