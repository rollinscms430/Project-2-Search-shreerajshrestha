# Word Ladders
# Given a start word and an end word, generate a chain of words that connects
# the two

import sys
from copy import deepcopy


class State(object):
    """Represents a state in the solution of the word puzzle

        Attributes:
        init_state: Initial state (i.e. initial word)
        dest_state: Destination state (i.e. ending word)
        path: List of intermediate steps from initial to destination state
    """

    def __init__(self, init_state, dest_state, path):
        assert isinstance(init_state, str)
        assert isinstance(dest_state, str)
        assert isinstance(path, list)
        self.state = init_state
        self.dest_state = dest_state
        self.path = path

    # Returns formatted String
    def __str__(self):
        return self.state + " " + self.dest_state + " " + str(self.path)

    # Returns boolean if current state is the destination state
    def is_final_state(self):
        return self.state == self.dest_state

    # Returns minimum depth required to get from current state to destination
    # Theoretical min depth is equal to the number of characters needed to be changed
    def get_minimum_path_depth(self):
        return sum(self.state[i] != self.dest_state[i] for i in range(len(self.state)))

    # Returns "distance" between self and given state
    # Distance is equal to the number of different characters
    def get_depth_from_origin(self, state):
        assert isinstance(state, str)
        return sum(state[i] != self.state[i] for i in range(len(state)))

    # Returns theoretical distance to destination state
    # Theoretical distance is equal to the number of characters needed to be changed
    def get_depth_to_destination(self, state):
        assert isinstance(state, str)
        return sum(state[i] != self.dest_state[i] for i in range(len(state)))


def search(this_state, state_space, depth_limit):
    """Solves word puzzle using iterative deepening search
        this_state: Current state
        state_space: Collection of all possible states (i.e. word list)
        depth_limit: Max depth to search
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
    # Initialize the word ladder game
    # Empty path because no moves have been made
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


# Make a list of words with same length as a given word from file
def generate_word_list(file_path, word):
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


def test():
    # Sample Case
    word1 = 'dog'
    word2 = 'cat'

    # Solve the word ladder puzzle
    word_list = generate_word_list('words.txt', word1)
    max_depth = len(word_list) - 1
    solution = iterative_deepening_dfs(word1, word2, word_list, max_depth)
    if solution is not []:
        for word in solution:
            print word
    else:
        print "No Solution Found!\n"


if __name__ == '__main__':
    #test()
    main()
