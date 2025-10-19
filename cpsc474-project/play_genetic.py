# ===========================================================
# Connect Four Genetic Algorithm — by Naheem Watson
# ===========================================================
# This program uses a genetic algorithm to optimize heuristic 
# weights for evaluating Connect Four board states.
# It combines grid search and evolutionary strategy to evolve
# better parameters for the AI player over multiple generations.
# 
# The code structure:
#   - ConnectFour class: represents the board and move logic
#   - Evaluation functions: assign scores to board states
#   - Genetic algorithm: evolves weights to improve performance
# ===========================================================

import itertools
import random
import matplotlib.pyplot as plt


# -----------------------------------------------------------
# ConnectFour CLASS
# -----------------------------------------------------------
# Handles game board setup, move validation, and evaluation
# of board states. The AI's goal is to find the most optimal 
# next move using evolved heuristic parameters.
# -----------------------------------------------------------

class ConnectFour:
    def __init__(self):
        self.rows = 6
        self.columns = 7
        self.board = [[' ' for _ in range(self.columns)] for _ in range(self.rows)]
        self.current_player = 'X'

    # --- Board Utility Methods ---
    # These functions handle displaying the board, validating 
    # moves, updating the board state, and switching turns.
    # They are shared across both simple and genetic AI players.


    def print_board(self):
        for row in self.board:
            print('| ' + ' | '.join(row) + ' |')
        print('-' * (self.columns * 4 + 1))
        print('| ' + ' | '.join(str(i) for i in range(self.columns)) + ' |')

    def is_valid_move(self, column):
        return 0 <= column < self.columns and self.board[0][column] == ' '

    def make_move(self, column):
        if not self.is_valid_move(column):
            return False
        for row in range(self.rows - 1, -1, -1):
            if self.board[row][column] == ' ':
                self.board[row][column] = self.current_player
                return True
        return False

    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    # --- Evaluation Function ---
    # Combines three main heuristics to score the board:
    #   1. Piece Count: number of sequences of two or more
    #   2. Potential Winning Moves: open 3-in-a-rows
    #   3. Center Control: how much the center is dominated
    # The weights for each heuristic are evolved via the 
    # genetic algorithm to find optimal balance.

    def evaluate_board(self, player):
        piece_count_score = self.calculate_piece_count(player)
        winning_moves_score = self.calculate_winning_moves(player)
        center_control_score = self.calculate_center_control(player)

        total_score = (
            self.piece_count * piece_count_score
            + self.potential_winning_moves * winning_moves_score
            + self.center_control_moves * center_control_score
        )
        return total_score

    def calculate_piece_count(self, player):
        piece_count = 0
        # Horizontal
        for row in range(self.rows):
            for col in range(self.columns - 3):
                window = [self.board[row][col + i] for i in range(4)]
                if window.count(player) >= 2:
                    piece_count += 1
        # Vertical
        for row in range(self.rows - 3):
            for col in range(self.columns):
                window = [self.board[row + i][col] for i in range(4)]
                if window.count(player) >= 2:
                    piece_count += 1
        # Diagonal (/)
        for row in range(3, self.rows):
            for col in range(self.columns - 3):
                window = [self.board[row - i][col + i] for i in range(4)]
                if window.count(player) >= 2:
                    piece_count += 1
        # Diagonal (\)
        for row in range(self.rows - 3):
            for col in range(self.columns - 3):
                window = [self.board[row + i][col + i] for i in range(4)]
                if window.count(player) >= 2:
                    piece_count += 1
        return piece_count

    def calculate_winning_moves(self, player):
        winning_moves = 0
        # Check for open 3-in-a-rows
        for row in range(self.rows):
            for col in range(self.columns - 3):
                window = [self.board[row][col + i] for i in range(4)]
                if window.count(player) == 3 and window.count(' ') == 1:
                    winning_moves += 1
        for row in range(self.rows - 3):
            for col in range(self.columns):
                window = [self.board[row + i][col] for i in range(4)]
                if window.count(player) == 3 and window.count(' ') == 1:
                    winning_moves += 1
        return winning_moves

    def calculate_center_control(self, player):
        center_cols = [3]
        score = 0
        for c in center_cols:
            for r in range(self.rows):
                if self.board[r][c] == player:
                    score += 1
        return score

    # --- Grid Search Method ---
    # Tests all possible moves and a range of heuristic weights.
    # Finds the move/weight combination with the highest score.
    # Used to simulate different AI behaviors during evolution.


    def grid_search(self):
        parameters = {
            'piece_count': [0, 1, 2, 3],
            'potential_winning_moves': [0, 1, 2, 3],
            'center_control_moves': [0, 1, 2, 3]
        }

        best_score = float('-inf')
        best_params = {}
        best_move = None

        for col in range(self.columns):
            if self.is_valid_move(col):
                self.make_move(col)

                for param_values in itertools.product(*parameters.values()):
                    self.piece_count, self.potential_winning_moves, self.center_control_moves = param_values
                    score = self.evaluate_board(self.current_player)

                    if score > best_score:
                        best_score = score
                        best_params = {
                            'piece_count': self.piece_count,
                            'potential_winning_moves': self.potential_winning_moves,
                            'center_control_moves': self.center_control_moves
                        }
                        best_move = col

                # Undo the move (fix)
                for row in range(self.rows):
                    if self.board[row][col] != ' ':
                        self.board[row][col] = ' '
                        break

                self.switch_player()

        return best_move, best_params, best_score

    def make_best_move(self):
        best_move, _, _ = self.grid_search()
        if best_move is not None:
            self.make_move(best_move)
        self.print_board()


# -----------------------------------------------------------
# GENETIC ALGORITHM FUNCTIONS
# -----------------------------------------------------------
# These functions define the evolutionary logic:
#   - generate_random_genome: creates random weight sets
#   - crossover: mixes traits from two parents
#   - mutate: slightly alters weights for exploration
#   - fitness: measures how effective a genome is
#   - evolve: runs full evolutionary cycle and visualizes progress
# -----------------------------------------------------------

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
    genome[param] = max(0, min(3, genome[param]))  # Keep in range


def fitness(game, genome):
    game.piece_count = genome['piece_count']
    game.potential_winning_moves = genome['winning_moves']
    game.center_control_moves = genome['center_control']
    return game.evaluate_board('X')

# The evolve() function runs multiple generations of genomes.
# It keeps the best-performing half of the population (parents),
# breeds new generations through crossover and mutation,
# and tracks the best score per generation using matplotlib.

def evolve(game, generations=20, population_size=10, mutation_rate=0.1):
    population = [generate_random_genome() for _ in range(population_size)]
    best_scores = []

    for gen in range(generations):
        scores = [(genome, fitness(game, genome)) for genome in population]
        scores.sort(key=lambda x: x[1], reverse=True)

        best_scores.append(scores[0][1])
        print(f"Generation {gen}: Best Score = {scores[0][1]:.2f}")

        parents = [g for g, s in scores[:len(scores)//2]]

        next_gen = []
        while len(next_gen) < population_size:
            p1, p2 = random.sample(parents, 2)
            child = crossover(p1, p2)
            if random.random() < mutation_rate:
                mutate(child)
            next_gen.append(child)

        population = next_gen

    plt.plot(best_scores)
    plt.title("Fitness Improvement over Generations")
    plt.xlabel("Generation")
    plt.ylabel("Best Fitness Score")
    plt.show()

    best_genome = max(population, key=lambda g: fitness(game, g))
    return best_genome


# -----------------------------------------------------------
# MAIN EXECUTION
# -----------------------------------------------------------
# Runs the evolutionary process for 30 generations,
# prints the best evolved heuristic weights, 
# and visualizes the AI’s learning curve.
# -----------------------------------------------------------

if __name__ == "__main__":
    game = ConnectFour()
    best = evolve(game, generations=30, population_size=10)
    print("Best evolved parameters:", best)
