# Makefile for Connect Four project

PYTHON = python3

# Default target
all: play

# Run all tests
test:
	$(PYTHON) test_connect4.py

# Run the genetic AI standalone
genetic:
	$(PYTHON) play_genetic.py

# Run the simple AI standalone
simple:
	$(PYTHON) play_simple.py

# Run interactive Connect4Extended
play:
	$(PYTHON) connect4.py

# Clean any __pycache__ directories
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
