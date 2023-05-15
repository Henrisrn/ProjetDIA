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


def ask_who_starts():
    while True:
        response = input("Qui commence? IA (1) ou joueur (2) ? ")
        if response == "1":
            return 1
        elif response == "2":
            return -1
        else:
            print("Réponse non valide. Veuillez entrer 1 ou 2.")

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

def coordinates_to_number(subgame_coord, cell_coord):
    num = (subgame_coord[0] * 3 + subgame_coord[1]) * 9 + (cell_coord[0] * 3 + cell_coord[1]) + 1
    return num

def number_to_coordinates(num):
    num -= 1
    subgame_coord = (num // 3, num % 3)
    cell_coord = ((num % 9) // 3, (num % 9) % 3)
    return subgame_coord, cell_coord

def ask_for_subgame():
    while True:
        subgame_num = input("Choisissez un sous-jeu pour commencer (1-9) : ")
        try:
            subgame_num = int(subgame_num)
            if 1 <= subgame_num <= 9:
                return number_to_coordinates(subgame_num)
            else:
                print("Le numéro doit être compris entre 1 et 9.")
        except ValueError:
            print("Veuillez entrer un nombre valide.")

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

souspartie = partie[0][0]
player = ask_who_starts()
if(player == 1):
            print("L'IA choisit une sous-partie.")
            next_position = souspartie.best_global_move(player, partie)
            #souspartie = partie[next_position[0]][next_position[1]]
if(player == -1):
            num = int(input("Entrez un chiffre entre 1 et 9 pour sélectionner une sous-partie : "))
            next_position = number_to_coordinates(num)[0]
            #souspartie = partie[next_position[0]][next_position[1]]
    
#Commencement de la boucle de jeu
while not (checkdraw(partie) or checkwin(partie)):
    displaygame(partie)
    souspartie = partie[next_position[0]][next_position[1]]
    
    # Vérifier si la sous-partie est terminée
    while souspartie.check_win() or souspartie.check_draw():
        if(player == 1):
            a = ((next_position[0] * 3 + next_position[1]) * 9 + (next_position[0] * 3 + next_position[1]) + 1)
            print("La sous-partie", a, "est terminée. L'IA choisit une autre sous-partie.")
            next_position = souspartie.best_global_move(player, partie)
            souspartie = partie[next_position[0]][next_position[1]]
        if(player == -1):
            print("La sous-partie",a, "est terminée. Veuillez choisir une autre sous-partie.")
            num = int(input("Entrez un chiffre entre 1 et 9 pour sélectionner une autre sous-partie : "))
            next_position = number_to_coordinates(num)[0]
            souspartie = partie[next_position[0]][next_position[1]]

    if player == 1:
        move = souspartie.best_move(player, partie, next_position[0], next_position[1])
        souspartie.player_move(player, move[0], move[1])
        a = ((next_position[0] * 3 + next_position[1]) * 9 + (next_position[0] * 3 + next_position[1]) + 1)
        b = ((move[0] * 3 + move[1]) * 9 + (move[0] * 3 + move[1]) + 1)
        print(f"L'IA joue dans la sous-partie ",a," à la position ",b,".")
    else:
        valid_move = False
        while not valid_move:
            num = int(input("Entrez un chiffre entre 1 et 9 pour sélectionner une case dans la sous-partie : "))
            move = number_to_coordinates(num)[1]
            valid_move = souspartie.player_move(player, move[0], move[1])
            if not valid_move:
                print("Cette case est déjà occupée. Veuillez choisir une autre case.")

    # Passer au joueur suivant et déterminer la position suivante
    player *= -1
    next_position = move

# Afficher le résultat final
displaygame(partie)
if checkwin(partie):
    print("Le gagnant est", cell_to_char(winner(partie)))
else:
    print("Match nul")
