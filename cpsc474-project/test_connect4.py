import time
from connect4 import ConnectFourExtended

print("=== Test: Connect Four ===")

def test_single_game():
    print("=== Test: Single AI Game ===")
    game = ConnectFourExtended()
    # Run a single automated AI-vs-AI match
    game.play(num_games=1)
    print("Single game test completed.\n")

def test_multiple_games(num_games=3):
    print(f"=== Test: Compare {num_games} Games ===")
    game = ConnectFourExtended()
    game.play(num_games=num_games)
    print("Multiple games comparison completed.\n")

if __name__ == "__main__":
    # Run one automated test game
    test_single_game()

    # Then run multiple comparisons
    test_multiple_games(num_games=5)

