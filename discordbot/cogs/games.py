import random
import asyncio
import discord
from discord.ext import commands

TRIVIA = [
    {"q": "What is the capital of France?", "a": "paris"},
    {"q": "How many continents are there?", "a": "7"},
    {"q": "What is the largest planet in our solar system?", "a": "jupiter"},
    {"q": "What language is Discord.py written in?", "a": "python"},
    {"q": "How many sides does a hexagon have?", "a": "6"},
]

HANGMAN_WORDS = ["python", "discord", "keyboard", "internet", "computer", "programming"]


class TicTacToeButton(discord.ui.Button):
    def __init__(self, x, y):
        super().__init__(style=discord.ButtonStyle.secondary, label="\u200b", row=y)
        self.x = x
        self.y = y

    async def callback(self, interaction: discord.Interaction):
        view: "TicTacToeView" = self.view
        if interaction.user.id != view.current_player.id:
            await interaction.response.send_message("It's not your turn!", ephemeral=True)
            return
        if view.board[self.y][self.x] != 0:
            return
        symbol = "X" if view.current_player.id == view.player_x.id else "O"
        view.board[self.y][self.x] = 1 if symbol == "X" else 2
        self.label = symbol
        self.style = discord.ButtonStyle.success if symbol == "X" else discord.ButtonStyle.danger
        self.disabled = True

        winner = view.check_winner()
        if winner:
            for child in view.children:
                child.disabled = True
            await interaction.response.edit_message(content=f"🎉 {view.current_player.mention} wins!", view=view)
            return
        if view.is_draw():
            for child in view.children:
                child.disabled = True
            await interaction.response.edit_message(content="🤝 It's a draw!", view=view)
            return

        view.current_player = view.player_o if view.current_player.id == view.player_x.id else view.player_x
        await interaction.response.edit_message(content=f"Tic Tac Toe: {view.current_player.mention}'s turn", view=view)


class TicTacToeView(discord.ui.View):
    def __init__(self, player_x, player_o):
        super().__init__(timeout=120)
        self.player_x = player_x
        self.player_o = player_o
        self.current_player = player_x
        self.board = [[0] * 3 for _ in range(3)]
        for y in range(3):
            for x in range(3):
                self.add_item(TicTacToeButton(x, y))

    def check_winner(self):
        b = self.board
        lines = []
        lines.extend(b)
        lines.extend([[b[r][c] for r in range(3)] for c in range(3)])
        lines.append([b[i][i] for i in range(3)])
        lines.append([b[i][2 - i] for i in range(3)])
        for line in lines:
            if line[0] != 0 and line[0] == line[1] == line[2]:
                return line[0]
        return None

    def is_draw(self):
        return all(cell != 0 for row in self.board for cell in row)


class Games(commands.Cog):
    """Interactive mini-games."""

    def __init__(self, bot):
        self.bot = bot
        self.active_hangman = {}

    @commands.hybrid_command(description="Answer a random trivia question.")
    async def trivia(self, ctx):
        question = random.choice(TRIVIA)
        await ctx.send(f"❓ {question['q']} (You have 15 seconds!)")

        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author

        try:
            msg = await self.bot.wait_for("message", timeout=15.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send(f"⏰ Time's up! The answer was **{question['a']}**.")
            return
        if msg.content.strip().lower() == question["a"]:
            await ctx.send("✅ Correct!")
        else:
            await ctx.send(f"❌ Wrong! The answer was **{question['a']}**.")

    @commands.hybrid_command(description="Start a game of hangman.")
    @commands.guild_only()
    async def hangman(self, ctx):
        if ctx.channel.id in self.active_hangman:
            await ctx.send("A hangman game is already active in this channel.")
            return
        word = random.choice(HANGMAN_WORDS)
        state = {"word": word, "guessed": set(), "lives": 6}
        self.active_hangman[ctx.channel.id] = state
        display = " ".join("_" for _ in word)
        await ctx.send(f"🪢 Hangman started! `{display}` — {state['lives']} lives. Guess letters with `!guess <letter>`.")

    @commands.hybrid_command(description="Guess a letter in the active hangman game.")
    @commands.guild_only()
    async def guess(self, ctx, letter: str):
        state = self.active_hangman.get(ctx.channel.id)
        if not state:
            await ctx.send("No active hangman game. Start one with `!hangman`.")
            return
        letter = letter.lower()[0]
        word = state["word"]
        if letter in state["guessed"]:
            await ctx.send("Already guessed that letter.")
            return
        state["guessed"].add(letter)
        if letter not in word:
            state["lives"] -= 1
        display = " ".join(c if c in state["guessed"] else "_" for c in word)
        if all(c in state["guessed"] for c in word):
            await ctx.send(f"🎉 You guessed it! The word was **{word}**.")
            del self.active_hangman[ctx.channel.id]
            return
        if state["lives"] <= 0:
            await ctx.send(f"💀 Game over! The word was **{word}**.")
            del self.active_hangman[ctx.channel.id]
            return
        await ctx.send(f"`{display}` — {state['lives']} lives left.")

    @commands.hybrid_command(description="Play tic-tac-toe against another user.")
    @commands.guild_only()
    async def tictactoe(self, ctx, opponent: discord.Member):
        if opponent.bot or opponent.id == ctx.author.id:
            await ctx.send("Choose a valid opponent (not yourself or a bot).")
            return
        view = TicTacToeView(ctx.author, opponent)
        await ctx.send(f"Tic Tac Toe: {ctx.author.mention} (X) vs {opponent.mention} (O). {ctx.author.mention}'s turn.", view=view)

    @commands.hybrid_command(description="Guess a secret number between 1 and 100.")
    async def guessnumber(self, ctx):
        number = random.randint(1, 100)
        await ctx.send("🔢 I'm thinking of a number between 1-100. You have 5 guesses!")

        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author and m.content.isdigit()

        for attempt in range(5):
            try:
                msg = await self.bot.wait_for("message", timeout=20.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send(f"⏰ Time's up! The number was **{number}**.")
                return
            guess = int(msg.content)
            if guess == number:
                await ctx.send(f"🎉 Correct! It took you {attempt + 1} guess(es).")
                return
            elif guess < number:
                await ctx.send("📈 Higher!")
            else:
                await ctx.send("📉 Lower!")
        await ctx.send(f"❌ Out of guesses! The number was **{number}**.")

    @commands.hybrid_command(description="Race to type a random phrase the fastest.")
    async def typerace(self, ctx):
        phrases = ["the quick brown fox jumps over the lazy dog", "discord bots are fun to build", "practice makes perfect"]
        phrase = random.choice(phrases)
        await ctx.send(f"⌨️ Type this as fast as you can:\n**{phrase}**")
        start = asyncio.get_event_loop().time()

        def check(m):
            return m.channel == ctx.channel and m.content.strip().lower() == phrase

        try:
            msg = await self.bot.wait_for("message", timeout=30.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("⏰ No one finished in time!")
            return
        elapsed = asyncio.get_event_loop().time() - start
        await ctx.send(f"🏁 {msg.author.mention} finished in **{elapsed:.2f}s**!")

    @commands.hybrid_command(description="Flip a series of cards for blackjack-lite (just for fun, no betting).")
    async def blackjack(self, ctx):
        def draw():
            return random.randint(1, 11)

        player = [draw(), draw()]
        dealer = [draw(), draw()]
        await ctx.send(f"🃏 Your hand: {player} (total {sum(player)}) | Dealer shows: {dealer[0]}")
        await ctx.send("This is a simplified demo — extend it with hit/stand buttons for the full game.")

    @commands.hybrid_command(description="Play connect four against another user (placeholder outline).")
    @commands.guild_only()
    async def connect4(self, ctx, opponent: discord.Member):
        await ctx.send(f"🔴🟡 Connect Four between {ctx.author.mention} and {opponent.mention} — extend `games.py` with a full grid+button UI similar to tictactoe.")

async def setup(bot):
    await bot.add_cog(Games(bot))
