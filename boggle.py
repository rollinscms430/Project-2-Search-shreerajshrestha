# Boggle
# Given a Boggle board, solve for the list of possible words
import sys
from copy import deepcopy
from random import random

class Grid(object):
    """Grid
    
    grid: matrix of elements
    """
    def __init__(self, grid):
        assert isinstance(grid, list)
        assert sum([len(grid[i]) != len(grid) for i in range(len(grid))]) == 0
        self.grid = grid
        self.dimension = len(grid)
    
    def __str__(self):
        string = ''
        for row in self.grid:
            for element in row:
                string += element + ' '
            st
            ring += '\n'
        return string
    
    def getElement(self, position):
        assert isinstance(position, tuple)
        letter = self.grid[position[0]][position[1]]
        return letter
    
    def getNearbyPositions(self, position):
        assert isinstance(position, tuple)
        positions = []
        for i in range(position[0] - 1, position[0] + 2):
            for j in range(position[1] - 1, position[1] + 2):
                if -1 < i < 4 and -1 < j < 4 and (i, j) != position:
                    positions.append((i, j))
        return positions


class WordState(object):
    """Word_State
    
    start_position: coordinates of starting element
    visited_positions: list of coordinates of elements in word
    current_value: current string of words
    """
    def __init__(self, position, visited_positions, current_value):
        self.position = position
        self.visited_positions = visited_positions
        self.current_value = current_value


def search(this_state, grid, prefix_hash, found_words):
    
    new_visited = deepcopy(this_state.visited_positions)
    new_value = deepcopy(this_state.current_value)
    
    new_visited.append(this_state.position)
    new_value += grid.getElement(this_state.position)
    
    if new_value in prefix_hash and prefix_hash[new_value] == 1 and new_value not in found_words:
        found_words.append(new_value)
    
    for position in grid.getNearbyPositions(this_state.position):
        if position not in this_state.visited_positions:
            
            potential_value = new_value + grid.getElement(position)
            if potential_value in prefix_hash:
                potential_state = WordState(position, new_visited, new_value)
                found_words += search(potential_state, grid, prefix_hash, [])
    
    return found_words


def exhaustive_bfs(position, grid, prefix_hash):
    
    # Initialize word state
    initial_state = WordState(position, [], '')
    return search(initial_state, grid, prefix_hash, [])


def build_prefix_hash(file_path):
    """Returns a dictionary of all valid words and their sub-states
    file_path: text file containing list of words
    """
    file = open(file_path)
    
    # prefix_hash
    # key: prefix
    # value: 1 if in final valid state, 0 otherwise
    # i.e. 'gy' = 0, 'gyro' = 1
    prefix_hash = {}
    
    for line in file:
        # Strip white space
        word = line.strip()
        # Only keep words of at least length 3
        if len(word) >= 3:
            # Add all substates of the word to the dictionary
            # Starting from length 2 (list of valid word beginnings)
            for i in range(2, len(word)+1):
                prefix = word[:i]
                
                # Check if in dictionary before adding
                if prefix not in prefix_hash:
                    # If word is a completed word (i.e. in a valid final state)
                    # set value = 1
                    # This will only work if word_list is in alphabetical order
                    # (i.e. completed subword comes before appearance in other words)
                    if len(prefix) == len(word):
                        prefix_hash[prefix] = 1
                    # Else word is not in final state, set value = 0
                    else:
                        prefix_hash[prefix] = 0
    return prefix_hash


def main():
    """Solves a Boggle board for all possible words
    """
    word_list_file_path = 'words.txt'
    
    example_grid = [['u', 'n', 't', 'h'],['g','a','e','s'],['s','r','t','r'],['h','m','i','a']]
    grid = Grid(example_grid)
    prefix_hash = build_prefix_hash(word_list_file_path)
    
    # Find all possible words using iterative deepening dfs
    total_words = []
    
    # Each element can be used as a starting position
    for row in range(grid.dimension):
        for column in range(grid.dimension):
            words = exhaustive_bfs((row, column), grid, prefix_hash)
            total_words += words
    
    for word in total_words:
        print word


if __name__ == '__main__':
    main()
