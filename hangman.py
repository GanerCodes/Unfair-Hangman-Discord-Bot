import random, string, copy
from dataclasses import dataclass

words = []
with open('words.txt', 'r') as f:
    f = f.readlines()
    for i in f:
        spl = i.split()
        words.append([spl[1], int(spl[0])])
words.sort(key = lambda x: x[1])

wordsByLength = copy.deepcopy(words)
wordsByLength.sort(key = lambda x: len(x[0]))
wordsByLengthAndPain = copy.deepcopy(words)
wordsByLengthAndPain.sort(key = lambda x: (len(x[0]), x[1]))

funnyMan = """\
 ┌────┐
 │    │
      │
      │
     ┌┴┐\
"""
def get_board(word : str, letters : str | list, failureCount : int, board = funnyMan, discordFormatting = False, backupWord = ""):
    winningState = set(word).issubset(set(letters))
    losingState = failureCount > 5
    if losingState and word.count('_') > 4:
        word = backupWord
    board = list(board)
    if failureCount > 0: board[17] = "O"
    if failureCount > 1: board[16] = "\\"
    if failureCount > 2: board[18] = "/"
    if failureCount > 3: board[25] = "│"
    if failureCount > 4: board[32] = "/"
    if failureCount > 5: board[34] = "\\"
    board = ''.join(board)

    r = "```" if discordFormatting else ""
    r += ' '.join('   ' if i == ' ' else (i if i in letters or losingState else ' ') for i in word) + '\n'
    r += ' '.join('   ' if i == ' ' else ('‾' if not losingState else ('‾' if i in letters else '─')) for i in word) + '\n'
    r += board
    if discordFormatting:
        yes, no = '🟢', '🔴'
    else:
        yes, no = '+', '-'
    r += "\nGuesses remaining: "
    if winningState:
        r += "You win!"
    elif losingState:
        r += "You lose!"
    else:
        r += no * failureCount + yes * (6 - failureCount)
    if discordFormatting: r += "```"
    return [r, 1 if winningState else -1 if losingState else 0]

def constrain(x: int | float, a: int | float, b: int | float):
    return min(max(x, a), b)

def chooseWord(difficulty : int = 5, words = words):
    difficulty = max(difficulty, 1)
    if difficulty < 6:
        proportion = min(difficulty**3 / 200 + 0.025, 0.5)
        start, end = proportion * (difficulty - 1) / 5, proportion * difficulty / 5
        start, end = int(start * len(words)), int(end * len(words))
        return random.choice(words[start:end])
    else:
        dictionary = wordsByLength if difficulty < 9 else wordsByLengthAndPain
        difficulty = 2 + int(1.5 * (difficulty - 5))
        sectionSize = len(wordsByLength) // 9
        return random.choice(dictionary[sectionSize * (difficulty - 1) : sectionSize * difficulty])

def getValidWords(letters, subset):
    return [i for i in subset if letters[-1] not in i]

@dataclass
class hangman_game:
    def __init__(self, painLevel : int):
        self.painLevel = painLevel
        self.word = chooseWord(painLevel)[0] if painLevel < 11 else [i[0] for i in wordsByLengthAndPain if (len(i[0]) == painLevel - 3 and '-' not in i[0])]
        self.guessList = "- "
        self.failCount = 0
    def getBoard(self):
        return get_board(self.word if type(self.word) == str else ('_' * (self.painLevel - 3)), self.guessList, failureCount = self.failCount, discordFormatting = True, backupWord = self.word[0])
    def getOrGenWord(self):
        if type(self.word) == str:
            return self.word
        else:
            return random.choice(self.word)
    def processChar(self, c):
        if not(len(c) == 1 and c.lower() in string.ascii_lowercase):
            return
        if c in self.guessList:
            self.failCount += 1
        else:
            if type(self.word) == str:
                if c in self.word:
                    self.guessList += c
                else:
                    self.failCount += 1
            else:
                self.guessList += c
                newList = getValidWords(self.guessList, self.word)
                # if self.painLevel != 15: #Limits the "dodges" the bot can do
                #     self.painLevel -= 1
                if len(newList) == 0 or self.painLevel < 11: #Choose a word with a letter inside, either mandatory or for easyness
                    self.word = random.choice(self.word[-len(self.word) // 2:])
                elif len(newList) < 4: #If there are less than 4 words left randomly choose one
                    self.failCount += 1
                    self.word = random.choice(newList)
                else:
                    self.failCount += 1
                    self.word = newList

if __name__ == "__main__":
    g = hangman_game(5)
    while 1:
        print(g.getBoard()[0])
        g.processChar(input('ENTER: '))