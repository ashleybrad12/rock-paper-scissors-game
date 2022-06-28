import random
import enum
import time


class Color(enum.Enum):
    red = '\033[91m'
    purple = '\033[95m'
    blue = '\033[94m'
    cyan = '\033[96m'
    green = '\033[92m'
    black = '\033[0m'
    bold = '\033[1m'
    underline = '\033[4m'

    @classmethod
    def get_color(cls):
        return random.choice([color.value for color in cls])


def print_pause(message, delay=2):
    print(Color.get_color() + message)
    time.sleep(delay)


moves = ['rock', 'paper', 'scissors']

"""The Player class is the parent class for all of the Players
in this game"""


def valid_input(prompt, option1, option2, option3):
    while True:
        response = input(prompt).lower()
        if option1 in response:
            break
        elif option2 in response:
            break
        elif option3 in response:
            break
        else:
            print("Sorry, I don't understand\n")
    return response


def player_style():
    players = [Player(), ReflectPlayer(), CyclePlayer,
               RandomPlayer(), RepeatPlayer()]
    return random.choice(players)


def beats(one, two):
    return ((one == 'rock' and two == 'scissors') or
            (one == 'scissors' and two == 'paper') or
            (one == 'paper' and two == 'rock'))


class Player:
    def __init__(self):
        self.my_move = None
        self.their_move = None

    def move(self):
        pass

    def learn(self, my_move, their_move):
        self.my_move = my_move
        self.their_move = their_move


class HumanPlayer(Player):
    def move(self):
        response = valid_input("Please choose rock, paper, or scissors?\n",
                               "rock", "paper", "scissors")
        return response


class ReflectPlayer(Player):
    def move(self):
        if self.their_move is None:
            return random.choice(moves)
        elif self.their_move in moves:
            return self.their_move


class CyclePlayer(Player):
    def move(self):
        if self.my_move is None:
            return random.choice(moves)
        else:
            index = moves.index(self.my_move) + 1
            if index == len(moves):
                index = 0
            return moves[index]


class RandomPlayer(Player):
    def move(self):
        return random.choice(moves)


class RepeatPlayer(Player):
    def move(self):
        return 'rock'


class Game:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def play_round(self):
        move1 = self.p1.move()
        move2 = self.p2.move()
        print(f"Player 1: {move1}  Player 2: {move2}")
        self.p1.learn(move1, move2)
        self.p2.learn(move2, move1)
        while True:
            if move1 == move2:
                print("It's a tie!")
                break
            elif beats(move1, move2) is True:
                print("Player 1 Wins!")
                self.p1.score += 1
                break

            else:
                self.p2.score += 1
                print("Player 2 Wins!")
                return self.p1.score and self.p2.score

    def play_game(self):
        print_pause("Let's play rock, paper, scissors."
                    " The best out of 5 rounds win!")
        print_pause("Let's go!")
        self.p1.score = 0
        self.p2.score = 0
        for round in range(5):
            print(f"Round {round +1}:")
            self.play_round()
        print_pause("Game over!")
        print_pause(' Here Is The Score: ')
        print(f'Player 1: {self.p1.score} | Player 2: {self.p2.score}\n')
        self.play_again()

    def play_again(self):
        while True:
            response = input("Would you like to play again?"
                             "('yes' or 'no')?\n").lower()
            if response == "no":
                print("Okay, Goodbye!")
                exit()
            elif response == "yes":
                self.play_game()
            else:
                print("Sorry, I don't understand")
                self.play_again


if __name__ == '__main__':
    game = Game(HumanPlayer(), player_style())
    game.play_game()
