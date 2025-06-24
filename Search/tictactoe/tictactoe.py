"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    # initial state is X's turn, alternates from then on 
    counter = 0

    for row in board:
        for i in row:
            if i != EMPTY:
                counter += 1

    # board is full no ones turn 
    if counter >= 9:
        return None

    if counter % 2 == 0:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()

    row_index = 0
    for row in board:
        cell = 0
        for i in row:
            if i == EMPTY:
                actions.add((row_index, cell))
            cell += 1
        row_index += 1

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    valid_actions = actions(board)

    if action not in valid_actions:
        raise Exception("Invalid action")
    
    result = copy.deepcopy(board)
    result[action[0]][action[1]] = player(board)

    return result


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    
    # check for horizontal 
    for row in board:
        if row == [X, X, X]:
            return X
        if row == [O, O, O]:
            return O

    # check for vertical 
    column_index = 0
    while column_index < 3: 
        column = []
        for row in board:
            column.append(row[column_index])
        
        if column == [X, X, X]:
            return X
        if column == [O, O, O]:
            return O
        
        column_index += 1

    # check for diagonals 
    player_with_center = board[1][1]

    if (board[0][0] == player_with_center and board[2][2] == player_with_center) or (
        board[2][0] == player_with_center and board[0][2] == player_with_center):

        return player_with_center

    # no winner in current state
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # check if board is full
    counter = 0
    for row in board:
        for cell in row:
            if cell != EMPTY:
                counter += 1

    if counter == 9:
        return True

    # board not full, check for a winner 
    if winner(board) == None:
        return False
    else:
        return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    game_winner = winner(board)

    match game_winner:
        case 'X':  
            return 1

        case 'O': 
            return -1
        
        case None: 
            return 0 


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board):
        return None

    optimal_action = None   
    current_score = None

    if player(board) == X:

        current_score = -math.inf        
        for action in actions(board):
            min = min_value(result(board, action))
            if min > current_score:
                current_score = min
                optimal_action = action

    else:
        current_score = math.inf        
        for action in actions(board):
            max = max_value(result(board, action))
            if max < current_score:
                current_score = max
                optimal_action = action

    return optimal_action


def max_value(board): 

    if terminal(board):
        return utility(board)
    
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action)))

    return v

def min_value(board):
    
    if terminal(board):
        return utility(board)
    
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action)))

    return v