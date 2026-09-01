# Discord Bot — 100+ Commands

A Python bot built with `discord.py`, organized into cogs by category so it stays maintainable
despite the large command count. Every command works both as a `!prefix` command and as a
`/slash` command (hybrid commands).

## Categories (103 commands total)

| Cog | File | Commands | Examples |
|---|---|---|---|
| Utility | `cogs/utility.py` | 21 | `ping`, `userinfo`, `serverinfo`, `poll`, `remindme`, `calc`, `convert` |
| Fun | `cogs/fun.py` | 29 | `joke`, `8ball`, `rps`, `ship`, `hug`, `fact`, `choose`, `roast` |
| Moderation | `cogs/moderation.py` | 16 | `kick`, `ban`, `timeout`, `warn`, `purge`, `lock`, `addrole` |
| Economy | `cogs/economy.py` | 18 | `balance`, `daily`, `work`, `gamble`, `slots`, `shop`, `leaderboard` |
| Games | `cogs/games.py` | 8 | `trivia`, `hangman`, `tictactoe`, `guessnumber`, `typerace` |
| Info | `cogs/info.py` | 11 | `help`, `botinfo`, `suggest`, `report`, `links` |

Run `!help` in Discord any time for the live, auto-generated list (it counts your actual loaded
commands, so it stays accurate if you add more).

## Setup

1. **Create a bot application**
   - Go to the [Discord Developer Portal](https://discord.com/developers/applications) → New Application.
   - Go to the "Bot" tab → Add Bot → copy the token.
   - Under "Privileged Gateway Intents", enable **Message Content Intent** and **Server Members Intent**
     (this bot needs both — `intents.message_content` and `intents.members` in `main.py`).
   - Under OAuth2 → URL Generator, select `bot` and `applications.commands` scopes, plus the
     permissions you want (Administrator is simplest for testing), and use the generated URL to
     invite the bot to your server.

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your token**
   ```bash
   cp .env.example .env
   # then edit .env and paste your bot token
   ```

4. **Run the bot**
   ```bash
   python main.py
   ```

   On startup it auto-loads every file in `cogs/`, so you can add a new cog just by dropping
   a `.py` file with a `setup(bot)` function into that folder.

## Notes on placeholder commands

A handful of commands (`weather`, `translate`, `define`, `cat`, `dog`, `meme`, `shorten`) are
stubbed with a note on which free API to plug in (e.g. OpenWeatherMap, dictionaryapi.dev,
thecatapi.com, dog.ceo, meme-api.com) — real responses depend on external services and their
own API keys, so I left them as clearly-marked placeholders you can wire up with `aiohttp`
in a few lines each rather than baking in specific third-party keys.

## Data persistence

The economy cog stores balances in `data/economy.json` (auto-created on first run). Moderation
warnings are stored in memory and reset on restart — swap in a database (SQLite/PostgreSQL) if
you want warnings and other state to persist long-term.

## Extending further

- `tictactoe` uses a full button-based UI (`discord.ui.View`) — a good template for building
  out `connect4` (currently a placeholder) the same way.
- Add cooldowns to any command with `@commands.cooldown(1, 30, commands.BucketType.user)`.
- Add permission checks with `@commands.has_permissions(...)` as shown throughout `moderation.py`.
