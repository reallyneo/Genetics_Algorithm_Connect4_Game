import time
from connect4 import ConnectFourExtended

def test_single_game():
    print("=== Test: Single Game ===")
    game = ConnectFourExtended()
    game.play()
    print("Single game test completed.\n")

def test_multiple_games(num_games=3):
    print(f"=== Test: Compare {num_games} Games ===")
    game = ConnectFourExtended()
    game.play(num_games=num_games)
    print("Multiple games comparison completed.\n")

if __name__ == "__main__":
    # Test a single interactive game
    test_single_game()

    # Test automatic comparison of genetic vs simple heuristic
    test_multiple_games(num_games=5)
