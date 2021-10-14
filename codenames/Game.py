import random


class Game:
    player_list = []
    words_map = []
    word_list = []
    starting_team = ['red', 'blue'][random.randint(0, 1)]

    class Field:
        guessed = False
        team = None
        word = ''

        def __init__(self, team, word, guessed=False):
            self.guessed = guessed
            self.team = team
            self.word = word

        def __str__(self):
            return f"guessed: {self.guessed}, team: {self.team}, word: {self.word}"

    def __init__(self, player_list=[], word=[], words_map=[]):
        self.word_list = word
        self.words_map = words_map
        self.player_list = player_list

    def print_matrix(self):
        for i in self.words_map:
            for j in i:
                print(j)
            print()
        print()

    def start_game(self):
        print("jatek generalas start")
        print("mezok alaphelyzetbe allitasa...")
        self.player_list = []
        self.words_map = []
        self.word_list = []
        self.starting_team = ['red', 'blue'][random.randint(0, 1)]
        print("kezdo csapat", self.starting_team)

        # load words from dictionary
        print("szotar beolvasasa")
        with open('codenames/wordlist-eng.txt', 'r') as file:
            for line in file:
                self.word_list.append(line.strip())

        # kezdo csapat eldontese
        remaining_words = {'red': 5, 'blue': 5}
        remaining_words[self.starting_team] = 6
        remaining_words['civil'] = 13
        remaining_words['killer'] = 1

        # generate word matrix
        words = []
        for i in range(5):
            row = []
            for j in range(5):
                random_word = self.word_list[random.randint(0, len(self.word_list)-1)]
                while random_word in words:
                    random_word = self.word_list[random.randint(0, len(self.word_list)-1)]

                words.append(random_word)

                team = random.choices(list(remaining_words.keys()), list(remaining_words.values()))[0]
                remaining_words[team] -= 1
                # ha eleri a 0-at akkor kiszedjuk oda ne generaljon tobbet
                if remaining_words[team] == 0:
                    remaining_words.pop(team)

                row.append(self.Field(team, random_word))
            self.words_map.append(row)
        print("jatek generalas kesz")
