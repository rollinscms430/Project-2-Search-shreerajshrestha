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
        return self.state + " " + self.dest_state + " " + str(self.path)

    def is_final_state(self):
        """
        Returns True if current state is the destination state, false otherwise.
        :return boolean:
        """
        return self.state == self.dest_state
    
    
    def get_depth_from_origin(self, state):
        """
        Returns the number of different characters needed to be changed.
        :return int: depth from the origin to given state
        """
        assert isinstance(state, str)
        return sum(state[i] != self.state[i] for i in range(len(state)))


def add_to_visited(state, visited):
    visited[state.state] = 1


def already_visited(state, visited):
    return state.state in visited


def solve(start_word, dest_word):

    # Initialize the word ladder game
    init_state = State(start_word, dest_word, [start_word])
    
    
    """
    
    """
    
    # Maintain a queue of frontier states
    queue = []
    queue.append(init_state)

    # Dictionary of previously expanded states
    visited = {}

    # Search for solution until queue of nodes to expand is empty
    while len(queue) > 0:
        
        print len(queue)
        
        this_state = queue.pop(0)

        # If state is the final word, then the work is done
        if this_state.is_final_state():
            return this_state.path

        for i in range(0, len(start_word)):
            
            word_char = list(start_word)
            word_char[i] = ''
            
            for j in range(0,26):
                char = chr(97 + j)  # chr(97) = 'a'
                word_char[i] = char
                potential_word = ''.join(word_char)
                
                new_path = deepcopy(init_state.path)
                new_path.append(potential_word)
                potential_state = State(potential_word, init_state.dest_state, new_path)
    
                # Only add the new state if not previously generated
                #current_cost = this_state.get_depth_from_origin(init_word) + this_state.get_depth_to_destination(new_state.state)
                #potential_cost = new_state.get_depth_to_destination(potential_state) + 1 # Cost to potential state is 1
                if not already_visited(new_state, visited):
                    add_to_visited(new_state, visited)
                    queue.append(new_state)


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
                file_path = sys.argv[3]
            else:
                print "ERROR: Both words must be of the same length!\n"
                quit()
    else:
        print "Proceeding with defaults\n", word1, word2, "words.txt\n"

    # Generate a list of words with same length as the initial word
    word_list = generate_word_list(file_path, word1)

    solution = solve(word1, word2)
    if solution:
        for word in solution:
            print word
    else:
        print "No Solution Found!\n"


if __name__ == '__main__':
    main()
