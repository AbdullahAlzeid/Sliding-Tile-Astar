# Sliding Tile Puzzle Solver Using A* Algorithm

## Overview
This repository contains a Python implementation of the A* (A-star) algorithm to solve the Sliding Tile Puzzle, an NxN grid-based puzzle. The implementation includes various heuristic functions like Manhattan Distance and Misplaced Tiles to efficiently find the solution.

## Features
- **Dynamic Puzzle Size**: Supports puzzles of sizes ranging from 3x3 to 6x6.
- **A* Algorithm**: Utilizes the A* search algorithm for finding the most efficient solution path.
- **Heuristic Functions**: Includes Manhattan Distance and Misplaced Tiles heuristics for optimized searching.
- **Performance Analysis**: Generates reports on the performance of the algorithm, including solution depth and maximum states stored.

## How to Run
1. Ensure Python is installed on your system.
2. Clone the repository: git clone https://github.com/AbdullahAlzeid/Sliding-Tile-Astar.git
3. Run the `Driver.py` script: python Driver.py
4. Follow the on-screen prompts to select the puzzle size and heuristic function.

## Key Components
- **Driver.py**: The main script to run the puzzle solver. ([Driver.py](https://github.com/AbdullahAlzeid/Sliding-Tile-Astar/blob/main/Driver.py))
- **Heuristic Functions**: Implements Manhattan Distance and Misplaced Tiles heuristics for the A* algorithm.

## Heuristic Functions
- **Manhattan Distance**: Calculates the sum of the distances of each tile from its goal position.
- **Misplaced Tiles**: Counts the number of tiles that are in the wrong position compared to the goal state.

## Report
- A detailed report testing performance of heuristics can be found [here](https://github.com/AbdullahAlzeid/Sliding-Tile-Astar/blob/main/Report/ICS%20381-Assignment%202.pdf).

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/AbdullahAlzeid/Sliding-Tile-Astar/blob/main/LICENSE) file for details.



