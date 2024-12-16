import math

class HexGame:
    def __init__(self, size=11):
        self.size = size
        self.board = [["." for _ in range(size)] for _ in range(size)]
        self.current_player = "X"

    def display_board(self):
        for i in range(self.size):
            print(" " * i + " ".join(self.board[i]))
        print()

    def is_valid_move(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size and self.board[x][y] == "."

    def make_move(self, x, y):
        if self.is_valid_move(x, y):
            self.board[x][y] = self.current_player
            self.current_player = "O" if self.current_player == "X" else "X"
            return True
        return False

    def check_winner(self):
        visited = set()

        def dfs(x, y, player, target_edge):
            if (x, y) in visited:
                return False

            if (player == "X" and y == target_edge) or (player == "O" and x == target_edge):
                return True

            visited.add((x, y))
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, 1), (1, -1)]

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.size and 0 <= ny < self.size and self.board[nx][ny] == player:
                    if dfs(nx, ny, player, target_edge):
                        return True

            return False

        for i in range(self.size):
            if self.board[i][0] == "X" and dfs(i, 0, "X", self.size - 1):
                return "X"
            if self.board[0][i] == "O" and dfs(0, i, "O", self.size - 1):
                return "O"

        return None

    def evaluate_board(self, player):
        opponent = "X" if player == "O" else "O"
        player_count = sum(row.count(player) for row in self.board)
        opponent_count = sum(row.count(opponent) for row in self.board)
        return player_count - opponent_count

    def minimax(self, depth, is_maximizing, alpha, beta):
        winner = self.check_winner()
        if winner == "O":
            return 1000
        elif winner == "X":
            return -1000
        elif all(cell != "." for row in self.board for cell in row):
            return 0

        if depth == 0:
            return self.evaluate_board("O")

        if is_maximizing:
            max_eval = -math.inf
            for x in range(self.size):
                for y in range(self.size):
                    if self.is_valid_move(x, y):
                        self.board[x][y] = "O"
                        eval = self.minimax(depth - 1, False, alpha, beta)
                        self.board[x][y] = "."
                        max_eval = max(max_eval, eval)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break
            return max_eval
        else:
            min_eval = math.inf
            for x in range(self.size):
                for y in range(self.size):
                    if self.is_valid_move(x, y):
                        self.board[x][y] = "X"
                        eval = self.minimax(depth - 1, True, alpha, beta)
                        self.board[x][y] = "."
                        min_eval = min(min_eval, eval)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break
            return min_eval

    def find_best_move(self):
        best_value = -math.inf
        best_move = None
        for x in range(self.size):
            for y in range(self.size):
                if self.is_valid_move(x, y):
                    self.board[x][y] = "O"
                    move_value = self.minimax(3, False, -math.inf, math.inf)
                    self.board[x][y] = "."
                    if move_value > best_value:
                        best_value = move_value
                        best_move = (x, y)
        return best_move

    def play(self):
        print("Welcome to Hex!")
        self.display_board()

        while True:
            if self.current_player == "X":
                print(f"Player {self.current_player}'s turn")
                try:
                    x, y = map(int, input("Enter your move (row and column): ").split())
                    if self.make_move(x, y):
                        self.display_board()
                        winner = self.check_winner()
                        if winner:
                            print(f"Player {winner} wins!")
                            break
                    else:
                        print("Invalid move. Try again.")
                except ValueError:
                    print("Invalid input. Please enter two integers.")
            else:
                print("Computer's turn")
                move = self.find_best_move()
                if move:
                    self.make_move(*move)
                    print(f"Computer chose: {move[0]} {move[1]}")
                    self.display_board()
                    winner = self.check_winner()
                    if winner:
                        print(f"Player {winner} wins!")
                        break

if __name__ == "__main__":
    try:
        size = int(input("Enter the board size (e.g., 11): "))
        game = HexGame(size)
        game.play()
    except ValueError:
        print("Invalid size. Please enter an integer.")
7