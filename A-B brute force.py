import sys
from copy import deepcopy
import time
start_time = time.time()

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
        current_player = self.current_player
        new_board.winner = self.winner

        new_board.current_sub_board_ij = in_SubBoard
        new_board.sub_boards[in_Board[0]][in_Board[1]].result(in_SubBoard, current_player)
        if new_board.sub_boards[in_SubBoard[0]][in_SubBoard[1]].winner is not None:
            new_board.current_sub_board_ij = None       
        new_board.current_player = 'X' if current_player =='O' else 'O'
        
            
        return new_board


    
    def utility(self, last_player):
        if self.winner is None:
            return 0
        elif self.winner == last_player:
            return sys.maxsize-1
        elif self.winner == "tie":
            return 0  # Match nul
        else:
            return -sys.maxsize


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
            value = Max_Value(board, new_board, alpha, beta, depth-1,board.current_sub_board_ij)
            if value < beta:
                beta = value
                best_action = [[sub_i, sub_j], [action_i, action_j]]
            print('--',-beta, best_action)
        return best_action
    else:
        for [sub_i, sub_j] in board.action():
            if board.sub_boards[sub_i][sub_j].winner is None:
                for action_i, action_j in board.sub_boards[sub_i][sub_j].actions:
                    new_board = board.result([sub_i, sub_j], [action_i, action_j])
                    value = Max_Value(board, new_board, alpha, beta, depth-1,[sub_i, sub_j])
                    if value < beta:
                        beta = value
                        best_action = [[sub_i, sub_j], [action_i, action_j]]
                    print('--',-beta, best_action)
        return best_action

 
def Max_Value(prev_board, board, a, b, depth,chosen_board):
     
    

    if board.terminalTest() or depth == 0:
        
        current_player = 'O'
        opponent ='X'
        mult = -1 if current_player == 'O' else 1
        
        #application heuristiques
        u = board.utility(current_player)
        somme = 0
        if(u == 0):
            new_winner = [subBoard.winner for row in board.sub_boards for subBoard in row]
            '''
            print(prev_winner,new_winner.count(None))
            print(new_winner)
            print('HHHHHHHHHHHHH',new_winner.count(None)-prev_winner.count(None))
            '''
            if(new_winner.count(None)<9):
                h1 = H1(new_winner, current_player, opponent)
                somme+=h1
                
                if(h1 > 0):
                    h2 = H2(new_winner, current_player,opponent)
                    h3 = H3(new_winner, current_player,opponent)
                    somme += h2 + h3
                    """
                    if(h2 == 0):
                        h4 = H4(new_winner, current_player,opponent)
                        somme += h4
                        """
                        
            for row in board.sub_boards:
                for new_subBoard in row:
                    new_cells = [cell for row in new_subBoard.cells for cell in row]
            


                    h5 = H5(new_cells, current_player,opponent)
                    h6 = H6(new_cells, current_player,opponent)
                    somme += h5 + h6
                    if(h5 == 0 and h6 == 0):
                        somme -= 20*new_cells.count(current_player)
                        
            
        #print('end',(u+somme))
        #board.print_board()
        """
        for subbords in board.sub_boards:
            for subbbords in subbords:
                print(subbbords.winner,end = ' ')
                print(board.action())
         """ 
         
          
        return (u+somme)*mult
    
    v = -sys.maxsize - 1
    if board.current_sub_board_ij is not None and board.sub_boards[board.current_sub_board_ij[0]][board.current_sub_board_ij[1]].winner is None:
        for action_subBoard in board.sub_boards[board.current_sub_board_ij[0]][board.current_sub_board_ij[1]].actions:

            v = max(v, Min_Value(board, board.result(board.current_sub_board_ij, action_subBoard), a, b, depth - 1,board.current_sub_board_ij))           
            #print('min',v, board.current_sub_board_ij, action_subBoard,end = '      ')
            if (b <v):
                return v
            a = max(a,v)
    

    else:
        
        for action_board in board.action():       
            for action_subBoard in board.sub_boards[action_board[0]][action_board[1]].actions:
                v = max(v, Min_Value(board, board.result(action_board, action_subBoard), a, b, depth - 1,action_board))
                #print('min',v, action_board, action_subBoard,end = '      ')
                if (b < v):
                    return v
                a = max(a,v)
                
    return v           
                
        

def Min_Value(prev_board, board, a, b, depth,chosen_board):

    
    if board.terminalTest() or depth == 0:
        
        current_player = 'X'
        opponent ='O'
        mult = -1 if current_player == 'O' else 1
        
        #application heuristiques
        u = board.utility(current_player)
        somme = 0
        if(u == 0):
            new_winner = [subBoard.winner for row in board.sub_boards for subBoard in row]
            '''
            print(prev_winner,new_winner.count(None))
            print(new_winner)
            print('HHHHHHHHHHHHH',new_winner.count(None)-prev_winner.count(None))
            '''
            if(new_winner.count(None)<9):
                h1 = H1(new_winner, current_player, opponent)
                somme+=h1
                
                if(h1 > 0):
                    h2 = H2(new_winner, current_player,opponent)
                    h3 = H3(new_winner, current_player,opponent)
                    somme += h2 + h3
                    """
                    if(h2 == 0):
                        h4 = H4(new_winner, current_player,opponent)
                        somme += h4
                        """
                        
            for row in board.sub_boards:
                for new_subBoard in row:
                    new_cells = [cell for row in new_subBoard.cells for cell in row]
            


                    h5 = H5(new_cells, current_player,opponent)
                    h6 = H6(new_cells, current_player,opponent)
                    somme += h5 + h6
                    if(h5 == 0 and h6 == 0):
                        somme -= 20*new_cells.count(current_player)
                        
            
        #print('end',(u+somme))
        #board.print_board()
        """
        for subbords in board.sub_boards:
            for subbbords in subbords:
                print(subbbords.winner,end = ' ')
                print(board.action())
         """ 
         
          
        return (u+somme)*mult
    v = sys.maxsize
    
    
    if board.current_sub_board_ij is not None and board.sub_boards[board.current_sub_board_ij[0]][board.current_sub_board_ij[1]].winner is None:
        for action_subBoard in board.sub_boards[board.current_sub_board_ij[0]][board.current_sub_board_ij[1]].actions:
        # ...
          

            v = min(v, Max_Value(board, board.result(board.current_sub_board_ij, action_subBoard), a, b, depth - 1,board.current_sub_board_ij))
            #print('max',v, board.current_sub_board_ij, action_subBoard, end = '      ')
            if(v<a):
                return v
            b = min(b,v)
        
    
    else:
        for action_board in board.action():       
            for action_subBoard in board.sub_boards[action_board[0]][action_board[1]].actions:
               
                #print('max',v, action_board, action_subBoard, end = '      ')
                v = min(v, Max_Value(board, board.result(action_board, action_subBoard), a, b, depth - 1,action_board))
                if(v<a):
                    return v
                b = min(b,v)
    return v
         

#%% Heuristics

def H1(new_winner, current_player, opponent): # gagner ou perdre une board vaut +-100 pts
    
        return 100*new_winner.count(current_player) - 100*new_winner.count(opponent)

    
    
def H2(new_winner, current_player,opponent): #gagner 2 boards sur colonne (victoire possible), ligne col diag vaut 200
    #matrice des win -lignes
    new_winner = [new_winner[i:i+3] for i in range(0, len(new_winner), 3)]
    
    # Lignes    
    new_row = [row for row in new_winner if row.count(current_player) == 2 and row.count(opponent) == 0 and row.count('tie')==0]

    
    # Colonnes

    new_col = [[row[col] for row in new_winner] for col in range(len(new_winner[0]))]
   
    new_col = [col for col in new_col if col.count(current_player) == 2 and col.count(opponent) == 0 and col.count('tie')==0]

    
    # Diagonales
    new_diag = [[new_winner[i][i] for i in range(len(new_winner))], [new_winner[i][len(new_winner) - 1 - i] for i in range(len(new_winner))]]
    new_diag = [diag for diag in new_diag if diag.count(current_player) == 2 and diag.count(opponent) == 0 and diag.count('tie')==0]
    
    return 200 * (len(new_diag)) + 200 * (len(new_row)) + 200 * (len(new_row))


def H3(new_winner, current_player,opponent): #faire opposition 150 pts
  
    #matrice des win -lignes
    new_winner = [new_winner[i:i+3] for i in range(0, len(new_winner), 3)]
    
    # Lignes
    new_row = [row for row in new_winner if row.count(opponent) == 2 and row.count(current_player) == 1]
  

    # Colonnes
    new_col = [[row[col] for row in new_winner] for col in range(len(new_winner[0]))]
    new_col = [col for col in new_col if col.count(opponent) == 2 and col.count(current_player) == 1]
  


    # Diagonales
    new_diag = [[new_winner[i][i] for i in range(len(new_winner))], [new_winner[i][len(new_winner) - 1 - i] for i in range(len(new_winner))]]
    new_diag = [diag for diag in new_diag if diag.count(opponent) == 2 and diag.count(current_player) == 0]
    
    return 150 * (len(new_diag)) + 150 * (len(new_col)) + 150 * (len(new_row))

def H4(new_winner, current_player, opponent):
    # Matrice des win - lignes
    new_winner = [new_winner[i:i+3] for i in range(0, len(new_winner), 3)]
    
    # Sous-plateaux bloqués
    blocked_subboards = 0
    
    # Vérification des colonnes, lignes et diagonales de chaque sous-plateau
    for subboard in new_winner:
        # Vérification des lignes
        if any(row.count(opponent) > 0 or row.count('tie') > 0 for row in subboard):
            blocked_subboards += 1
        # Vérification des colonnes
        if any(col.count(opponent) > 0 or col.count('tie') > 0 for col in zip(*subboard)):
            blocked_subboards += 1
        # Vérification des diagonales
        diag1 = [subboard[i][i] for i in range(len(subboard))]
        diag2 = [subboard[i][len(subboard) - 1 - i] for i in range(len(subboard))]
        if diag1.count(opponent) > 0 or diag1.count('tie') > 0:
            blocked_subboards += 1
        if diag2.count(opponent) > 0 or diag2.count('tie') > 0:
            blocked_subboards += 1
    
    return -150 * blocked_subboards

def H5(new_subBoard, current_player, opponent): #prendre 2 cases sur une colonne de petite board (victoire possible) + 5 pts


    #matrice des win -lignes
    new_subBoard = [new_subBoard[i:i+3] for i in range(0, len(new_subBoard), 3)]
    
    # Lignes
    new_row = [row for row in new_subBoard if row.count(current_player) == 2 and row.count(opponent) == 0]

    
    # Colonnes
    new_col = [[row[col] for row in new_subBoard] for col in range(len(new_subBoard[0]))]
    new_col = [col for col in new_col if col.count(current_player) == 2 and col.count(opponent) == 0]

    
    # Diagonales
    new_diag = [[new_subBoard[i][i] for i in range(len(new_subBoard))], [new_subBoard[i][len(new_subBoard) - 1 - i] for i in range(len(new_subBoard))]]
    new_diag = [diag for diag in new_diag if diag.count(current_player) == 2 and diag.count(opponent) == 0]

    
    return 5 * (len(new_diag)) + 5 * (len(new_col)) + 5 * (len(new_row))

def H6(new_subBoard, current_player, opponent): #faire opposition sur petite board 20 pts
    
    #matrice des win -lignes
    new_subBoard = [new_subBoard[i:i+3] for i in range(0, len(new_subBoard), 3)]
    
    # Lignes
    new_row = [row for row in new_subBoard if row.count(opponent) == 2 and row.count(current_player) == 1]
    

    # Colonnes
    new_col = [[row[col] for row in new_subBoard] for col in range(len(new_subBoard[0]))]
    new_col = [col for col in new_col if col.count(opponent) == 2 and col.count(current_player) == 1]



    # Diagonales
    new_diag = [[new_subBoard[i][i] for i in range(len(new_subBoard))], [new_subBoard[i][len(new_subBoard) - 1 - i] for i in range(len(new_subBoard))]]
    new_diag = [diag for diag in new_diag if diag.count(opponent) == 2 and diag.count(current_player) == 0]
    return 150 * (len(new_diag)) + 150 * (len(new_col)) + 150 * (len(new_row))
   

   

#%% Main
def play_ultimate_tic_tac_toe(joueur):
    board = Board()
    board.current_player = joueur

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
            best_action = Alpha_Beta_Search(board,  5)
            board = board.result(best_action[0], best_action[1])
            board.current_player = 'X'

    board.print_board()

    if board.winner == "X":
        print("Le joueur X a gagné !")
    elif board.winner == "O":
        print("L'ordinateur a gagné !")
    else:
        print("Match nul !")
 


play_ultimate_tic_tac_toe('O')

