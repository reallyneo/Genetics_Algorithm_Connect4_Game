Connect Four AI Project

Description
This project implements a Connect Four game with two different AI strategies: one based on a genetic algorithm and another using a simple heuristic-based approach. The game allows users to play against either AI, compare the performance of both AIs, and evaluate the effectiveness of the strategies.

Installation
To install and set up the project, follow these steps:

Clone the repository:
sh
Copy code
git clone https://github.com/your-username/connect-four-ai.git
cd connect-four-ai

Install dependencies:
Ensure you have Python 3 installed. No additional libraries are required for this project.

Usage
To run the Connect Four game, you can use the provided Makefile or directly execute the Python scripts.

Using Makefile

Build the project:
sh
Copy code
make all

Run the game:
sh
Copy code
python3 connect4.py

Clean the build files:
sh
Copy code
make clean
Direct Execution

Run the game:
sh
Copy code
python3 connect4.py

Playing the Game

Single Game:
When prompted, enter the number of games to compare. Press Enter for a single game.

Multiple Games:
Enter the number of games you want to compare between the genetic algorithm-based strategy and the simple heuristic-based approach.

Dependencies

Python 3.x

File Descriptions

connect4.py: Contains the main implementation of the Connect Four game and integrates both AI strategies.
play_genetic.py: Implements the genetic algorithm-based AI for Connect Four.
play_simple.py: Implements the simple heuristic-based AI for Connect Four.
Makefile: Provides a simple build system to run and clean the project.

Authors
Naheem Watson
