#IMPORTATION DES LIBRAIRIES
import sys
import datetime

#CREATION D'UNE CLASSE PETIT JEU PERMETTANT DE SIMULER UN MORPION SIMPLE
class PetitJeu():
    #Constructeur de la classe avec la grille de base
    def __init__(self):
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
    #Fonction qui permet de dire qui à gagné ou non sur une partie de morpion classique
    def whowin(self):
        # Parcours des lignes
        for row in self.board:
            if row[0] == row[1] == row[2] and row[0] != 0:
                return row[1]

        # Parcours des colonnes
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] != 0:
                return self.board[0][col]

        # Parcours des diagonales
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != 0:
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != 0:
            return self.board[0][2]

        return False
    #Fonction qui permet de dire si une partie est fini ou non (retourne uniquement un booléens)
    def check_win(self):
        # Parcours des lignes
        for row in self.board:
            if row[0] == row[1] == row[2] and row[0] != 0:
                return True

        # Parcours des colonnes
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] != 0:
                return True

        # Parcours des diagonales
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != 0:
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != 0:
            return True

        return False
    #Fonction minimax à l'echelle de jeu global
    def best_global_move(self, player, global_board):
        # Minimise ou maximise les chances du joueur
        best_eval = -sys.maxsize if player == 1 else sys.maxsize
        move = (-1, -1)

        # Parcours de toutes les cases du plateau global
        for row in range(3):
            for col in range(3):
                # Vérification si la sous-partie n'est ni gagnée ni à égalité
                if not (global_board[row][col].check_win() or global_board[row][col].check_draw()):
                    # Evaluation de la sous-partie
                    eval = self.evaluate_board(global_board, row, col)
                    # Mise à jour de la meilleure évaluation et du meilleur mouvement
                    if player == 1 and eval > best_eval:
                        best_eval = eval
                        move = (row, col)
                    elif player == -1 and eval < best_eval:
                        best_eval = eval
                        move = (row, col)
        return move
    #Fonction qui vérifie si le morpion est égalité 
    def check_draw(self):
        for row in self.board:
            for cell in row:
                if cell == 0:
                    return False
        return True

    # La fonction minimax est utilisée pour évaluer les coups possibles en jeu et choisir le meilleur coup en fonction de l'IA
    # ou du joueur humain (maximizing_player). Elle utilise les paramètres alpha et beta pour effectuer une recherche
    # approfondie tout en élaguant les branches de l'arbre de recherche pour améliorer l'efficacité.
    # Elle prend en compte le plateau global (global_board) et la position locale (local_row, local_col) dans l'évaluation.
    def minimax(self, depth, maximizing_player, alpha, beta, global_board, local_row, local_col):
        if depth == 9999 or self.check_win():
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
    # La fonction evaluate_board évalue le plateau global en fonction de la situation actuelle du jeu
    # et renvoie un score en fonction de l'avantage du joueur (1 pour l'IA, -1 pour le joueur humain).
    def evaluate_board(self, global_board, local_row, local_col):
        score = 0
        for row in range(3):
            for col in range(3):
                score += global_board[row][col].evaluate_local_board() * (1 if self.board[local_row][local_col] == 1 else -1)

        # Ajout de l'évaluation supplémentaire pour prendre en compte l'envoi de l'adversaire sur une case pleine
        for row in range(3):
            for col in range(3):
                if global_board[row][col].check_draw():
                    score += 15 if self.board[local_row][local_col] == 1 else -15

        return score

    # La fonction evaluate_local_board calcule un score pour un sous-jeu (sous-partie) en fonction
    # de l'avantage du joueur (1 pour l'IA, -1 pour le joueur humain).
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
                score += 20
            elif line.count(-1) == 2 and line.count(0) == 1:
                score -= 20
            elif line.count(1) == 1 and line.count(0) == 2:
                score += 10
            elif line.count(-1) == 1 and line.count(0) == 2:
                score -= 10

        return score
    # La fonction best_move trouve le meilleur coup pour un joueur en utilisant la fonction minimax.
    # Elle prend en compte le plateau global (global_board) et la position locale (local_row, local_col)
    # pour déterminer le meilleur coup.
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
            res += " ".join([cell_to_char(cell) for cell in row]) + "\n"
        return res
    # La fonction player_move tente de placer un coup du joueur (1 pour l'IA, -1 pour le joueur humain)
    # sur le plateau de jeu à une position spécifique (row, col). Si le coup est valide, la fonction
    # met à jour le plateau de jeu et renvoie True, sinon elle renvoie False.
    def player_move(self, player, row, col):
        if self.board[row][col] == 0:
            self.board[row][col] = player
            return True
        return False
#Vérifie si la partie est gagné ou non retourne booléens
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
#Retourne le gagnant de la partie
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


#Permet de vérifié si match nul
def checkdraw(board):
    for row in board:
        for cell in row:
            if not (cell.check_win() or cell.check_draw()):
                return False
    return True
#Converti les cellules du morpion pour affichage
def cell_to_char(cell):
    if cell == 0:
        return "."
    elif cell == 1:
        return "X"
    else:
        return "O"
#Verifie si la coordonée rentré est valide
def is_valid_coordinate(x, y):
    return 0 <= x < 3 and 0 <= y < 3

# Afficher le plateau de jeu global
def displaygame(game):
    horizontal_line = "-" * 21
    for row in game:
        for i in range(3):  # Pour chaque ligne des sous-jeux
            line = ""
            for subgame in row:  # Pour chaque sous-jeu de la ligne
                subgame_rows = subgame.print_board().split("\n")
                line += subgame_rows[i] + " │ "
            print(line.strip())
        print(horizontal_line)
#Création de la partie avec variable d'initialisation
partie = [[PetitJeu() for j in range(3)] for j in range(3)]
position = (0, 0)
next_position = (0, 0)
player = 1

#Commencement de la boucle de jeu
while not (checkdraw(partie) or checkwin(partie)):
    displaygame(partie)
    souspartie = partie[next_position[0]][next_position[1]]
    
    # Vérifier si la sous-partie est terminée
    while souspartie.check_win() or souspartie.check_draw():
        if(player == 1):
            print("La sous-partie", next_position, "est terminée. L'IA choisit une autre sous-partie.")
            next_position = souspartie.best_global_move(player, partie)
            souspartie = partie[next_position[0]][next_position[1]]
        if(player == -1):
            
            print("Entrez la sous partie que vous voulez : ")
            row = int(input("Entrez la ligne (0-2) : "))
            col = int(input("Entrez la colonne (0-2) : "))
            souspartie = partie[row][col]
            """
            print("La sous-partie", next_position, "est terminée. L'IA choisit une autre sous-partie.")
            next_position = souspartie.best_global_move(player, partie)
            souspartie = partie[next_position[0]][next_position[1]]"""

    print("Sous-partie actuelle :", next_position)
    # Gestion des coups pour l'IA et le joueur humain
    if player == 1:  # L'IA joue en tant que joueur 1
        t1 = datetime.datetime.now()
        position = souspartie.best_move(player, partie, next_position[0], next_position[1])
        souspartie.player_move(player, position[0], position[1])
        print("L'IA a joué en position :", position)
        t2 = datetime.datetime.now()-t1
        print("Temps pris : ",t2)
    else:  # Le joueur humain joue en tant que joueur -1
        """position = souspartie.best_move(player, partie, next_position[0], next_position[1])
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
                print("Veuillez entrer des coordonnées valides.")
    # Changer de joueur et déterminer la prochaine position
    next_position = (position[0] % 3, position[1] % 3)
    player = -player


displaygame(partie)

winning_player = winner(partie)
if winning_player is None:
    print("Match nul !")
else:
    print("Le joueur", winning_player, "a gagné la partie !")
