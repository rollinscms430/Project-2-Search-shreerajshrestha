# Anagrams
# Given a text file, Anagrams returns a list of all anagrams in the file

import sys

class AnagramDict(object):
    
    """Finds anagrams in a given text file
        file_path: Path to text file
    """
    
    def __init__(self, file_path):
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
    for char_set in sorted(anagram_dict):
        anagram_list = anagram_dict[char_set]
        print ''.join(char_set), str(anagram_list),

def main():
    if len(sys.argv) > 1:
        print_anagram_dict(AnagramDict(sys.argv[1]).anagram_dict)
    else:
        print_anagram_dict(AnagramDict('words.txt').anagram_dict)

if __name__ == '__main__':
    main()