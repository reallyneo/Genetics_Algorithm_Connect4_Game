import random

class ConnectFour:
    def __init__(self):
        # Initialize the Connect Four game
        self.rows = 6
        self.columns = 7
        self.board = [[' ' for _ in range(self.columns)] for _ in range(self.rows)]
        self.current_player = 'X'

    def select_simple_move(self):
        # Priority 1: Check for immediate win or block
        for col in range(self.columns):
            if self.is_valid_move(col):
                self.make_move(col)
                if self.check_winner():
                    self.undo_move(col)
                    return col
                self.undo_move(col)

        # Priority 2: Build sequences
        for col in range(self.columns):
            if self.is_valid_move(col):
                self.make_move(col)
                if self.builds_sequence():
                    self.undo_move(col)
                    return col
                self.undo_move(col)

        # Priority 3: Center columns
        center_columns = [3, 4]
        for col in center_columns:
            if self.is_valid_move(col):
                return col

        # Priority 4: Random move
        return self.random_move()
    
    def builds_sequence(self, row, col, player):
        # Check horizontally
        if self.count_adjacent(row, col, 0, 1, player) + self.count_adjacent(row, col, 0, -1, player) >= 2:
            return True

        # Check vertically
        if self.count_adjacent(row, col, 1, 0, player) >= 2:
            return True

        # Check diagonally (top-left to bottom-right)
        if self.count_adjacent(row, col, 1, 1, player) + self.count_adjacent(row, col, -1, -1, player) >= 2:
            return True

        # Check diagonally (bottom-left to top-right)
        if self.count_adjacent(row, col, -1, 1, player) + self.count_adjacent(row, col, 1, -1, player) >= 2:
            return True

        return False

    def count_adjacent(self, row, col, d_row, d_col, player):
        count = 0
        # Start from the current position
        r, c = row, col
        # Move in the specified direction until reaching the edge or a different player's piece
        while 0 <= r < self.rows and 0 <= c < self.columns and self.board[r][c] == player:
            count += 1
            r += d_row
            c += d_col
        return count
    
    def is_valid_move(self, column):
        return 0 <= column < self.columns and self.board[0][column] == ' '
    
    def random_move(self):
        # Generate a list of valid columns where a move can be made
        valid_columns = [col for col in range(self.columns) if self.is_valid_move(col)]
        
        # Randomly select a column from the list of valid columns
        if valid_columns:
            return random.choice(valid_columns)
        else:
            return None 

if __name__ == "__main__":
    game = ConnectFour()
    game.select_simple_move()