"""
    File name: word_ladders.py
    Author: Shree Raj Shrestha and Alexandra DeLucia
    Date created: 2/16/2017
    Date last modified: 2/28/2017
    Python Version: 2.7
"""

import sys
from copy import deepcopy


class State(object):
    """
    Represents a state in the solution of the word puzzle.
    :attr state: the current state
    :attr dest_state: destination state
    :attr path: List of intermediate steps from initial to destination state
    """

    def __init__(self, init_state, dest_state, path):
        """
        Defualt constructor for State class.
        :param init_state: initial state (i.e. initial word)
        :param dest_state: destination state (i.e. ending word)
        :param path: path taken so far to the destination state
        """
        assert isinstance(init_state, str)
        assert isinstance(dest_state, str)
        assert isinstance(path, list)
        self.state = init_state
        self.dest_state = dest_state
        self.path = path

    def __str__(self):
        """
        Returns object as formatted string.
        :return string: the formatted string object of state
        """
        return self.state + " " + self.dest_state + " " + str(self.path)

    def is_final_state(self):
        """
        Returns True if current state is the destination state, false otherwise.
        :return boolean:
        """
        return self.state == self.dest_state
    
    def get_minimum_path_depth(self):
        """
        Returns minimum depth required to get from current state to destination.
        The theoritical minimum depth it number of different characters 
        between inital and destination state.
        :return int: minimum theoritical depth to destination
        """
        return sum(self.state[i] != self.dest_state[i] for i in range(len(self.state)))

    def get_depth_from_origin(self, state):
        """
        Returns the number of different characters needed to be changed.
        :return int: depth from the origin to given state
        """
        assert isinstance(state, str)
        return sum(state[i] != self.state[i] for i in range(len(state)))

    def get_depth_to_destination(self, state):
        """
        Returns the theoritical distance to destination state, which
        is equal to the number of characters needed to be changed.
        :return int: depth from the origin to given state
        """
        assert isinstance(state, str)
        return sum(state[i] != self.dest_state[i] for i in range(len(state)))


def add_to_visited(state, visited):
    """
    Adds a state to visited
    :param state: State object
    :param visited: dictionary containing other visited states
    :return: none
    """
    visited[state.state] = 1


def already_visited(state, visited):
    """
    Checks if a state is in visited
    :param state: State object
    :param visited: dictionary containing other visited states
    :return: Boolean
    """
    return state.state in visited


def min_depth(word1, word2):
    """
    Returns the distance between word1 and word2
    "Distance" is the number of different characters
    :param word1: Intitial word
    :param word2: Destination word
    :return: number
    """
    return sum(word1[i] != word2[i] for i in range(len(word1)))


def greedy_bfs(start_word, dest_word, word_list):
    """
    Returns path from start word to destination word
    :param start_word: intial word
    :param dest_word: destination word
    :param word_list: list of valid words
    :return: list of intermediate words between start and destination
    """
    # Initialize frontier queue
    frontier = []
    
    # Initialize path to all words in word list with start word, the root node
    frontier.append(start_word)
    path_to = {word:[start_word] for word in word_list}
    
    # Search for solution until queue of nodes to expand is empty
    while len(frontier) > 0:
        
        # Pop next node
        this_word = frontier.pop(0)
        
        # If the final word is found, return the 
        if this_word == dest_word:
            return path_to[this_word]
        
        # Iterate over each character of the word
        for i in range(len(this_word)-1,-1,-1):
            
            word_array = list(this_word)
            word_array[i] = ''
            
            # Replace character at index for all letters in alphabet
            for j in range(0, 26):
                char = chr(97 + j) # chr(97) = 'a'
                word_array[i] = char
                new_word = ''.join(word_array)
                
                # Expand current node with a valid node
                if new_word != start_word and new_word in word_list:
                    
                    # Only add unexplored words to frontier
                    # If an explored word is added to the frontier, there is
                    # a possibility of loops being formed as well as
                    # unfeasible solutions being explored.
                    if path_to[new_word] == [start_word]:
                        frontier.append(new_word)
                        
                        # Append path taken so far with the path to new word
                        path_to[new_word] = path_to[this_word] + [new_word]


def search(this_state, state_space, depth_limit):
    """
    The recursive solution to the word puzzle for iterative deepening search.
    :param this_state: current state
    :param state_space: collection of all possible states (i.e. word list)
    :param depth_limit: max depth from origin to search until
    :return list: words that lead from initial to destination state
    """
    # If final state is found, return the solution
    if this_state.is_final_state():
        solution_path = this_state.path
        solution_path.append(this_state.state)
        return solution_path

    # If the depth limit has been reached, return empty list
    if depth_limit < 0:
        return []

    # Trim the domain of the state space
    trimmed_state_space = []
    for state in state_space:

        # Only try a state if below one depth level
        # i.e. Only a distance of 1 step
        if this_state.get_depth_from_origin(state) == 1:

            # Only try state if it improves the solution
            if this_state.get_depth_to_destination(state) < depth_limit:
                trimmed_state_space.append(state)

    # Expand current path by trying all possible words in the trimmed domain
    new_path = deepcopy(this_state.path)
    new_path.append(this_state.state)
    for potential_state in trimmed_state_space:

        # If state is in the path, loop forms, so ignore to prevent looping
        if potential_state not in this_state.path:

            # Add word to the path and create a new state
            new_state = State(potential_state, this_state.dest_state, new_path)

            # Reduce limit by 1 and recursively search from new state
            path = search(new_state, state_space, depth_limit - 1)

            # Recursive call ends, return path if it is not empty
            if path != []:
                return path

    # Return empty path by default
    return []


def iterative_deepening_dfs(init_state, dest_state, state_space, max_depth):
    """
    Implements the iterative deepening search technique. Do depth first
    search starting at a minimum depth to maximum depth, if solution not found.
    :param init_state: the initial state of the puzzle
    :param dest_state: the destination state of the puzzle
    :param state_space: collection of all possible states (i.e. word list)
    :param max_depth: max depth for iterative dfs
    :return list: words that lead from initial to destination state
    """
    
    # Initialize the word ladder game
    initial_state = State(init_state, dest_state, [])

    # The minimum for number of optimal moves is the number of
    # different characters since one move allows one character change
    depth_limit = initial_state.get_minimum_path_depth()

    # Loop until solution is found or maximum depth is reached
    while depth_limit < max_depth:
        solution = search(initial_state, state_space, depth_limit)
        if len(solution) > 0:
            return solution
        else:
            depth_limit += 1

    # Return empty list by default
    return []


def generate_word_list(file_path, word):
    """
    Make a list of words with same length as a given word from file
    :param file_path: the path of the word list file
    :param word: the initial word
    :return: list of words
    """
    try:
        word_list = {}

        for line in open(file_path):
            this_word = line.strip()
            if len(this_word) == len(word):
                word_list[this_word] = 1
        return word_list

    # Throw error if file not found
    except IOError:
        print "Error: The file does not exist or was not provided!\n"

    # Default return, empty list
    return {}


def main():
    """
    Given a word file, start word and end word, returns list of words that
    lead to the final word with one character change
    :param: none
    :return: none
    """

    # Initialize default parameters
    word1 = 'snakes'
    word2 = 'brains'
    file_path = 'words.txt'
    
    # Check if user provided input parameters
    if len(sys.argv) > 1:
        if len(sys.argv) != 3:
            print "Usage: <start word> <end word>"
            quit()
        elif len(sys.argv) == 3:
            # Ensure the words are of the same length
            if len(str(sys.argv[1])) == len(str(sys.argv[2])):
                word1 = sys.argv[1]
                word2 = sys.argv[2]
                file_path = sys.argv[3]
            else:
                print "ERROR: Both words must be of the same length!\n"
                quit()
    else:
        print "Proceeding with defaults\n", word1, word2, "words.txt\n"

    # Generate a list of words with same length as the initial word
    word_list = generate_word_list(file_path, word1)
    
    print "Solving using Greedy Breadth First Search..."
    solution = greedy_bfs(word1, word2, word_list)
    if solution:
        for word in solution:
            print word
    else:
        print "No Solution Found!\n"
    
    # Solve the word ladder puzzle using iterative deepening dfs technique
    # NOTE: The theoretical maximum for moves is size of the word list minus 1
    # Proof: For word list ['do','de','be','by','my']
    # Assuming that words in path cannot be used
    # From 'do' to 'my', the only possible path is the list itself in order
    # The number of moves in this case is 4, size of list minus 1
    print "\nSolving using Iterative Deepening Depth First Search..."
    max_depth = len(word_list) - 1
    solution = iterative_deepening_dfs(word1, word2, word_list, max_depth)
    if solution is not []:
        for word in solution:
            print word
    else:
        print "No Solution Found!\n"


if __name__ == '__main__':
    main()
