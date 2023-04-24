import sys

def check_win(board):
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != 0:
            return True
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != 0:
            return True
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != 0:
        return True
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != 0:
        return True
    return False

def check_draw(board):
    for row in board:
        for cell in row:
            if cell == 0:
                return False
    return True

def minimax(board, depth, maximizing_player):
    if check_win(board):
        if maximizing_player:
            return -1
        else:
            return 1
    if check_draw(board):
        return 0

    if maximizing_player:
        max_eval = -sys.maxsize
        for row in range(3):
            for col in range(3):
                if board[row][col] == 0:
                    board[row][col] = 1
                    eval = minimax(board, depth + 1, False)
                    board[row][col] = 0
                    max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = sys.maxsize
        for row in range(3):
            for col in range(3):
                if board[row][col] == 0:
                    board[row][col] = -1
                    eval = minimax(board, depth + 1, True)
                    board[row][col] = 0
                    min_eval = min(min_eval, eval)
        return min_eval

def best_move(board):
    max_eval = -sys.maxsize
    move = (-1, -1)
    for row in range(3):
        for col in range(3):
            if board[row][col] == 0:
                board[row][col] = 1
                eval = minimax(board, 0, False)
                board[row][col] = 0
                if eval > max_eval:
                    max_eval = eval
                    move = (row, col)
    return move

def print_board(board):
    for row in board:
        print(" | ".join([str(cell) if cell != 0 else " " for cell in row]))
        print("---------")

def player_move(board, player, row, col):
    if board[row][col] == 0:
        board[row][col] = player
        return True
    return False

def game():
    board = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]

    player = 1
    while not check_win(board) and not check_draw(board):
        print(f"Player {player}'s turn:")
        print_board(board)
        if player == 1:
            move = best_move(board)
            row, col = move
        else:
            # Ici, on fait jouer l'IA contre elle-même.
            # Vous pouvez remplacer cette partie par une entrée
            # Ici, on fait jouer l'IA contre elle-même.
            # Vous pouvez remplacer cette partie par une entrée utilisateur si vous voulez jouer contre l'IA.
            row = int(input("Entrez la ligne : "))
            col = int(input("Entrez la colonne : "))
            #move = best_move(board)
            #row, col = move

        if player_move(board, player, row, col):
            if player == 1:
                player = -1
            else:
                player = 1

    print("Final board:")
    print_board(board)

    if check_win(board):
        print(f"Player {player * -1} wins!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    game()
