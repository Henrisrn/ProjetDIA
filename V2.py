# -*- coding: utf-8 -*-
"""
Created on Tue May  2 15:23:13 2023

@author: varac
"""

import sys
class PetitJeu():
    def __init__(self):
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]

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

    def check_draw(self):
        for row in self.board:
            for cell in row:
                if cell == 0:
                    return False
        return True

    def minimax(self, depth, maximizing_player, alpha, beta):
        if self.check_win():
            if maximizing_player:
                return -1
            else:
                return 1
        if self.check_draw():
            return 0

        if maximizing_player:
            max_eval = -sys.maxsize
            for row in range(3):
                for col in range(3):
                    if self.board[row][col] == 0:
                        self.board[row][col] = 1
                        eval = self.minimax(depth + 1, False, alpha, beta)
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
                        eval = self.minimax(depth + 1, True, alpha, beta)
                        self.board[row][col] = 0
                        min_eval = min(min_eval, eval)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break
            return min_eval
        
    def ultimate_minimax(self, depth, maximizing_player, alpha, beta, main_board):
        if self.check_win():
            if maximizing_player:
                return -1
            else:
                return 1
        if self.check_draw():
            return 0

        if maximizing_player:
            max_eval = -sys.maxsize
            for row in range(3):
                for col in range(3):
                    if self.board[row][col] == 0:
                        self.board[row][col] = 1
                        next_board = main_board[row][col]
                        if not next_board.check_win() and not next_board.check_draw():
                            eval = next_board.minimax(depth + 1, False, alpha, beta)
                        else:
                            eval = self.minimax(depth + 1, False, alpha, beta)
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
                        next_board = main_board[row][col]
                        if not next_board.check_win() and not next_board.check_draw():
                            eval = next_board.minimax(depth + 1, True, alpha, beta)
                        else:
                            eval = self.minimax(depth + 1, True, alpha, beta)
                        self.board[row][col] = 0
                        min_eval = min(min_eval, eval)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break
            return min_eval

    def best_move(self, player, main_board):
        best_eval = -sys.maxsize if player == 1 else sys.maxsize
        move = (-1, -1)
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == 0:
                    self.board[row][col] = player
                    eval = self.ultimate_minimax(0, player == -1, -sys.maxsize, sys.maxsize, main_board)
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

def cell_to_char(cell):
    if cell == 0:
        return "."
    elif cell == 1:
        return "X"
    else:
        return "O"
    
def checkwin(board):
    for row in board:
        if row[0].check_win() and row[0].check_win() == row[1].check_win() == row[2].check_win():
            return True
    for col in range(3):
        if board[0][col].check_win() and board[0][col].check_win() == board[1][col].check_win() == board[2][col].check_win():
            return True
    if board[0][0].check_win() and board[0][0].check_win() == board[1][1].check_win() == board[2][2].check_win():
        return True
    if board[0][2].check_win() and board[0][2].check_win() == board[1][1].check_win() == board[2][0].check_win():
        return True
    return False
def winner(board):
    for row in board:
        if row[0].check_win() and row[0].check_win() == row[1].check_win() == row[2].check_win():
            return row[0].check_win()
    for col in range(3):
        if board[0][col].check_win() and board[0][col].check_win() == board[1][col].check_win() == board[2][col].check_win():
            return board[0][col].check_win()
    if board[0][0].check_win() and board[0][0].check_win() == board[1][1].check_win() == board[2][2].check_win():
        return board[0][0].check_win()
    if board[0][2].check_win() and board[0][2].check_win() == board[1][1].check_win() == board[2][0].check_win():
        return board[0][2].check_win()
    return None

def is_valid_coordinate(x, y):
    return 0 <= x < 3 and 0 <= y < 3


def checkdraw(board):
    for row in board:
        for cell in row:
            if not (cell.check_win() or cell.check_draw()):
                return False
    return True

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

    while souspartie.check_win() or souspartie.check_draw():
        print("La sous-partie", next_position, "est terminée. Veuillez choisir une autre sous-partie.")
        next_position = (int(input("Entrez le numéro de la sous-partie (0-2) : ")), int(input("Entrez le numéro de la sous-partie (0-2) : ")))
        souspartie = partie[next_position[0]][next_position[1]]

    print("Sous-partie actuelle :", next_position)

    if player == 1:  # L'IA joue en tant que joueur 1
        position = souspartie.best_move(player, partie)
        souspartie.player_move(player, position[0], position[1])
        print("L'IA a joué en position :", position)
    else:  # Le joueur humain joue en tant que joueur -1
        valid_move = False
        while not valid_move:
            try:
                row = int(input("Entrez la ligne (0-2) : "))
                col = int(input("Entrez la colonne (0-2) : "))
                if is_valid_coordinate(row, col):
                    valid_move = souspartie.player_move(player, row, col)
                    if not valid_move:
                        print("Mouvement invalide, veuillez réessayer.")
                    else:
                        position = (row, col)
                else:
                    print("Coordonnées hors limites, veuillez entrer des coordonnées valides.")
            except ValueError:
                print("Veuillez entrer des coordonnées valides.")

    next_position = (position[0] % 3, position[1] % 3)
    player = -player

displaygame(partie)

winning_player = winner(partie)
if winning_player is None:
    print("Match nul !")
else:
    print("Le joueur", winning_player, "a gagné la partie !")
