import itertools
import random
import matplotlib.pyplot as plt

# this program does not check if the opponent has a winning move, so need to check in my main
class ConnectFour:
    def __init__(self):
        # Initialize the Connect Four game
        self.rows = 6
        self.columns = 7
        self.board = [[' ' for _ in range(self.columns)] for _ in range(self.rows)]
        self.current_player = 'X'

    # Other methods (print_board, is_valid_move, make_move, check_winner, switch_player, etc.)

    def evaluate_board(self, player):
        # Initialize scores for each factor
        piece_count_score = 0
        winning_moves_score = 0
        center_control_score = 0

        # Check for piece count in a row
        piece_count_score += self.calculate_piece_count(self.board, player)

        # Check for potential winning moves
        winning_moves_score += self.calculate_winning_moves(self.board, player)

        # Check for moves that gain control of the center
        center_control_score += self.calculate_center_control(self.board, player)

        # Calculate total score as a combination of the individual scores
        total_score = piece_count_score + winning_moves_score + center_control_score

        return total_score
    
    def calculate_piece_count(self, player):
        # Calculate the number of player pieces in a row
        # Iterate through each position in the board
        # Add points for each player piece in a row horizontally, vertically, and diagonally
        piece_count = 0
        # Add points for each player piece in a row horizontally
        for row in range(6):
            for col in range(4):
                if self.board[row][col] == player and self.board[row][col+1] == player and self.board[row][col+2] == player and self.board[row][col+3] == player:
                    piece_count += 1
        # Add points for each player piece in a row vertically
        for row in range(3):
            for col in range(7):
                if self.board[row][col] == player and self.board[row+1][col] == player and self.board[row+2][col] == player and self.board[row+3][col] == player:
                    piece_count += 1
        # Add points for each player piece in a row diagonally (top-left to bottom-right)
        for row in range(3):
            for col in range(4):
                if self.board[row][col] == player and self.board[row+1][col+1] == player and self.board[row+2][col+2] == player and self.board[row+3][col+3] == player:
                    piece_count += 1
        # Add points for each player piece in a row diagonally (bottom-left to top-right)
        for row in range(3, 6):
            for col in range(4):
                if self.board[row][col] == player and self.board[row-1][col+1] == player and self.board[row-2][col+2] == player and self.board[row-3][col+3] == player:
                    piece_count += 1
        return piece_count
    
    def calculate_winning_moves(self, player):
        # Calculate the presence of potential winning moves
        # Iterate through each position in the board
        # Add points for potential winning moves horizontally, vertically, and diagonally
        winning_moves = 0
        # Add points for potential winning moves horizontally
        for row in range(6):
            for col in range(4):
                if self.board[row][col] == player and self.board[row][col+1] == player and self.board[row][col+2] == player and self.board[row][col+3] == ' ':
                    winning_moves += 1
        # Add points for potential winning moves vertically
        for row in range(3):
            for col in range(7):
                if self.board[row][col] == player and self.board[row+1][col] == player and self.board[row+2][col] == player and self.board[row+3][col] == ' ':
                    winning_moves += 1
        # Add points for potential winning moves diagonally (top-left to bottom-right)
        for row in range(3):
            for col in range(4):
                if self.board[row][col] == player and self.board[row+1][col+1] == player and self.board[row+2][col+2] == player and self.board[row+3][col+3] == ' ':
                    winning_moves += 1
        # Add points for potential winning moves diagonally (bottom-left to top-right)
        for row in range(3, 6):
            for col in range(4):
                if self.board[row][col] == player and self.board[row-1][col+1] == player and self.board[row-2][col+2] == player and self.board[row-3][col+3] == ' ':
                    winning_moves += 1
        return winning_moves
    
    def calculate_center_control(self, player):
        # Calculate moves that gain control of the center
        # Add points for placing player pieces in the center columns (3 and 4)
        center_control = 0
        for row in range(6):
            if self.board[row][3] == player or self.board[row][4] == player:
                center_control += 1
        return center_control

    def grid_search(self):
        # Define the parameter grid
        parameters = {
            'piece_count': [0, 1, 2, 3],
            'potential_winning_moves': [0, 1, 2, 3],
            'center_control_moves': [0, 1, 2, 3]
        }

        best_score = float('-inf')
        best_params = {}
        best_move = None

        # Iterate through all possible moves
        for col in range(self.columns):
            if self.is_valid_move(col):
                # Make the move
                self.make_move(col)
                
                # Perform grid search for each move
                for param_values in itertools.product(*parameters.values()):
                    piece_count, potential_winning_moves, center_control_moves = param_values

                    # Set parameters for the evaluation function
                    self.piece_count = piece_count
                    self.potential_winning_moves = potential_winning_moves
                    self.center_control_moves = center_control_moves

                    # Calculate score using the evaluation function
                    score = self.evaluate_board(self.current_player)

                    # Update best parameters if necessary
                    if score > best_score:
                        best_score = score
                        best_params = {'piece_count': piece_count, 'potential_winning_moves': potential_winning_moves,
                                       'center_control_moves': center_control_moves}
                        best_move = col

                # Undo the move
                self.board[self.board.index([' ' for _ in range(self.columns)])][col] = ' '
                self.switch_player()

        return best_move, best_params, best_score

    def make_best_move(self):
        best_move, _, _ = self.grid_search()
        self.make_move(best_move)
        self.print_board()


def generate_random_genome():
    return {
        'piece_count': random.uniform(0, 3),
        'winning_moves': random.uniform(0, 3),
        'center_control': random.uniform(0, 3)
    }

def crossover(p1, p2):
    return {
        'piece_count': random.choice([p1['piece_count'], p2['piece_count']]),
        'winning_moves': random.choice([p1['winning_moves'], p2['winning_moves']]),
        'center_control': random.choice([p1['center_control'], p2['center_control']])
    }

def mutate(genome):
    param = random.choice(list(genome.keys()))
    genome[param] += random.uniform(-0.5, 0.5)
    genome[param] = max(0, min(3, genome[param]))  # keep weights in range


def fitness(game, genome):
    # Plug weights into the game and evaluate board
    game.piece_count = genome['piece_count']
    game.potential_winning_moves = genome['winning_moves']
    game.center_control_moves = genome['center_control']
    return game.evaluate_board('X')

def evolve(game, generations=20, population_size=10, mutation_rate=0.1):
    population = [generate_random_genome() for _ in range(population_size)]
    best_scores = []

    for gen in range(generations):
        scores = [(genome, fitness(game, genome)) for genome in population]
        scores.sort(key=lambda x: x[1], reverse=True)

        best_scores.append(scores[0][1])
        print(f"Generation {gen}: Best Score = {scores[0][1]:.2f}")

        # Select top 50% as parents
        parents = [g for g, s in scores[:len(scores)//2]]

        # Create next generation
        next_gen = []
        while len(next_gen) < population_size:
            p1, p2 = random.sample(parents, 2)
            child = crossover(p1, p2)
            if random.random() < mutation_rate:
                mutate(child)
            next_gen.append(child)

        population = next_gen

    # Visualization
    plt.plot(best_scores)
    plt.title("Fitness Improvement over Generations")
    plt.xlabel("Generation")
    plt.ylabel("Best Fitness Score")
    plt.show()

    best_genome = max(population, key=lambda g: fitness(game, g))
    return best_genome
    
if __name__ == "__main__":
    game = ConnectFour()
    best = evolve(game, generations=30, population_size=10)
    print("Best evolved parameters:", best)


