"""
    File name: word_ladders.py
    Author: Shree Raj Shrestha and Alexandra DeLucia
    Date created: 2/16/2017
    Date last modified: 2/26/2017
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
        Defulat constructor for State class.
        :param init_state: initial state (i.e. initial word)
        :param dest_state: destination state (i.e. ending word)
        :param path: path taken so far to the initial state
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
        return state + " " + dest_state + " " + str(path)


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
        print "Searching at depth level ", depth_limit
        solution = search(initial_state, state_space, depth_limit)
        if len(solution) > 0:
            return solution
        else:
            print depth_limit, " is not deep enough!\n"
            depth_limit += 1

    # Return empty list by default
    return []


def generate_word_list(file_path, word):
    """
    Make a list of words with same length as a given word from file
    :param file_path: the path of the word list file
    :param word: the initial word
    """
    try:
        word_list = []
        
        for line in open(file_path):
            this_word = line.strip()
            if len(this_word) == len(word):
                word_list.append(this_word)
        return word_list

    # Throw error if file not found
    except IOError:
        print "Error: The file does not exist or was not provided!\n"

    # Default return, empty list
    return []


def main():
    """
    Given a word file, start word and end word, returns list of words that
    lead to the final word with one character change
    :param: none
    :return: none
    """
    
    # Initialize default parameters
    file_path = 'words.txt'
    word1 = 'snakes'
    word2 = 'brains'

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
            else:
                print "ERROR: Both words must be of the same length!\n"
                quit()
    else:
        print "Proceeding with defaults\nwords.txt", word1, word2, "\n"

    # Generate a list of words with same length as the initial word
    word_list = generate_word_list(file_path, word1)

    # Solve the word ladder puzzle using iterative deepening dfs technique
    # NOTE: The theoretical maximum for moves is size of the word list minus 1
    # Proof: For word list ['do','de','be','by','my']
    # Assuming that words in path cannot be used
    # From 'do' to 'my', the only possible path is the list itself in order
    # The number of moves in this case is 4, size of list minus 1
    max_depth = len(word_list) - 1
    solution = iterative_deepening_dfs(word1, word2, word_list, max_depth)
    if solution is not []:
        for word in solution:
            print word
    else:
        print "No Solution Found!\n"


if __name__ == '__main__':
    main()
