import random
import time
import os
import argparse
from typing import List

class GameOfLife:
    def __init__(self, size: int, prob: float, steps: int):
        self.size = size
        self.prob = prob
        self.steps = steps
        self.board = self.get_empty_board()

    def get_empty_board(self) -> List[List[int]]:
        """Return an n x n table of dead cells (a list of lists)."""
        return [[0 for _ in range(self.size)] for _ in range(self.size)]

    def print_board(self) -> None:
        """Print the board to the console."""
        for row in self.board:
            print(" ".join("." if cell == 0 else "X" for cell in row))

    def get_random_board(self) -> List[List[int]]:
        """Generate an n x n board where each cell is alive (1) with probability p and dead (0) otherwise."""
        return [[1 if random.random() < self.prob else 0 for _ in range(self.size)] for _ in range(self.size)]

    def add_glider(self) -> None:
        """Put a glider pattern in the top-left corner of the board."""
        glider = [
            [0, 0, 1],
            [1, 0, 1],
            [0, 1, 1]
        ]
        for i in range(3):
            for j in range(3):
                self.board[i][j] = glider[i][j]

    def count_live_neighbors(self, x: int, y: int) -> int:
        """Count the number of live neighbors for the cell at position (x, y)."""
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        live_neighbors = 0

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size:  # handle edges of the board
                live_neighbors += self.board[nx][ny]

        return live_neighbors

    def step(self) -> None:
        """Compute the next generation of the board based on the current state."""
        new_board = self.get_empty_board()
        for i in range(self.size):
            for j in range(self.size):
                live_neighbors = self.count_live_neighbors(i, j)

                if self.board[i][j] == 1:  # Alive cell
                    if live_neighbors < 2 or live_neighbors > 3:
                        new_board[i][j] = 0  # Dies
                    else:
                        new_board[i][j] = 1  # Lives
                elif self.board[i][j] == 0 and live_neighbors == 3:
                    new_board[i][j] = 1  # Becomes alive (reproduction)

        self.board = new_board

    def run_simulation(self) -> None:
        """Run the Game of Life for the given number of steps."""
        for _ in range(self.steps):
            os.system('clear')  # Clear the screen (Windows only)
            self.print_board()
            time.sleep(0.5)  # Wait for half a second
            self.step()  # Generate the next step

def main():
    # Parsing command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", "-s", type=int, default=10, help="Size of the board")
    parser.add_argument("--prob", "-p", type=float, default=0.2, help="Probability of a cell being alive")
    parser.add_argument("--steps", "-n", type=int, default=20, help="Number of steps to run the simulation for")
    args = parser.parse_args()

    # Initialize the game
    game = GameOfLife(size=args.size, prob=args.prob, steps=args.steps)

    # Add a glider to the board
    game.add_glider()

    # Run the simulation
    game.run_simulation()

if __name__ == "__main__":
    main()
