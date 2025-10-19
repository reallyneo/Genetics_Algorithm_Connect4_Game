import random

class ConnectFour:
    def __init__(self):
        """Initialize the Connect Four game board and player turn."""
        self.rows = 6
        self.columns = 7
        self.board = [[' ' for _ in range(self.columns)] for _ in range(self.rows)]
        self.current_player = 'X'

    # -----------------------------------------------------------
    # BASIC BOARD FUNCTIONS
    # -----------------------------------------------------------

    def print_board(self):
        """Print the board nicely with column numbers."""
        for row in self.board:
            print('| ' + ' | '.join(row) + ' |')
        print('-' * (self.columns * 4 + 1))
        print('| ' + ' | '.join(str(i) for i in range(self.columns)) + ' |')

    def is_valid_move(self, column):
        """Check if a move can be made in the given column."""
        return 0 <= column < self.columns and self.board[0][column] == ' '

    def make_move(self, column):
        """Place the current player's piece in the chosen column."""
        if not self.is_valid_move(column):
            return False
        for row in reversed(range(self.rows)):
            if self.board[row][column] == ' ':
                self.board[row][column] = self.current_player
                return True
        return False

    def undo_move(self, column):
        """Undo the last move in a column (used for simulation)."""
        for row in range(self.rows):
            if self.board[row][column] != ' ':
                self.board[row][column] = ' '
                return

    def switch_player(self):
        """Switch between players X and O."""
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    # -----------------------------------------------------------
    # WIN / SEQUENCE LOGIC
    # -----------------------------------------------------------

    def check_winner(self):
        """Check for four-in-a-row horizontally, vertically, or diagonally."""
        for row in range(self.rows):
            for col in range(self.columns - 3):
                if (self.board[row][col] == self.board[row][col+1] ==
                    self.board[row][col+2] == self.board[row][col+3]) and self.board[row][col] != ' ':
                    return True

        for col in range(self.columns):
            for row in range(self.rows - 3):
                if (self.board[row][col] == self.board[row+1][col] ==
                    self.board[row+2][col] == self.board[row+3][col]) and self.board[row][col] != ' ':
                    return True

        for row in range(self.rows - 3):
            for col in range(self.columns - 3):
                # Diagonal down-right
                if (self.board[row][col] == self.board[row+1][col+1] ==
                    self.board[row+2][col+2] == self.board[row+3][col+3]) and self.board[row][col] != ' ':
                    return True
                # Diagonal up-right
                if (self.board[row+3][col] == self.board[row+2][col+1] ==
                    self.board[row+1][col+2] == self.board[row][col+3]) and self.board[row+3][col] != ' ':
                    return True

        return False

    # -----------------------------------------------------------
    # SIMPLE AI STRATEGY
    # -----------------------------------------------------------

    def select_simple_move(self):
        """
        Decide a move using simple priorities:
        1. Win or block immediately.
        2. Build sequences.
        3. Prefer center columns.
        4. Otherwise, random valid move.
        """

        # Priority 1: Check for immediate win or block
        for col in range(self.columns):
            if self.is_valid_move(col):
                self.make_move(col)
                if self.check_winner():
                    self.undo_move(col)
                    return col
                self.undo_move(col)

        # Priority 2: Build sequences (try to form small chains)
        for col in range(self.columns):
            if self.is_valid_move(col):
                # find lowest empty row for this column
                for row in reversed(range(self.rows)):
                    if self.board[row][col] == ' ':
                        if self.builds_sequence(row, col, self.current_player):
                            return col
                        break

        # Priority 3: Prefer center columns
        for col in [3, 2, 4]:
            if self.is_valid_move(col):
                return col

        # Priority 4: Random move
        return self.random_move()

    def builds_sequence(self, row, col, player):
        """Check if placing a piece here would help form a sequence of 2+."""
        # Horizontal
        if self.count_adjacent(row, col, 0, 1, player) + self.count_adjacent(row, col, 0, -1, player) >= 2:
            return True
        # Vertical
        if self.count_adjacent(row, col, 1, 0, player) >= 2:
            return True
        # Diagonal down-right / up-left
        if self.count_adjacent(row, col, 1, 1, player) + self.count_adjacent(row, col, -1, -1, player) >= 2:
            return True
        # Diagonal up-right / down-left
        if self.count_adjacent(row, col, -1, 1, player) + self.count_adjacent(row, col, 1, -1, player) >= 2:
            return True
        return False

    def count_adjacent(self, row, col, d_row, d_col, player):
        """Count consecutive pieces from (row, col) in a given direction."""
        count = 0
        r, c = row + d_row, col + d_col
        while 0 <= r < self.rows and 0 <= c < self.columns and self.board[r][c] == player:
            count += 1
            r += d_row
            c += d_col
        return count

    def random_move(self):
        """Select a random valid column."""
        valid_columns = [col for col in range(self.columns) if self.is_valid_move(col)]
        return random.choice(valid_columns) if valid_columns else None


# -----------------------------------------------------------
# TEST RUN
# -----------------------------------------------------------
if __name__ == "__main__":
    game = ConnectFour()
    game.print_board()
    move = game.select_simple_move()
    print(f"Simple AI chooses column {move}")
