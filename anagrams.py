"""
    File name: anagrams.py
    Author: Shree Raj Shrestha and Alexandra DeLucia
    Date created: 2/16/2017
    Date last modified: 2/26/2017
    Python Version: 2.7
"""

import sys


class AnagramDict(object):
    """
    Represents a dictionary of all different anagrams in a word file.
    :attr anagram_dict: the dictionary that stoers the anagrams
    """
    
    def __init__(self, file_path):
        """
        Default constructor for AnagramDict class. 
        :param file_path: the path of the words file
        :return: none
        """
        assert isinstance(file_path, str)
        anagram_dict = {}
        for line in open(file_path):
            word = line.strip()
            char_set = tuple(sorted(word))
            if not char_set in anagram_dict:
                anagram_dict[char_set] = [word]
            else:
                anagram_dict[char_set].append(word)
        
        self.anagram_dict = anagram_dict


def print_anagram_dict(anagram_dict):
    """
    Prints the anagram dictionary.
    :param anagram_dict: the dictionary of anagrams found
    :return: none
    """
    # Print all lists in anagram dictionary with length more than one
    for char_set in anagram_dict:
        anagram_list = anagram_dict[char_set]
        if len(anagram_list) > 1:
            print anagram_list


def main():
    """
    Given a text file, Anagrams returns a list of all anagrams in the file.
    :return: none
    """
    # Get user parameters, run with default file if not provided
    if len(sys.argv) > 1:
        print_anagram_dict(AnagramDict(sys.argv[1]).anagram_dict)
    else:
        print_anagram_dict(AnagramDict('words.txt').anagram_dict)


if __name__ == '__main__':
    main()
