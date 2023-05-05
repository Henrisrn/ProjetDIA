import sys

class PetitJeu():
    def __init__(self):
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
    def whowin(self):
        for row in self.board:
            if row[0] == row[1] == row[2] and row[0] != 0:
                return row[1]
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] != 0:
                return self.board[0][col]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != 0:
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != 0:
            return self.board[0][2]
        return False
    def check_win(self):
        for row in self.board:
            if row[0] == row[1] == row[2] and row[0] != 0:
                return True
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] != 0:
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != 0:
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != 0:
            return True
        return False
    def best_global_move(self, player, global_board):
        best_eval = -sys.maxsize if player == 1 else sys.maxsize
        move = (-1, -1)
        for row in range(3):
            for col in range(3):
                if not (global_board[row][col].check_win() or global_board[row][col].check_draw()):
                    eval = self.evaluate_board(global_board, row, col)
                    if player == 1 and eval > best_eval:
                        best_eval = eval
                        move = (row, col)
                    elif player == -1 and eval < best_eval:
                        best_eval = eval
                        move = (row, col)
        return move
    def check_draw(self):
        for row in self.board:
            for cell in row:
                if cell == 0:
                    return False
        return True
    """def evaluate_board(self):
        score = 0
        lines = [
            self.board[0], self.board[1], self.board[2],
            [self.board[0][0], self.board[1][0], self.board[2][0]],
            [self.board[0][1], self.board[1][1], self.board[2][1]],
            [self.board[0][2], self.board[1][2], self.board[2][2]],
            [self.board[0][0], self.board[1][1], self.board[2][2]],
            [self.board[0][2], self.board[1][1], self.board[2][0]]
        ]

        for line in lines:
            if line.count(1) == 2 and line.count(0) == 1:
                score += 10
            elif line.count(-1) == 2 and line.count(0) == 1:
                score -= 10

        return score"""

    def minimax(self, depth, maximizing_player, alpha, beta, global_board, local_row, local_col):
        if depth == 4 or self.check_win():
            if maximizing_player:
                return -1 + self.evaluate_board(global_board, local_row, local_col)  # Utiliser l'évaluation heuristique étendue
            else:
                return 1 - self.evaluate_board(global_board, local_row, local_col)  # Utiliser l'évaluation heuristique étendue
        if self.check_draw():
            return 0


        if maximizing_player:
            max_eval = -sys.maxsize
            for row in range(3):
                for col in range(3):
                    if self.board[row][col] == 0:
                        self.board[row][col] = 1
                        eval = self.minimax(depth + 1, False, alpha, beta, global_board, local_row, local_col)

                        self.board[row][col] = 0
                        max_eval = max(max_eval, eval)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break
            return max_eval
        else:
            min_eval = sys.maxsize
            for row in range(3):
                for col in range(3):
                    if self.board[row][col] == 0:
                        self.board[row][col] = -1
                        eval = self.minimax(depth + 1, True, alpha, beta, global_board, local_row, local_col)
                        self.board[row][col] = 0
                        min_eval = min(min_eval, eval)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break
            return min_eval

    def evaluate_board(self, global_board, local_row, local_col):
        score = 0
        for row in range(3):
            for col in range(3):
                score += global_board[row][col].evaluate_local_board() * (1 if self.board[local_row][local_col] == 1 else -1)

        return score

    def evaluate_local_board(self):
        score = 0
        lines = [
            self.board[0], self.board[1], self.board[2],
            [self.board[0][0], self.board[1][0], self.board[2][0]],
            [self.board[0][1], self.board[1][1], self.board[2][1]],
            [self.board[0][2], self.board[1][2], self.board[2][2]],
            [self.board[0][0], self.board[1][1], self.board[2][2]],
            [self.board[0][2], self.board[1][1], self.board[2][0]]
        ]

        for line in lines:
            if line.count(1) == 2 and line.count(0) == 1:
                score += 10
            elif line.count(-1) == 2 and line.count(0) == 1:
                score -= 10

        return score
    def best_move(self, player, global_board, local_row, local_col):
        best_eval = -sys.maxsize if player == 1 else sys.maxsize
        move = (-1, -1)
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == 0:
                    self.board[row][col] = player
                    eval = self.minimax(0, player == -1, -sys.maxsize, sys.maxsize, global_board, local_row, local_col)
                    self.board[row][col] = 0
                    if player == 1 and eval > best_eval:
                        best_eval = eval
                        move = (row, col)
                    elif player == -1 and eval < best_eval:
                        best_eval = eval
                        move = (row, col)
        return move


    def print_board(self):
        res = ""
        for row in self.board:
            res += " | ".join([cell_to_char(cell) for cell in row]) + "\n"
        return res

    def player_move(self, player, row, col):
        if self.board[row][col] == 0:
            self.board[row][col] = player
            return True
        return False

def checkwin(board):
    for row in board:
        if row[0].whowin() != False and row[0].whowin() == row[1].whowin() == row[2].whowin():
            return True
    for col in range(3):
        if board[0][col].whowin() != False and board[0][col].whowin() == board[1][col].whowin() == board[2][col].whowin():
            return True
    if board[0][0].whowin() != False and board[0][0].whowin() == board[1][1].whowin() == board[2][2].whowin():
        return True
    if board[0][2].whowin() != False and board[0][2].whowin() == board[1][1].whowin() == board[2][0].whowin():
        return True
    return False
def winner(board):
    for player in [-1, 1]:
        for i in range(3):
            if board[i][0].whowin() == board[i][1].whowin() == board[i][2].whowin() == player:
                return board[i][0].whowin()
            if board[0][i].whowin() == board[1][i].whowin() == board[2][i].whowin() == player:
                return board[0][i].whowin()
        if board[0][0].whowin() == board[1][1].whowin() == board[2][2].whowin() == player:
            return board[0][0].whowin()
        if board[0][2].whowin() == board[1][1].whowin() == board[2][0].whowin() == player:
            return board[0][2].whowin()
    return None



def checkdraw(board):
    for row in board:
        for cell in row:
            if not (cell.check_win() or cell.check_draw()):
                return False
    return True

def cell_to_char(cell):
    if cell == 0:
        return "."
    elif cell == 1:
        return "X"
    else:
        return "O"

def is_valid_coordinate(x, y):
    return 0 <= x < 3 and 0 <= y < 3

def displaygame(game):
    for row in game:
        for i in range(3):  # Pour chaque ligne des sous-jeux
            line = ""
            for subgame in row:  # Pour chaque sous-jeu de la ligne
                subgame_rows = subgame.print_board().split("\n")
                line += subgame_rows[i] + "   │││   "
            print(line.strip())
        print()
        print("───────────────────────────────────────────")
        print()

partie = [[PetitJeu() for j in range(3)] for j in range(3)]
position = (0, 0)
next_position = (0, 0)
player = 1

while not (checkdraw(partie) or checkwin(partie)):
    displaygame(partie)
    souspartie = partie[next_position[0]][next_position[1]]
    
    # Vérifier si la sous-partie est terminée
    while souspartie.check_win() or souspartie.check_draw():
        print("La sous-partie", next_position, "est terminée. L'IA choisit une autre sous-partie.")
        next_position = souspartie.best_global_move(player, partie)
        souspartie = partie[next_position[0]][next_position[1]]

    print("Sous-partie actuelle :", next_position)

    if player == 1:  # L'IA joue en tant que joueur 1
        position = souspartie.best_move(player, partie, next_position[0], next_position[1])
        souspartie.player_move(player, position[0], position[1])
        print("L'IA a joué en position :", position)
    else:  # Le joueur humain joue en tant que joueur -1
        position = souspartie.best_move(player, partie, next_position[0], next_position[1])
        souspartie.player_move(player, position[0], position[1])
        print("L'IA a joué en position :", position)
        """
        valid_move = False
        while not valid_move:
            try:
                row = int(input("Entrez la ligne (0-2) : "))
                col = int(input("Entrez la colonne (0-2) : "))
                valid_move = souspartie.player_move(player, row, col)
                if not valid_move:
                    print("Mouvement invalide, veuillez réessayer.")
                else:
                    position = (row, col)
            except ValueError:
                print("Veuillez entrer des coordonnées valides.")"""

    next_position = (position[0] % 3, position[1] % 3)
    player = -player


displaygame(partie)

winning_player = winner(partie)
if winning_player is None:
    print("Match nul !")
else:
    print("Le joueur", winning_player, "a gagné la partie !")
