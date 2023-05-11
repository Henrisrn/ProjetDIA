
import sys
from copy import deepcopy


#%% Classes
class SubBoard:
    def __init__(self):
        self.cells = [[" " for _ in range(3)] for _ in range(3)]
        self.actions = [[i, j] for i in range(3) for j in range(3) if self.cells[i][j] == " "]
        self.winner = None
    
    def result(self, action, player):
        self.cells[action[0]][action[1]] = player
        if self.TerminalTest(player):
            self.winner = player
            return
        self.actions.remove(action)
  

        

    def TerminalTest(self, player):
        # Vérification des lignes
        for row in self.cells:
            if row == [player] * 3:
                self.winner = player
                return True

        # Vérification des colonnes
        for col in range(3):
            if [self.cells[row][col] for row in range(3)] == [player] * 3:
                self.winner = player
                return True

        # Vérification des diagonales
        if [self.cells[i][i] for i in range(3)] == [player] * 3 or [self.cells[i][2 - i] for i in range(3)] == [player] * 3:
            if self.cells[1][1] != " ":
                return True

        # Vérification d'un match nul
        if all(cell != " " for row in self.cells for cell in row):
            self.winner = "tie"
            return True

        return False



class Board:
    def __init__(self):
        self.sub_boards = [[SubBoard() for _ in range(3)] for _ in range(3)]
        
        self.current_sub_board_ij = None
        
        
        
        
        
    
        self.current_player = "X"
        self.winner = None
    
    def action(self):
        return [[i,j] for i in range(3) for j in range(3) if self.sub_boards[i][j].winner is None]
        
    
     
    def terminalTest(self):
        current_player = self.current_player

        # Vérification des lignes et des colonnes
        for i in range(3):
            if all(self.sub_boards[i][j].winner == current_player for j in range(3)):
                self.winner = current_player
                return True
            if all(self.sub_boards[j][i].winner == current_player for j in range(3)):
                self.winner = current_player
                return True
        
        # Vérification des diagonales
        if all(self.sub_boards[i][i].winner == current_player for i in range(3)) \
                or all(self.sub_boards[i][2 - i].winner == current_player for i in range(3)):
            self.winner = current_player
            return True

        # Vérification d'une égalité
        if all(self.sub_boards[i][j].winner == "tie" for i in range(3) for j in range(3)):
            self.winner = "tie"
            return True

        return False

     

    def result(self, in_Board, in_SubBoard):
        new_board = Board()
        new_board.sub_boards = deepcopy(self.sub_boards)
        new_board.current_player = self.current_player
        new_board.winner = self.winner

        new_board.current_sub_board_ij = in_SubBoard
        new_board.sub_boards[in_Board[0]][in_Board[1]].result(in_SubBoard, new_board.current_player)
        if new_board.sub_boards[in_Board[0]][in_Board[1]].TerminalTest(new_board.current_player):
            new_board.current_sub_board_ij = None       

            
        return new_board


    
    def utility(self):
        if self.winner is None:
            return 0
        elif self.winner == self.current_player:
            return 100
        elif self.winner == "tie":
            return 1  # Match nul
        else:
            return -100


    # Affichage       
    # Affichage
    def print_board(self):
        horizontal_line = "-" * 21

        for i in range(3):
            for k in range(3):
                for j in range(3):
                    for l in range(3):
                        cell = self.sub_boards[i][j].cells[k][l]
                        if cell == " ":
                            print(".", end=" ")
                        else:
                            print(cell, end=" ")
                    if j != 2:
                        print("|", end=" ")
                print()

            if i != 2:
                print(horizontal_line)
        print()

        
    
    

#%% Alpha Beta

def Alpha_Beta_Search(board, depth):
    alpha = -sys.maxsize - 1
    beta = sys.maxsize
    best_action = None

    if board.current_sub_board_ij is not None:
        sub_i, sub_j = board.current_sub_board_ij
        for action_i, action_j in board.sub_boards[sub_i][sub_j].actions:
            new_board = board.result(board.current_sub_board_ij, [action_i, action_j])
            value = Max_Value(new_board, alpha, beta, depth-1)
            if value > alpha:
                alpha = value
                best_action = [board.current_sub_board_ij, [action_i, action_j]]
        return best_action
    else:
        for [sub_i, sub_j] in board.action():
            if board.sub_boards[sub_i][sub_j].winner is None:
                for action_i, action_j in board.sub_boards[sub_i][sub_j].actions:
                    new_board = board.result([sub_i, sub_j], [action_i, action_j])
                    value = Max_Value(new_board, alpha, beta, depth-1)
                    if value > alpha:
                        alpha = value
                        best_action = [[sub_i, sub_j], [action_i, action_j]]
        return best_action

 
def Max_Value(board, a, b, depth):
    board.current_player = 'O'
    if board.terminalTest() or depth == 0:
        """
        print('end',board.utility())
        board.print_board()
        for subbords in board.sub_boards:
            for subbbords in subbords:
                print(subbbords.winner,end = ' ')
                print(board.action())
          """      
        return board.utility()
    v = -sys.maxsize - 1
    
    if board.current_sub_board_ij is not None and board.sub_boards[board.current_sub_board_ij[0]][board.current_sub_board_ij[1]].winner is None:
        for action_subBoard in board.sub_boards[board.current_sub_board_ij[0]][board.current_sub_board_ij[1]].actions:
        # ...

            v = max(v, Min_Value(board.result(board.current_sub_board_ij, action_subBoard), a, b, depth - 1))

            if v >= b:
                return v
            a = max(a, v)
    else:
        
        for action_board in board.action():       
            for action_subBoard in board.sub_boards[action_board[0]][action_board[1]].actions:
                v = max(v, Min_Value(board.result(action_board, action_subBoard), a, b, depth - 1))
                if v >= b:
                    return v
                a = max(a, v)
    return v

def Min_Value(board, a, b, depth):
    
    board.current_player = 'X'
    if board.terminalTest() or depth == 0:
        """
        print('end',board.utility())
        board.print_board()
        for subbords in board.sub_boards:
            for subbbords in subbords:
                print(subbbords.winner,end = ' ')
           """  
        
        return board.utility()
    v = sys.maxsize
    if board.current_sub_board_ij is not None and board.sub_boards[board.current_sub_board_ij[0]][board.current_sub_board_ij[1]].winner is None:
        for action_subBoard in board.sub_boards[board.current_sub_board_ij[0]][board.current_sub_board_ij[1]].actions:
        # ...
          

            v = min(v, Max_Value(board.result(board.current_sub_board_ij, action_subBoard), a, b, depth - 1))
            if v <= a:
                return v
            b = min(b, v)
    else:
        for action_board in board.action():       
            for action_subBoard in board.sub_boards[action_board[0]][action_board[1]].actions:
               

                v = min(v, Max_Value(board.result(action_board, action_subBoard), a, b, depth - 1))
                if v <= a:
                    return v
                b = min(b, v)
        
    
    return v   


#%% Main
def play_ultimate_tic_tac_toe():
    board = Board()
    

    while not board.terminalTest():
        if board.current_player == "X":
            # Joueur humain
            print("Joueur X, c'est votre tour.")
            board.print_board()

            # Demander les coordonnées du coup
            valid_input = False
            while not valid_input:
                board_input = input("Entrez les coordonnées du sous-plateau (ex: 0 1): ")
                sub_board_input = input("Entrez les coordonnées de la case (ex: 1 2): ")
                try:
                    in_board = list((map(int, board_input.strip().split())))
                    in_sub_board = list(map(int, sub_board_input.strip().split()))
                    
                    
                    
                    if in_board in board.action() and in_sub_board in board.sub_boards[in_board[0]][in_board[1]].actions:
                        valid_input = True
                    else:
                        print("Coup invalide. Réessayez.")
                except ValueError:
                    print("Entrée invalide. Réessayez.")

            board = board.result(in_board, in_sub_board)
            board.current_player = 'O'
        else:
            # Ordinateur (Alpha-Beta)
            print("Tour de l'ordinateur (O)...")
            best_action = Alpha_Beta_Search(board,  8)
            board = board.result(best_action[0], best_action[1])
            board.current_player = 'X'

    board.print_board()

    if board.winner == "X":
        print("Le joueur X a gagné !")
    elif board.winner == "O":
        print("L'ordinateur a gagné !")
    else:
        print("Match nul !")
 


play_ultimate_tic_tac_toe()


