import discord, string
from hangman import hangman_game

with open("token") as f:
    TOKEN = f.read()

bot = discord.Client()

games = {}

@bot.event
async def on_ready():
    print("Ready")

@bot.event
async def on_message(msg):
    if msg.channel.id in games:
        if msg.content.lower() == "hangman end":
            await msg.channel.send(f'Ended game of hangman.' + (f''' The word was "{games[msg.channel.id].getOrGenWord()}"''' if type(games[msg.channel.id]) == hangman_game else ''))
            del games[msg.channel.id]
            return
        currentGame = games[msg.channel.id]
        if currentGame == "waitForPainLevel":
            if set(msg.content).issubset(string.digits):
                painLvl = min(15, max(1, int(msg.content)))
                games[msg.channel.id] = hangman_game(painLvl)
                await msg.channel.send(f'Started game at difficulty level {painLvl}\n' + games[msg.channel.id].getBoard()[0])
        elif type(currentGame) == hangman_game:
            if len(msg.content) == 1:
                currentGame.processChar(msg.content.lower())
                gameBoard = currentGame.getBoard()
                await msg.channel.send(gameBoard[0])
                if gameBoard[1] != 0:
                    await msg.channel.send("Game finished. Type `hangman start` to play again!")
                    del games[msg.channel.id]
    else:
        if msg.content.lower() == "hangman help":
            await msg.channel.send("""\
Hangman help:
    Hangman help               | Displays this menu
    Hangman start              | Starts a game of hangman
    Hangman start <difficulty> | Starts a game of hangman with a predefined difficulty
    Hangman end                | Stops a game of hangman""")
        elif msg.content.lower() == "hangman start":
            await msg.channel.send("Enter a difficulty number (1 - 15):")
            games[msg.channel.id] = "waitForPainLevel"
        elif msg.content.lower().startswith("hangman start"):
            if set(dif := msg.content.lower().removeprefix("hangman start ")).issubset(string.digits):
                painLvl = min(15, max(1, int(dif)))
                games[msg.channel.id] = hangman_game(painLvl)
                await msg.channel.send(f'Started game at difficulty level {painLvl}\n' + games[msg.channel.id].getBoard()[0])

bot.run(TOKEN)