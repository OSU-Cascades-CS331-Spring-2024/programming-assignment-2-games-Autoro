'''
    Defines Player class, and subclasses Human and Minimax Player.
'''

import math
from enum import Enum
from othello_board import OthelloBoard

class Player:
    def __init__(self, symbol):
        self.symbol = symbol

    #PYTHON: use obj.symbol instead
    def get_symbol(self):
        return self.symbol
    
    #parent get_move should not be called
    def get_move(self, board):
        raise NotImplementedError()

class HumanPlayer(Player):
    def __init__(self, symbol):
        Player.__init__(self, symbol)

    def clone(self):
        return HumanPlayer(self.symbol)
        
#PYTHON: return tuple instead of change reference as in C++
    def get_move(self, board):
        col = int(input("Enter col:"))
        row = int(input("Enter row:"))
        return col, row

class MinimaxTurn(Enum):
    """
    Represents the current turn for the minimax algorithm.
    """

    MIN = 0
    MAX = 1

class MinimaxPlayer(Player):
    """
    Represents a player that uses the minimax algorithm to play Othello.
    """

    def __init__(self, symbol, max_depth):
        Player.__init__(self, symbol)
        if symbol == 'X':
            self.oppSym = 'O'
        else:
            self.oppSym = 'X'

        self.max_depth = max_depth
    
    def get_next_game_state(self, board : OthelloBoard, move : tuple[int, int], symbol : str) -> OthelloBoard:
        """
        Creates a copy of a game board with the results of a move for a player applied.

        Args:
            board (OthelloBoard): The original game board that will be copied.
            move tuple[int, int]: A move that will be applied to a the new game board.
            symbol (str): The symbol of the player performing the move.

        Returns:
            OthelloBoard: The new game board with the move applied.
        """

        new_board = board.clone_of_board()
        new_board.play_move(move[0], move[1], symbol)

        return new_board

    def get_score(self, board : OthelloBoard) -> int:
        """
        Gets the score of the player for a given game board.

        Args:
            board (OthelloBoard): The game board to use for calculating the score.

        Returns:
            int: The player's score for the game board.
        """

        return board.count_score(self.symbol) - board.count_score(self.oppSym)
    
    def minimax(self, board : OthelloBoard, depth : int, turn : MinimaxTurn, last_turn_skipped : bool) -> int:
        """
        Simulates playing out a given game board to find the best score that can be achieved.

        Args:
            board (OthelloBoard): The current game board to play out.
            depth (int): The maximum number of turns that will be played out before determining an optimal path.
            turn (MinimaxTurn): The turn which simulation will start on.
            last_turn_skipped (bool): Whether or not the last turn was skipped.

        Returns:
            int: The optimal score that was found through simulation.
        """

        if depth == 0:
            return self.get_score(board)
        
        current_symbol = self.symbol if turn == MinimaxTurn.MAX else self.oppSym
        eval_function = max if turn == MinimaxTurn.MAX else min
        value = -math.inf if turn == MinimaxTurn.MAX else math.inf
        next_turn = MinimaxTurn.MIN if turn == MinimaxTurn.MAX else MinimaxTurn.MIN
        
        if not board.has_legal_moves_remaining(current_symbol):
            # If the current player is out of moves and the last player skipped their turn, then
            # return the score. Otherwise give the other player a turn with the current game board.
            if last_turn_skipped:
                return self.get_score(board)
            else:
                return self.minimax(board, depth, next_turn, 1)
        
        for move in board.get_legal_moves_remaining(current_symbol):
            next_board = self.get_next_game_state(board, move, current_symbol)

            value = eval_function(value, self.minimax(next_board, depth - 1, next_turn, 0))

        return value

    def get_move(self, board : OthelloBoard) -> tuple[int, int]:
        """
        Gets the next move for the player.

        Args:
            board (OthelloBoard): The current game board.

        Returns:
            tuple[int, int]: The move the player decided to make.
        """

        best_move = None
        best_value = -math.inf

        for move in board.get_legal_moves_remaining(self.symbol):
            next_board = board.clone_of_board()
            next_board.play_move(move[0], move[1], self.symbol)

            value = self.minimax(next_board, self.max_depth, MinimaxTurn.MIN, 0)

            if value > best_value:
                best_move = move
                best_value = value

        return best_move[0], best_move[1]
