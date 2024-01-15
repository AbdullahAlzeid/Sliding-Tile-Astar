from copy import deepcopy
import random
import heapq
import math


def get_puzzle_size():
    while True:
        try:
            n = int(input('Enter the N value for puzzle size (3<=N<=6): '))
            if 3 <= n <= 6:
                return n
            else:
                print('Please Enter a Correct N Value!')
        except ValueError:
            print('Enter a valid integer!')


def solvable(state):
    n = len(state)
    flat_state = [tile for row in state for tile in row]
    inv_count = 0
    for i in range(n*n):
        for j in range(i+1, n*n):
            if flat_state[j] != 0 and flat_state[i] != 0 and flat_state[i] > flat_state[j]:
                inv_count += 1

    if n % 2 == 0:
        blank_row = [i for i, row in enumerate(state) if 0 in row][0]
        if blank_row % 2 == 0:
            return inv_count % 2 == 1
    return inv_count % 2 == 0


def generate_initial_state(n):
    state = [list(range(1 + i * n, 1 + i * n + n)) for i in range(n)]
    state[n-1][n-1] = 0

    # number of random moves to make (The larger the number multiplied by n the more shuffled the puzzle will be)
    shuffle = n * 10

    for _ in range(shuffle):
        state, _ = random.choice(GenerateChildren(state))
    return state


def generate_goal_state(n):
    elements = list(range(1, n * n)) + [0]
    return [elements[i * n:(i + 1) * n] for i in range(n)]


def GenerateChildren(state, last_move=None):
    for i in range(len(state)):
        for j in range(len(state)):
            if state[i][j] == 0:
                oldi, oldj = (i, j)

    directions = [(-1, 0, "U"), (1, 0, "D"), (0, -1, "L"), (0, 1, "R")]
    successors = []

    opposite_moves = {"U": "D", "D": "U", "L": "R", "R": "L"}
    if last_move and last_move in opposite_moves:
        directions = [d for d in directions if d[2]
                      != opposite_moves[last_move]]

    for d in directions:
        newi, newj = oldi + d[0], oldj + d[1]

        if 0 <= newi < len(state) and 0 <= newj < len(state):
            child = deepcopy(state)
            child[oldi][oldj], child[newi][newj] = child[newi][newj], child[oldi][oldj]
            successors.append((child, d[2]))

    return successors

# This is a wrapper for A* method


def a_star_method(initial, goal, heuristic):
    return a_star(initial, goal, heuristic=heuristic)


def a_star(initial_state, goal_state, heuristic):
    visited = set()
    pq = [(heuristic(initial_state, goal_state), 0, initial_state, [])]
    max_states = 0

    while pq:
        max_states = max(max_states, len(pq))
        f, g, current_state, path = heapq.heappop(pq)

        if current_state == goal_state:
            return path, max_states

        hashed_state = tuple(map(tuple, current_state))
        if hashed_state in visited:
            continue

        visited.add(hashed_state)

        last_move = path[-1] if path else None
        for neighbor, move in GenerateChildren(current_state, last_move):
            hashed_neighbor = tuple(map(tuple, neighbor))
            if hashed_neighbor not in visited:
                new_g = g + 1
                new_f = new_g + heuristic(neighbor, goal_state)
                heapq.heappush(pq, (new_f, new_g, neighbor, path + [move]))

    return [], max_states


def misplaced_tiles(state, goal_state):
    return sum(1 for i in range(len(state)) for j in range(len(state)) if state[i][j] != 0 and state[i][j] != goal_state[i][j])


def manhattan_distance(state, goal_state):
    distance = 0
    for num in range(1, len(state) * len(state)):
        x1, y1 = next((i, j) for i, row in enumerate(state)
                      for j, cell in enumerate(row) if cell == num)
        x2, y2 = next((i, j) for i, row in enumerate(goal_state)
                      for j, cell in enumerate(row) if cell == num)
        distance += abs(x1 - x2) + abs(y1 - y2)
    return distance


def euclidean_distance(state, goal_state):
    distance = 0
    for num in range(1, len(state) * len(state)):
        x1, y1 = next((i, j) for i, row in enumerate(state)
                      for j, cell in enumerate(row) if cell == num)
        x2, y2 = next((i, j) for i, row in enumerate(goal_state)
                      for j, cell in enumerate(row) if cell == num)
        distance += math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    return distance


def generate_report(algorithm_name, algorithm, n, heuristic):

    splitter = "-" * 40 + "\n"

    with open("N3_mis.txt", "w") as f:
        solution_depths = []
        states_stored = []

        for i in range(10):
            initial = generate_initial_state(n)
            final = generate_goal_state(n)

            solution_sequence, max_states_stored = algorithm(
                initial, final, heuristic=heuristic)
            solution_depth = len(solution_sequence)

            f.write(f"Run {i + 1}:\n")
            f.write("Initial State:\n")
            for row in initial:
                f.write(" ".join(map(str, row)) + "\n")
            f.write("\nFinal State:\n")
            for row in final:
                f.write(" ".join(map(str, row)) + "\n")
            f.write(f"\nAlgorithm Used: {algorithm_name}\n")
            f.write("Solution Sequence:\n")
            f.write(" --> ".join(solution_sequence) + "\n")
            f.write(f"\nSolution Depth: {solution_depth}\n")
            f.write(f"Max States Stored: {max_states_stored}\n\n")

            solution_depths.append(solution_depth)
            states_stored.append(max_states_stored)

            f.write(splitter)

        f.write("Descriptive Statistics:\n")
        f.write(f"Minimum Solution Depth: {min(solution_depths)}\n")
        f.write(f"Maximum Solution Depth: {max(solution_depths)}\n")
        f.write(
            f"Average Solution Depth: {sum(solution_depths) / len(solution_depths):.2f}\n")
        f.write(f"Minimum States Stored: {min(states_stored)}\n")
        f.write(f"Maximum States Stored: {max(states_stored)}\n")
        f.write(
            f"Average States Stored: {sum(states_stored) / len(states_stored):.2f}\n")


def main():

    n = get_puzzle_size()

    # generate report used to get summary of the algorithm of choice
    # generate_report("A* with misplaced tiles",
    #                 a_star_method, n, misplaced_tiles)

    Initial_State = generate_initial_state(n)

    Goal_State = generate_goal_state(n)

    print("\nInitial State:")
    for row in Initial_State:
        print(row)
    print("\nGoal State:")
    for row in Goal_State:
        print(row)

    # This sets method to our wrapper function which calls A*
    method = a_star_method

    # Set the heuristic you want to use with A*
    heuristic_used = manhattan_distance

    print("\nFinding a Path Solution using A* with",
          heuristic_used.__name__, "heuristic . . .\n")

    path, max_states = method(
        Initial_State, Goal_State, heuristic=heuristic_used)

    if path:
        print(
            f"Solution found through A* using {heuristic_used.__name__} heuristic!")
        print(" --> ".join(path))
        print(f"Solution depth: {len(path)}")
        print(f"Maximum number of states concurrently stored: {max_states}")
    else:
        print(
            f"No solution found using A* with {heuristic_used.__name__} heuristic.")


if __name__ == "__main__":
    main()
