# othello-python
> CS 331 Programming Assignment 2  
> Alex Miesbauer

An Othello game that allows for human vs human, human vs AI, or AI vs AI play.

Originally created by Erich Kramer at OSU for Professor Rebecca Hutchinson.
Cleaned up by Rob Churchill.

## How to play a game:

1. Run `python3 game_driver.py [player_type] [player_type]`.
2. Choose `human`, or `minimax` as the player types.
3. Follow the prompts to choose where to place stones.

### Optional arguments:
* `-s --size`: The number of columns and rows to use for the Othello board.
* `-d --maxdepth`: The maximum depth the AI is allowed to simulate to when taking a turn.
* `-t --maxtime`: The maximum time the AI is allowed to simulate for each turn.

## Analysis

### 4x4 Board
#### Results:
* Depth 5 - Minimax won, average minimax time 0.0120s
* Depth 3 - Minimax won, average minimax time 0.0101s
* Depth 2 - Player won, average minimax time 0.0048s
* Depth 1 - Player won, average minimax time 0.0018s

1. While attempting to make the same moves for each game, minimax won 2 of the 4 games.
2. For depths 5 and 3, minimax made the same moves. For depth limits 2 and 1 it deviated from its normal moves which allowed me to win.
3. The average times listed above get shorter the lower the depth limit as one might expect. The less plies it is allowed to simulate means the less overall time it will take per turn. One interesting thing that stands out though is the difference between each depth. The average times for depth 5 and depth 3 are close, whereas the avergae time was more than halved each time between depths 3, 2, and 1. Depths 5 and and 3 were likely allowed to simulate to the end of the game each time, but depths 2 and 1 were likely cut off early.

### 8x8 Board
#### Results:
* Depth 5 - Unfinished, minimax took over 10 seconds per turn
* Depth 2 - Player won, average minimax time 0.0872s

1. The depth 5 game was unfinished, and the player won the depth 2 game.
2. Even though the depth 5 game was unfinished, the opening moves for depth 5 were different than those of depth 2.
3. If the depth 5 game was able to finish, its average time per turn would have likely been incredibly long. Out of curiosity I tried simulating a game between 2 AIs with a depth limit of 5 and a time limit of 60 seconds per turn. The game ran for over 10 minutes without finishing, and the AIs hit the 60 second time limit several times. Given the exponential nature of searching the different game states combined with the larger game board, a depth limit of 5 makes minimax take vastly more time than a depth limit of 2.
