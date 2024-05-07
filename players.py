'''
    Defines Player class, and subclasses Human and Minimax Player.
'''

import math
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

class MinimaxPlayer(Player):
    def __init__(self, symbol):
        Player.__init__(self, symbol)
        if symbol == 'X':
            self.oppSym = 'O'
        else:
            self.oppSym = 'X'
    
    def get_new_board(self, board : OthelloBoard, move : tuple[int, int], symbol : str) -> OthelloBoard:
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

    def min_value(self, board : OthelloBoard, depth : int, skipped_count : int) -> int:
        """
        Finds the minimum possible score for a given game board.

        Args:
            board (OthelloBoard): The game board to find the minimum score for.
            depth (int): The remaining depth iterations that can be performed. Returns immediately if the value is 0.
            skipped_count (int): The number of previously skipped turns. Returns if the skipped count is greater than 1,
                                 and no more moves are left.
        
        Returns:
            int: The minimized score of the given game board.
        """
                
        if depth == 0:
            return self.get_score(board)
        
        if not board.has_legal_moves_remaining(self.oppSym):
            # If min is out of moves and max skipped their last turn, then return the score.
            # Otherwise give max a turn with the current game board.
            if skipped_count > 0:
                return self.get_score(board)
            else:
                return self.max_value(board, depth, 1)
        
        value = math.inf

        for move in board.get_legal_moves_remaining(self.oppSym):
            new_board = self.get_new_board(board, move, self.oppSym)

            value = min(value, self.max_value(new_board, depth - 1, 0))

        return value
    
    def max_value(self, board : OthelloBoard, depth : int, skipped_count : int) -> int:
        """
        Finds the maximum possible score for a given game board.

        Args:
            board (OthelloBoard): The game board to maximize for.
            depth (int): The remaining depth iterations that can be performed. Returns immediately if the value is 0.
            skipped_count (int): The number of previously skipped turns. Returns if the skipped count is greater than 1,
                                 and no more moves are left.
        
        Returns:
            int: The maximized score of the given game board.
        """

        if depth == 0:
            return self.get_score(board)
        
        if not board.has_legal_moves_remaining(self.symbol):
            # If max is out of moves and min skipped their last turn, then return the score.
            # Otherwise give min a turn with the current game board.
            if skipped_count > 0:
                return self.get_score(board)
            else:
                return self.min_value(board, depth, 1)
        
        value = -math.inf

        for move in board.get_legal_moves_remaining(self.symbol):
            new_board = self.get_new_board(board, move, self.symbol)

            value = max(value, self.min_value(new_board, depth - 1, 0))

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
            new_board = board.clone_of_board()
            new_board.play_move(move[0], move[1], self.symbol)

            value = self.min_value(new_board, 5, 0)

            if value > best_value:
                best_move = move
                best_value = value

        return best_move[0], best_move[1]
