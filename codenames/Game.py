import random


class Game:
    player_list = []
    words_map = []
    words = []

    class Field:
        guessed = False
        team = None
        word = ''

        def __init__(self, team, word, guessed=False):
            self.guessed = guessed
            self.team = team
            self.word = word

    def __init__(self, player_list=[], word=[], words_map=[]):
        self.words = word
        self.words_map = words_map
        self.player_list = player_list

    def start_game(self):
        # load words from dictionary
        with open('wordlist-eng.txt', 'r') as file:
            self.words.append(file.readline().strip())

        # kezdo csapat eldontese
        remaining_words = {'red': 5, 'blue': 5}
        remaining_words[['red', 'blue'][random.randint(2)]] = 6
        remaining_words['civil'] = 13
        remaining_words['killer'] = 1
        print("remaining_words dict", remaining_words)

        # generate word matrix and map matrix
        words = []
        for i in range(5):
            row = []
            for j in range(5):
                random_word = self.words[random.randint(len(self.words))]
                while random_word in words:
                    random_word = self.words[random.randint(len(self.words))]
                words.append(random_word)

                team = remaining_words[['red', 'blue', 'killer', 'civil'][random.randint(len(remaining_words.keys()))]]
                remaining_words[team] -= 1
                # ha eleri a 0-at akkor kiszedjuk oda ne generaljon tobbet
                if remaining_words[team] == 0:
                    remaining_words.pop(team)

                row.append(self.Field(team, random_word))
            self.words_map.append(row)
