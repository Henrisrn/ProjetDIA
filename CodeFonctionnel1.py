import time
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

    def minimax(self, depth, maximizing_player):
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
                        eval = self.minimax( depth + 1, False)
                        self.board[row][col] = 0
                        max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = sys.maxsize
            for row in range(3):
                for col in range(3):
                    if self.board[row][col] == 0:
                        self.board[row][col] = -1
                        eval = self.minimax(depth + 1, True)
                        self.board[row][col] = 0
                        min_eval = min(min_eval, eval)
            return min_eval

    def best_move(self):
        max_eval = -sys.maxsize
        move = (-1, -1)
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == 0:
                    self.board[row][col] = 1
                    eval = self.minimax(0, False)
                    self.board[row][col] = 0
                    if eval > max_eval:
                        max_eval = eval
                        move = (row, col)
        return move

    def print_board(self):
        for row in self.board:
            print(" | ".join([str(cell) if cell != 0 else " " for cell in row]))
            print("---------")

    def player_move(self, player, row, col):
        if self.board[row][col] == 0:
            self.board[row][col] = player
            return True
        return False
    
    
def checkwin(board):
    for row in board:
        if row[0].check_win() == row[1].check_win() == row[2].check_win() and row[0].check_win() == True:
            return True
    for col in range(3):
        if board[0][col].check_win() == board[1][col].check_win() == board[2][col].check_win() and board[0][col].check_win() != False:
            return True
        if board[0][0].check_win() == board[1][1].check_win() == board[2][2].check_win() and board[0][0].check_win() != False:
            return True
        if board[0][2].check_win() == board[1][1].check_win() == board[2][0].check_win() and board[0][2].check_win() != False:
            return True
        return False
def checkdraw(board):
        for row in board:
            for cell in row:
                if cell.check_win() != True or cell.check_draw() != True:
                    return False
        return True
    
def Faitlemove(jeu):
    move = jeu.best_move()
    jeu.player_move(1,move[0],move[1])
    jeu.print_board()

def displaygame(game):
        for row in game:
            for i in row:
                i.print_board()
                print()
            print()
            print("-----------------------")
            print()
        
partie = [[PetitJeu() for j in range(3)]for j in range(3)]
print(partie)
print(partie)
print(checkdraw(partie))
print(checkwin(partie))
position = (1,1)
while(checkdraw(partie) != True and checkwin(partie)!= True):
    souspartie = partie[position[0]][position[1]]
    position = souspartie.best_move()
    souspartie.player_move(1,position[0],position[1])
    souspartie = partie[position[0]][position[1]]
    position = souspartie.best_move()
    souspartie.player_move(-1,position[0],position[1])

    souspartie = partie[position[0]][position[1]]
    position = souspartie.best_move()
    souspartie.player_move(1,position[0],position[1])
    souspartie = partie[position[0]][position[1]]
    position = souspartie.best_move()
    souspartie.player_move(-1,position[0],position[1])
displaygame(partie)


