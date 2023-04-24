import time

class UltimateTicTacToe:
    def __init__(self):
        self.board = [[0] * 9 for _ in range(9)]
        self.small_won = [0] * 9
        self.last_move = -1
        self.player = 1

    def play(self, small_board, cell):
        if self.small_won[small_board] or self.board[small_board][cell]:
            return False
        self.board[small_board][cell] = self.player
        self.check_small_board(small_board)
        self.last_move = cell
        self.player = 3 - self.player
        return True

    def check_small_board(self, small_board):
        b = self.board[small_board]
        for i in range(3):
            if b[i * 3] == b[i * 3 + 1] == b[i * 3 + 2] and b[i * 3]:
                self.small_won[small_board] = b[i * 3]
            if b[i] == b[i + 3] == b[i + 6] and b[i]:
                self.small_won[small_board] = b[i]
        if b[0] == b[4] == b[8] and b[0]:
            self.small_won[small_board] = b[0]
        if b[2] == b[4] == b[6] and b[2]:
            self.small_won[small_board] = b[2]

    def is_game_over(self):
        for i in range(3):
            if self.small_won[i * 3] == self.small_won[i * 3 + 1] == self.small_won[i * 3 + 2] and self.small_won[i * 3]:
                return True, self.small_won[i * 3]
            if self.small_won[i] == self.small_won[i + 3] == self.small_won[i + 6] and self.small_won[i]:
                return True, self.small_won[i]
        if self.small_won[0] == self.small_won[4] == self.small_won[8] and self.small_won[0]:
            return True, self.small_won[0]
        if self.small_won[2] == self.small_won[4] == self.small_won[6] and self.small_won[2]:
            return True, self.small_won[2]
        if all(self.small_won):
            return True, 0
        return False, None

    def display(self):
        for i in range(9):
            if i % 3 == 0 and i != 0:
                print('-' * 21)
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    print('|', end=' ')
                print(self.board[i][j] if self.board[i][j] else '.', end=' ')
            print()
        print()

def main():
    game = UltimateTicTacToe()
    player_type = ['Human', 'AI']
    print("Choose who starts (1 = Human, 2 = AI):")
    game.player = int(input())
    while not game.is_game_over()[0]:
        game.display()
        print("Player:", player_type[game.player - 1])
        if game.player == 1:
            print("Enter small            board and cell (1-9) separated by a space:")
            small_board, cell = map(int, input().split())
            small_board -= 1
            cell -= 1
            if not game.play(small_board, cell):
                print("Invalid move. Try again.")
            else:
                game_over, winner = game.is_game_over()
                if game_over:
                    game.display()
                    if winner:
                        print(f"Player {player_type[winner - 1]} wins!")
                    else:
                        print("It's a draw!")
        else:
            start_time = time.time()
            move = get_best_move(game)
            elapsed_time = time.time() - start_time
            print(f"AI chose small board {move[0] + 1} and cell {move[1] + 1} in {elapsed_time:.2f} seconds")
            game.play(*move)
            game_over, winner = game.is_game_over()
            if game_over:
                game.display()
                if winner:
                    print(f"Player {player_type[winner - 1]} wins!")
                else:
                    print("It's a draw!")


def get_best_move(game):
    import random
    valid_moves = [(i, j) for i in range(9) for j in range(9) if not game.board[i][j] and not game.small_won[i]]
    return random.choice(valid_moves)

if __name__ == "__main__":
    main()

