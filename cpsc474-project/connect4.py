import time
from play_genetic import ConnectFour as GeneticConnectFour
from play_simple import ConnectFour as SimpleConnectFour

# ===========================================================
# CONNECT FOUR EXTENDED FRAMEWORK
# -----------------------------------------------------------
# This file coordinates matches between:
#   - The Genetic AI (imported from play_genetic.py)
#   - The Simple Heuristic AI (imported from play_simple.py)
# It measures win rates and performance time for both.
# ===========================================================

class ConnectFourExtended(GeneticConnectFour):
    def __init__(self):
        super().__init__()
    
    ### --- BOARD & MOVE UTILITIES ---
    def print_board(self):
        """Pretty print of the current board with column numbers."""
        for row in self.board:
            print('| ' + ' | '.join(row) + ' |')
        print('-' * (self.columns * 4 + 1))
        print('| ' + ' | '.join(str(i) for i in range(self.columns)) + ' |')

    def is_valid_move(self, column):
        """Return True if the move is valid (column not full and in range)."""
        return 0 <= column < self.columns and self.board[0][column] == ' '

    def make_move(self, column):
        """Places a piece in the chosen column if valid."""
        if not self.is_valid_move(column):
            print("Invalid move. Please choose another column.")
            return False
        row = self.rows - 1
        while row >= 0:
            if self.board[row][column] == ' ':
                self.board[row][column] = self.current_player
                return True
            row -= 1
    
    ### --- WIN CHECKING ---
    def check_winner(self):
        """Checks all rows, columns, and diagonals for 4 in a row."""
        for row in range(self.rows):
            for col in range(self.columns - 3):
                if (self.board[row][col] == self.board[row][col+1] == self.board[row][col+2] == self.board[row][col+3]) and \
                        (self.board[row][col] != ' '):
                    return True

        for col in range(self.columns):
            for row in range(self.rows - 3):
                if (self.board[row][col] == self.board[row+1][col] == self.board[row+2][col] == self.board[row+3][col]) and \
                        (self.board[row][col] != ' '):
                    return True

        for row in range(self.rows - 3):
            for col in range(self.columns - 3):
                # Check diagonal down-right
                if (self.board[row][col] == self.board[row+1][col+1] == self.board[row+2][col+2] == self.board[row+3][col+3]) and \
                        (self.board[row][col] != ' '):
                    return True
                # Check diagonal up-right
                if (self.board[row][col+3] == self.board[row+1][col+2] == self.board[row+2][col+1] == self.board[row+3][col]) and \
                        (self.board[row][col+3] != ' '):
                    return True
        return False

    def switch_player(self):
        """Switches between 'X' and 'O'."""
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    # -----------------------------------------------------------
    # GENETIC AI GAME LOOP
    # -----------------------------------------------------------
    def play_game_genetic(self, verbose=True):
        if verbose:
            print("\n🧬 Playing with Genetic Algorithm AI...")
            self.print_board()

        while True:
            best_move, _, _ = self.grid_search()
            if best_move is None:
                if verbose:
                    print("No valid move found — draw or full board.")
                return False

            self.make_move(best_move)
            if verbose:
                self.print_board()

            if self.check_winner():
                if verbose:
                    print(f"Genetic AI ({self.current_player}) wins!")
                return True

            if all(self.board[i][j] != ' ' for i in range(self.rows) for j in range(self.columns)):
                if verbose:
                    print("It's a draw!")
                return False

            self.switch_player()


            self.switch_player()
    
    # -----------------------------------------------------------
    # SIMPLE AI GAME LOOP
    # -----------------------------------------------------------
    def play_game_simple(self, verbose=True):
        simple_game = SimpleConnectFour()
        if verbose:
            print("\n🧩 Playing with Simple Heuristic AI...")
            simple_game.print_board()

        while True:
            column = simple_game.select_simple_move()
            if simple_game.make_move(column):
                if verbose:
                    simple_game.print_board()

                if simple_game.check_winner():
                    if verbose:
                        print(f"Simple AI ({simple_game.current_player}) wins!")
                    return True

                if all(simple_game.board[i][j] != ' ' for i in range(simple_game.rows) for j in range(simple_game.columns)):
                    if verbose:
                        print("It's a draw!")
                    return False

                simple_game.switch_player()

    

    # -----------------------------------------------------------
    # COMPARISON LOOP
    # -----------------------------------------------------------
    def play(self, num_games=None):
        """
        Plays either a single manual game (if num_games is None)
        or runs an automated comparison between both AIs.
        The first AI match will print its board for visual check;
        the rest will run silently for speed.
        """
        if num_games is None:
            ### --- MANUAL PLAYER MODE ---
            print("Welcome to Connect Four!")
            self.print_board()
            while True:
                column = int(input(f"Player {self.current_player}, choose a column (0-{self.columns-1}): "))
                if self.make_move(column):
                    self.print_board()
                    if self.check_winner():
                        print(f"Player {self.current_player} wins!")
                        break
                    if all(self.board[i][j] != ' ' for i in range(self.rows) for j in range(self.columns)):
                        print("It's a draw!")
                        break
                    self.switch_player()
        else:
            ### --- AI COMPARISON MODE ---
            wins_genetic_algorithm = 0
            wins_heuristic = 0
            total_duration_genetic_algorithm = 0
            total_duration_heuristic = 0

            for i in range(num_games):
                print(f"\n==============================")
                print(f" Starting Game {i + 1}/{num_games}")
                print(f"==============================")

                verbose = (i == 0)  # 👈 Only print details for the first game

                # --- GENETIC AI GAME ---
                start_time = time.time()
                game_result = self.play_game_genetic(verbose=verbose)
                if game_result:
                    wins_genetic_algorithm += 1
                total_duration_genetic_algorithm += time.time() - start_time

                # --- SIMPLE AI GAME ---
                start_time = time.time()
                game_result = self.play_game_simple(verbose=verbose)
                if game_result:
                    wins_heuristic += 1
                total_duration_heuristic += time.time() - start_time

            ### --- SUMMARY STATISTICS ---
            win_rate_genetic_algorithm = wins_genetic_algorithm / num_games
            win_rate_heuristic = wins_heuristic / num_games
            average_duration_genetic_algorithm = total_duration_genetic_algorithm / num_games
            average_duration_heuristic = total_duration_heuristic / num_games

            print("\n=== COMPARISON RESULTS ===")
            print(f"Genetic AI Win Rate:  {win_rate_genetic_algorithm:.2%}")
            print(f"Simple AI Win Rate:   {win_rate_heuristic:.2%}")
            print(f"Avg. Time (Genetic):  {average_duration_genetic_algorithm:.2f}s")
            print(f"Avg. Time (Simple):   {average_duration_heuristic:.2f}s")




# -----------------------------------------------------------
# MAIN ENTRY POINT
# -----------------------------------------------------------
if __name__ == "__main__":
    game = ConnectFourExtended()
    num_games_input = input("Enter number of games to compare (press Enter for manual game): ").strip()
    num_games = int(num_games_input) if num_games_input else None
    game.play(num_games)
