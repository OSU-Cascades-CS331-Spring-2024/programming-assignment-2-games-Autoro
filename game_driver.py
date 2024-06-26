'''
    Defines game driver class, used to play a game of Othello.
'''
import sys
import argparse
from players import *
from othello_board import OthelloBoard


class GameDriver:
    def __init__(self, p1type, p2type, num_rows, num_cols, max_depth, max_time):
        if p1type.lower() in "human":
            self.p1 = HumanPlayer('X')
        elif p1type.lower() in "minimax" or p1type in "ai":
            self.p1 = MinimaxPlayer('X', max_depth, max_time)
        else:
            print("Invalid player 1 type!")
            exit(-1)

        if p2type.lower() in "human":
            self.p2 = HumanPlayer('O')
        elif p2type.lower() in "minimax" or p1type in "ai":
            self.p2 = MinimaxPlayer('O', max_depth, max_time)
        else:
            print("Invalid player 2 type!")
            exit(-1)

        self.board = OthelloBoard(num_rows, num_cols, self.p1.symbol, self.p2.symbol)
        self.board.initialize()

    def display(self):
        print("Player 1 (", self.p1.symbol, ") score: ",
                self.board.count_score(self.p1.symbol))

    def process_move(self, curr_player, opponent):
        invalid_move = True
        while invalid_move:
            (col, row) = curr_player.get_move(self.board)
            if not self.board.is_legal_move(col, row, curr_player.symbol):
                print("Invalid move")
            else:
                print("Move:", [col,row], "\n")
                self.board.play_move(col,row,curr_player.symbol)
                return

    def run(self):
        current = self.p1
        opponent = self.p2
        self.board.display()

        cant_move_counter, toggle = 0, 0

        print("Player 1(", self.p1.symbol, ") move:")
        while True:
            if self.board.has_legal_moves_remaining(current.symbol):
                cant_move_counter = 0
                self.process_move(current, opponent)
                self.board.display()
            else:
                print("Can't move")
                if cant_move_counter == 1:
                    break
                else:
                    cant_move_counter +=1
            toggle = (toggle + 1) % 2
            if toggle == 0:
                current, opponent = self.p1, self.p2
                print("Player 1(", self.p1.symbol, ") move:")
            else:
                current, opponent = self.p2, self.p1
                print("Player 2(", self.p2.symbol, ") move:")

        #decide win/lose/tie state
        state = self.board.count_score(self.p1.symbol) - self.board.count_score(self.p2.symbol)
        if state == 0:
            print("Tie game!!")
        elif state >0:
            print("Player 1 Wins!")
        else:
            print("Player 2 Wins!")

        if isinstance(self.p1, MinimaxPlayer) or isinstance(self.p2, MinimaxPlayer):
            print()
        
            if isinstance(self.p1, MinimaxPlayer):
                print(f"Player 1 minimax average run time: {self.p1.get_average_run_time():.4f}s")

            if isinstance(self.p2, MinimaxPlayer):
                print(f"Player 2 minimax average run time: {self.p2.get_average_run_time():.4f}s")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("player1", choices=["human", "minimax"], help="The type of player to use for player 1.")
    parser.add_argument("player2", choices=["human", "minimax"], help="The type of player to use for player 2.")
    parser.add_argument("-s", "--size", type=int, default=4, help="The number of rows and columns of the Othello board.")
    parser.add_argument("-d", "--maxdepth", type=int, default=5, help="The maximum depth the MinimaxPlayer can simulate to.")
    parser.add_argument("-t", "--maxtime", type=int, default=10, help="The maximum time in seconds the MinimaxPlayer can simulate for.")

    args = parser.parse_args()

    game = GameDriver(args.player1, args.player2, args.size, args.size, args.maxdepth, args.maxtime)
    game.run()
